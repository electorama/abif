#!/usr/bin/python3
"""ABIF - Aggregated Ballot Information Format

The Aggregated Ballot Information Format (ABIF) is a format for
concisely expressing the results of an ranked or rated election.

"""

import abif
import argparse
import json
import os
import re

from lark import Lark, Transformer, v_args

from lark.exceptions import UnexpectedToken, UnexpectedCharacters

ABIF_DIR = os.path.dirname(os.path.realpath(__file__, strict=True))
ABIF_GRAMMAR_FILE = os.path.join(ABIF_DIR, 'abif.ebnf')

with open(ABIF_GRAMMAR_FILE, 'r', encoding='utf-8') as f:
    ABIF_GRAMMAR_STR = f.read()

ABIF_WORKING_TESTS = [
    'testfiles/test001.abif',
    'testfiles/test002.abif',
    'testfiles/test003.abif',
    'testfiles/test004.abif',
    'testfiles/test010.abif',
    'testfiles/test011.abif',
    'testfiles/test012.abif',
    'testfiles/test013.abif',
    'testfiles/test015.abif',
    'testfiles/test016.abif',
    'testfiles/test017.abif',
    'testfiles/test018.abif',
    'testfiles/test019.abif'
]


class ABIF_Parser:
    """Class for parsing Aggregated Ballot Information Format (ABIF) files
    """

    def __init__(self):
        self.parser = self.get_parser()
        return None

    def get_parser(self):
        with open(ABIF_GRAMMAR_FILE, "r") as f:
            self.abif_grammar_bnf = f.read()

        self.abif_parser = Lark(self.abif_grammar_bnf,
                                parser="earley",
                                ambiguity="resolve").parse

        return self.abif_parser


class ABIF_File(Transformer):
    """File with ABIF-formatted ballots
    """

    def __init__(self, filename=None, verbose=False):
        """ Initialize ABIF class from file """
        self.ballots = []
        self.filename = filename
        self.err = None
        self.verbose = verbose

        if self.filename == None:
            raise (BaseException())
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

    def transform(self):
        pobj = self.parseobj
        return super().transform(pobj)

    def count(self):
        """ Return the number of ballots represented by abif file """
        # As of 2021-07-19, this ensures that the file parses, and
        # then does a very crude regexp-based count of the ballot
        # bundles.

        # Try running lark-based parser
        self.parse()

        count_retval = 0
        for (i, line) in enumerate(self.ballots):
            match = re.search(r'^(\d+)\s*[:\*]', line)
            if match:
                thiscount = int(match.group(1))
                count_retval += thiscount
        self.ballotqty = count_retval

        return self.ballotqty

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
            self.parseobj = lark_parser(self.file_as_string)
        except UnexpectedCharacters as err:
            self.err = str(err)
            print("ERROR (UnexpectedCharacters): " + self.filename)
            print(self.err)
            if self.verbose:
                print("================")
                print("FILE: " + self.filename)
                print("---------------")
                print(self.file_as_string)
            raise
        except:
            print("ERROR-GACK: " + self.filename)
            if self.verbose:
                print(self.file_as_string)
            raise

        outstr += "================\n"
        outstr += "FILE: " + self.filename + "\n"
        outstr += "---------------\n"
        outstr += self.file_as_string
        if self.parseobj:
            outstr += "================\n"
            outstr += "PARSEOUT:\n"
            outstr += "---------------\n"
            outstr += str(self.parseobj.pretty()) + "\n"
        outstr += "---------------\n"
        return outstr


@v_args(inline=True)
class ABIFtoJabmodTransformer(Transformer):
    def __init__(self):
        super().__init__()
        self.ballotcount = 0
        self.votelines = []
        self.candidates = {}
        self.metadata = {}

    def comment_string(self, token):
        return str(token)

    def comment(self, *args):
        for arg in args:
            if isinstance(arg, str) and arg != '#':
                return ("comment", str(arg))
        return ("comment", "")

    def ballot_count(self, token):
        count = int(token)
        self.ballotcount += count
        return count

    def json_pair(self, key, _, value):
        k = str(key).strip('"')
        v = str(value).strip('"')
        return (k, int(v) if v.isdigit() else v)

    def json_line(self, *items):
        for item in items:
            if isinstance(item, tuple) and len(item) == 2:
                if item[0] != "comment":
                    self.metadata.update(dict([item]))
        return None

    def cand_key(self, token):
        return str(token)

    def cand_square_quoted(self, *tokens):
        # Parse content between brackets
        content = ""
        for token in tokens:
            if str(token) not in ('[', ']'):
                content += str(token)
        return content

    def cand_line(self, *items):
        # Extract candidate ID and name
        if len(items) >= 3 and str(items[0]) == '=':
            id_token = items[1]
            content_index = 3
        else:
            id_token = items[0]
            content_index = 2

        if content_index < len(items):
            name_token = items[content_index]
            cand_id = str(id_token)
            name = str(name_token)

            # Clean up name if it's in square brackets
            if '[' in name and ']' in name:
                name = name.strip('[]')

            self.candidates[cand_id] = name
        return None

    def cand_id(self, token):
        return str(token)

    def cand_tok_rating(self, cand_id, _, rating):
        return {"candidate": str(cand_id), "rating": int(rating)}

    def cand_voter_pref(self, pref):
        if isinstance(pref, dict):
            return pref
        return {"candidate": str(pref), "rating": None}

    def cand_sep(self, sep):
        return str(sep)

    def count_sep(self, *_):
        return ":"

    def cand_element_list(self, *items):
        prefs = []
        separators = []

        for item in items:
            if isinstance(item, dict):
                prefs.append(item)
            elif item in ['>', '=', ',']:
                separators.append(item)

        return {"prefs": prefs, "separators": separators}

    def cands_and_seps(self, elements):
        return elements

    def voteline(self, count, _, elements, *comment_parts):
        preferences = elements["prefs"]
        separators = elements["separators"]

        # Build the preference string
        prefstr_parts = []

        # Extract the comment if present
        comment = None
        for part in comment_parts:
            if isinstance(part, tuple) and part[0] == "comment":
                comment = part[1]

        # Build prefs structure for jabmod
        prefs = {}
        for i, pref in enumerate(preferences):
            candidate = pref["candidate"]
            rating = pref["rating"]

            pref_data = {
                "rating": rating,
                "rank": i + 1
            }

            # Add delimiter if not the last preference
            if i < len(separators):
                pref_data["nextdelim"] = separators[i]
                prefstr_parts.append(
                    f"{candidate}/{rating}{separators[i]}" if rating is not None else f"{candidate}{separators[i]}")
            else:
                prefstr_parts.append(
                    f"{candidate}/{rating}" if rating is not None else candidate)

            prefs[candidate] = pref_data

        # Build the prefstr
        prefstr = "".join(prefstr_parts)

        voteline = {
            "qty": count,
            "comment": comment,
            "prefs": prefs,
            "prefstr": prefstr
        }

        self.votelines.append(voteline)
        return None

    def get_jabmod(self):
        """Return the complete jabmod structure."""
        return {
            "candidates": self.candidates,
            "metadata": {**self.metadata, "ballotcount": self.ballotcount},
            "votelines": sorted(self.votelines, key=lambda x: x["qty"], reverse=True)
        }


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

    if verbose:
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
    parser.add_argument('-j', '--jabmod',
                        help='print JSON ABIF model (jabmod) for given ABIF',
                        action="store_true")
    parser.add_argument('-v', '--verbose',
                        help='print long output',
                        action="store_true")
    parser.add_argument('files', help='optional list of files to test',
                        nargs='*', default=None)
    args = parser.parse_args()

    if (args.files):
        fnarray = args.files
    else:
        parser.print_usage()
        fnarray = get_test_filenames(args.all_tests)

    for filename in fnarray:
        if args.jabmod:
            transformer = ABIFtoJabmodTransformer()
            with open(filename, 'r', encoding='utf-8') as f:
                abif_str = f.read()

            parser = Lark(ABIF_GRAMMAR_STR, parser="lalr", transformer=transformer)
            parser.parse(abif_str)
            jabmod = transformer.get_jabmod()
            print(json.dumps(jabmod, indent=4))
        else:
            print(analyze_file(filename, args.verbose))


if __name__ == "__main__":
    # execute only if run as a script
    main()
