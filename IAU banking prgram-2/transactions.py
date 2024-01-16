from typing import Optional

import sorts
from consts import *
import models
import utils


def transaction_services(users: models.Users, user_index: int) -> models.Users:

    print("لطفا عملیات مورد نظر خود را انتخاب نمایید")
    print("  ┌─────────────┐  ╭───────────────────────────╮        ")
    print("  │             │  │ ▶︎ 1 •مشاهده موجودی       │     ")
    print("  │             │  ├───────────────────────────┴╮        ")
    print("  │             │  │ ▶︎ 2 • انتقال وجه          │      ")
    print("  │  I  A  U    │  ├───────────────────────────┬╯       ")
    print("  │  S A R I    │  │ ▶︎ 3 • واریز به حساب      │      ")
    print("  │  B A N K    │  ├───────────────────────────┴─╮       ")
    print("  │             │  │ ▶︎ 4 • برداشت از حساب       │    ")
    print("  │             │  ├──────────────────┬──────────╯       ")
    print("  │             │  │ ▶︎ 5 • خروج      │               ")
    print("  └─────────────┘  ╰──────────────────╯                  ")

    failed_attempt = FAILED_ATTEMPT
    user_choice = ""
    while failed_attempt:
        user_choice = input("☞ Enter your choice: ")
        if user_choice not in USER_TRANSACTION_CHOICES:
            failed_attempt -= 1
            print("ورودی نامعتبر!از ۱ تا ۴ انتخاب کنید")
            print("تلاش باقی مانده : %d " % failed_attempt)
        else:
            break

    if not failed_attempt:
        print("تلاش های ناموفق شما بسیار بود؛لطفا اندکی صبر نمایید و سپس مجددا تلاش کنید!!!")
        return users

    if user_choice == "1":
        print(f"موجودی حساب شما: {users.data[user_index][BALANCE]}")
        utils.proceed_next()

    if user_choice == "2":
        users = transfer_money(users, user_index)
        
    if user_choice == "3":
        users = deposit_money(users, user_index)

    if user_choice == "4":
        users = withdraw_money(users, user_index)

    if user_choice == "5":
        print("قطع عملیات!!!")
        return users

    return users

def transfer_money(users: models.Users, user_index: int) -> models.Users:
    return _transfer_internal(users, user_index)

def deposit_money(users, user_index: int) -> models.Users:
    deposit = _get_money(float('inf'))
    if not deposit:
        print("واریز وجه به حساب ناموقق بود")
        return users
        
    print(f"همچنان میخواهید وجه به حساب {deposit} انتقال دهید?")
    user_choice = utils.get_yes_no_choice()
    if not user_choice:
        print("قطع عملیات!!!")
        return users

    if user_choice == "2":
        print("قطع عملیات!!!")
        return users

    user = users.data[user_index]
    current_balance = user[BALANCE]
    expect_balance = float(current_balance) + float(deposit)
    print(f"موجودی حساب شما بعد از واریز: {expect_balance} خواهد شد")

    print("واریز به حساب انجام شود?")
    user_choice = utils.get_yes_no_choice()
    if not user_choice:
        print("قطع عملیات!!!")
        return users

    if user_choice == "2":
        print("قطع عملیات!!!")
        return users

    users.update_information(user_index, BALANCE, str(expect_balance))
    print("وجه مورد نظر با موفقیت واریز گردید!!!")
    print(f"موجودی حساب شما: {expect_balance}")

    return users

def withdraw_money(users: models.Users, user_index: int) -> models.Users:
    user = users.data[user_index]
    current_balance = float(user[BALANCE])
    withdraw = _get_money(current_balance)
    if not withdraw:
        print("برداشت از حساب ناموفق")
        return users

    print(f"ایا میخواهید به برداشت از حساب {withdraw} ادامه دهید?")
    user_choice = utils.get_yes_no_choice()
    if not user_choice:
        print("قطع عملیات!!!")
        return users

    if user_choice == "2":
        print("قطع عملیات!!!")
        return users

    expect_balance = float(current_balance) - float(withdraw)
    print(f"موجودی شما پس از برداشت وجه: {expect_balance} خواهد شد")

    print("با برداشت وجه موافقت میکنید؟")
    user_choice = utils.get_yes_no_choice()
    if not user_choice:
        print("قطع عملیات!!!")
        return users

    if user_choice == "2":
        print("قطع عملیات!!!")
        return users

    users.update_information(user_index, BALANCE, str(expect_balance))
    print("وجه مورد نظر با موفقیت برداشت شد!!!")
    print(f"موجودی حساب شما: {expect_balance}")

    return users

def _transfer_internal(users: models.Users, user_index: int) -> models.Users:
    failed_attempt = FAILED_ATTEMPT
    receiver_account_number = ""
    account_number = users.data[user_index][ACCOUNT_NUMBER]
    while failed_attempt:
        receiver_account_number = input("☞ شماره حساب را وارد کنید: ")
        if not utils.is_valid_account_number(receiver_account_number, "users"):
            failed_attempt -= 1
            print("شماره حساب نامعتبر!!!")
            print("شما %d تلاش باقی مانده دارید" % failed_attempt)
        elif receiver_account_number == account_number:
            failed_attempt -= 1
            print("حساب خودتان است لطفا مجددا تلاش فرمایید")
            print("شما %d تلاش باقی مانده دارید" % failed_attempt)
        elif receiver_account_number not in users.users_set:
            failed_attempt -= 1
            print("حسابی موجود نیست")
            print("شما %d تلاش باقی مانده دارید" % failed_attempt)
        else:
            break

    if not failed_attempt:
        print("شما شماره حساب اشتباهی را چندین بار وارد نموده اید؛لطفا اندکی صبر و سپس مجددا امتحان فرمایید")
        return users

    receiver_index = sorts.binary_search(users.data, ACCOUNT_NUMBER, receiver_account_number)

    receiver = users.data[receiver_index]
    receiver_balance = float(receiver[BALANCE])
    receiver_name = receiver[LAST_NAME] + " " + receiver[MIDDLE_NAME] + " " + receiver[FIRST_NAME]
    print(f"Account number: {receiver_account_number}")
    print(f"Account holder: {receiver_name}")

    print("☞ میخواهید ادامه دهید؟ اگر بله ۱ را و ۲ را اگر نه؛ بفشارید")
    user_choice = utils.get_yes_no_choice()
    if not user_choice:
        print("قطع عملیات!!!")
        return users

    if user_choice == "2":
        print("قطع عملیات!!!")
        return users

    user = users.data[user_index]
    user_balance = float(user[BALANCE])
    transfer_money = _get_money(user_balance)
    if not transfer_money:
        print("قطع عملیات")
        return users
    
    user_name = user[LAST_NAME] + " " + user[MIDDLE_NAME] + " " + user[FIRST_NAME]

    print("اطلاعات تراکنش")
    print(f"فرستنده: {user_name}")
    print(f"شماره حساب مقصد: {receiver_account_number}")
    print(f"گیرنده: {receiver_name}")
    print(f"مبلغ: {transfer_money}")

    print("تایید میکنید؟")
    user_choice = utils.get_yes_no_choice()
    if not user_choice:
        print("قطع عملیات")
        return users

    if user_choice == "2":
        print("قطع عملیات")
        return users

    receiver_balance += transfer_money
    user_balance -= transfer_money

    users.update_information(user_index, BALANCE, str(user_balance))
    users.update_information(receiver_index, BALANCE, str(receiver_balance))

    print("وجه مورد نظر با موفقیت انتقال پیدا کرد")
    print(f"موجودی شما: {user_balance}")

    return users

def _get_money(balance: float) -> float:
    failed_attempt = FAILED_ATTEMPT
    money = 0
    while failed_attempt:
        money = input("لطفا مبلغ واریزی را وارد نمایید: ")
        if not utils.is_valid_balance(money):
            failed_attempt -= 1
            print("مبغ اشتباه است؛لطفا عدد وارد نمایید")
            print("شما %d تلاش باقی مانده دارید" % failed_attempt)
        elif float(money) > balance:
            failed_attempt -= 1
            print("موجودی کافی نیست؛مبلغ دیگری وارد نمایید")
            print("شما %d تلاش باقی مانده دارید" % failed_attempt)
        else:
            break

    if not failed_attempt:
        print("شما مبلغ واریزی را چندین بار اشتباه وارد کرده اید؛لطفا اندکی صبر و سپس مجددا اقدام نمایید.")
        return 0

    return float(money)