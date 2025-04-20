#!/usr/bin/env python3 -u
"""
MapReduce Job 0: Document Counter Reducer.

This reducer sums the count of documents in the collection.
It receives "1" for each document and outputs the total count.

Input: Key: None, Value: "1" for each document
Output: A single integer representing the total number of documents
"""
import sys

TOTAL_DOCS = 0
for line in sys.stdin:
    # each line is a “1”
    TOTAL_DOCS += int(line.strip())
# output the single integer
print(TOTAL_DOCS)
