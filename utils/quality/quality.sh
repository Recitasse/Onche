#!/bin/bash

if [ -e bin_quality_report_flake8.txt ]; then
    rm -f bin_quality_report_flake8.txt
fi

flake8 ../../bin > bin_quality_report_flake8.txt

if [ -e tests_quality_report_flake8.txt ]; then
    rm -f tests_quality_report_flake8.txt
fi

flake8 ../../tests > tests_quality_report_flake8.txt

if [ -e tools_quality_report_flake8.txt ]; then
    rm -f tools_quality_report_flake8.txt
fi

flake8 ../../tools > tools_quality_report_flake8.txt

if [ -e utils_quality_report_flake8.txt ]; then
    rm -f utils_quality_report_flake8.txt
fi

flake8 ../../utils > utils_quality_report_flake8.txt