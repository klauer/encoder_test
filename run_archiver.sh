#!/bin/bash

ARCHIVE_FN=archive_$(date +%F).txt

echo "Archiving to $ARCHIVE_FN"
python -u archive.py | tee $ARCHIVE_FN
