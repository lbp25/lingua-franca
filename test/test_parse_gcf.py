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
        testExtract_gcf("Dékalé saà 3h48min cet après-midi",
                       "2017-06-27 15:48:00", "décale donc ça")
        testExtract_gcf("construire un bunker à 9h42min du matin",
                       "2017-06-27 09:42:00", "construire 1 bunker")
        testExtract_gcf("ou plutôt à 9h43 ce matin",
                       "2017-06-27 09:43:00", "ou plutôt")
        testExtract_gcf("faire un feu à 8h du soir",
                       "2017-06-27 20:00:00", "faire 1 feu")
        testExtract_gcf("faire la fête jusqu'à 18h cette nuit",
                       "2017-06-27 18:00:00", "faire fête jusqu'à")
        testExtract_gcf("cuver jusqu'à 4h cette nuit",
                       "2017-06-27 04:00:00", "cuver jusqu'à")
        testExtract_gcf("réveille-moi dans 20 secondes aujourd'hui",
                       "2017-06-27 00:00:20", "réveille-moi")
        testExtract_gcf("réveille-moi dans 33 minutes",
                       "2017-06-27 00:33:00", "réveille-moi")
        testExtract_gcf("tais-toi dans 12 heures et 3 minutes",
                       "2017-06-27 12:03:00", "tais-toi")
        testExtract_gcf("ouvre-la dans 1 heure 3",
                       "2017-06-27 01:03:00", "ouvre-la")
        testExtract_gcf("ferme-la dans 1 heure et quart",
                       "2017-06-27 01:15:00", "ferme-la")
        testExtract_gcf("scelle-la dans 1 heure et demi",
                       "2017-06-27 01:30:00", "scelle-la")
        testExtract_gcf("zippe-la dans 2 heures moins 12",
                       "2017-06-27 01:48:00", "zippe-la")
        testExtract_gcf("soude-la dans 3 heures moins le quart",
                       "2017-06-27 02:45:00", "soude-la")
        testExtract_gcf("mange la semaine prochaine",
                       "2017-07-04 00:00:00", "mange")
        testExtract_gcf("bois la semaine dernière",
                       "2017-06-20 00:00:00", "bois")
        testExtract_gcf("mange le mois prochain",
                       "2017-07-27 00:00:00", "mange")
        testExtract_gcf("bois le mois dernier",
                       "2017-05-27 00:00:00", "bois")
        testExtract_gcf("mange l'an prochain",
                       "2018-06-27 00:00:00", "mange")
        testExtract_gcf("bois l'année dernière",
                       "2016-06-27 00:00:00", "bois")
        testExtract_gcf("reviens à lundi dernier",
                       "2017-06-26 00:00:00", "reviens")
        testExtract_gcf("capitule le 8 mai 1945",
                       "1945-05-08 00:00:00", "capitule")
        testExtract_gcf("rédige le contrat 3 jours après jeudi prochain",
                       "2017-07-09 00:00:00", "rédige contrat")
        testExtract_gcf("signe le contrat 2 semaines après jeudi dernier",
                       "2017-07-06 00:00:00", "signe contrat")
        testExtract_gcf("lance le four dans un quart d'heure",
                       "2017-06-27 00:15:00", "lance four")
        testExtract_gcf("enfourne la pizza dans une demi-heure",
                       "2017-06-27 00:30:00", "enfourne pizza")
        testExtract_gcf("arrête le four dans trois quarts d'heure",
                       "2017-06-27 00:45:00", "arrête four")
        testExtract_gcf("mange la pizza dans une heure",
                       "2017-06-27 01:00:00", "mange pizza")
        testExtract_gcf("bois la bière dans 2h23",
                       "2017-06-27 02:23:00", "bois bière")
        testExtract_gcf("faire les plantations le 3ème jour de mars",
                       "2018-03-03 00:00:00", "faire plantations")
        testExtract_gcf("récolter dans 10 mois",
                       "2018-04-27 00:00:00", "récolter")
        testExtract_gcf("point 6a: dans 10 mois",
                       "2018-04-27 06:00:00", "point")
        testExtract_gcf("l'après-midi démissionner à 4:59",
                       "2017-06-27 16:59:00", "démissionner")
        testExtract_gcf("cette nuit dormir",
                       "2017-06-27 02:00:00", "dormir")
        testExtract_gcf("ranger son bureau à 1700 heures",
                       "2017-06-27 17:00:00", "ranger son bureau")

        testExtractDate2_gcf("range le contrat 2 semaines après lundi",
                            "2017-07-17 00:00:00", "range contrat")
        testExtractDate2_gcf("achète-toi de l'humour à 15h",
                            "2017-07-01 15:00:00", "achète-toi humour")
        # Disabling test until French Extract-date incorporates the fixes for
        # UTC / Local timezones.  Until then this test fails periodically
        # whenever test is run and the date in the local timezone (where the
        # test is being run) is a different than the date in UTC.
        #
        # testExtractNoDate_fr("tais-toi aujourd'hui",
        #                   datetime.now().strftime("%Y-%m-%d") + " 00:00:00",
        #                   "tais-toi")
        self.assertEqual(extract_datetime("", lang="fr-fr"), None)
        self.assertEqual(extract_datetime("phrase inutile", lang="fr-fr"),
                         None)
        self.assertEqual(extract_datetime(
            "apprendre à compter à 37 heures", lang="fr-fr"), None)

    def test_extractdatetime_default_fr(self):
        default = time(9, 0, 0)
        anchor = datetime(2017, 6, 27, 0, 0)
        res = extract_datetime("faire les plantations le 3ème jour de mars",
                               anchor, lang='fr-fr', default_time=default)
        self.assertEqual(default, res[0].time())

    def test_extract_duration_fr(self):
        self.assertEqual(extract_duration("10 secondes", lang="fr-fr"),
                         (timedelta(seconds=10.0), ""))
        self.assertEqual(extract_duration("5 minutes", lang="fr-fr"),
                         (timedelta(minutes=5), ""))
        self.assertEqual(extract_duration("2 heures", lang="fr-fr"),
                         (timedelta(hours=2), ""))
        self.assertEqual(extract_duration("3 jours", lang="fr-fr"),
                         (timedelta(days=3), ""))
        self.assertEqual(extract_duration("25 semaines", lang="fr-fr"),
                         (timedelta(weeks=25), ""))
        # No conversion for work to number yet for fr
        self.assertEqual(extract_duration("sept heures"),
                         (timedelta(hours=7), ""))
        self.assertEqual(extract_duration("7.5 secondes", lang="fr-fr"),
                         (timedelta(seconds=7.5), ""))
        self.assertEqual(extract_duration("5 jours et vingt-neuf secondes"),
                         (timedelta(days=5, seconds=29), "et"))
        # Fraction not yet implemented
        #self.assertEqual(extract_duration("huit jours et demi et trente-neuf secondes"),
        #                 (timedelta(days=8.5, seconds=39), "et "))
        self.assertEqual(extract_duration("démarre un minuteur pour 30 minutes", lang="fr-fr"),
                         (timedelta(minutes=30), "démarre 1 minuteur pour"))
        #self.assertEqual(extract_duration("Quatre minutes et demi avant le coucher du soleil"),
        #                 (timedelta(minutes=4.5), "avant le coucher du soleil"))
        self.assertEqual(extract_duration("Une heure dix-neuf minutes"),
                         (timedelta(hours=1, minutes=19), ""))
        self.assertEqual(extract_duration("réveille moi dans 3 semaines, "
                                          " 497 jours et"
                                          " 391.6 secondes", lang="fr-fr"),
                         (timedelta(weeks=3, days=497, seconds=391.6),
                          "réveille moi dans  et"))
        self.assertEqual(extract_duration("Le film dure une heure, cinquante-sept minutes"),
                         (timedelta(hours=1, minutes=57),
                             "film dure"))
        self.assertEqual(extract_duration("10-secondes", lang="fr-fr"),
                         (timedelta(seconds=10.0), ""))
        self.assertEqual(extract_duration("5-minutes", lang="fr-fr"),
                         (timedelta(minutes=5), ""))

    def test_spaces_fr(self):
        self.assertEqual(normalize("  c'est   le     test", lang="fr-fr"),
                         "c'est test")
        self.assertEqual(normalize("  c'est  le    test  ", lang="fr-fr"),
                         "c'est test")
        self.assertEqual(normalize("  c'est     un    test", lang="fr-fr"),
                         "c'est 1 test")

    def test_numbers_fr(self):
        self.assertEqual(normalize("c'est un deux trois  test",
                                   lang="fr-fr"),
                         "c'est 1 2 3 test")
        self.assertEqual(normalize("  c'est  le quatre cinq six  test",
                                   lang="fr-fr"),
                         "c'est 4 5 6 test")
        self.assertEqual(normalize("c'est  le sept huit neuf test",
                                   lang="fr-fr"),
                         "c'est 7 8 9 test")
        self.assertEqual(normalize("c'est le sept huit neuf  test",
                                   lang="fr-fr"),
                         "c'est 7 8 9 test")
        self.assertEqual(normalize("voilà le test dix onze douze",
                                   lang="fr-fr"),
                         "voilà test 10 11 12")
        self.assertEqual(normalize("voilà le treize quatorze test",
                                   lang="fr-fr"),
                         "voilà 13 14 test")
        self.assertEqual(normalize("ça fait quinze seize dix-sept",
                                   lang="fr-fr"),
                         "ça fait 15 16 17")
        self.assertEqual(normalize("ça fait dix-huit dix-neuf vingt",
                                   lang="fr-fr"),
                         "ça fait 18 19 20")
        self.assertEqual(normalize("ça fait mille cinq cents",
                                   lang="fr-fr"),
                         "ça fait 1500")
        self.assertEqual(normalize("voilà cinq cents trente et un mille euros",
                                   lang="fr-fr"),
                         "voilà 531000 euros")
        self.assertEqual(normalize("voilà trois cents soixante mille cinq"
                                   " cents quatre-vingt-dix-huit euros",
                                   lang="fr-fr"),
                         "voilà 360598 euros")
        self.assertEqual(normalize("voilà vingt et un euros", lang="fr-fr"),
                         "voilà 21 euros")
        self.assertEqual(normalize("joli zéro sur vingt", lang="fr-fr"),
                         "joli 0 sur 20")
        self.assertEqual(normalize("je veux du quatre-quart", lang="fr-fr"),
                         "je veux quatre-quart")
        self.assertEqual(normalize("pour la neuf centième fois", lang="fr-fr"),
                         "pour 900e fois")
        self.assertEqual(normalize("pour la première fois", lang="fr-fr"),
                         "pour 1er fois")
        self.assertEqual(normalize("le neuf cents quatre-vingt-dix"
                                   " millième épisode", lang="fr-fr"),
                         "990000e épisode")
        self.assertEqual(normalize("la septième clé", lang="fr-fr"),
                         "7e clé")
        self.assertEqual(normalize("la neuvième porte", lang="fr-fr"),
                         "9e porte")
        self.assertEqual(normalize("le cinquième jour", lang="fr-fr"),
                         "5e jour")
        self.assertEqual(normalize("le trois-cents-soixante-cinquième jour",
                                   lang="fr-fr"),
                         "365e jour")
        self.assertEqual(normalize("la 1ère fois", lang="fr-fr"),
                         "1er fois")
        self.assertEqual(normalize("le centième centime", lang="fr-fr"),
                         "100e centime")
        self.assertEqual(normalize("le millième millésime", lang="fr-fr"),
                         "1000e millésime")
        self.assertEqual(normalize("le trentième anniversaire", lang="fr-fr"),
                         "30e anniversaire")

    # TODO function not localized
    def test_gender_fr(self):
        #        self.assertEqual(get_gender("personne", lang="fr-fr"),
        #                         None)
        self.assertRaises(FunctionNotLocalizedError,
                          get_gender, "personne", lang="fr-fr")


if __name__ == "__main__":
    unittest.main()
