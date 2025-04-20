#!/usr/bin/env python3
r"""
MapReduce Job 3: Inverse Document Frequency Calculator.

This reducer calculates IDF values for each term based on document frequency.
It processes both DF and posting records, computes the IDF, and attaches
it to each term-document pair.

Input: Key: term, Value: either "DF\t1" or "POST\tdocid\ttf"
Output: Key: term, Value: "docid\ttf\tidf"
"""
import sys
import math

# Grab N = total number of documents
with open("total_document_count.txt", "r", encoding="utf-8") as f:
    N = int(f.read().strip())

CURRENT = None
DF = 0
postings = []  # (docid, tf)


def flush():
    """
    Process the current term by calculating its IDF and emitting records.

    For each posting of the current term, emit a line with:
    term, document ID, term frequency, and inverse document frequency.
    """
    if not CURRENT:
        return
    idf = math.log10(N/DF) if DF else 0.0

    for current_docid, current_tf in postings:
        # emit term\tdocid\ttf\tidf
        print(f"{CURRENT}\t{current_docid}\t{current_tf}\t{idf}")


for line in sys.stdin:
    parts = line.rstrip("\n").split("\t")
    term, tag = parts[0], parts[1]
    if CURRENT and term != CURRENT:
        flush()
        DF = 0
        postings = []
    CURRENT = term
    if tag == "DF":
        DF += int(parts[2])
    else:  # POST
        docid, tf = parts[2], parts[3]
        postings.append((docid, tf))

flush()
