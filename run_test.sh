#!/bin/bash

TEST_FN=test_$(date +%F).txt

echo "Logging to $TEST_FN"
python -u test.py | tee $TEST_FN
