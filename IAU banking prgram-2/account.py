import time
from collections import defaultdict
from typing import List, Optional

import maskpass

import sorts
from consts import *
import utils
import interface

import models

def authentication(privilege: str) -> (Optional[models.Users], int):
    """
    ورود یا افتتاح حساب
    """

    interface.clean_terminal_screen()

    print(utils.greeting())
    print(" به بانک دانشگاه ازاد خوش امدید\n")
    print("اگر از قبل حساب دارید گزینه ۱ و گزینه ۲ اگر قصد افتتاح حساب جدید دارید")
    print("  ┌─────────────┐  ╭──────────────────────────╮                  ")
    print("  │             │  │ ▶︎ 1 •ورود به سیستم      │                ")
    print("  │  I  A  U    │  ├──────────────────────────┴────╮     ")
    print("  │  S A R I    │  │ ▶︎ 2 • افتتاح حساب            │   ")
    print("  │  B A N K    │  ├──────────────────┬────────────╯     ")
    print("  │             │  │ ▶︎ 3 • خروج      │                ")
    print("  └─────────────┘  ╰──────────────────╯                  ")


    failed_attempt = FAILED_ATTEMPT
    user_choice = ""
    while failed_attempt:
        user_choice = input("☞ گزینه ایی انتخاب نمایید ")
        if user_choice not in AUTHENTICATION_CHOICES:
            failed_attempt -= 1
            print("ورودی نامعتبر!از ۱ تا ۳ انتخاب کنید")
            print("شما %d تلاش باقی مانده دارید" % failed_attempt)
        else:
            break

    if not failed_attempt:
        print("تلاش های ناموفق شما بسیار بود؛لطفا اندکی صبر نمایید و سپس مجددا تلاش کنید")
        return None, -1

    users = models.Users(privilege)
    user_index = -1

    if user_choice == "1":
        if not users.data:
            print("هنوز حسابی موجود نیست")
            return None, -1

        print("ایا میخواهید وارد حسابتان شوید؟")
        account_number = ""
        failed_attempt = FAILED_ATTEMPT
        while failed_attempt:
            account_number = input("☞ لطفا شماره حساب را وارد نمایید ")
            if account_number not in users.users_set:
                failed_attempt -= 1
                print("حسابی موجود نیست لطفا شماره حساب خود را وارد نمایید")
                print("شما %d تلاش باقی مانده دارید" % failed_attempt)
            else:
                break

        if not failed_attempt:
            print("تلاش های ناموفق شما بسیار بود؛لطفا اندکی صبر نمایید و سپس مجددا تلاش کنید")
            return None, -1

        user_index = sorts.binary_search(users.data, ACCOUNT_NUMBER, account_number)
        if user_index == -1:
            print("تلاش های ناموفق شما بسیار بود؛لطفا اندکی صبر نمایید و سپس مجددا تلاش کنید")
            return None, -1

        user = users.data[user_index]
        print(utils.greeting())
        print(" %s" % account_number)
        failed_attempt = FAILED_ATTEMPT
        hashed_password = user[PASSWORD]
        while failed_attempt:
            password = maskpass.askpass(prompt="☞ رمزعبور را وارد نمایید: ")
            if not utils.check_password(password, hashed_password):
                failed_attempt -= 1
                print("رمزعبور نامعتبر")
                print("شما %d تلاش باقی مانده دارید" % failed_attempt)
            else:
                break

        if not failed_attempt:
            print("تلاش های ناموفق شما بسیار بود؛لطفا اندکی صبر نمایید و سپس مجددا تلاش کنید")
            return None, -1

        print("ورود موفقیت امیز بود")
        print("خوش امدید %s!!!" % user[FIRST_NAME])

    if user_choice == "2":
        print("ایا میخواهید حساب انلاین جدید افتتاح نمایید؟")
        print("لطفا اطلاعات مورد نیاز را به درستی وارد کنید و از صحت تمامی اطلاعات وارد شده اطمینان حاصل فرمایید.")

        first_name = get_name(FIRST_NAME_MAX_LEN, FAILED_ATTEMPT, "نام")
        if not first_name:
            return None, -1

        last_name = get_name(LAST_NAME_MAX_LEN, FAILED_ATTEMPT, "خانوادگی")
        if not last_name:
            return None, -1

        gender = get_gender(GENDER_SET_CHOICE)
        if not gender:
            return None, -1
        
        date_of_birth = get_date_of_birth()
        if not date_of_birth:
            return None, -1

        phone_number = get_phone_number()
        if not phone_number:
            return None, -1

        email = get_email()

        password = get_password(utils.generate_hashed_password(""))
        if not password:
            return None, -1

        user_information = defaultdict(str)
        user_information[FIRST_NAME] = first_name
        user_information[LAST_NAME] = last_name
        user_information[GENDER] = gender
        user_information[DATE_OF_BIRTH] = date_of_birth
        user_information[PHONE_NUMBER] = phone_number
        user_information[EMAIL] = email
        user_information[PASSWORD] = password
        user_information[BALANCE] = "0"
        user_index = users.create_new(user_information)

        print("ایجاد حساب با موفیقت انجام شد!")

    if user_choice == "3":
        return None, -1

    print("مرحله بعدی")

    return users, user_index

def get_name(name_max_len: int, failed_attempt: int, kind: str) -> str:
    name = ""
    while failed_attempt:
        name = input("☞ لطفا نامتان را %s نام: " % kind)
        if not utils.is_valid_name(name, name_max_len):
            failed_attempt -= 1
            print(" اشتباه:%s نام!!! از نام معتبر استفاده نمایید %s نام" % (kind, kind))
            print("شما %d تلاش باقی مانده دارید" % failed_attempt)
        else:
            break

    if not failed_attempt:
        print("لطفا اطلاعات مورد نیاز را به درستی وارد کنید و از صحت تمامی اطلاعات وارد شده اطمینان حاصل فرمایید.")
        name = ""

    return name

def get_gender(gender_list: List[str]) -> str:
    print("☞ لطفا ازبین گزینه های زیر موردی انتخاب نمایید")
    print("  ┌─────────────┐  ╭──────────────────╮   ")
    print("  │             │  │ ▶︎ 1 • مرد      │   ")
    print("  │  I  A  U    │  ├──────────────────┴─╮   ")
    print("  │  S A R I    │  │ ▶︎ 2 • زن      │   ")
    print("  │  B A N K    │  ├────────────────────┴╮   ")
    print("  │             │  │ ▶︎ 3 • غیره       │   ")
    print("  └─────────────┘  ╰─────────────────────╯   ")
    
    failed_attempt = FAILED_ATTEMPT
    gender = ""
    while failed_attempt:
        gender = input("☞ لطفا جنسیتتان را انتخاب نمایید: ")
        if gender not in gender_list:
            failed_attempt -= 1
            print("گزینه نادرست؛مجددا انتخاب نمایید")
            print("شما %d تلاش باقی مانده دارید" % failed_attempt)
        else:
            break
    if not failed_attempt:
        print("تلاش های ناموفق شما بسیار بود؛لطفا اندکی صبر نمایید و سپس مجددا تلاش کنید")
        return ""

    if gender == "1":
        return "مرد"

    if gender == "2":
        return "زن"

    if gender == "3":
        return "غیره"

    return ""

def get_date_of_birth() -> str:
    print("☞ لطفا تاریخ تولد خود را برحسب روز؛ماه و سال انتخاب نمایید")
    current_time = time.strftime("%d:%m:%Y")
    current_time_list = current_time.split(":")
    current_day, current_month, current_year = current_time_list

    year = utils.get_temporal("سال", int(current_year))
    if not year:
        return ""
    
    month = utils.get_temporal("ماه", 12)
    if not month:
        return ""

    day = utils.get_temporal("روز", 31)
    if not day:
        return ""

    if not utils.is_valid_day([int(day), int(month), int(year)],
                              [int(current_day), int(current_month), int(current_year)]):
        return ""

    return day + "/" + month + "/" + year

def get_phone_number() -> str:
    failed_attempt = FAILED_ATTEMPT
    phone_number = ""
    while failed_attempt:
        phone_number = input("☞ لطفا شماره همراه خود را وارد نمایید ")
        if not utils.is_valid_phone_number(phone_number):
            failed_attempt -= 1
            print("شماره اشتباه است؛مجددا تلاش کنید")
            print("شما %d تلاش باقی مانده دارید" % failed_attempt)
        else:
            break
    if not failed_attempt:
        print("تلاش های ناموفق شما بسیار بود؛لطفا اندکی صبر نمایید و سپس مجددا تلاش کنید")
        phone_number = ""

    return phone_number

def get_email() -> str:
    print("☞ ایا میخواهید ایمیل خود را اضافه کنید؟ اگر بله ۱ و ۲ برای خیر وارد نمایید")

    user_choice = utils.get_yes_no_choice()
    if not user_choice:
        return ""

    if user_choice == "2":
        return ""

    email = ""
    failed_attempt = FAILED_ATTEMPT
    while failed_attempt:
        email = input("☞ لطفا ایمیل خود را وارد نمایید ")
        if not utils.is_valid_email(email):
            failed_attempt -= 1
            print("ایمیل اشتباه بود مجددا تلاش نمایید")
            print("شما %d تلاش باقی مانده دارید" % failed_attempt)
        else:
            break

    if not failed_attempt:
        print("تلاش های ناموفق شما بسیار بود؛لطفا اندکی صبر نمایید و سپس مجددا تلاش کنید")
        email = ""

    return email

def get_password(previous_password: str) -> str:
    password = ""
    failed_attempt = FAILED_ATTEMPT
    while failed_attempt:
        password = maskpass.askpass(prompt="☞ لطفاً رمز عبور خود را وارد کنید. باید حداقل 8 کاراکتر داشته باشد، شامل اعداد، حروف کوچک، حروف بزرگ و کاراکترهای خاص باشد.: ")
        if not utils.is_valid_password(password):
            failed_attempt -= 1
            print("رمزعبور نامعتبر است؛لطفا مجددا تلاش نمایید")
            print("شما %d تلاش باقی مانده دارید" % failed_attempt)
        elif utils.check_password(password, previous_password):
            failed_attempt -= 1
            print("رمزعبور نامعتبر؛ رمز انتخابی با رمز کنونی یکی است")
            print("شما %d تلاش باقی مانده دارید" % failed_attempt)
        else:
            break

    if not failed_attempt:
        print("تلاش های ناموفق شما بسیار بود؛لطفا اندکی صبر نمایید و سپس مجددا تلاش کنید")
        password = ""

    failed_attempt = FAILED_ATTEMPT
    while failed_attempt:
        re_enter_password = maskpass.askpass(prompt="☞ رمزعبور را مجددا وارد نمایید ")
        if password != re_enter_password:
            failed_attempt -= 1
            print("رمز عبور جدید نباید با گذشته یکسان باشد. مجدداً تلاش کنید.!!!")
            print("شما %d تلاش باقی مانده دارید" % failed_attempt)
        else:
            break

    if not failed_attempt:
        print("تلاش های ناموفق شما بسیار بود؛لطفا اندکی صبر نمایید و سپس مجددا تلاش کنید")
        password = ""

    return utils.generate_hashed_password(password)
