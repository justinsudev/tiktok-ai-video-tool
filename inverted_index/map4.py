#!/usr/bin/env python3
r"""
MapReduce Job 4: TF-IDF Weight Calculator.

This mapper calculates term weights using TF-IDF scores and
prepares data for normalization calculation.

Input: Key: term, Value: document ID, term frequency, and IDF
Output: Two types of records:
    1. Key: document ID, Value: "NORM\tsquared_weight"
    2. Key: document ID, Value: "POST\tterm\ttf\tidf"
"""
import sys

for line in sys.stdin:
    line = line.strip()

    # Split the line once and extract each component by index
    parts = line.split("\t")
    term = parts[0]
    docid = parts[1]
    tf_s = parts[2]
    idf_s = parts[3]

    # Convert to float for calculation
    tf = float(tf_s)
    idf = float(idf_s)
    w = tf * idf
    sq = w*w

    # tag the square for norm calculation
    print(f"{docid}\tNORM\t{sq}")
    # carry the full posting forward
    print(f"{docid}\tPOST\t{term}\t{tf_s}\t{idf_s}")
