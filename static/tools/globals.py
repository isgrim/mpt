# -*- coding: utf-8 -*-
"""
Global Variables and global functions

"""


__author__ = "Dulip Withanage"

import json
import os
import sys
from lxml import etree

from debug import Debuggable, Debug

numeral_map = tuple(zip(
    (1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1),
    ('M', 'CM', 'D', 'CD', 'C', 'XC', 'L', 'XL', 'X', 'IX', 'V', 'IV', 'I')
))


class GV(object):
    '''    Global variables    '''

    def __init__(self):
        # GLOBAL VARIABLES

        # projects
        self.PROJECT_INPUT_FILE_JSON_IS_NOT_VALID = u'project input file json is not valid'
        self.PROJECT_INPUT_FILE_TYPE_IS_NOT_SPECIFIED = u'project input file type is not specified'
        self.PROJECT_INPUT_FILE_HAS_MORE_THAN_TWO_DOTS = u'project input file has more than two dots'
        self.PROJECT_INPUT_FILE_DOES_NOT_EXIST = u'project input_file does not exist'
        self.PROJECT_IS_NOT_ACTIVE = u'project is not active'
        self.PROJECT_OUTPUT_FILE_IS_NOT_DEFINED = u'project output file is not defined'
        self.PROJECT_OUTPUT_FILE_WAS_NOT_CREATED = u'project output file was not created'
        self.PROJECT_TYPESETTER_IS_NOT_AVAILABLE = u'project typesetter is not available'
        self.PROJECT_TYPESETTER_IS_NOT_SPECIFIED = u'project typesetter is not specified'
        self.PROJECT_TYPESETTER_NAME_IS_NOT_SPECIFIED = u'project typesetter name is not specified'
        self.PROJECT_TYPESETTER_VAR_IS_NOT_SPECIFIED = u'project typesetter varaible is not specified'
        self.PROJECT_TYPESETTERS_ARE_NOT_SPECIFIED = u'project typesetters are not specified'
        self.PROJECTS_VAR_IS_NOT_SPECIFIED = u'project variable is not  specified'
        self.PROJECTS_TYPESETTER_RUNS_WITH_NO_ARGUMENTS = u'projects typesetter runs with no arguments'

        # typesetter errors
        self.TYPESETTER_EXECUTABLE_VARIABLE_IS_UNDEFINED = u'typesetter executable variable is undefined'
        self.TYPESETTER_FILE_OUTPUT_TYPE_IS_UNDEFINED = u'typesetter file output type is undefined'
        self.TYPESETTER_METADATA_FILE_WAS_NOT_SPECIFIED = u'Metadata file wasn\'t specified '
        self.TYPESETTER_METYPESET_RUNS_WITH_DEFAULT_METADATA_FILE = u'typesetter metypeset runs with default metadata file'
        self.TYPESETTER_IS_NOT_SPECIFIED = u'typesetter is not specified '
        self.TYPESETTER_PATH_IS_NOT_SPECIFIED = u'typesetter path is not specified '
        self.TYPESETTER_BINARY_IS_UNAVAILABLE = u'typesetter binary is unavailable '
        self.TYPESETTER_RUNS_WITH_NO_ARGUMENTS = u'typesetter runs with no arguments'

        # xml
        self.XML_ELEMENT_NOT_FOUND = u'xml element not found'
        self.XML_FILE_NOT_CREATED = u'xml file not created'
        self.XML_INPUT_FILE_IS_NOT_FOUND = u'xml input file is not found'
        self.XML_INPUT_FILE_IS_NOT_VALID = u'xml input file is not valid'

        # WORDS
        self.OUTPUT_FOLDER = u'Output Folder'

        self.debug = Debug()
        self.numeral_map = numeral_map

        self.version='0.0.1'

    @staticmethod
    def fatal_error(module, message):
        """
        Prints a formatted error message and exits

        Parameters
        ----------
        module: python module
             Returns the name of the module
        message: str
            Error message


        See Also
        --------
        module.get_module_name()

        """
        print(u'[FATAL ERROR] [{0}] {1}'.format(
            module.get_module_name(), message))
        sys.exit(1)

    def is_json(self, s):
        """
        Checks whether a string is valid json string

        Parameters
        ----------
        s : str
            JSON data as string

        Raises
        ------
        ValueError  error
             Inappropriate json string

        """
        try:
            return json.loads(s)
        except ValueError as e:
            return False
        return True

    def read_json(self, pth):
        """
        Reads a json file from system path or exits

        Parameters
        ----------
        pth: str
             path of the  file in the folder structure

        Returns
        -------
        json : json
            json object

        """
        if os.path.isfile(pth):
            with open(pth) as j:
                return json.load(j)
        else:
            self.debug.print_debug(
                self, self.PROJECT_INPUT_FILE_JSON_IS_NOT_VALID)
            sys.exit(1)

    def create_dirs_recursive(self, pth):
        """
        Recursively create directories for a system path or exists if folder exists

        Parameters
        ----------
        pth : str
            system path to be created

        """
        p = ''
        for path in pth:
            p = p + os.path.sep + path.strip('/').strip('/')
            if not os.path.exists(p):
                try:
                    os.makedirs(p)
                except OSError as o:
                    print o
                    sys.exit(1)
        return p

    def set_numbering_tags(self, tags ,tr):
        """
        Automatic numbering of the list of elements

        Parameters
        ----------
        tags: list
         list of elements

        Returns
        -------
        tr : elementtree


        """
        for tag in tags:
            sh = tr.findall('.//' + tag)
            sid = 1
            for i in sh:
                i.set('id', tag.replace('-', '') + str(sid))
                sid += 1
        return tr