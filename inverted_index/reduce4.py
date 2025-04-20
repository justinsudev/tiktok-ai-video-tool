#!/usr/bin/env python3
r"""
MapReduce Job 4: Document Normalization Factor Calculator.

This reducer calculates the L2 normalization factor for each document
by summing the squares of all term weights and taking the square root.
It then attaches this normalization factor to each term-document pair.

Input: Two types of records:
    1. Key: document ID, Value: "NORM\tsquared_weight"
    2. Key: document ID, Value: "POST\tterm\ttf\tidf"
Output: Key: term, Value: "docid\ttf\tidf\tnorm"
"""
import sys
import math

CURRENT_DOC = None
NORM_SUM = 0.0
POSTINGS = []  # each entry: (term, tf_str, idf_str)


def flush():
    """
    Emit all postings for the last document, with the final L2 norm.

    Calculates the normalization factor for the current document and
    outputs one line for each term in the document with the proper format.
    """
    # We'll modify function to avoid using global
    if CURRENT_DOC is None:
        return

    # compute the normalization factor
    norm = math.sqrt(NORM_SUM)

    # emit one line per term: term \t docid \t tf \t idf \t norm
    for posting_term, posting_tf, posting_idf in POSTINGS:
        print(
            f"{posting_term}\t{CURRENT_DOC}\t{posting_tf}\t"
            f"{posting_idf}\t{norm}"
        )


for line in sys.stdin:
    # expected input: docid \t TAG \t ...
    parts = line.rstrip("\n").split("\t")
    docid, tag = parts[0], parts[1]

    # if we hit a new doc, flush the old one
    if CURRENT_DOC is not None and docid != CURRENT_DOC:
        flush()
        # Reset state after flush
        NORM_SUM = 0.0
        POSTINGS = []

    CURRENT_DOC = docid

    if tag == "NORM":
        # parts = [docid, "NORM", square]
        square = float(parts[2])
        NORM_SUM += square
    else:
        # parts = [docid, "POST", term, tf_s, idf_s]
        _, _, term, tf_s, idf_s = parts
        POSTINGS.append((term, tf_s, idf_s))

# flush the very last document
flush()
