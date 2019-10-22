if get(s:, 'loaded', 0)
    finish
endif
let s:loaded = 1

let g:ncm2_alchemist#proc = yarp#py3('ncm2_alchemist')
let g:ncm2_alchemist#source = extend(get(g:, 'g:ncm2_alchemist#source', {}), {
            \ 'name': 'alchemist',
            \ 'priority': 9,
            \ 'mark': 'alch',
            \ 'scope': ['ex', 'exs', 'elixir'],
            \ 'subscope_enable': 1,
            \ 'word_pattern': '[\w]+',
            \ 'complete_pattern': ['\.'],
            \ 'on_complete': 'ncm2_alchemist#on_complete',
            \ 'on_warmup': 'ncm2_alchemist#on_warmup',
            \ }, 'keep')


func! ncm2_alchemist#init()
    call ncm2#register_source(g:ncm2_alchemist#source)
endfunc

func! ncm2_alchemist#on_warmup(ctx)
    call g:ncm2_alchemist#proc.jobstart()
endfunc

func! ncm2_alchemist#on_complete(ctx)
    call g:ncm2_alchemist#proc.try_notify('on_complete', a:ctx, getline(1, '$'))
endfunc

func! ncm2_alchemist#alchemist_vim_path()
    if empty(get(g:, 'ncm2_alchemist_vim_path'))
      for l:path in split(&runtimepath, ',')
        if l:path =~ '/alchemist.vim/' && !empty(glob(l:path . "elixir_sense"))
          let g:ncm2_alchemist_vim_path = l:path
          break
        endif
      endfor
    endif

    return get(g:, 'ncm2_alchemist_vim_path')
endfunc
