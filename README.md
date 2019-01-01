# ncm2-alchemist

[![Project Status: Active - The project has reached a stable, usable state and is being actively developed.](http://www.repostatus.org/badges/latest/active.svg)](http://www.repostatus.org/#active)

[ncm2](https://github.com/ncm2/ncm2) source for elixir via
[alchemist.vim](https://github.com/slashmili/alchemist.vim).

ncm2-alchemist offers asynchronous completion of code written in Elixir using
[alchemist.vim](https://github.com/slashmili/alchemist.vim) and
[ncm2](https://github.com/ncm2/ncm2).


## Installation

Using [vim-plug](https://github.com/junegunn/vim-plug):
```vim
Plug 'slashmili/alchemist.vim'
Plug 'ncm2/ncm2'

Plug 'pbogut/ncm2-alchemist'
```

Using [Vundle](https://github.com/VundleVim/Vundle.vim):
```vim
Plugin 'slashmili/alchemist.vim'
Plugin 'ncm2/ncm2'

Plugin 'pbogut/ncm2-alchemist'
```

## Configuration

The plugin requires no configuration. However, it is possible to change some
options.

### Available settings

| Variable                        | Default               |
|:--------------------------------|:----------------------|
| `g:ncm2_alchmist_vim_path`      | `find by runtimepath` |

- `g:ncm2_alchmist_vim_path`

Path to `alchemist.vim` plugin, if installed via `Plug` it should be
something like `~/.config/nvim/plugged/alchemist.vim/`. This plugin will try
to find it automatically based on `runtimepath`.

## Contribution

Always welcome.

## Credits

Plugin is based on [ncm2-jedi](https://github.com/ncm2/ncm2-jedi),
[ncm2-go](https://github.com/ncm2/ncm2-go) and
[alchemist.vim](https://github.com/slashmili/alchemist.vim/blob/master/rplugin/python3/deoplete/sources/alchemist.py) deoplete source.

## License

MIT License;
The software is provided "as is", without warranty of any kind.
