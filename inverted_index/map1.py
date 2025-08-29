#!/usr/bin/env python3
"""
MapReduce Job 1: HTML Document Parser.

This mapper extracts document ID and content from HTML documents.
It uses BeautifulSoup to parse HTML and extract text content.

Input: Raw HTML documents
Output: Key: document ID, Value: document text content
"""
import sys
import bs4

# Parse one HTML document at a time.  Note that this is still O(1) memory
# WRT the number of documents in the dataset.
HTML = ""
for line in sys.stdin:
    # Assume well-formed HTML docs:
    # - Starts with <!DOCTYPE html>
    # - End with </html>
    # - Contains a trailing newline
    if "<!DOCTYPE html>" in line:
        HTML = line
    else:
        HTML += line

    # If we're at the end of a document, parse
    if "</html>" not in line:
        continue

    # Configure Beautiful Soup parser
    soup = bs4.BeautifulSoup(HTML, "html.parser")

    # Get docid from document
    doc_id_element = soup.find("meta", attrs={"eecs485_docid": True})
    if doc_id_element is None:
        # Skip documents without a docid
        continue
    doc_id = doc_id_element.get("eecs485_docid")

    # Parse content from document
    # get_text() will strip extra whitespace and
    # concatenate content, separated by spaces
    element = soup.find("html")
    content = element.get_text(separator=" ", strip=True)
    # Remove extra newlines
    content = content.replace("\n", "")

    print(f"{doc_id}\t{content}")
