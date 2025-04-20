#!/usr/bin/env python3 -u
r"""
MapReduce Job 2: Term Frequency Calculator.

This reducer counts occurrences of each term within each document.
It groups by (term, docid) pairs and emits the term frequency.

Input: Key: term, Value: document ID
Output: Key: term, Value: "docid\tterm_frequency"
"""
import sys

CURRENT_TERM = None   # tuple (term, docid)
COUNT = 0


def flush():
    """
    Emit all term-document pairs with the accumulated count.

    If the current term is None, return without emitting anything.
    """
    if CURRENT_TERM is None:
        return

    current_term, current_docid = CURRENT_TERM
    # Emit the raw count (not 1 + log10(count))
    print(f"{current_term}\t{current_docid}\t{COUNT}")


for line in sys.stdin:
    term, docid = line.rstrip("\n").split("\t")
    key = (term, docid)
    if CURRENT_TERM and key != CURRENT_TERM:
        flush()
        COUNT = 0
    CURRENT_TERM = key
    COUNT += 1

# Last one
flush()
