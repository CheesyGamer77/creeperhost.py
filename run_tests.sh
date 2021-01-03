#!/bin/bash

echo "Starting tests..."
python3 tests/test.py
test_results = $(echo $?)

exit $test_results