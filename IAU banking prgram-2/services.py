from typing import Optional

import account
import sorts
from consts import *
import interface
import messages
import models
import transactions
import utils


def users_services(users: models.Users, user_index: int, feedbacks_messages: messages.MessageQueue) -> \
        (Optional[models.Users], Optional[messages.MessageQueue]):
    interface.clean_terminal_screen()
    interface.display_horizontal_line()

    print(" آیا درخواست دیگری دارید؟")
    print("☞ لطفا از بین گزینه های زیر انتخاب نمایید")
    print("  ┌─────────────┐  ╭───────────────────────────╮           ")
    print("  │  ╭┼┼╮       │  │ ▶︎ 1 • دریافت اطلاعات      │         ")
    print("  │  ╰┼┼╮       │  ├───────────────────────────┴────╮      ")
    print("  │  ╰┼┼╯       │  │ ▶︎ 2 • بروزرسانی اطلاعات        │    ")
    print("  │             │  ├──────────────────────────────┬─╯      ")
    print("  │  I  A  U    │  │ ▶︎ 3 • تغییر رمز             │      ")
    print("  │  S A R I    │  ├────────────────────────────┬─╯        ")
    print("  │  B A N K    │  │ ▶︎ 4 • حذف حساب            │        ")
    print("  │             │  ├────────────────────────────┴────╮     ")
    print("  │             │  │ ▶︎ 5 • انجام عملیات             │   ")
    print("  │             │  ├───────────────────────┬─────────╯     ")
    print("  │ ║│┃┃║║│┃║│║ │  │ ▶︎ 6 • بازخوردها      │             ")
    print("  │ ║│┃┃║║│┃║│║ │  ├───────────────────────┴─╮             ")
    print("  │             │  │ ▶︎ 7 • خروج از سیستم    │           ")
    print("  └─────────────┘  ╰─────────────────────────╯             ")

    failed_attempt = FAILED_ATTEMPT
    user_choice = ""
    while failed_attempt:
        user_choice = input("☞ گزینه ای انتخاب نمایید: ")
        if user_choice not in USER_SERVICES_CHOICES:
            failed_attempt -= 1
            print("ورودی نامعتبر!از ۱ تا ۷ انتخاب کنید")
            print("شما %d تلاش باقی مانده دارید" % failed_attempt)
        else:
            break

    if not failed_attempt:
        print("تلاش های ناموفق شما بسیار بود؛لطفا اندکی صبر نمایید و سپس مجددا تلاش کنید")
        return None, feedbacks_messages

    if user_choice == "1":
        _display_user_information(users.data[user_index])

    if user_choice == "2":
        users = _update_information(users, user_index)

    if user_choice == "3":
        users = _update_password(users, user_index)

    if user_choice == "4":
        users.delete_user(user_index)
        return None, feedbacks_messages

    if user_choice == "5":
        users = transactions.transaction_services(users, user_index)

    if user_choice == "6":
        feedbacks_messages = messages.add_message(feedbacks_messages, users.data[user_index][ACCOUNT_NUMBER])

    if user_choice == "7":
        return None, feedbacks_messages

    return users, feedbacks_messages

def admins_services(admins: models.Users, users: models.Users, user_index: int,
                    feedbacks_messages: messages.MessageQueue) -> \
        (Optional[models.Users], Optional[messages.MessageQueue]):
    interface.clean_terminal_screen()
    interface.display_horizontal_line()

    print("عملیات مورد نظر را انتخاب نمایید:")
    print("☞ از بین گزینه‌های زیر که توسط مدیران ارائه شده‌اند، لطفاً یکی را انتخاب نمایید.")
    print("  ┌─────────────┐  ╭───────────────────────────╮                ")
    print("  │  ╭┼┼╮       │  │ ▶︎ 1 • دریافت اطلاعات      │              ")
    print("  │  ╰┼┼╮       │  ├───────────────────────────┴────╮           ")
    print("  │  ╰┼┼╯       │  │ ▶︎ 2 • بروزرسانی اطلاعات        │         ")
    print("  │             │  ├──────────────────────────────┬─╯           ")
    print("  │  I  A  U    │  │ ▶︎ 3 • تغییر رمز             │           ")
    print("  │  S A R I    │  ├────────────────────────────┬─╯             ")
    print("  │  B A N K    │  │ ▶︎ 4 • حذف حساب            │             ")
    print("  │             │  ├────────────────────────────┴───────╮       ")
    print("  │             │  │ ▶︎ 5 • دریافت اطلاعات کاربران       │     ")
    print("  │             │  ├────────────────────────────────────┴─╮     ")
    print("  │             │  │ ▶︎ 6 • دریافت اطلاعات بر اساس فیلد    │   ")
    print("  │             │  ├────────────────────────────┬─────────╯     ")
    print("  │ ║│┃┃║║│┃║│║ │  │ ▶︎ 7 • خواندن بازخوردها    │             ")
    print("  │ ║│┃┃║║│┃║│║ │  ├─────────────────────────┬──╯               ")
    print("  │             │  │ ▶︎ 8 • خروج از سیستم     │                ")
    print("  └─────────────┘  ╰─────────────────────────╯                  ")

    failed_attempt = FAILED_ATTEMPT
    admin_choice = ""
    while failed_attempt:
        admin_choice = input("☞ گزینه ایی انتخاب نمایید ")
        if admin_choice not in ADMIN_SERVICES_CHOICES:
            failed_attempt -= 1
            print("ورودی نامعتبر!از ۱ تا ۸ انتخاب کنید")
            print("شما %d تلاش باقی مانده دارید" % failed_attempt)
        else:
            break

    if not failed_attempt:
        print("تلاش های ناموفق شما بسیار بود؛لطفا اندکی صبر نمایید و سپس مجددا تلاش کنید")
        return None, feedbacks_messages

    if admin_choice == "1":
        _display_user_information(admins.data[user_index])

    if admin_choice == "2":
        admins = _update_information(admins, user_index)

    if admin_choice == "3":
        users = _update_password(admins, user_index)

    if admin_choice == "4":
        users.delete_user(user_index)
        return None, feedbacks_messages

    if admin_choice == "5":
        account_number = _get_account_number(users)
        if not account_number:
            return users, feedbacks_messages

        user_index = sorts.binary_search(users.data, ACCOUNT_NUMBER, account_number)
        if user_index == -1:
            print("کاربر موجود نیست لطفا مجددا اقدام نمایید")
            return users, feedbacks_messages

        _display_user_information(users.data[user_index])

    if admin_choice == "6":
        _get_user_information_by_field(users)

    if admin_choice == "7":
        feedbacks_messages = messages.read_message(feedbacks_messages)

    if admin_choice == "8":
        return None, feedbacks_messages

    return admins, feedbacks_messages

def _display_user_information(user: dict) -> None:
    """
    Display user's information
    """

    interface.display_horizontal_line()

    print("اطلاعات شما به شرح زیر است")
    print("نام: %s %s %s" % (user[LAST_NAME] , user[FIRST_NAME]))
    print("جنسیت: %s" % user[GENDER])
    print("تاریخ تولد: %s" % user[DATE_OF_BIRTH])
    print("شماره همراه: %s" % user[PHONE_NUMBER])
    print("ایمیل: %s" % user[EMAIL])
    print("شماره حساب: %s" % user[ACCOUNT_NUMBER])
    print("تاریخ صدور: %s" % user[ISSUED_DATE])

    interface.display_horizontal_line()
    utils.proceed_next()


def _update_information(users: models.Users, user_index: int) -> models.Users:
    print("چه اطلاعاتی را میخواهید ویرایش نمایید؟")
    print("☞ لطفا گزینه مورد نظر را از لیست زیر انتخاب نمایید")
    print("  ┌─────────────┐  ╭────────────────────────╮        ")
    print("  │    ╭┼┼╮     │  │ ▶︎ 1 • نام             │      ")
    print("  │    ╰┼┼╮     │  ├────────────────────────┴╮       ")
    print("  │    ╰┼┼╯     │  │ ▶︎ 2 • نام خانوادگی     │       ")
    print("  │             │  ├────────────────────┬────╯         ")
    print("  │   I  A  U   │  │ ▶︎ 3 • جنسیت       │          ")
    print("  │   S A R I   │  ├────────────────────┴──────╮     ")
    print("  │   B A N K   │  │ ▶︎ 4 • تاریخ تولد         │   ")
    print("  │             │  ├──────────────────────────┬╯     ")
    print("  │ ║│┃┃║║│┃║│║ │  │ ▶︎ 5 • شماره همراه       │    ")
    print("  │ ║│┃┃║║│┃║│║ │  ├───────────────────┬──────╯      ")
    print("  │             │  │ ▶︎ 6 • ایمیل      │           ")
    print("  │             │  ├──────────────────┬╯             ")
    print("  │             │  │ ▶︎ 7 • خروج      │            ")
    print("  └─────────────┘  ╰──────────────────╯              ")

    failed_attempt = FAILED_ATTEMPT
    user_choice = ""
    while failed_attempt:
        user_choice = input("☞ گزینه ایی انتخاب نمایید ")
        if user_choice not in USER_UPDATE_INFORMATION_CHOICES:
            failed_attempt -= 1
            print("ورودی نامعتبر!از ۱ تا ۸ انتخاب کنید")
            print("شما %d تلاش باقی مانده دارید" % failed_attempt)
        else:
            break

    if not failed_attempt:
        print("تلاش های ناموفق شما بسیار بود؛لطفا اندکی صبر نمایید و سپس مجددا تلاش کنید")
        return users

    if user_choice == "1":
        first_name = account.get_name(FIRST_NAME_MAX_LEN, FAILED_ATTEMPT, "نام")
        if not first_name:
            return users

        users.update_information(user_index, FIRST_NAME, first_name)
        print("نام شما با موفقیت تغییر یافت")


    if user_choice == "3":
        last_name = account.get_name(FIRST_NAME_MAX_LEN, FAILED_ATTEMPT, "خانوادگی")
        if not last_name:
            return users

        users.update_information(user_index, LAST_NAME, last_name)
        print("نام خانوادگی شما با موفقیت تغییر یافت")

    if user_choice == "4":
        gender = account.get_gender(GENDER_SET_CHOICE)
        if not gender:
            return users

        users.update_information(user_index, GENDER, gender)
        print("جنسیت شما با موفقیت تغییر یافت")

    if user_choice == "5":
        date_of_birth = account.get_date_of_birth()
        if not date_of_birth:
            return users

        users.update_information(user_index, DATE_OF_BIRTH, date_of_birth)
        print("تاریخ تولد شما با موفقیت تغییر یافت")

    if user_choice == "6":
        phone_number = account.get_phone_number()
        if not phone_number:
            return users

        users.update_information(user_index, PHONE_NUMBER, phone_number)
        print("شماره همراه شما با موفقیت تغییر یافت")

    if user_choice == "7":
        email = account.get_email()
        if not email:
            return users

        users.update_information(user_index, EMAIL, email)
        print("ایمیل شما با موفقیت تغییر یافت")

    if user_choice == "8":
        return users

    print("لطفا اطلاعات جدید خود را بررسی نمایید")
    _display_user_information(users.data[user_index])

    return users

def _update_password(users: models.Users, user_index: int) -> models.Users:
    new_password = account.get_password(users.data[user_index][PASSWORD])
    if not new_password:
        return users

    users.update_information(user_index, PASSWORD, new_password)
    print("رمزعبور شما با موفقیت تغییر یافت")

    return users

def _get_account_number(users: models.Users) -> str:
    failed_attempt = FAILED_ATTEMPT
    account_number = ""
    while failed_attempt:
        account_number = input("☞ لطفا شماره حساب کاربر مد نظر را وارد نمایید ")
        if not utils.is_valid_account_number(account_number, "users"):
            failed_attempt -= 1
            print("شماره حساب نامعتبر؛ لطفا مجددا تلاش فرمایید")
            print("شما %d تلاش باقی مانده دارید" % failed_attempt)
        elif account_number not in users.users_set:
            failed_attempt -= 1
            print("شماره حساب موجود نیست؛ لطفا مجددا تلاش فرمایید")
            print("شما %d تلاش باقی مانده دارید" % failed_attempt)
        else:
            break

    if not failed_attempt:
        print("تلاش های ناموفق شما بسیار بود؛لطفا اندکی صبر نمایید و سپس مجددا تلاش کنید")
        phone_number = ""

    return account_number

def _get_user_information_by_field(users: models.Users) -> None:
    print("☞ لطفا ازبین گزینه های زیر انتخاب نمایید")
    print("  ┌─────────────┐  ╭────────────────────────────╮     ")
    print("  │             │  │ ▶︎ 1 • شماره حساب          │   ")
    print("  │  I  A  U    │  ├─────────────────────┬──────╯     ")
    print("  │  S A R I    │  │ ▶︎ 2 • موجودی       │          ")
    print("  │  B A N K    │  ├─────────────────────┴──╮         ")
    print("  │             │  │ ▶︎ 3 • نام             │       ")
    print("  └─────────────┘  ╰────────────────────────╯          ")

    failed_attempt = FAILED_ATTEMPT
    user_choice = ""
    while failed_attempt:
        user_choice = input("☞ لطفا شماره حساب کاربر را وارد نمایید ")
        if user_choice not in FIELDS_SEARCH:
            failed_attempt -= 1
            print(f"شما نمیتوانید جستجو نمایید: {field}, مجددا تلاش فرمایید")
            print("شما %d تلاش باقی مانده دارید" % failed_attempt)
        else:
            break

    if not failed_attempt or not user_choice:
        print("تلاش های ناموفق شما بسیار بود؛لطفا اندکی صبر نمایید و سپس مجددا تلاش کنید")
        phone_number = ""

    field = FIELDS_SEARCH[user_choice]
    sort_data = sorts.Sorting(users.data, field, "").arr
    if not sort_data:
        print("هیچ کاربری درحال حاضر در دیتابیس موجود نمیباشد")
        return

    for user in sort_data:
        _display_user_information(user)