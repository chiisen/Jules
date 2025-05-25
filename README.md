# Gregorian to Chinese Lunar Calendar Converter

## Project Overview

This project provides a Python-based utility to convert Gregorian calendar dates (also known as Western calendar dates) into the corresponding Chinese Lunar Calendar dates. It's designed to be a simple, command-line accessible tool for users who need to find the Lunar calendar equivalent of a given Gregorian date.

The primary script, `lunar_converter.py`, takes a date string in "YYYY-MM-DD" format as input and outputs the Lunar date in a traditional Chinese format, including the sexagesimal (Ganzhi) year name, the lunar month (with leap month indication), and the lunar day.

## Key Features

*   **Input Format**: Accepts Gregorian dates as strings in "YYYY-MM-DD" format.
*   **Date Validation**:
    *   Checks for correct input format.
    *   Validates that the input is a legitimate date (e.g., not February 30th).
    *   Ensures the date falls within the supported range.
*   **Supported Date Range**: 1900-01-01 to 2049-12-31 (inclusive).
*   **Output Format**: Displays the Lunar date as "干支年 月份 日期" (e.g., "甲辰年 四月十八").
*   **Leap Month Handling**: Correctly identifies and indicates leap lunar months (e.g., "閏二月").
*   **Error Messages**: Provides clear error messages in Chinese for invalid inputs:
    *   "請輸入日期" (Please enter a date)
    *   "日期格式不正確，請使用 YYYY-MM-DD 格式" (Incorrect date format, please use YYYY-MM-DD format)
    *   "請輸入有效的日期" (Please enter a valid date)
    *   "此日期超出支援範圍" (This date is outside the supported range)
*   **Core Library**: Utilizes the `sxtwl` Python library for accurate underlying astronomical calculations.

## Testing

The project includes a `test_runner.py` script, which contains a suite of test cases to verify the functionality of `lunar_converter.py`. These tests cover:
*   Basic successful conversions.
*   Conversions of special dates (e.g., Lunar New Year).
*   Handling of invalid inputs (format errors, non-existent dates).
*   Boundary conditions for the supported date range.
*   Leap month conversions.

## Development Process Summary

The converter was developed through the following key phases:
1.  **Library Research**: Investigated and selected the `sxtwl` library for its accuracy and feature set for Chinese calendar calculations.
2.  **Core Logic Implementation**: Developed the fundamental date conversion function, including mappings for Heavenly Stems, Earthly Branches, and month/day names, as well as the calculation for the sexagesimal year name.
3.  **Input Validation & Error Handling**: Added robust checks for input date strings to handle potential errors gracefully and provide user-friendly messages.
4.  **Test Script Development**: Created a comprehensive test suite (`test_runner.py`) to ensure the converter functions correctly across a wide range of scenarios, including those specified in the initial requirements.
5.  **Output Refinement**: Ensured that output messages and formats align with the project goals and user expectations.
6.  **Submission**: The completed scripts (`lunar_converter.py` and `test_runner.py`) were submitted.
```
