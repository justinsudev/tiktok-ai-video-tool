#!/bin/bash
# Debug script for the simple test case
set -e

# Create temp directory for testing
TEST_DIR="test_debug"
rm -rf "$TEST_DIR"
mkdir -p "$TEST_DIR"

# Copy our MapReduce scripts
cp map?.py "$TEST_DIR"/
cp reduce?.py "$TEST_DIR"/
cp partition.py "$TEST_DIR"/
cp stopwords.txt "$TEST_DIR"/

# Make scripts executable
chmod +x "$TEST_DIR"/*.py

# Copy test data
TEST_CASE="test_pipeline03"
TEST_DATA_DIR="../tests/testdata/$TEST_CASE/crawl"
cp -r "$TEST_DATA_DIR" "$TEST_DIR"/input

# Run the pipeline manually
cd "$TEST_DIR"

echo "Running job 0: Count documents"
madoop -input input -output output0 -mapper ./map0.py -reducer ./reduce0.py -numReduceTasks 1
cp output0/part-00000 total_document_count.txt
echo "Document count: $(cat total_document_count.txt)"

echo "Running job 1: Parse documents"
madoop -input input -output output1 -mapper ./map1.py -reducer ./reduce1.py
echo "Sample output from job 1:"
head -n 2 output1/part-* || true

echo "Running job 2: Term frequencies"
madoop -input output1 -output output2 -mapper ./map2.py -reducer ./reduce2.py
echo "Sample output from job 2:"
head -n 2 output2/part-* || true

echo "Running job 3: IDF join"
madoop -input output2 -output output3 -mapper ./map3.py -reducer ./reduce3.py
echo "Sample output from job 3:"
head -n 2 output3/part-* || true

echo "Running job 4: Document normalization"
madoop -input output3 -output output4 -mapper ./map4.py -reducer ./reduce4.py -numReduceTasks 1
echo "Sample output from job 4:"
head -n 2 output4/part-* || true

echo "Preparing input for job 5"
mkdir -p input5
cp output3/part-* input5/ || true
cp output4/part-* input5/ || true
ls -la input5/

echo "Running job 5: Final index"
madoop -input input5 -output output -mapper ./map5.py -reducer ./reduce5.py -partitioner ./partition.py -numReduceTasks 3
echo "Final output:"
ls -la output/

# Compare our output with expected output
echo "Comparing with expected output"
echo "Our output:"
if [ -f output/part-00000 ]; then
    cat output/part-* | sort > output.txt
    echo "First few lines of our output:"
    head -n 5 output.txt
else
    echo "No output files found!"
fi

echo "Expected output:"
EXPECTED_FILE="../../tests/testdata/$TEST_CASE/expected.txt"
if [ -f "$EXPECTED_FILE" ]; then
    echo "First few lines of expected output:"
    head -n 5 "$EXPECTED_FILE"
else
    echo "Expected output file not found: $EXPECTED_FILE"
fi