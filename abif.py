#!/usr/bin/python3
"""ABIF - Aggregated Ballot Information Format

The Aggregated Ballot Information Format (ABIF) is a format for
concisely expressing the results of an ranked or rated election.

"""

import abif
import re


class ABIF:
    """Class for parsing Aggregated Ballot Information Format (ABIF) files
    """

    def __init__(self, filename=None):
        """ Initialize ABIF class from file """
        self.ballots = []
        self.filename = filename

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
        count_retval = 0
        for (i, line) in enumerate(self.ballots):
            match = re.search(r'^(\d+)\s*[:\*]', line)
            if match:
                thiscount = int(match.group(1))
                count_retval += thiscount
        self.ballots = count_retval

        return self.ballots


def main():
    """ Test function for running abif.py """

    fnarray = [
        "test001.abif",
        "test002.abif",
        "test003.abif",
        "test004.abif",
        "test005.abif",
        "test006.abif",
        "test007.abif",
        "test008.abif",
        "test009.abif"
    ]

    for filename in fnarray:
        obj = abif.ABIF(filename)
        print("Count of " + obj.filename + " is " + str(obj.count()))


if __name__ == "__main__":
    # execute only if run as a script
    main()