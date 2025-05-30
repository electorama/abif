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

FOOTER = """----------------
For more detailed analysis, try abiftool or awt (the "abif web tool")
which can be found at the following locations:
 * abiftool: https://github.com/electorama/abiftool
 *      awt: https://abif.electorama.com/
"""


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

    def metadata_pair(self, key, colon, value):
        retkey = str(key).strip('"')
        retval = value
        return (retkey, retval)

    def metadata_key(self, key):
        return key

    def metadata_value(self, value):
        if isinstance(value, str):
            if value == "true":
                retval = True
            elif value == "false":
                retval = False
            elif value == "null":
                retval = None
            elif value.startswith('"') and value.endswith('"'):
                # Strip quotes but keep as a string
                retval = value[1:-1]
            elif re.fullmatch(r'-?\d+', value):
                return int(value)
            # regex for simple decimal/floating-point number
            elif re.fullmatch(r'-?\d+\.\d+', value):
                retval = float(value)
            else:
                retval = value

        return retval

    def metadata_line(self, *items):
        for item in items:
            if isinstance(item, tuple) and len(item) == 2:
                key, value = item
                if key != "comment":
                    self.metadata[key] = value
        return None

    def cand_key(self, token):
        return str(token).strip('"')

    def cand_square_quoted(self, open_bracket, content, close_bracket):
        return str(content)

    def cand_tok(self, item):
        return item

    def cand_id_sep(self, colon):
        return colon

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

            # Process name from the token
            # If already processed by cand_square_quoted, it will be a string
            name = str(name_token)

            self.candidates[cand_id] = name
        return None

    def cand_id(self, token):
        # Always return a dictionary to be consistent with cand_tok_rating
        return {"candidate": str(token), "rating": None}

    def cand_tok_rating(self, cand_id, _, rating):
        # Make sure cand_id is properly handled whether it's a string or dict
        candidate = cand_id["candidate"] if isinstance(cand_id, dict) else str(cand_id)
        return {"candidate": candidate, "rating": int(rating)}

    # This method ensures preference items are always dictionaries
    def pref_item(self, item):
        if isinstance(item, dict) and "candidate" in item:
            return item
        elif isinstance(item, str):
            return {"candidate": item, "rating": None}
        return item

    def pref_sep(self, sep):
        return str(sep)

    def eq(self, *args):
        return "="

    def gt(self, *args):
        return ">"

    def comma(self, *args):
        return ","

    def count_sep(self, *args):
        return ":"

    def prefs(self, first_item, *args):
        prefs = [first_item]
        separators = []

        for i, arg in enumerate(args):
            if isinstance(arg, str) and arg in ['>', '=', ',']:
                separators.append(arg)
            elif isinstance(arg, dict) and "candidate" in arg:
                prefs.append(arg)

        return {"prefs": prefs, "separators": separators}

    def voteline(self, count, _, elements=None, *comment_parts):
        # Handle case of blank ballots
        preferences = []
        separators = []

        if elements:
            preferences = elements.get("prefs", [])
            separators = elements.get("separators", [])

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

            pref_data = {}
            pref_data["rank"] = i + 1
            if rating:
                pref_data["rating"] = rating

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
            "metadata": {"ballotcount": self.ballotcount, **self.metadata},
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


def convert_abif_file_to_jabmod(abif_filename):
    with open(abif_filename, 'r', encoding='utf-8') as f:
        abif_str = f.read()

    transformer = ABIFtoJabmodTransformer()
    parser = Lark(ABIF_GRAMMAR_STR, parser="lalr", transformer=transformer)
    parser.parse(abif_str)
    return transformer.get_jabmod()


def analyze_file(abif_filename, verbose):
    jabmod = convert_abif_file_to_jabmod(abif_filename)

    outstr = ""
    if verbose:
        outstr += f"====================================================================\n"
        outstr += f"Analysis for {abif_filename}:\n"
        outstr += f" Ballot count: {jabmod['metadata']['ballotcount']}\n"
        outstr += f" Candidates:\n"
        for candkey, candval in jabmod['candidates'].items():
            outstr += f" * {candkey}: {candval}\n"
    else:
        outstr += f"{abif_filename} ballot count: {jabmod['metadata']['ballotcount']}\n"
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
            jabmod = convert_abif_file_to_jabmod(filename)
            print(json.dumps(jabmod, indent=4))
        else:
            print(analyze_file(filename, args.verbose), end="")
    if args.verbose:
        print(FOOTER)


if __name__ == "__main__":
    # execute only if run as a script
    main()
