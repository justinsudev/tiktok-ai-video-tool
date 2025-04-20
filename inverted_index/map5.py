#!/usr/bin/env python3
"""
MapReduce Job 5: Inverted Index Segmentation.

This mapper prepares data for the final inverted index by segmenting
documents based on document ID modulo 3. This enables distributing
the inverted index across multiple files.

Input: Key: term, Value: doc ID, term frequency, IDF, normalization factor
Output: Key: segment number (docid % 3), Value: term and posting information
"""
import sys

for line in sys.stdin:
    term, docid, tf_s, idf_s, norm_s = line.strip().split("\t")
    seg = int(docid) % 3
    # prefix with segment, then a tab, then the final posting
    print(f"{seg}\t{term} {idf_s} {docid} {tf_s} {norm_s}")
