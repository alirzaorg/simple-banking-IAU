import datetime
import json
import string
from os.path import exists

import bcrypt
from typing import List

from consts import *


def greeting() -> str:
    """
   تشخیص ساعت سیستم و ارسال پیام مربوط با توجه به وقت
    """

    current_time = datetime.datetime.now().time().strftime("%H:%M:%S")
    hour_min_sec = current_time.split(':')
    hours = int(hour_min_sec[0])

    if 2 <= hours < 12:
        return "صبح بخیر"
    if 12 <= hours < 18:
        return "ظهر بخیر"
    if 18 <= hours < 22:
        return "عصر بخیر"
    return "سلام!!!"

def generate_hashed_password(plain_text_password: str) -> str:
    """
  رمزگزاری رمزعبور ها با استفاده از الگوریتم: bcrypt algorithms
    """

    return bcrypt.hashpw(str.encode(plain_text_password), bcrypt.gensalt(SALT_LEN)).decode()

def check_password(plain_text_password: str, hashed_password: str) -> bool:
    """
    مطابقت دادن رمز با رمزعبور دیتابیس
    """

    return bcrypt.checkpw(plain_text_password.encode(), hashed_password.encode())

def is_valid_name(name: str, max_len: int) -> bool:
    if len(name) > max_len or len(name) == 0:
        return False

    set_character = set(name)
    for character in set_character:
        if character in string.punctuation or character.isnumeric():
            return False
    return True

def get_temporal(temporal: str, max_time: int) -> str:
    failed_attempt = FAILED_ATTEMPT
    time = ""
    while failed_attempt:
        time = input("☞ لطفا وارد کنید %s وقتی که بدنیا امدید: " % temporal)
        if not time.isnumeric():
            failed_attempt -= 1
            print("نوع سال نامعتبر است، شما باید یک عدد صحیح مثبت معتبر وارد کنید")
            print("شما %d تلاش باقی مانده دارید" % failed_attempt)
        elif int(time) > max_time:
            failed_attempt -= 1
            print("سال تولد اشتباه است شما نمیتوانید بعد این تاریخ بدنیا امده باشید %d" % max_time)
            print("شما %d تلاش باقی مانده دارید" % failed_attempt)
        else:
            break

    if not failed_attempt:
        print("تلاش های ناموفق شما بسیار بود؛لطفا اندکی صبر نمایید و سپس مجددا تلاش کنید")
        time = ""

    result = [""]
    if temporal == "سال":
        result = ["0" for _ in range(4)]
        i = 3
        for digit in time[::-1]:
            result[i] = digit
            i -= 1
    else:
        result = ["0" for _ in range(2)]
        i = 1
        for digit in time[::-1]:
            result[i] = digit
            i -= 1

    return "".join(result)

def is_valid_day(date: List[int], current_date: List[int]) -> bool:

    day, month, year = date
    if month < 1 or month > 12:
        print("ماه ورودی اشتباه است")
        return False

    max_day_in_month = 0
    if month in {1, 3, 5, 7, 8, 10, 12}:
        max_day_in_month = 31
    elif month in {4, 6, 9, 11}:
        max_day_in_month = 30
    elif year % 4 == 0 or year % 100 == 0 or year % 400 == 0:
        max_day_in_month = 29
    else:
        max_day_in_month = 28

    if day < 1 or day > max_day_in_month:
        print("شما روز اشتباهی در این ماه انتخاب نموده اید")
        return False

    # تشخیص سن برای ایجاد حساب (بالای ۱۸)
    if year > current_date[2] - 18:
        print("برای ایجاد حساب جدید، باید حداقل ۱۸ سال سن داشته باشید")
        return False

    if year < current_date[2] - 18:
        return True

    if month > current_date[1]:
        print("برای ایجاد حساب جدید، باید حداقل ۱۸ سال سن داشته باشید")
        return False

    if month < current_date[1]:
        return True

    if day < current_date[0]:
        print("برای ایجاد حساب جدید، باید حداقل ۱۸ سال سن داشته باشید")
        return False

    return True

def is_valid_phone_number(phone_number: str) -> bool:
    if len(phone_number) != PHONE_NUMBER_LEN:
        print("شماره همراه باید این مقدار باشد %d\n" % 10)
        return False

    if phone_number[0] != "0":
        print("شماره همراه باید با صفر شروع شود \n")
        return False

    for digit in phone_number:
        if not digit.isnumeric():
            print("%s مقدار ورودی عدد نیست\n" % digit)
            return False

    return True

def is_valid_email(email: str) -> bool:

    return True

def is_valid_password(password: str) -> bool:
    if len(password) < MIN_PASSWORD_LEN:
        print("طول رمز عبور باید حداقل ۸ کاراکتر باشد")
        return False

    if len(password) > MAX_PASSWORD_LEN:
        print("طول کلمه عبور نباید از 100 کاراکتر بیشتر باشد!!!")
        return False

    have_number, have_lowercase, have_uppercase, have_specical_character = False, False, False, False
    for char in password:
        if char == " ":
            return False
        if char.isnumeric():
            have_number = True
        elif char.islower():
            have_lowercase = True
        elif char.isupper():
            have_uppercase = True
        elif char in string.punctuation:
            have_specical_character = True

    return have_number and have_lowercase and have_uppercase and have_specical_character

def is_valid_account_number(account_number: str, privilege: str) -> bool:
    if len(account_number) != ACCOUNT_CONFIGS[privilege][ACCOUNT_NUMBER_LEN]:
        return False

    for digit in account_number:
        if not digit.isnumeric():
            return False

    return True

def get_yes_no_choice() -> str:
    print("  ┌─────────────┐  ╭─────────────────╮     ")
    print("  │  I  A  U    │  │ ▶︎ 1 • بله      │  ")
    print("  │  S A R I    │  ├────────────────┬╯     ")
    print("  │  B A N K    │  │ ▶︎ 2 • خیر     │   ")
    print("  └─────────────┘  ╰────────────────╯      ")

    failed_attempt = FAILED_ATTEMPT
    user_choice = ""
    while failed_attempt:
        user_choice = input("☞ انتخاب نمایید ")
        if user_choice not in YES_NO_CHOICES:
            failed_attempt -= 1
            print("انتخاب نامعتبر؛ ازبین ۱و ۲ انتخاب نمایید")
            print("شما %d تلاش باقی مانده دارید" % failed_attempt)
        else:
            break

    if not failed_attempt:
        print("تلاش های ناموفق شما بسیار بود؛لطفا اندکی صبر نمایید و سپس مجددا تلاش کنید")
        return ""

    return user_choice

def is_valid_balance(balance: str) -> bool:
    for digit in balance:
        if not digit.isnumeric() and digit != ".":
            return False

    return True

def is_valid_message(message: str) -> bool:
    if len(message) > MESSAGE_MAX_CHARACTERS:
        print(f"پیام شما از {MESSAGE_MAX_CHARACTERS} کاراکتر بیشتر است")
        return False

    words = message.split(" ")
    if len(words) > MESSAGE_MAX_WORDS:
        print(f"پیام شما از {MESSAGE_MAX_WORDS} کاراکتر بیشتر است")
        return False

    return True

def proceed_next() -> None:
    _ = input("در صورت تمایل به رفتن به مرحله بعد، هر کلیدی را فشار دهید")

def get_data_from_json(filename: str):
    """
    خواندن اطلاعات از فایل داده ها
    """

    if not exists(filename):
        return {}

    file = open(filename, "r")
    data = file.read()

    # تبدیل استرینگ json به python
    return json.loads(data)

def write_data_to_json(data, filename: str) -> None:
    """
    داده ها را در فایلی با نام filename می نویسد
    """

    file = open(filename, "w")
    json_data = json.dumps(data)
    file.write(json_data)


if __name__ == '__main__':
    print(greeting())
