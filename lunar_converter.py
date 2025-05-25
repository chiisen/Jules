import sxtwl # Requires: pip install sxtwl
from datetime import datetime, date
import re

# 1. Define Mappings (from previous implementation)
HEAVENLY_STEMS = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
EARTHLY_BRANCHES = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
CHINESE_MONTH_NAMES = ['正月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '十一月', '腊月']
CHINESE_DAY_DIGITS = ["", "一", "二", "三", "四", "五", "六", "七", "八", "九"]

# Date range constants
MIN_DATE_OBJ = date(1900, 1, 1)
MAX_DATE_OBJ = date(2049, 12, 31)

# Helper function to format Lunar Day Name (from previous implementation)
def get_lunar_day_name(d: int) -> str:
    if not 1 <= d <= 30:
        # This should ideally not be triggered if sxtwl provides valid day numbers (1-30)
        raise ValueError("Lunar day must be between 1 and 30 for formatting.") 
    if d == 10: return '初十'
    if d == 20: return '二十'
    if d == 30: return '三十'
    if 1 <= d <= 9: return '初' + CHINESE_DAY_DIGITS[d]
    if 11 <= d <= 19: return '十' + CHINESE_DAY_DIGITS[d % 10]
    if 21 <= d <= 29: return '廿' + CHINESE_DAY_DIGITS[d % 10]
    # Fallback, though all valid days (1-30) should be covered.
    return "无效日期" 

# Calculate Sexagesimal Year Name (LNY-based) (from previous implementation)
def get_sexagesimal_year_name(lunar_year: int) -> str:
    stem_index = (lunar_year - 1984 + 6000) % 10
    branch_index = (lunar_year - 1984 + 6000) % 12
    return HEAVENLY_STEMS[stem_index] + EARTHLY_BRANCHES[branch_index] + '年'

# Core conversion logic (renamed from gregorian_to_lunar)
def _core_gregorian_to_lunar(year: int, month: int, day: int) -> str:
    """
    Performs the actual Gregorian to Lunar conversion, assuming valid inputs.
    """
    day_obj = sxtwl.fromSolar(year, month, day)

    lunar_year = day_obj.getLunarYear()
    lunar_month_num = day_obj.getLunarMonth() 
    lunar_day = day_obj.getLunarDay()
    is_leap_month = day_obj.isLunarLeap()

    ganzhi_year_name = get_sexagesimal_year_name(lunar_year)

    formatted_lunar_month = ""
    if is_leap_month:
        formatted_lunar_month += "閏"
    
    if 1 <= lunar_month_num <= 12:
        formatted_lunar_month += CHINESE_MONTH_NAMES[lunar_month_num - 1]
    else:
        # This case should not be reached if sxtwl works as expected.
        formatted_lunar_month += "无效月份" 

    formatted_lunar_day = get_lunar_day_name(lunar_day)
    
    return f"{ganzhi_year_name} {formatted_lunar_month}{formatted_lunar_day}"

# New public function with input validation
def gregorian_to_lunar(date_str: str) -> str:
    """
    Converts a Gregorian date string ("YYYY-MM-DD") to a formatted Chinese Lunar date string,
    with input validation.
    """
    # 1. Handle Empty Input
    if date_str is None or not date_str.strip():
        return "請輸入日期"

    # 2. Validate Date Format (YYYY-MM-DD) using regex
    # This regex checks for the structure YYYY-MM-DD.
    if not re.fullmatch(r"^\d{4}-\d{2}-\d{2}$", date_str):
        return "日期格式不正確，請使用 YYYY-MM-DD 格式"

    # 3. Validate Date Legitimacy (e.g., no February 30th)
    try:
        # Attempt to parse the date string into a datetime.date object.
        # datetime.strptime will raise ValueError if the date is not legitimate
        # (e.g., "2024-02-30", "2023-13-01").
        dt_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return "請輸入有效的日期"

    # 4. Check Supported Date Range
    if not (MIN_DATE_OBJ <= dt_obj <= MAX_DATE_OBJ):
        return "此日期超出支援範圍"

    # 5. Successful Validation: Proceed to core conversion
    # Pass the already parsed and validated year, month, day components
    return _core_gregorian_to_lunar(dt_obj.year, dt_obj.month, dt_obj.day)

if __name__ == '__main__':
    # Test cases for validation and successful conversion
    validation_test_cases = {
        None: "請輸入日期",
        "": "請輸入日期",
        "   ": "請輸入日期",
        "abcde": "日期格式不正確，請使用 YYYY-MM-DD 格式",
        "2024/01/10": "日期格式不正確，請使用 YYYY-MM-DD 格式",
        "24-01-10": "日期格式不正確，請使用 YYYY-MM-DD 格式", 
        "2023-13-01": "請輸入有效的日期", 
        "2023-02-29": "請輸入有效的日期", # 2023 is not a leap year
        "2024-02-30": "請輸入有效的日期", 
        "1899-12-31": "此日期超出支援範圍",
        "1900-01-01": "己亥年 腊月初一", 
        "2049-12-31": "己巳年 腊月初七", 
        "2050-01-01": "此日期超出支援範圍",
        "2024-05-25": "甲辰年 四月十八", 
    }

    print("Running validation test cases for gregorian_to_lunar:")
    all_tests_passed = True 
    for date_input, expected_output in validation_test_cases.items():
        try:
            result = gregorian_to_lunar(date_input)
            is_correct = (result == expected_output)
            print(f"Input: '{str(date_input)}' -> Output: \"{result}\", Expected: \"{expected_output}\" {'OK' if is_correct else 'FAIL'}")
            if not is_correct:
                all_tests_passed = False
        except Exception as e: 
            all_tests_passed = False
            print(f"Input: '{str(date_input)}' -> UNEXPECTED Error: {e}, Expected: \"{expected_output}\" FAIL")

    print("\nRe-running some previous successful conversion tests via the new public function:")
    core_success_tests = {
        "2024-03-10": "甲辰年 二月初一", 
        "2023-03-25": "癸卯年 閏二月初四",
        "1900-01-31": "庚子年 正月初一",
        "1984-02-02": "甲子年 正月初一",
    }
    for date_str, expected in core_success_tests.items():
        result = gregorian_to_lunar(date_str)
        is_correct = (result == expected)
        print(f"Input: {date_str} -> Output: \"{result}\", Expected: \"{expected}\" {'OK' if is_correct else 'FAIL'}")
        if not is_correct:
            all_tests_passed = False

    if all_tests_passed:
        print("\nAll validation and core logic tests passed successfully!")
    else:
        print("\nSome validation or core logic tests FAILED.")
# This is the absolute end of the Python script.
# No characters, including comments or newlines that are not part of the script, should follow.
