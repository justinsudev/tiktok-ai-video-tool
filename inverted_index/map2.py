#!/usr/bin/env python3
"""
MapReduce Job 2: Term Tokenization.

This mapper processes document content by tokenizing text,
removing stopwords, and emitting term-document pairs.

Input: Key: document ID, Value: document text content
Output: Key: term, Value: document ID
"""
import sys
import re

# load stopwords into a set
with open("stopwords.txt", "r", encoding="utf-8") as stopwords_file:
    stop = set(w.strip() for w in stopwords_file)

for line in sys.stdin:
    line = line.rstrip("\n")
    if not line:
        continue
    docid, content = line.split("\t", 1)

    # lowercase and strip non-alphanumeric (but keep digits)
    text = content.casefold()
    text = re.sub(r"[^a-z0-9 ]+", "", text)

    for term in text.split():
        if term and term not in stop:
            print(f"{term}\t{docid}")
