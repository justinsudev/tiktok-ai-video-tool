#!/usr/bin/env python3
"""
MapReduce Job 1: Document Content Aggregator.

This reducer combines content from the same document that may have been
split across multiple mapper outputs.

Input: Key: document ID, Value: document content fragment
Output: Key: document ID, Value: combined document content
"""
import sys

CURRENT_DOC = None
current_content = []
for line in sys.stdin:
    doc_id, content = line.rstrip("\n").split("\t", 1)
    # If we've moved to a new doc_id, emit the previous one
    if doc_id != CURRENT_DOC and CURRENT_DOC is not None:
        print(f"{CURRENT_DOC}\t{' '.join(current_content)}")
        current_content = []
    CURRENT_DOC = doc_id
    current_content.append(content)
# emit the last doc
if CURRENT_DOC is not None:
    FULL_TEXT = " ".join(current_content)
    print(f"{CURRENT_DOC}\t{FULL_TEXT}")
