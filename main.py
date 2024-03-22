from LaTeXpy import LaTeX

# redo packages?

# packages = { # from : what
#     'inputenc'  : ['utf8'],  
#     'babel'     : ['russian'],
#     'amsmath'   : [],
#     'esdiff'    : ['thinc'],
#     'mathtools' : [],
#     'fontenc'   : ['T1'],
#     'geometry'  : ['top=26mm', 'bottom=20mm', 'left=20mm', 'right=20mm'],
# }

docSettings: dict[str, str       |
                       list[str] |
                       list[dict[str, str |
                                      list[str]]]] = {
    'fileName'     : 'myFile',
    'filePath'     : 'default', # latex folder dir
    'fileMode'     : 'w',
    'fileEncoding' : 'utf-8',
    'docClassType' : 'article',
    'docClassPars' : ['a4paper, 12pt, oneside'],
    'packages'     : [
        {
            'packageName' : 'babel',
            'packageArgs' : ['russian']
        },
        {
            'packageName' : 'amsmath',
            'packageArgs' : ['']
        },
        {
            'packageName' : 'geometry',
            'packageArgs' : ['top=26mm', 'bottom=20mm', 'left=20mm', 'right=20mm']
        },
        # ...
    ],
    'title'  : 'title', # no title
    'author' : 'author', # no author
}

if __name__ == '__main__':
    # print(LaTeX.docSettingsTemplate)
    
    doc = LaTeX()
