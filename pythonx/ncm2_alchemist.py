# -*- coding: utf-8 -*-

from __future__ import absolute_import
import vim
from ncm2 import Ncm2Source, getLogger
import re
import jedi
import os
import sys

PLUGIN_BASE_PATH = vim.eval('ncm2_alchemist#alchemist_vim_path()')
sys.path.insert(0, PLUGIN_BASE_PATH)
from elixir_sense import ElixirSenseClient

DEBUG = False

logger = getLogger(__name__)


class Source(Ncm2Source):

    def __init__(self, nvim):
        Ncm2Source.__init__(self, nvim)

        self.vim = nvim
        alchemist_script = "%s/elixir_sense/run.exs" % PLUGIN_BASE_PATH
        self.re_completions = re.compile(r'kind:(?P<kind>[^,]*), word:(?P<word>[^,]*), abbr:(?P<abbr>[\w\W]*), menu:(?P<menu>[\w\W]*), info:(?P<info>[\w\W]*)$')
        self.re_is_only_func = re.compile(r'^[a-z]')

        self.sense_client = ElixirSenseClient(debug=DEBUG, cwd=os.getcwd(), ansi=False, elixir_sense_script=alchemist_script, elixir_otp_src="")

    def on_complete(self, ctx, lines):
        path = ctx['filepath']
        typed = ctx['typed']
        lnum = ctx['lnum']
        startccol = ctx['startccol']
        ccol = ctx['ccol']

        logger.info('context [%s]', ctx)

        response = self.sense_client.process_command('suggestions', "\n".join(lines), lnum, ccol)
        logger.info('response %s', response)
        if response[0:6] == 'error:':
            return

        completions = []
        server_results = response.split('\n')[:-1]
        for result in server_results:
            matches = self.re_completions.match(result)
            kind = matches.group('kind')
            abbr = matches.group('abbr')
            menu = matches.group('menu')
            word = matches.group('word')
            # get only last part
            word = word.split(".")[-1]

            item = dict(word=word,
                        icase=1,
                        dup=1,
                        menu=abbr if kind == "f" else menu)

            item = self.match_formalize(ctx, item)

            if self.vim.funcs.exists('g:alchemist#extended_autocomplete'):
                if self.vim.eval('g:alchemist#extended_autocomplete') == 1:
                    item['info'] = matches.group('info').replace("<n>", "\n").strip()

            if kind == "f":
                self.render_snippet(item)

            completions.append(item)

        logger.info('completions %s', completions)

        self.complete(ctx, startccol, completions)

    def render_snippet(self, item):
        abbr = item['menu']

        params = re.search(r'\((.*)\)', abbr)
        if not params:
            return

        logger.info('snippet params: %s', params.group(1))
        num = 1
        req_params = []
        opt_params = []


        params = params.group(1).split(',')
        for param in params:
            param = param.strip()

            if param.find('\\\\') > 0:
                if num > 1:
                    opt_params.append(self.snippet_placeholder(num, ', ' + param))
                else:
                    opt_params.append(self.snippet_placeholder(num, param))
            else:
                req_params.append(self.snippet_placeholder(num, param))

            num += 1

        ud = item['user_data']
        ud['is_snippet'] = 1
        ud['snippet'] = item['word'] + \
            '(' + ', '.join(req_params) + ''.join(opt_params) + ')${0}'

    def snippet_placeholder(self, num, txt=''):
        txt = txt.replace('\\', '\\\\')
        txt = txt.replace('$', r'\$')
        txt = txt.replace('}', r'\}')
        if txt == '':
            return '${%s}' % num
        return '${%s:%s}'  % (num, txt)


source = Source(vim)

on_complete = source.on_complete
