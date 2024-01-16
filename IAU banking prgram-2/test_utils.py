from unittest import TestCase

from utils import *


class Test(TestCase):



    def test_is_valid_name(self):
        self.countTestCases()
        self.assertTrue(is_valid_name("long", 4))
        self.assertTrue(is_valid_name("도주용", 4))
        self.assertFalse(is_valid_name("long", 3))
        self.assertFalse(is_valid_name("long%", 6))
        self.assertFalse(is_valid_name("long#", 6))
        self.assertFalse(is_valid_name("""lon"g""", 6))
        self.assertFalse(is_valid_name("!long", 6))
        self.assertFalse(is_valid_name("long'", 6))
        self.assertFalse(is_valid_name("long1", 6))


    # def test_get_temporal(self):
    #     self.fail()
    #
    #


    def test_is_valid_day(self):
        self.assertTrue(is_valid_day([26, 10, 2003], [4, 8, 2022])) 
        self.assertTrue(is_valid_day([18, 8, 1988], [4, 8, 2022]))
        self.assertFalse(is_valid_day([30, 2, 2018], [4, 8, 2022]))
        self.assertFalse(is_valid_day([31, 9, 2019], [4, 8, 2022]))
        self.assertFalse(is_valid_day([0, 12, 2010], [4, 8, 2022]))
        self.assertFalse(is_valid_day([40, 5, 1967], [4, 8, 2022]))
        self.assertFalse(is_valid_day([11, 15, 2008], [4, 8, 2022]))
        self.assertFalse(is_valid_day([3, 30, 2004], [4, 8, 2022]))
        self.assertFalse(is_valid_day([8, 0, 2009], [4, 8, 2022]))


    # def test_is_valid_phone_number(self):
    #     self.fail()
    #
    #
    # def test_is_valid_email(self):
    #     self.fail()
    #


    def test_is_valid_password(self):
        self.assertTrue(is_valid_password("21101998Abc."))
        self.assertTrue(is_valid_password("26102003@Abcd")) 
        self.assertTrue(is_valid_password("aA^U@UgVVE~An%eMxnzN#SAJ^^hG=p3CRuT875B`o6=%c36n*@=JW7c9mH~_SPPa%9"
                                          "nQAAvnLAvfPCjThG`QhtsG#gS=Wymkg#~q"))
        self.assertFalse(is_valid_password("21101998Abc"))
        self.assertFalse(is_valid_password("21101998abc."))
        self.assertFalse(is_valid_password("26102003_abcd"))
        self.assertFalse(is_valid_password("abcd1234"))
        self.assertFalse(is_valid_password("dochautuan@gmail.com"))
        self.assertFalse(is_valid_password("OPTIMIZATION@1234"))
        self.assertFalse(is_valid_password("tuandz"))
        self.assertFalse(is_valid_password("21101998Abc. "))
        self.assertFalse(is_valid_password("_D3ns3J+c/3rD=FJ/$#/-hh~y4svT$8Kuner-aF&KD23ZXLrL#w-%aVKwc'fiz5kM7i="
                                           "FRaHFyYB*6/aw8-rTda$RtWwxbUnwq`+tuan"))


    # def test_is_valid_account_number(self):
    #     self.fail()
    #
    #
    # def test_get_yes_no_choice(self):
    #     self.fail()
    #
    #
    # def test_is_valid_balance(self):
    #     self.fail()
    #
    #
    # def test_is_valid_message(self):
    #     self.fail()
    #
    #
    # def test_proceed_next(self):
    #     self.fail()
