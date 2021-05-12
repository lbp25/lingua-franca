#
# Copyright 2017 Mycroft AI Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import unittest
import datetime

from lingua_franca import load_language, unload_language, set_default_lang
from lingua_franca.format import nice_number
from lingua_franca.format import nice_time
from lingua_franca.format import pronounce_number


def setUpModule():
    load_language('fr-gcf')
    set_default_lang('gcf')


def tearDownModule():
    unload_language('gcf')


NUMBERS_FIXTURE_GCF = {
    1.435634: '1,436',
    2: '2',
    5.0: '5',
    1234567890: '1234567890',
    12345.67890: '12345,679',
    0.027: '0,027',
    0.5: 'on dèmi',
    1.333: '1 é 1 tiew',
    2.666: '2 é 2 tiew',
    0.25: 'on kaw',
    1.25: '1 é 1 kaw',
    0.75: '3 kaw',
    1.75: '1 é 3 kaw',
    3.4: '3 é 2 senkièm',
    16.8333: '16 é 5 sizièm',
    12.5714: '12 é 4 sétièm',
    9.625: '9 é 5 huitièm',
    6.777: '6 é 7 névièm',
    3.1: '3 é 1 dizièm',
    2.272: '2 é 3 onzièm',
    5.583: '5 é 7 douzièm',
    8.384: '8 é 5 trézièm',
    0.071: 'on katorzièm',
    6.466: '6 é 7 kinzièm',
    8.312: '8 é 5 sézièm',
    2.176: '2 é 3 disétièm',
    200.722: '200 é 13 dizuitièm',
    7.421: '7 é 8 diznévièm',
    0.05: 'on ventièm'
}


class TestNiceNumberFormat_gcf(unittest.TestCase):
    def test_convert_float_to_nice_number_gcf(self):
        for number, number_str in NUMBERS_FIXTURE_GCF.items():
            self.assertEqual(nice_number(number, lang="fr-gcf"), number_str,
                             'should format {} as {} and not {}'.format(
                                 number, number_str, nice_number(
                                     number, lang="fr-gcf")))

    def test_specify_denominator_gcf(self):
        self.assertEqual(nice_number(5.5, lang="fr-gcf",
                                     denominators=[1, 2, 3]),
                         '5 et demi',
                         'should format 5.5 as 5 et demi not {}'.format(
                             nice_number(5.5, lang="fr-gcf",
                                         denominators=[1, 2, 3])))
        self.assertEqual(nice_number(2.333, lang="fr-gcf",
                                     denominators=[1, 2]),
                         '2,333',
                         'should format 2.333 as 2,333 not {}'.format(
                             nice_number(2.333, lang="fr-gcf",
                                         denominators=[1, 2])))

    def test_no_speech_gcf(self):
        self.assertEqual(nice_number(6.777, lang="fr-gcf", speech=False),
                         '6 7/9',
                         'should format 6.777 as 6 7/9 not {}'.format(
                             nice_number(6.777, lang="fr-gcf", speech=False)))
        self.assertEqual(nice_number(6.0, lang="fr-gcf", speech=False),
                         '6',
                         'should format 6.0 as 6 not {}'.format(
                             nice_number(6.0, lang="fr-gcf", speech=False)))
        self.assertEqual(nice_number(1234567890, lang="fr-gcf", speech=False),
                         '1 234 567 890',
                         'should format 1234567890 as'
                         '1 234 567 890 not {}'.format(
                             nice_number(1234567890, lang="fr-gcf",
                                         speech=False)))
        self.assertEqual(nice_number(12345.6789, lang="fr-gcf", speech=False),
                         '12 345,679',
                         'should format 12345.6789 as'
                         '12 345,679 not {}'.format(
                             nice_number(12345.6789, lang="fr-gcf",
                                         speech=False)))


# def pronounce_number(number, lang="en-us", places=2):
class TestPronounceNumber_gcf(unittest.TestCase):
    def test_convert_int_gcf(self):
        self.assertEqual(pronounce_number(0, lang="fr-gcf"), "zéro")
        self.assertEqual(pronounce_number(1, lang="fr-gcf"), "yonn")
        self.assertEqual(pronounce_number(10, lang="fr-gcf"), "dis")
        self.assertEqual(pronounce_number(15, lang="fr-gcf"), "kinz")
        self.assertEqual(pronounce_number(20, lang="fr-gcf"), "ven")
        self.assertEqual(pronounce_number(27, lang="fr-gcf"), "venn-sèt")
        self.assertEqual(pronounce_number(30, lang="fr-gcf"), "trant")
        self.assertEqual(pronounce_number(33, lang="fr-gcf"), "tranntwa")
        self.assertEqual(pronounce_number(71, lang="fr-gcf"),
                         "soisant-é-onz")
        self.assertEqual(pronounce_number(80, lang="fr-gcf"), "katrèven")
        self.assertEqual(pronounce_number(74, lang="fr-gcf"),
                         "soisann-katoz")
        self.assertEqual(pronounce_number(79, lang="fr-gcf"),
                         "soisann-diznèf")
        self.assertEqual(pronounce_number(91, lang="fr-gcf"),
                         "katrèven-onz")
        self.assertEqual(pronounce_number(97, lang="fr-gcf"),
                         "katrèven-disèt")
        self.assertEqual(pronounce_number(300, lang="fr-gcf"), "300")

    def test_convert_negative_int_gcf(self):
        self.assertEqual(pronounce_number(-1, lang="fr-gcf"), "mwen yonn")
        self.assertEqual(pronounce_number(-10, lang="fr-gcf"), "mwen dis")
        self.assertEqual(pronounce_number(-15, lang="fr-gcf"), "mwen kenz")
        self.assertEqual(pronounce_number(-20, lang="fr-gcf"), "mwen ven")
        self.assertEqual(pronounce_number(-27, lang="fr-gcf"),
                         "mwen vennsèt")
        self.assertEqual(pronounce_number(-30, lang="fr-gcf"), "mwen trant")
        self.assertEqual(pronounce_number(-33, lang="fr-gcf"),
                         "mwen tranntwa")

    def test_convert_decimals_gcf(self):
        self.assertEqual(pronounce_number(0.05, lang="fr-gcf"),
                         "zéro virgil zéro senk")
        self.assertEqual(pronounce_number(-0.05, lang="fr-gcf"),
                         "mwen zéro virgil zéro senk")
        self.assertEqual(pronounce_number(1.234, lang="fr-gcf"),
                         "yonn virgil dé twa")
        self.assertEqual(pronounce_number(21.234, lang="fr-gcf"),
                         "vent-é-yun virgil dé twa")
        self.assertEqual(pronounce_number(21.234, lang="fr-gcf", places=1),
                         "vent-é-yun virgil dé")
        self.assertEqual(pronounce_number(21.234, lang="fr-gcf", places=0),
                         "vent-é-yun")
        self.assertEqual(pronounce_number(21.234, lang="fr-gcf", places=3),
                         "vent-é-yun virgil dé twa kat")
        self.assertEqual(pronounce_number(21.234, lang="fr-gcf", places=4),
                         "vent-é-yun virgil dé twa kat")
        self.assertEqual(pronounce_number(21.234, lang="fr-gcf", places=5),
                         "vent-é-yun virgil dé twa kat")
        self.assertEqual(pronounce_number(-1.234, lang="fr-gcf"),
                         "mwen yonn virgil dé twa")
        self.assertEqual(pronounce_number(-21.234, lang="fr-gcf"),
                         "mwen vent-é-yun virgil dé twa")
        self.assertEqual(pronounce_number(-21.234, lang="fr-gcf", places=1),
                         "mwen vent-é-yun virgil dé")
        self.assertEqual(pronounce_number(-21.234, lang="fr-gcf", places=0),
                         "mwen vent-é-yun")
        self.assertEqual(pronounce_number(-21.234, lang="fr-gcf", places=3),
                         "mwen vent-é-yun virgil dé twa kat")
        self.assertEqual(pronounce_number(-21.234, lang="fr-gcf", places=4),
                         "mwen vent-é-yun virgil dé twa kat")
        self.assertEqual(pronounce_number(-21.234, lang="fr-gcf", places=5),
                         "mwen vent-é-yun virgil dé twa kat")


# def nice_time(dt, lang="en-us", speech=True, use_24hour=False,
#              use_ampm=False):
class TestNiceDateFormat_gcf(unittest.TestCase):
    def test_convert_times_gcf(self):
        dt = datetime.datetime(2017, 1, 31,
                               13, 22, 3)

        self.assertEqual(nice_time(dt, lang="fr-gcf"),
                         "inè é venndé minit")
        self.assertEqual(nice_time(dt, lang="fr-gcf", use_ampm=True),
                         "inè-d-swa é venndé minit")
        self.assertEqual(nice_time(dt, lang="fr-gcf", speech=False),
                         "1:22")
        self.assertEqual(nice_time(dt, lang="fr-gcf", speech=False,
                                   use_ampm=True),
                         "1:22 PM")
        self.assertEqual(nice_time(dt, lang="fr-gcf", speech=False,
                                   use_24hour=True),
                         "13:22")
        self.assertEqual(nice_time(dt, lang="fr-gcf", speech=False,
                                   use_24hour=True, use_ampm=True),
                         "13:22")
        self.assertEqual(nice_time(dt, lang="fr-gcf", use_24hour=True,
                                   use_ampm=True),
                         "trézè venndé")
        self.assertEqual(nice_time(dt, lang="fr-gcf", use_24hour=True,
                                   use_ampm=False),
                         "trézè venndé")

        dt = datetime.datetime(2017, 1, 31,
                               13, 0, 3)
        self.assertEqual(nice_time(dt, lang="fr-gcf"),
                         "inè")
        self.assertEqual(nice_time(dt, lang="fr-gcf", use_ampm=True),
                         "inè-d-swa")
        self.assertEqual(nice_time(dt, lang="fr-gcf", speech=False),
                         "1:00")
        self.assertEqual(nice_time(dt, lang="fr-gcf", speech=False,
                                   use_ampm=True),
                         "1:00 PM")
        self.assertEqual(nice_time(dt, lang="fr-gcf", speech=False,
                                   use_24hour=True),
                         "13:00")
        self.assertEqual(nice_time(dt, lang="fr-gcf", speech=False,
                                   use_24hour=True, use_ampm=True),
                         "13:00")
        self.assertEqual(nice_time(dt, lang="fr-gcf", use_24hour=True,
                                   use_ampm=True),
                         "trézè")
        self.assertEqual(nice_time(dt, lang="fr-gcf", use_24hour=True,
                                   use_ampm=False),
                         "trézè")

        dt = datetime.datetime(2017, 1, 31,
                               13, 2, 3)
        self.assertEqual(nice_time(dt, lang="fr-gcf"),
                         "inè é dé minit")
        self.assertEqual(nice_time(dt, lang="fr-gcf", use_ampm=True),
                         "inè-d-swa é dé minit")
        self.assertEqual(nice_time(dt, lang="fr-gcf", speech=False),
                         "1:02")
        self.assertEqual(nice_time(dt, lang="fr-gcf", speech=False,
                                   use_ampm=True),
                         "1:02 PM")
        self.assertEqual(nice_time(dt, lang="fr-gcf", speech=False,
                                   use_24hour=True),
                         "13:02")
        self.assertEqual(nice_time(dt, lang="fr-gcf", speech=False,
                                   use_24hour=True, use_ampm=True),
                         "13:02")
        self.assertEqual(nice_time(dt, lang="fr-gcf", use_24hour=True,
                                   use_ampm=True),
                         "trézè é dé minit")
        self.assertEqual(nice_time(dt, lang="fr-gcf", use_24hour=True,
                                   use_ampm=False),
                         "trézè é dé minit")

        dt = datetime.datetime(2017, 1, 31,
                               0, 2, 3)
        self.assertEqual(nice_time(dt, lang="fr-gcf"),
                         "minwi dé")
        self.assertEqual(nice_time(dt, lang="fr-gcf", use_ampm=True),
                         "minxi dé")
        self.assertEqual(nice_time(dt, lang="fr-gcf", speech=False),
                         "12:02")
        self.assertEqual(nice_time(dt, lang="fr-gcf", speech=False,
                                   use_ampm=True),
                         "12:02 AM")
        self.assertEqual(nice_time(dt, lang="fr-gcf", speech=False,
                                   use_24hour=True),
                         "00:02")
        self.assertEqual(nice_time(dt, lang="fr-gcf", speech=False,
                                   use_24hour=True, use_ampm=True),
                         "00:02")
        self.assertEqual(nice_time(dt, lang="fr-gcf", use_24hour=True,
                                   use_ampm=True),
                         "minwi dé")
        self.assertEqual(nice_time(dt, lang="fr-gcf", use_24hour=True,
                                   use_ampm=False),
                         "minwi dé")

        dt = datetime.datetime(2017, 1, 31,
                               12, 15, 9)
        self.assertEqual(nice_time(dt, lang="fr-fr"),
                         "midi un ka")
        self.assertEqual(nice_time(dt, lang="fr-fr", use_ampm=True),
                         "midi un ka")
        self.assertEqual(nice_time(dt, lang="fr-fr", speech=False),
                         "12:15")
        self.assertEqual(nice_time(dt, lang="fr-fr", speech=False,
                                   use_ampm=True),
                         "12:15 PM")
        self.assertEqual(nice_time(dt, lang="fr-fr", speech=False,
                                   use_24hour=True),
                         "12:15")
        self.assertEqual(nice_time(dt, lang="fr-fr", speech=False,
                                   use_24hour=True, use_ampm=True),
                         "12:15")
        self.assertEqual(nice_time(dt, lang="fr-fr", use_24hour=True,
                                   use_ampm=True),
                         "midi kinz")
        self.assertEqual(nice_time(dt, lang="fr-fr", use_24hour=True,
                                   use_ampm=False),
                         "midi kinz")

        dt = datetime.datetime(2017, 1, 31,
                               19, 40, 49)
        self.assertEqual(nice_time(dt, lang="fr-gcf"),
                         "huitè mwen ven")
        self.assertEqual(nice_time(dt, lang="fr-gcf", use_ampm=True),
                         "huitè-d-swa mwen ven")
        self.assertEqual(nice_time(dt, lang="fr-gcf", speech=False),
                         "7:40")
        self.assertEqual(nice_time(dt, lang="fr-gcf", speech=False,
                                   use_ampm=True),
                         "7:40 PM")
        self.assertEqual(nice_time(dt, lang="fr-gcf", speech=False,
                                   use_24hour=True),
                         "19:40")
        self.assertEqual(nice_time(dt, lang="fr-gcf", speech=False,
                                   use_24hour=True, use_ampm=True),
                         "19:40")
        self.assertEqual(nice_time(dt, lang="fr-gcf", use_24hour=True,
                                   use_ampm=True),
                         "diznévè karant")
        self.assertEqual(nice_time(dt, lang="fr-gcf", use_24hour=True,
                                   use_ampm=False),
                         "diznévè karant")

        dt = datetime.datetime(2017, 1, 31,
                               1, 15, 00)
        self.assertEqual(nice_time(dt, lang="fr-gcf", use_24hour=True),
                         "inè kenz")

        dt = datetime.datetime(2017, 1, 31,
                               1, 35, 00)
        self.assertEqual(nice_time(dt, lang="fr-gcf"),
                         "dézè mwen vennsenk")

        dt = datetime.datetime(2017, 1, 31,
                               1, 45, 00)
        self.assertEqual(nice_time(dt, lang="fr-gcf"),
                         "dézè mwen-l-ka")

        dt = datetime.datetime(2017, 1, 31,
                               4, 50, 00)
        self.assertEqual(nice_time(dt, lang="fr-gcf"),
                         "senkè mwen dis")

        dt = datetime.datetime(2017, 1, 31,
                               5, 55, 00)
        self.assertEqual(nice_time(dt, lang="fr-gcf"),
                         "sizè mwen senk")

        dt = datetime.datetime(2017, 1, 31,
                               5, 30, 00)
        self.assertEqual(nice_time(dt, lang="fr-gcf", use_ampm=True),
                         "senkè é dèmi")


if __name__ == "__main__":
    unittest.main()
