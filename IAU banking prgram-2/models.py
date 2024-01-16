import datetime
import random
from collections import defaultdict


import sorts
from consts import *
import utils


class Users:

    def __init__(self, privilege: str = "users"):

        self.privilege = privilege
        self.configs = ACCOUNT_CONFIGS[privilege]
        raw_data = utils.get_data_from_json(self.configs[FILE_NAME])
        sorting = sorts.Sorting(raw_data, ACCOUNT_NUMBER, "")
        self.data = sorting.arr if sorting.arr else []
        self.users_set = set([account[ACCOUNT_NUMBER] for account in self.data])

    def create_new(self, user_information: defaultdict[str]) -> int:
        """
        ساختن کاربر جدید مطابق اطلاعات داده شده
        """

        new_account_number = self.generate_account_number(self.configs[ACCOUNT_NUMBER_LEN])
        while new_account_number in self.users_set:
            new_account_number = self.generate_account_number(self.configs[ACCOUNT_NUMBER_LEN])

        today_date = datetime.date.today().strftime("%d/%m/%Y")
        user_information[ACCOUNT_NUMBER] = new_account_number
        user_information[ISSUED_DATE] = today_date
        self.data.append(user_information)
        self.users_set.add(new_account_number)
        utils.write_data_to_json(self.data, self.configs[FILE_NAME])

        return len(self.data) - 1


    def delete_user(self, index: int) -> None:
        """
       حذف کاربر از دیتابیس و داده های موجود
        """

        account_number = self.data[index][ACCOUNT_NUMBER]
        self.data = self.data[:index] + self.data[index + 1:]
        self.users_set.remove(account_number)
        utils.write_data_to_json(self.data, self.configs[FILE_NAME])


    @staticmethod
    def generate_account_number(account_len: int):
        """
        ایجاد یک شماره حساب جدید و منحصر به فرد

        شامل هشت رقم اول بانک و هشت رقم تصادفی
        """

        new_number = []
        for _ in range(account_len):
            new_number.append(str(random.randint(0, 9)))

        return ''.join(new_number)


    def update_information(self, index: int, field: str, change: str):
        """
        تغییر اطلاعات کاربر
        """

        self.data[index][field] = change
        utils.write_data_to_json(self.data, self.configs[FILE_NAME])
