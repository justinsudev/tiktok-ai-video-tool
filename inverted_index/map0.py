#!/usr/bin/env python3
"""
MapReduce Job 0: Document Counter.

This mapper identifies HTML documents in the input stream and emits a '1'
for each document found. Used to count the total number of documents in
the collection for later IDF calculations.

Input: Raw HTML documents
Output: Key: None, Value: "1" for each document
"""
import sys

for line in sys.stdin:
    # Case‑insensitive match for the DOCUMENT boundary
    if "<!doctype html" in line.lower():
        print("1")
