import win32clipboard

if __name__ == '__main__':
    formats = {val: name for name, val in vars(win32clipboard).items() if name.startswith('CF_')}


    def format_name(fmt):
        if fmt in formats:
            return formats[fmt]
        try:
            return win32clipboard.GetClipboardFormatName(fmt)
        except:
            return "unknown"


    win32clipboard.OpenClipboard(None)

    fmt = 0
    while True:
        fmt = win32clipboard.EnumClipboardFormats(fmt)
        if fmt == 0: break
        print('{:5} ({})'.format(fmt, format_name(fmt)))

    win32clipboard.CloseClipboard()

fmts = {
    1: 'CF_TEXT', 2: 'CF_BITMAP', 3: 'CF_METAFILEPICT', 4: 'CF_SYLK', 5: 'CF_DIF', 6: 'CF_TIFF', 7: 'CF_OEMTEXT',
    8: 'CF_DIB', 9: 'CF_PALETTE', 10: 'CF_PENDATA', 11: 'CF_RIFF', 12: 'CF_WAVE', 13: 'CF_UNICODETEXT',
    14: 'CF_ENHMETAFILE', 15: 'CF_HDROP', 16: 'CF_LOCALE', 17: 'CF_DIBV5', 18: 'CF_MAX', 128: 'CF_OWNERDISPLAY',
    129: 'CF_DSPTEXT', 130: 'CF_DSPBITMAP', 131: 'CF_DSPMETAFILEPICT', 142: 'CF_DSPENHMETAFILE'
}

_available = {13, 1, 49329, 50105, 16, 7}
available = {code: name for code, name in fmts.items() if code in _available}
res = {1: 'CF_TEXT', 7: 'CF_OEMTEXT', 13: 'CF_UNICODETEXT', 16: 'CF_LOCALE'}
