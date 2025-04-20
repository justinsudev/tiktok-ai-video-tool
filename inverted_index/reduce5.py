#!/usr/bin/env python3
"""
MapReduce Job 5: Final Inverted Index Formatter.

This reducer creates the final inverted index format by grouping all
document occurrences for each term onto a single line. It formats each
line as: "term idf docid1 tf1 norm1 docid2 tf2 norm2 ..."

Input: Key: segment number, Value: term and posting information
Output: Formatted inverted index lines with term and all document occurrences
"""
import sys

CURRENT_TERM = None
CURRENT_IDF = None
CURRENT_LINE = ""

for line in sys.stdin:
    # each line is "seg\tterm idf docid tf norm"
    # Get everything after the tab
    _, rest = line.rstrip("\n").partition("\t")[::2]
    parts = rest.split()

    term, idf = parts[0], parts[1]
    docid, tf, norm = parts[2], parts[3], parts[4]

    if term != CURRENT_TERM:
        # Emit the previous term's line
        if CURRENT_TERM:
            print(CURRENT_LINE)

        # Start a new term
        CURRENT_TERM = term
        CURRENT_IDF = idf
        CURRENT_LINE = f"{term} {idf} {docid} {tf} {norm}"
    else:
        # Add to the current term
        CURRENT_LINE += f" {docid} {tf} {norm}"

# Emit the last term's line
if CURRENT_TERM:
    print(CURRENT_LINE)
