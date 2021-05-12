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
from datetime import datetime, time, timedelta

from lingua_franca import load_language, unload_language, set_default_lang
from lingua_franca.internal import FunctionNotLocalizedError
from lingua_franca.parse import get_gender
from lingua_franca.parse import extract_datetime
from lingua_franca.parse import extract_duration
from lingua_franca.parse import extract_number
from lingua_franca.parse import normalize


def setUpModule():
    load_language('fr-gcf')
    set_default_lang('gcf')


def tearDownModule():
    unload_language('gcf')


class TestNormalize_gcf(unittest.TestCase):
    def test_articles_gcf(self):
        self.assertEqual(normalize("cé yon test", remove_articles=True,
                                   lang="fr-gcf"),
                         "cé test")
        self.assertEqual(normalize("é lòt test", remove_articles=True,
                                   lang="fr-gcf"),
                         "é lòt test")
        self.assertEqual(normalize("é tantativ-là", remove_articles=True,
                                   lang="fr-gcf"),
                         "é tantativ")
        self.assertEqual(normalize("dènié tantative-là",
                                   remove_articles=False, lang="fr-gcf"),
                         "dènié tantativ-là")

    def test_extractnumber_gcf(self):
        self.assertEqual(extract_number("mi prèmyé test-là", lang="fr-gcf"),
                         1)
        self.assertEqual(extract_number("cé 2 test", lang="fr-gcf"), 2)
        self.assertEqual(extract_number("mi sègon test-là", lang="fr-gcf"),
                         2)
        self.assertEqual(extract_number("mi twa test",
                                        lang="fr-gcf"),
                         3)
        self.assertEqual(extract_number("mi test niméro 4-là",
                                        lang="fr-gcf"), 4)
        self.assertEqual(extract_number("on tiè lit", lang="fr-gcf"),
                         1.0 / 3.0)
        self.assertEqual(extract_number("3 kuiyè", lang="fr-gcf"), 3)
        self.assertEqual(extract_number("1/3 lit", lang="fr-gcf"),
                         1.0 / 3.0)
        self.assertEqual(extract_number("on ka-bòl", lang="fr-gcf"), 0.25)
        self.assertEqual(extract_number("1/4 vè", lang="fr-gcf"), 0.25)
        self.assertEqual(extract_number("2/3 bòl", lang="fr-gcf"), 2.0 / 3.0)
        self.assertEqual(extract_number("3/4 bòl", lang="fr-gcf"), 3.0 / 4.0)
        self.assertEqual(extract_number("1 é 3/4 bòl", lang="fr-gcf"), 1.75)
        self.assertEqual(extract_number("1 bòl é dèmi", lang="fr-gcf"), 1.5)
        self.assertEqual(extract_number("on bòl é dèmi", lang="fr-gcf"), 1.5)
        self.assertEqual(extract_number("on bòl é dèmi", lang="fr-gcf"), 1.5)
        self.assertEqual(extract_number("on bòl é dèmi", lang="fr-gcf"),
                         1.5)
        self.assertEqual(extract_number("twa-ka bòl", lang="fr-gcf"),
                         3.0 / 4.0)
        self.assertEqual(extract_number("32.2 dègré", lang="fr-gcf"), 32.2)
        self.assertEqual(extract_number("2 virgil 2 cm", lang="fr-gcf"), 2.2)
        self.assertEqual(extract_number("2 virgil 0 2 cm", lang="fr-gcf"),
                         2.02)
        self.assertEqual(extract_number("sa ka fè zéro virgil 2 cm", lang="fr-gcf"),
                         0.2)
        self.assertEqual(extract_number("pwen di tou", lang="fr-gcf"), False)
        self.assertEqual(extract_number("32.00 secondes", lang="fr-gcf"), 32)
        self.assertEqual(extract_number("manjé trantéyun bouji",
                                        lang="fr-gcf"), 31)
        self.assertEqual(extract_number("on trantièm",
                                        lang="fr-gcf"), 1.0 / 30.0)
        self.assertEqual(extract_number("on santièm",
                                        lang="fr-gcf"), 0.01)
        self.assertEqual(extract_number("on millièm",
                                        lang="fr-gcf"), 0.001)
        self.assertEqual(extract_number("on 20e",
                                        lang="fr-gcf"), 1.0 / 20.0)

    def test_extractdatetime_gcf(self):
        def extractWithFormat_gcf(text):
            date = datetime(2017, 6, 27, 0, 0)
            [extractedDate, leftover] = extract_datetime(text, date,
                                                         lang="fr-gcf")
            extractedDate = extractedDate.strftime("%Y-%m-%d %H:%M:%S")
            return [extractedDate, leftover]

        def testExtract_gcf(text, expected_date, expected_leftover):
            res = extractWithFormat_gcf(text)
            self.assertEqual(res[0], expected_date)
            self.assertEqual(res[1], expected_leftover)

        def extractWithFormatDate2_gcf(text):
            date = datetime(2017, 6, 30, 17, 0)
            [extractedDate, leftover] = extract_datetime(text, date,
                                                         lang="fr-gcf")
            extractedDate = extractedDate.strftime("%Y-%m-%d %H:%M:%S")
            return [extractedDate, leftover]

        def testExtractDate2_gcf(text, expected_date, expected_leftover):
            res = extractWithFormatDate2_gcf(text)
            self.assertEqual(res[0], expected_date)
            self.assertEqual(res[1], expected_leftover)

        def extractWithFormatNoDate_gcf(text):
            [extractedDate, leftover] = extract_datetime(text, lang="fr-gcf")
            extractedDate = extractedDate.strftime("%Y-%m-%d %H:%M:%S")
            return [extractedDate, leftover]

        def testExtractNoDate_gcf(text, expected_date, expected_leftover):
            res = extractWithFormatNoDate_gcf(text)
            self.assertEqual(res[0], expected_date)
            self.assertEqual(res[1], expected_leftover)

        testExtract_gcf("Plannifié anbuch-là pou dan 5 jou",
                       "2017-07-02 00:00:00", "plannifié anbuch")
        testExtract_gcf("Ki tan i kay fè aprè-dèmen ?",
                       "2017-06-29 00:00:00", "ki tan i kay fè")
        testExtract_gcf("Mèt on rapèl à 10:45pm",
                       "2017-06-27 22:45:00", "mèt 1 rapèl")
        testExtract_gcf("Ki tan i kay fè vandrèdi maten ?",
                       "2017-06-30 08:00:00", "ki tan i kay fè")
        testExtract_gcf("Ki tan i kay fè dèmen",
                       "2017-06-28 00:00:00", "ki tan i kay fè")
        testExtract_gcf("Raplé-mwen kriyé manman adan 8 sèmenn é"
                       " 2 jou", "2017-08-24 00:00:00",
                       "raplé-mwen kriyé manman")
        testExtract_gcf("Jwé misik à Beyonce 2 jou apré vandrèdi",
                       "2017-07-02 00:00:00", "jwé misik beyonce")
        testExtract_gcf("komansé envasion-là à 15 è 45 jédi",
                       "2017-06-29 15:45:00", "komansé envasion")
        testExtract_gcf("Lendi, komandé gato-là en boulanjri-là",
                       "2017-07-03 00:00:00", "komandé gato en boulanjri")
        testExtract_gcf("Jwé chanson à Joyeux anniversaire dan 5 lanné",
                       "2022-06-27 00:00:00", "jwé chanson joyeux"
                       " anniversaire")
        testExtract_gcf("Skypé Manman à 12 è 45 jédi pwochen",
                       "2017-07-06 12:45:00", "skypé manman")
        testExtract_gcf("Ki tant i kay fè jédi pwochen ?",
                       "2017-07-06 00:00:00", "ki tan i kay fè")
        testExtract_gcf("Ki tan i kay fè vandrèdi matin ?",
                       "2017-06-30 08:00:00", "ki tan i kay fè")
        testExtract_gcf("Ki tan i kay fè vandrèdi au swa? ",
                       "2017-06-30 19:00:00", "ki tan i kay fè")
        testExtract_gcf("Ki tan i kay fè vandredi an lapré-midi-là?",
                       "2017-06-30 15:00:00", "ki tan i kay fè")
        testExtract_gcf("Raplé-mwen kriyé manman lè 3 août",
                       "2017-08-03 00:00:00", "raplé-mwen kriyé manman")
        testExtract_gcf("Achté fé dartifis pou lè 14 juil",
                       "2017-07-14 00:00:00", "Achté fé dartifis pou")
        testExtract_gcf("Ki tan i ké fè 2 simenn apré vandrèdi",
                       "2017-07-14 00:00:00", "ki tan i ké fè")
        testExtract_gcf("Ki tan i ké fè mewkrèdi à 7 è",
                       "2017-06-28 07:00:00", "ki tan i ké fè")
        testExtract_gcf("ki ta i kay fè mewkrèdi à 7 è",
                       "2017-06-28 07:00:00", "ki tan i kay fè")
        testExtract_gcf("Pran rendez-vous à 12:45 jédi pwochen",
                       "2017-07-06 12:45:00", "pran rendez-vous")
        testExtract_gcf("Ki tan i ka jédi ?",
                       "2017-06-29 00:00:00", "ki tan i ka fè")
        testExtract_gcf("Organizé on visit 2 simenn é 6 jou apré"
                       " sanmdi",
                       "2017-07-21 00:00:00", "organizé 1 visit")
        testExtract_gcf("Komansé envazion-là à 3 zè 45 jédi",
                       "2017-06-29 03:45:00", "komansé envazion")
        testExtract_gcf("Komansé envazion-là à 20 è jédi",
                       "2017-06-29 20:00:00", "komansé envazion")
        testExtract_gcf("Lansé lafèt-là jédi à 8 è-d-swa",
                       "2017-06-29 20:00:00", "lansé lafèt")
        testExtract_gcf("Komansé envazion-là à 4 è-d-swa",
                       "2017-06-29 16:00:00", "komansé envaZion")
        testExtract_gcf("Komansé envazion-là jédi midi",
                       "2017-06-29 12:00:00", "Komansé envazion")
        testExtract_gcf("Komansé envazion-là jédi minwi",
                       "2017-06-29 00:00:00", "Komansé envazion")
        testExtract_gcf("Komansé envazion-là jédi à disétè",
                       "2017-06-29 17:00:00", "Komansé envazion")
        testExtract_gcf("Raplé mwen lévé adan 4 lanné",
                       "2021-06-27 00:00:00", "Raplé mwen lévé")
        testExtract_gcf("Raplé mwen lévé adan 4 lanné é 4 jou",
                       "2021-07-01 00:00:00", "Raplé mwen lévé")
        testExtract_gcf("Ki tan i kay fè 3 jou apré dèmen ?",
                       "2017-07-01 00:00:00", "ki tan i kay fè")
        testExtract_gcf("3 décembre",
                       "2017-12-03 00:00:00", "")
        testExtract_gcf("Annou kontré à 8:00 au swè-là",
                       "2017-06-27 20:00:00", "Annou kontré")
        testExtract_gcf("Annou kontré dèmen à minwi é dèmi",
                       "2017-06-28 00:30:00", "Annou kontré")
        testExtract_gcf("Annou kontré à midi é ka",
                       "2017-06-27 12:15:00", "Annou kontré")
        testExtract_gcf("Annou kontré à midi mwen-l-ka",
                       "2017-06-27 11:45:00", "Annou kontré")
        testExtract_gcf("Annou kontré à midi mwen dis",
                       "2017-06-27 11:50:00", "Annou kontré")
        testExtract_gcf("Annou kontré à midi dis",
                       "2017-06-27 12:10:00", "Annou kontré")
        testExtract_gcf("Annou kontré à minui mwen 23",
                       "2017-06-27 23:37:00", "Annou kontré")
        testExtract_gcf("Annou mangé à 3 è mwen 23 minit",
                       "2017-06-27 02:37:00", "Annou mangé")
        testExtract_gcf("Annou mangé osi à 4 è mwen-l-ka lè maten",
                       "2017-06-27 03:45:00", "Annou mangé osi")
        testExtract_gcf("Annou mangé ankò à minwi mwen-l-ka",
                       "2017-06-27 23:45:00", "Annou mangé ankò")
        testExtract_gcf("Annou bwè à 4 è é ka ",
                       "2017-06-27 04:15:00", "Annou bwè")
        testExtract_gcf("Annou bwè osi à 18 è é dèmi",
                       "2017-06-27 18:30:00", "Annou bwè osi")
        testExtract_gcf("Annou dòmi à 20 è mwen-l-ka",
                       "2017-06-27 19:45:00", "dormons")
        testExtract_gcf("Annou bwè on dènyé vè à 10 è mwen 12 lè swa",
                       "2017-06-27 21:48:00", "Annou bwè dènyé vè")
        testExtract_gcf("kité lil-là à 15h45",
                       "2017-06-27 15:45:00", "kité lil")
        testExtract_gcf("kité lil-là à 3h45min dè lapré-midi")
                       "2017-06-27 15:45:00", "kité lil")
        testExtract_gcf("Dékalé sa à 3h48min an aprèmidi-là",
                       "2017-06-27 15:48:00", "dékalé sa")
        testExtract_gcf("Konstwi on bunker à 9h42min lè maten",
                       "2017-06-27 09:42:00", "konstwi 1 bunker")
        testExtract_gcf("oubyen plito à 9h43 bo matin",
                       "2017-06-27 09:43:00", "oubyen plito")
        testExtract_gcf("limé on difé à 8h d-swa",
                       "2017-06-27 20:00:00", "limé 1 difé")
        testExtract_gcf("fè lafèt jous 18h lannuit-lasa",
                       "2017-06-27 18:00:00", "fè lafèt jous")
        testExtract_gcf("dòmi jous à 4h lannuit-lasa",
                       "2017-06-27 04:00:00", "dòmi jous")
        testExtract_gcf("Lévé-mwen adan 20 sègond jòd-là",
                       "2017-06-27 00:00:20", "lévé-mwen")
        testExtract_gcf("lévé-mwen adan 33 minit",
                       "2017-06-27 00:33:00", "lévè-mwen")
        testExtract_gcf("fèmé-y adan 12 è é 3 minit",
                       "2017-06-27 12:03:00", "fèmé-y")
        testExtract_gcf("wouvè-y adan 1 è 3",
                       "2017-06-27 01:03:00", "wouvè-y")
        testExtract_gcf("fèmé-y adan 1 è é ka",
                       "2017-06-27 01:15:00", "fèmé-y")
        testExtract_gcf("Sélé-y adan 1 è é dèmi",
                       "2017-06-27 01:30:00", "sélé-y")
        testExtract_gcf("Zipé-y adan 2 è mwen 12",
                       "2017-06-27 01:48:00", "zipé-y")
        testExtract_gcf("Soudé-y adan 3 è mwen-l-ka",
                       "2017-06-27 02:45:00", "soudé-y")
        testExtract_gcf("manjé-y simenn pwochenn,",
                       "2017-07-04 00:00:00", "manjé")
        testExtract_gcf("bwè simenn pasé",
                       "2017-06-20 00:00:00", "bwè")
        testExtract_gcf("manjé an mwa ka vinn",
                       "2017-07-27 00:00:00", "manjé")
        testExtract_gcf("bwè lè mwa pasé",
                       "2017-05-27 00:00:00", "bwè")
        testExtract_gcf("manjé lanné ka vinn",
                       "2018-06-27 00:00:00", "manjé")
        testExtract_gcf("bwè anné pasé",
                       "2016-06-27 00:00:00", "bwè")
        testExtract_gcf("rouvinn à lendi pasé",
                       "2017-06-26 00:00:00", "rouvinn")
        testExtract_gcf("Kapitulé lè 8 mé 1945",
                       "1945-05-08 00:00:00", "Kapitulé")
        testExtract_gcf("Rédigé kontra-là 3 jou apré jédi pwochen",
                       "2017-07-09 00:00:00", "Rédigé kontra")
        testExtract_gcf("Sinyé kontra-là 2 simenn apré jédi pasé",
                       "2017-07-06 00:00:00", "Sinyé kontra ")
        testExtract_gcf("Mèt fouw-là adan on kaw-dè",
                       "2017-06-27 00:15:00", "mèt fouw")
        testExtract_gcf("Anfouwné pizza-là andan on dèmi è",
                       "2017-06-27 00:30:00", "Anfouwné pizza")
        testExtract_gcf("Arété fouw-là adan twa-kaw dè",
                       "2017-06-27 00:45:00", "arété fouw")
        testExtract_gcf("Manjé pizza-là adan inè-d-tan",
                       "2017-06-27 01:00:00", "manjé pizza")
        testExtract_gcf("bwè biè-là adan 2h23",
                       "2017-06-27 02:23:00", "bwè biè")
        testExtract_gcf("fè plantasyon 3èm jou à maws",
                       "2018-03-03 00:00:00", "fè plantasyon")
        testExtract_gcf("Rékolté adan 10 mwa",
                       "2018-04-27 00:00:00", "Rékolté")
        testExtract_gcf("pwen 6a: adan 10 mwa",
                       "2018-04-27 06:00:00", "pwen")
        testExtract_gcf("aprémidi-là démissionné à 4:59",
                       "2017-06-27 16:59:00", "démisionné")
        testExtract_gcf("lannuit-lasa dòmi",
                       "2017-06-27 02:00:00", "dòmi")
        testExtract_gcf("Ranjé biwo-ay à 17:00 è",
                       "2017-06-27 17:00:00", "Ranjé biwo-ay")

        testExtractDate2_gcf("Ranjé kontra-là 2 simenn apré lendi",
                            "2017-07-17 00:00:00", "ranjé Kontra")
        testExtractDate2_gcf("Achté-w tiwen imouw à 15h",
                            "2017-07-01 15:00:00", "achté-w imouw")
        # Disabling test until Guadeloupean Creole Extract-date incorporates the fixes for
        # UTC / Local timezones.  Until then this test fails periodically
        # whenever test is run and the date in the local timezone (where the
        # test is being run) is a different than the date in UTC.
        #
        # testExtractNoDate_gcf("pé jòd-là",
        #                   datetime.now().strftime("%Y-%m-%d") + " 00:00:00",
        #                   "pé")
        self.assertEqual(extract_datetime("", lang="fr-gcf"), None)
        self.assertEqual(extract_datetime("fwaz initil", lang="fr-gcf"),
                         None)
        self.assertEqual(extract_datetime(
            "Aprann konté à 37 è", lang="fr-gcf"), None)

    def test_extractdatetime_default_gcf(self):
        default = time(9, 0, 0)
        anchor = datetime(2017, 6, 27, 0, 0)
        res = extract_datetime("fè sé plantasyon-là 3ème jou à maws",
                               anchor, lang='fr-gcf', default_time=default)
        self.assertEqual(default, res[0].time())

    def test_extract_duration_gcf(self):
        self.assertEqual(extract_duration("10 sègond", lang="fr-gcf"),
                         (timedelta(seconds=10.0), ""))
        self.assertEqual(extract_duration("5 minit", lang="fr-gcf"),
                         (timedelta(minutes=5), ""))
        self.assertEqual(extract_duration("2 zè", lang="fr-gcf"),
                         (timedelta(hours=2), ""))
        self.assertEqual(extract_duration("3 jou", lang="fr-gcf"),
                         (timedelta(days=3), ""))
        self.assertEqual(extract_duration("25 simenn", lang="fr-gcf"),
                         (timedelta(weeks=25), ""))
        # No conversion for work to number yet for gcf
        self.assertEqual(extract_duration("sétè"),
                         (timedelta(hours=7), ""))
        self.assertEqual(extract_duration("7.5 sègond", lang="fr-gcf"),
                         (timedelta(seconds=7.5), ""))
        self.assertEqual(extract_duration("5 jou é ventnèf sègond"),
                         (timedelta(days=5, seconds=29), "é"))
        # Fraction not yet implemented
        #self.assertEqual(extract_duration("huit jou é dèmi é trante-nèf sègond"),
        #                 (timedelta(days=8.5, seconds=39), "é "))
        self.assertEqual(extract_duration("démaré on minitè pou 30 minit", lang="fr-gcf"),
                         (timedelta(minutes=30), "démaré 1 minitè pou"))
        #self.assertEqual(extract_duration("Kat minit é dèmi avan couché à soley-là"),
        #                 (timedelta(minutes=4.5), "avan couché à soley-là"))
        self.assertEqual(extract_duration("Inè diznèf minit"),
                         (timedelta(hours=1, minutes=19), ""))
        self.assertEqual(extract_duration("Lévé-mwen adan 3 simenn, "
                                          " 497 jou é"
                                          " 391.6 sègond", lang="fr-gcf"),
                         (timedelta(weeks=3, days=497, seconds=391.6),
                          "Lévé-mwen adan  é"))
        self.assertEqual(extract_duration("Film-là ka diré inè-d-tan, senkantsèt minit"),
                         (timedelta(hours=1, minutes=57),
                             "film-là diré"))
        self.assertEqual(extract_duration("10-secondes", lang="fr-gcf"),
                         (timedelta(seconds=10.0), ""))
        self.assertEqual(extract_duration("5-minit", lang="fr-gcf"),
                         (timedelta(minutes=5), ""))

    def test_spaces_gcf(self):
        self.assertEqual(normalize("  sé test-là", lang="fr-gcf"),
                         "sé test")
        self.assertEqual(normalize("  sé test-là ", lang="fr-gcf"),
                         "sé test")
        self.assertEqual(normalize("  sé on test", lang="fr-gcf"),
                         "sé 1 test")

    def test_numbers_gcf(self):
        self.assertEqual(normalize("sé yonn dé twa  test",
                                   lang="fr-gcf"),
                         "sé 1 2 3 test")
        self.assertEqual(normalize(" sé kat senk sis  test-là",
                                   lang="fr-gcf"),
                         "sé 4 5 6 test")
        self.assertEqual(normalize("sé sèt huit nèf test-là",
                                   lang="fr-gcf"),
                         "sé 7 8 9 test")
        self.assertEqual(normalize("sé sèt huit nèf test-là",
                                   lang="fr-gcf"),
                         "sé 7 8 9 test")
        self.assertEqual(normalize("mi test dix onze douze-là",
                                   lang="fr-gcf"),
                         "mi test 10 11 12")
        self.assertEqual(normalize("mi trèz katorz test-là",
                                   lang="fr-gcf"),
                         "mi 13 14 test-là")
        self.assertEqual(normalize("sa ka fè kenz sèz disèt",
                                   lang="fr-gcf"),
                         "sa ka fè 15 16 17")
        self.assertEqual(normalize("sa ka fè dizuit diznèf ven",
                                   lang="fr-gcf"),
                         "sa ka fè 18 19 20")
        self.assertEqual(normalize("sa ka fè mil senk san",
                                   lang="fr-gcf"),
                         "sa ka fè 1500")
        self.assertEqual(normalize("mi senk san trant é yun mil éwo",
                                   lang="fr-gcf"),
                         "mi 531000 éwo")
        self.assertEqual(normalize("mi twa san swasant mil senk"
                                   " san katrèven-dizuit éwo",
                                   lang="fr-gcf"),
                         "mi 360598 euros")
        self.assertEqual(normalize("mi ventéyun éwo", lang="fr-gcf"),
                         "voilà 21 euros")
        self.assertEqual(normalize("bèl zéwo si ven", lang="fr-gcf"),
                         "bèl 0 si 20")
        self.assertEqual(normalize("an vlé on kat-kaw", lang="fr-gcf"),
                         "an vlé kat-kaw")
        self.assertEqual(normalize("pou nèf santièm fwa-là ", lang="fr-gcf"),
                         "pou 900e fwa")
        self.assertEqual(normalize("pou pwèmyé fwa", lang="fr-gcf"),
                         "pou 1er fwa")
        self.assertEqual(normalize("nèf san katrèven-dis"
                                   " millienm épizòd", lang="fr-gcf"),
                         "990000e épizòd")
        self.assertEqual(normalize("sétyèm clé-là", lang="fr-gcf"),
                         "7e clé-là")
        self.assertEqual(normalize("névyèm pòt-là", lang="fr-gcf"),
                         "9e pòt-là")
        self.assertEqual(normalize("senkyèm jou", lang="fr-gcf"),
                         "5e jou")
        self.assertEqual(normalize("le trois-cents-soixante-cinquième jour",
                                   lang="fr-fr"),
                         "365e jour")
        self.assertEqual(normalize("1ère fwa", lang="fr-gcf"),
                         "1er fois")
        self.assertEqual(normalize("santyèm santim-là", lang="fr-gcf"),
                         "100e santim")
        self.assertEqual(normalize(" millièm millézim", lang="fr-gcf"),
                         "1000e millésime")
        self.assertEqual(normalize("le trentième anniversaire", lang="fr-gcf"),
                         "30e anivewsè")

    # TODO function not localized
    def test_gender_gcf(self):
        #        self.assertEqual(get_gender("moun", lang="fr-gcf"),
        #                         None)
        self.assertRaises(FunctionNotLocalizedError,
                          get_gender, "moun", lang="fr-gcf")


if __name__ == "__main__":
    unittest.main()
