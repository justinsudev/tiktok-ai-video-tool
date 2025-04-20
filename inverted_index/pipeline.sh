#!/usr/bin/env bash
set -Eeuo pipefail

# ─── CONFIGURATION ────────────────────────────────────────────────────────────
INPUT_DIR=${1:-crawl}

DOC_COUNT_DIR=output0
PARSE_DIR=output1
TF_DIR=output2
IDF_DIR=output3
DOC_NORM_DIR=output4
INDEX_DIR=output

# ─── CLEAN OLD OUTPUTS ────────────────────────────────────────────────────────
rm -rf output output[0-9] total_document_count.txt map4.log

# ─── JOB 0: COUNT DOCUMENTS ───────────────────────────────────────────────────
madoop \
  -input   "$INPUT_DIR" \
  -output  "$DOC_COUNT_DIR" \
  -mapper  ./map0.py \
  -reducer ./reduce0.py \
  -numReduceTasks 1

cp "$DOC_COUNT_DIR"/part-00000 total_document_count.txt

# ─── JOB 1: PARSE DOCS ─────────────────────────────────────────────────────────
madoop \
  -input   "$INPUT_DIR" \
  -output  "$PARSE_DIR" \
  -mapper  ./map1.py \
  -reducer ./reduce1.py

# ─── JOB 2: TERM FREQUENCIES ───────────────────────────────────────────────────
madoop \
  -input   "$PARSE_DIR" \
  -output  "$TF_DIR" \
  -mapper  ./map2.py \
  -reducer ./reduce2.py

# ─── JOB 3: DF → IDF & ATTACH ──────────────────────────────────────────────────
madoop \
  -input   "$TF_DIR" \
  -output  "$IDF_DIR" \
  -mapper  ./map3.py \
  -reducer ./reduce3.py

printf '*** job 4: doc normalisations (1 reducer) ***\n'
madoop -input output3 -output output4 \
       -mapper ./map4.py \
       -reducer ./reduce4.py \
       -numReduceTasks 1

# ─── JOB 5: FINAL INDEX SHARDS (docid%3) ───────────────────────────────────────
madoop \
  -input       "$DOC_NORM_DIR" \
  -output      "$INDEX_DIR" \
  -mapper      ./map5.py \
  -reducer     ./reduce5.py \
  -partitioner ./partition.py \
  -numReduceTasks 3

# ─── COPY INTO index_server FOR TESTS ──────────────────────────────────────────
TARGET=../index_server/index/inverted_index
mkdir -p "$TARGET"
i=0
for part in "$INDEX_DIR"/part-*; do
  cp "$part" "$TARGET"/inverted_index_${i}.txt
  ((i++))
done

echo 'Pipeline complete.'
