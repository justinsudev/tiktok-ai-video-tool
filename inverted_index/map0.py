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
    # Case‑insensitive match for the DOCTYPE declaration
    if "<!doctype html" in line.lower():
        # Emit 1 for each document found
        print("1")
