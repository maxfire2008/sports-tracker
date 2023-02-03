#!/bin/pwsh
cd reference
py .\generate_test_data.py
cd ../
py .\insert_students.py --dry-run=0
