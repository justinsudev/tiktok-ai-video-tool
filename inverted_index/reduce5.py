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
    parts = line.rstrip("\n").split("\t")
    if len(parts) < 2:
        continue  # Skip malformed lines

    # Get everything after the tab
    rest = parts[1]
    rest_parts = rest.split()
    if len(rest_parts) < 5:
        continue  # Skip malformed lines

    term, idf = rest_parts[0], rest_parts[1]
    docid, tf, norm = rest_parts[2], rest_parts[3], rest_parts[4]

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
