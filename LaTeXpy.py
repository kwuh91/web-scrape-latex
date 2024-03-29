from typing import TextIO
import os
import atexit

from validation import is_path_exists_or_creatable, \
                       is_path_exists_or_creatable_portable, \
                       validFileModes, \
                       validDocClasses

class LaTeX:
  
    # constructor
    def __init__(self, settings: dict[str, str       |
                                           list[str] |
                                           dict[str, list[str]]] = None):
        # declare class fields
        self.__cleanup_required:  bool = True  # needed for atexit && __exit__ logic
        self.__isPackages:        bool = False # are there any packages ?      

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

        if fileMode in validFileModes:
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
        if docClassType in validDocClasses:
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

        # finish up
        if self.__title:
            self.__file.write(f'\n')

            textVar = f'\\begin{{document}}'
            self.__file.write(textVar + '\n')

            textVar = f'\\maketitle'
            self.__file.write(textVar + '\n')

        else:
            textVar = f'\\begin{{document}}'
            self.__file.write(textVar + '\n')

        self.__file.write(f'\n')

        atexit.register(self.__cleanup)

    def __str__(self) -> str:
        pass # todo

    def __repr__(self) -> str:
        pass # todo

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.__cleanup

    def __cleanup(self):
        textVar: str
        if self.__cleanup_required:
            # ... cleanup logic

            textVar = f'\\end{{document}}'
            self.__file.write(textVar + '\n')

            self.__file.close()

            self.__cleanup_required = False

    # json document settings template
    docSettingsTemplate: str = \
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
