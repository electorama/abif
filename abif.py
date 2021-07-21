#!/usr/bin/python3
"""ABIF - Aggregated Ballot Information Format

The Aggregated Ballot Information Format (ABIF) is a format for
concisely expressing the results of an ranked or rated election.

"""

import abif
import argparse
import re

from lark import Lark, Transformer, v_args
from lark.exceptions import UnexpectedToken, UnexpectedCharacters

ABIF_GRAMMAR_FILE = 'abif.ebnf'

ABIF_WORKING_TESTS = [
    'testfiles/test001.abif',
    'testfiles/test002.abif',
    'testfiles/test003.abif',
    'testfiles/test004.abif',
    'testfiles/test010.abif',
    'testfiles/test011.abif',
    'testfiles/test012.abif',
    'testfiles/test013.abif',
    'testfiles/test014.abif'
]


class ABIF_Parser():
    """Class for parsing Aggregated Ballot Information Format (ABIF) files
    """

    def __init__(self):
        return None

    def get_parser(self):
        with open("abif.ebnf", "r") as f:
            self.abif_grammar_bnf = f.read()

        self.abif_parser = Lark(self.abif_grammar_bnf).parse

        return self.abif_parser


class ABIF_File:
    """File with ABIF-formatted ballots
    """

    def __init__(self, filename=None, verbose=False):
        """ Initialize ABIF class from file """
        self.ballots = []
        self.filename = filename
        self.err = None
        self.verbose = verbose

        if self.filename == None:
            raise(BaseException())
        else:
            self._load()
        return None

    def _load(self):
        """ Load ABIF file into memory """

        i = 0
        with open(self.filename) as f:
            for (i, line) in enumerate(f):
                self.ballots.append(line)

        return self.filename

    def count(self):
        """ Return the number of ballots represented by abif file """
        # As of 2021-07-19, this ensures that the file parses, and
        # then does a very crude regexp-based count of the ballot
        # bundles.

        # Try running lark-based parser
        try:
            self.parse()
        except:
            # Presumably an invalid file
            #
            # FIXME: put much better exception handling, and perhaps
            # even use the parser to perform the count.
            return None
        count_retval = 0
        for (i, line) in enumerate(self.ballots):
            match = re.search(r'^(\d+)\s*[:\*]', line)
            if match:
                thiscount = int(match.group(1))
                count_retval += thiscount
        self.ballots = count_retval

        return self.ballots

    def _read_file(self):
        afilehandle = open(self.filename, 'r')
        self.file_as_string = afilehandle.read()
        afilehandle.close()

    def _get_error_string(self):
        return self.err

    def parse(self):
        """ Parse file using Lark parser, returning output as text blob
        """

        self._read_file()

        lark_parser = abif.ABIF_Parser().get_parser()

        outstr = ""
        try:
            parseresult_obj = lark_parser(self.file_as_string)
        except UnexpectedCharacters as err:
            self.err = str(err)
            print("ERROR (UnexpectedCharacters): " + self.filename)
            print(self.err)
            if(self.verbose):
                print("================")
                print("FILE: " + self.filename)
                print("---------------")
                print(self.file_as_string)
            raise
        except:
            print("ERROR-GACK: " + self.filename)
            if(self.verbose):
                print(self.file_as_string)
            raise

        outstr += "================\n"
        outstr += "FILE: " + self.filename + "\n"
        outstr += "---------------\n"
        outstr += self.file_as_string
        if(parseresult_obj):
            outstr += "================\n"
            outstr += "PARSEOUT:\n"
            outstr += "---------------\n"
            outstr += str(parseresult_obj.pretty()) + "\n"
        outstr += "---------------\n"
        return outstr


def get_test_filenames(allfiles=False):
    from os import listdir
    from os.path import join

    fnarray = []
    if allfiles:
        for f in listdir('testfiles'):
            if f.endswith('abif'):
                fnarray.append(join('testfiles', f))

        fnarray.sort()
    else:
        fnarray = ABIF_WORKING_TESTS

    return fnarray


def analyze_file(afilename, verbose):
    obj = abif.ABIF_File(afilename, verbose=verbose)

    if(verbose):
        outstr = obj.parse()
    else:
        outstr = ""

    outstr += obj.filename + " -- Count: "
    outstr += str(obj.count())

    return outstr


def main():
    """ Test function for running abif.py """

    parser = argparse.ArgumentParser(description=__doc__.splitlines()[1])

    parser.add_argument('--all-tests', help='get all tests from testfiles dir',
                        action="store_true")
    parser.add_argument('-v', '--verbose',
                        help='print long output',
                        action="store_true")
    parser.add_argument('files', help='optional list of files to test',
                        nargs='*', default=None)
    args = parser.parse_args()

    if(args.files):
        fnarray = args.files
    else:
        parser.print_usage()
        fnarray = get_test_filenames(args.all_tests)

    for filename in fnarray:
        print(analyze_file(filename, args.verbose))


if __name__ == "__main__":
    # execute only if run as a script
    main()

