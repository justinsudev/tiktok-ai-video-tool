#!/usr/bin/env python3 -u
r"""
Custom Partitioner for Final Inverted Index Segmentation.

This partitioner assigns records to reducers based on the segment number
calculated in map5.py. It ensures documents with the same docid % 3 value
go to the same reducer, resulting in three segment files.

Input: Each line from map5.py output with format: "segment\trest_of_data"
Output: The segment number as an integer
"""
import sys

for line in sys.stdin:
    # map5.py outputs:  <segment>\t<term> <idf> <docid> <tf> <norm>
    # so the partition key is the integer before the tab
    key, _, _ = line.partition("\t")
    print(int(key))
