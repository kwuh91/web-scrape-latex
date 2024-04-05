from typing import TextIO
import os
import atexit

from validation import is_path_exists_or_creatable, \
                       is_path_exists_or_creatable_portable, \
                       VALID_FILE_MODES, \
                       VALID_DOC_CLASSES

class LaTeX:
  
    # constructor
    def __init__(self, settings: dict[str, str       |
                                           list[str] |
                                           dict[str, list[str]]] = None):
        # declare class fields
        self.__cleanup_required:  bool = True  # needed for atexit && __exit__ logic
        self.__isPackages:        bool = False # are there any packages ?      
        self.__islastCharacterNL: bool = False

        self.__fileNameExtension: str 
        self.__fileName:          str 
        self.__filePath:          str
        self.__fileMode:          str
        self.__fileEncoding:      str
        self.__file:              TextIO
        self.__docClassType:      str
        self.__docClassPars:      list[str]
        self.__packages:          dict[str, list[str]]
        
        self.__title:             str
        self.__author:            str

        textVar:                  str    

        # set default parameters
        if settings is None:
            settings = {
                'fileName'     : 'myFile',
                'filePath'     : 'default', 
                'fileMode'     : 'w',
                'fileEncoding' : 'utf-8',
                'docClassType' : 'article',
                'docClassPars' : [''],
                'packages'     : {},
                'title'  : '', 
                'author' : '', 
            }

        self.__fileNameExtension = '.tex'
        self.__fileName          = settings['fileName'] + \
                                   self.__fileNameExtension

        # set file path
        if settings['filePath'] == 'default':
            # latex folder path
            latexFolderPath: str = os.path.join(os.path.dirname(__file__), 'latex')

            self.__filePath = os.path.join(latexFolderPath, self.__fileName)

        else:
            filePath: str = settings['filePath']

            # validate path
            if is_path_exists_or_creatable(filePath):
                self.__filePath = os.path.join(filePath, self.__fileName)
            else:
                raise Exception('invalid path')

        # validate file mode
        fileMode: str = settings['fileMode']

        if fileMode in VALID_FILE_MODES:
            self.__fileMode = fileMode
        else:
            raise Exception('invalid file mode')

        # set file encoding
        self.__fileEncoding = settings['fileEncoding']

        # open file
        self.__file = open(file     = self.__filePath, 
                           mode     = self.__fileMode, 
                           encoding = self.__fileEncoding)
        
        # initialize .tex doc
        textVar = f'\\documentclass'
        docClassPars: list[str] = settings['docClassPars']
        docClassParsIsEmpty: bool = not any(bool(i) for i in docClassPars)

        # iterate through docClass parameters
        if not docClassParsIsEmpty:
            textVar += f'['

            sizePars: int = len(docClassPars)
            self.__docClassPars = docClassPars
            index: int
            docClassPar: str
            for index, docClassPar in enumerate(self.__docClassPars):
                textVar += docClassPar
                textVar += f', ' if index < sizePars - 1 else f']'
        
        # validate document class type
        docClassType: str = settings['docClassType']
        if docClassType in VALID_DOC_CLASSES:
            self.__docClassType = docClassType
        else:
            raise Exception('invalid document class type')

        textVar += f'{{{self.__docClassType}}}'
        self.__file.write(textVar + '\n\n')
        
        # import packages
        self.__packages = settings['packages']
        packageName: str
        packageArgs: list[str]
        for packageName, packageArgs in self.__packages.items():     
            textVar = f'\\usepackage'

            packageNameIsEmpty: bool = not bool(packageName)
            packageArgsIsEmpty: bool = not any(bool(i) for i in packageArgs)

            packageArgsSize: int = len(packageArgs)
            
            if packageNameIsEmpty and not packageArgsIsEmpty:       # packageName is     empty
                raise Exception('no package name given')            # packageArgs is not empty
            
            elif not packageNameIsEmpty and packageArgsIsEmpty:     # packageName is not empty
                textVar += f'{{{packageName}}}'                     # packageArgs is     empty
            
            elif not packageNameIsEmpty and not packageArgsIsEmpty: # packageName is not empty
                textVar += f'['                                     # packageArgs is not empty

                index: int
                packageArg: str
                for index, packageArg in enumerate(packageArgs):
                    textVar += packageArg
                    textVar += f', ' if index < packageArgsSize - 1 else f']'

                textVar += f'{{{packageName}}}'
            
            else:                                                   # packageName is     empty
                textVar = ''                                        # packageArgs is     empty

            if textVar:     
                if not self.__isPackages:
                    self.__file.write(f'% Preamble\n')

                self.__file.write(textVar + '\n')
                self.__isPackages = True

        if self.__isPackages:
            self.__file.write(f'\n')
        
        # write title to file
        self.__title = settings['title']
        if self.__title:
            textVar = f'% Document metadata'
            self.__file.write(textVar + '\n')
            
            textVar = f'\\title{{{self.__title}}}'
            self.__file.write(textVar + '\n')

        # write author to file
        self.__author = settings['author']
        if self.__title and self.__author:
            textVar = f'\\author{{{self.__author}}}'
            self.__file.write(textVar + '\n')

        if self.__title:
            self.__file.write(f'\n')

        textVar = f'\\newcommand{{\\lt}}{{\\ensuremath <}}'
        self.__file.write(textVar + '\n')
        textVar = f'\\newcommand{{\\gt}}{{\\ensuremath >}}'
        self.__file.write(textVar + '\n')

        self.__file.write(f'\n')

        # finish up
        if self.__title:
            textVar = f'\\begin{{document}}'
            self.__file.write(textVar + '\n')

            textVar = f'\\maketitle'
            self.__file.write(textVar + '\n')

        else:
            textVar = f'\\begin{{document}}'
            self.__file.write(textVar + '\n')

        self.__islastCharacterNL = True

        atexit.register(self.__cleanup)

    def __str__(self) -> str:
        pass # todo

    def __repr__(self) -> str:
        pass # todo

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.__cleanup

    def __cleanup(self) -> None:
        textVar: str
        if self.__cleanup_required:
            # ... cleanup logic

            textVar = f'\\end{{document}}'
            textVar = '\n' + textVar if self.__islastCharacterNL else '\n\n' + textVar
            self.__file.write(textVar + '\n')

            self.__file.close()

            self.__islastCharacterNL = True
            self.__cleanup_required  = False

    # decorator which adapts string for latex
    def __prepareText(func):
        def __wrapper(self, text: str, *args, **kwargs) -> None:
            text = text.replace('∪', '\\cup ')
            text = text.replace('∑', '\\sum')
            text = text.replace('…', '\\ldots ')

            return func(self, text, *args, **kwargs)
        return __wrapper

    @__prepareText
    def writeSection(self, text: str, centered=True) -> None:
        textVar: str

        textVar = f'\\section*{{\\centerline{{{text}}}}}' if centered else f'\\section*{{{text}}}'
        self.__file.write('\n' + textVar + '\n')
        self.__islastCharacterNL = True

    @__prepareText
    def writeSubSection(self, text: str) -> None:
        textVar: str

        textVar = f'\\subsection*{{{text}}}'
        self.__file.write('\n' + textVar + '\n\n')
        self.__islastCharacterNL = True

    @__prepareText
    def write(self, text: str) -> None:
        self.__file.write(text + ' ')
        self.__islastCharacterNL = False

    @__prepareText
    def writeFormula(self, text: str, display=False) -> None:
        textVar: str

        if display:
            textVar = '' if self.__islastCharacterNL else '\n'

            textVar += f'\\begin{{gather*}}\n'
            textVar += f'{text}\n'
            textVar += f'\\end{{gather*}}'

            textVar += '\n'
            self.__islastCharacterNL = True
        else:
            textVar = f'${text}$'

            textVar += ' '
            self.__islastCharacterNL = False

        self.__file.write(textVar)

    # json document settings template
    DOC_SETTINGS_TEMPLATE: str = \
        "docSettings: dict[str, str       |                 \n" \
        "                       list[str] |                 \n" \
        "                       dict[str, list[str]]] = {   \n" \
        "    'fileName'     : 'myFile',                     \n" \
        "    'filePath'     : 'default', # latex folder dir \n" \
        "    'fileMode'     : 'w',                          \n" \
        "    'fileEncoding' : 'utf-8',                      \n" \
        "    'docClassType' : 'article',                    \n" \
        "    'docClassPars' : [''],                         \n" \
        "    'packages'     : { # from : what               \n" \
        "        'packageName' : ['packageArgs'],           \n" \
        "        # ...                                      \n" \
        "    },                                             \n" \
        "    'title'  : '', # no title                      \n" \
        "    'author' : '', # no author                     \n" \
        "}                                                  \n" \
