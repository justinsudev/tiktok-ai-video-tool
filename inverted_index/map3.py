#!/usr/bin/env python3
r"""
MapReduce Job 3: Term Frequency and Document Frequency Preparation.

This mapper processes term frequency data and prepares it for IDF calculation.
It emits two types of key-value pairs:
1. Document frequency count for each term
2. Term-document posting information

Input: Key: term, Value: document ID and term frequency
Output: Key: term, Value: either "DF\t1" or "POST\tdocid\ttf"
"""
import sys

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    term, rest = line.split("\t", 1)
    docid, tf = rest.split()

    # count one DF
    print(f"{term}\tDF\t1")
    # carry the posting
    print(f"{term}\tPOST\t{docid}\t{tf}")
