#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Reads a xml file , transforms it to a intermediate format (e.g. formattion objects: FO ) and converts  to PDF subsequently


Usage:
    xmlDisseminate.py  <input_file>  <path>  [options]
Options:
    -d, --debug  Enable debug output
    -s --saxon=<location_of_the_saxon_jar_file>
    -x --xsl=<filename>     Stylesheet file



Example
--------

python $BUILD_DIR/static/tools/xmlDisseminate.py


"""

__author__ = "Dulip Withanage"

from debug import Debuggable, Debug
from globals import GV
import sys
import os
from docopt import docopt
from subprocess import Popen, PIPE


class XD(Debuggable):

    def __init__(self):
        self.args = self.read_command_line()
        self.debug = Debug()
        self.gv = GV()
        Debuggable.__init__(self, 'Main')
        if self.args.get('--debug'):
            self.debug.enable_debug()
        self.dr = self.args.get('<path>')
        self.f = self.args.get('<input_file>')

    @staticmethod
    def read_command_line():
        """
        Reads and  generates a docopt dictionary from the command line parameters.

        Returns
        -------
        docopt : dictionary
          A dictionary, where keys are names of command-line elements  such as  and values are theparsed values of those
          elements.
        """
        return docopt(__doc__, version='xml2PDF 0.1')

    def check_saxon(self):
        """Checks if saxon is available in the default path

        Returns
        --------
        saxon : boolean
            True, if saxon is available. False, if not.

        """
        s='meTypeset/runtime/saxon9.jar'
        if os.path.isfile(s):
            return s
        elif self.args.get('--saxon'):
            if os.path.isfile(self.args.get('--saxon')):
                return self.args.get('--saxon')
            else:
                return False
        else:
            return False


    def get_module_name(self):
        """
        Reads the name of the module for debugging and logging

        Returns
        -------
        name string
         Name of the Module
        """
        name = 'XML PDF Converter'
        return name
    def process(self, args):
        """Runs  typesetter with given arguments

        Creates the execution path for  the conversion process. Output,exit-code and  system error codes are captured and returned.


        Parameters
        ----------
        args : list
            application arguments in the correct oder.


        Returns
        -------
        output :str
            system standard output.
        err :str
            system standard error.
        exit_code: str
            system exit_code.

        See Also
        --------
        subprocess.Popen()

        """

        m = ' '.join(args).strip().split(' ')
        process = Popen(m, stdout=PIPE)
        output, err = process.communicate()
        exit_code = process.wait()
        return output, err, exit_code

    def run(self):
        """
        Runs the  converter

        See Also
        --------
        check_saxon, process

        """
        if not self.check_saxon():
            self.debug.print_debug(self, self.gv.SAXON_IS_NOT_AVAILABLE)
            sys.exit(1)
        else:
            self.debug.print_console(self, self.gv.RUNNING_SAXON_CONVERSION)
            args=["java","-jar",self.check_saxon()]
            output, err, exit_code = self.process(args)
            if exit_code == 1:
                print err
                sys.exit(1)
"""
/usr/local/mpt/static/stylesheets/heiup_formatter.xsl
java -jar /Volumes/DATENSTICK/14\ XSL-FO/bin/saxon/saxon9he.jar
-s:/Volumes/DATENSTICK/14\ XSL-FO/out/xml/Testdokument.xml
-xsl:/Volumes/DATENSTICK/14\ XSL-FO/stylesheets/heiup_formatter.xsl
-o:/Volumes/DATENSTICK/14\ XSL-FO/out/fo/Testdokument_epdf_xep.fo
medium=electronic formatter=XEP

/bin/xep/xep
-fo /Volumes/DATENSTICK/14\ XSL-FO/out/fo/Testdokument_epdf_xep.fo
-pdf /Volumes/DATENSTICK/14\ XSL-FO/out/pdf/Testdokument_epdf_xep.pdf

/usr/local/AHFormatterV63/run.sh
-d /Volumes/DATENSTICK/14\ XSL-FO/out/fo/Testdokument_epdf_ah.fo
-o /Volumes/DATENSTICK/14\ XSL-FO/out/pdf/Testdokument_epdf_ah.pdf
"""
def main():
    """
    Calls the conversion process

    See Also
    --------
    run

    """
    xp = XD()
    xp.run()


if __name__ == '__main__':
    main()
