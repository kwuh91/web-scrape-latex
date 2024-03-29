from LaTeXpy import LaTeX

docSettings: dict[str, str       |
                       list[str] |
                       dict[str, list[str]]] = {
    'fileName'     : 'myFile',
    'filePath'     : 'default', # latex folder dir
    'fileMode'     : 'w',
    'fileEncoding' : 'utf-8',
    'docClassType' : 'article',
    'docClassPars' : ['a4paper, 12pt, oneside'],
    'packages'     : { 
        'babel'     : ['russian'],
        'amsmath'   : [],
        'geometry'  : ['top=26mm', 'bottom=20mm', 'left=20mm', 'right=20mm'],
        # ...
    },
    'title'  : 'title', # no title
    'author' : 'author', # no author
}

if __name__ == '__main__':
    # print(LaTeX.docSettingsTemplate)
    
    doc = LaTeX(docSettings)
