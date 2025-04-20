#!/bin/bash
# Setup the directory structure for the search engine

# Make all scripts executable
chmod +x inverted_index/map?.py inverted_index/reduce?.py inverted_index/partition.py

# Ensure the index_server directory structure exists
mkdir -p index_server/index/inverted_index

echo "Directory setup complete"