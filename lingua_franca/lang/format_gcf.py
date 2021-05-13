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
from lingua_franca.lang.format_common import convert_to_mixed_fraction
from lingua_franca.lang.common_data_gcf import _NUM_STRING_GCF, \
    _FRACTION_STRING_GCF


def nice_number_gcf(number, speech=True, denominators=range(1, 21)):
    """ French helper for nice_number
    This function formats a float to human understandable functions. Like
    4.5 becomes "4 et demi" for speech and "4 1/2" for text
    Args:
        number (int or float): the float to format
        speech (bool): format for speech (True) or display (False)
        denominators (iter of ints): denominators to use, default [1 .. 20]
    Returns:
        (str): The formatted string.
    """
    strNumber = ""
    whole = 0
    num = 0
    den = 0

    result = convert_to_mixed_fraction(number, denominators)

    if not result:
        # Give up, just represent as a 3 decimal number
        whole = round(number, 3)
    else:
        whole, num, den = result

    if not speech:
        if num == 0:
            strNumber = '{:,}'.format(whole)
            strNumber = strNumber.replace(",", " ")
            strNumber = strNumber.replace(".", ",")
            return strNumber
        else:
            return '{} {}/{}'.format(whole, num, den)
    else:
        if num == 0:
            # if the number is not a fraction, nothing to do
            strNumber = str(whole)
            strNumber = strNumber.replace(".", ",")
            return strNumber
        den_str = _FRACTION_STRING_GCF[den]
        # if it is not an integer
        if whole == 0:
            # if there is no whole number
            if num == 1:
                # if numerator is 1, return "on dèmi", for example
                strNumber = 'un {}'.format(den_str)
            else:
                # else return "kat-tyèw", for example
                strNumber = '{} {}'.format(num, den_str)
        elif num == 1:
            # if there is a whole number and numerator is 1
            if den == 2:
                # if denominator is 2, return "1 é dèmi", for example
                strNumber = '{} et {}'.format(whole, den_str)
            else:
                # else return "1 é 1 tièw", for example
                strNumber = '{} et 1 {}'.format(whole, den_str)
        else:
            # else return "2 é 3 kaw", for example
            strNumber = '{} et {} {}'.format(whole, num, den_str)

    return strNumber


def pronounce_number_gcf(number, places=2):
    """
    Convert a number to it's spoken equivalent
    For example, '5.2' would return 'senk virgil dé'
    Args:
        num(float or int): the number to pronounce (under 100)
        places(int): maximum decimal places to speak
    Returns:
        (str): The pronounced number
    """
    if abs(number) >= 100:
        # TODO: Support for numbers over 100
        return str(number)

    result = ""
    if number < 0:
        result = "mwen "
    number = abs(number)

    if number > 16:
        tens = int(number-int(number) % 10)
        ones = int(number-tens)
        if ones != 0:
            if tens > 10 and tens <= 60 and int(number-tens) == 1:
                result += _NUM_STRING_GCF[tens] + "-et-" + _NUM_STRING_GCF[ones]
            elif number == 71:
                result += "swasant-é-yonz"
            elif tens == 70:
                result += _NUM_STRING_GCF[60] + "-"
                if ones < 7:
                    result += _NUM_STRING_GCF[10 + ones]
                else:
                    result += _NUM_STRING_GCF[10] + "-" + _NUM_STRING_GCF[ones]
            elif tens == 90:
                result += _NUM_STRING_GCF[80] + "-"
                if ones < 7:
                    result += _NUM_STRING_GCF[10 + ones]
                else:
                    result += _NUM_STRING_GCF[10] + "-" + _NUM_STRING_GCF[ones]
            else:
                result += _NUM_STRING_GCF[tens] + "-" + _NUM_STRING_GCF[ones]
        else:
            if number == 80:
                result += "katrèven"
            else:
                result += _NUM_STRING_GCF[tens]
    else:
        result += _NUM_STRING_GCF[int(number)]

    # Deal with decimal part
    if not number == int(number) and places > 0:
        if abs(number) < 1.0 and (result == "mwen " or not result):
            result += "zéro"
        result += " virgil"
        _num_str = str(number)
        _num_str = _num_str.split(".")[1][0:places]
        for char in _num_str:
            result += " " + _NUM_STRING_GCF[int(char)]
    return result


def nice_time_gcf(dt, speech=True, use_24hour=False, use_ampm=False):
    """
    Format a time to a comfortable human format
    For example, generate 'cinq heures trente' for speech or '5:30' for
    text display.
    Args:
        dt (datetime): date to format (assumes already in local timezone)
        speech (bool): format for speech (default/True) or display (False)=Fal
        use_24hour (bool): output in 24-hour/military or 12-hour format
        use_ampm (bool): include the am/pm for 12-hour format
    Returns:
        (str): The formatted time string
    """
    if use_24hour:
        # e.g. "03:01" or "14:22"
        string = dt.strftime("%H:%M")
    else:
        if use_ampm:
            # e.g. "3:01 AM" or "2:22 PM"
            string = dt.strftime("%I:%M %p")
        else:
            # e.g. "3:01" or "2:22"
            string = dt.strftime("%I:%M")
        if string[0] == '0':
            string = string[1:]  # strip leading zeros

    if not speech:
        return string

    # Generate a speakable version of the time
    speak = ""
    if use_24hour:

        # "13 é trante"
        if dt.hour == 0:
            speak += "minwi"
        elif dt.hour == 12:
            speak += "midi"
        elif dt.hour == 1:
            speak += "inè"
        else:
            speak += pronounce_number_gcf(dt.hour) + " è"

        if dt.minute != 0:
            speak += " " + pronounce_number_gcf(dt.minute)

    else:
        # Prepare for "twa zè mwen-l-ka "
        if dt.minute == 35:
            minute = -25
            hour = dt.hour + 1
        elif dt.minute == 40:
            minute = -20
            hour = dt.hour + 1
        elif dt.minute == 45:
            minute = -15
            hour = dt.hour + 1
        elif dt.minute == 50:
            minute = -10
            hour = dt.hour + 1
        elif dt.minute == 55:
            minute = -5
            hour = dt.hour + 1
        else:
            minute = dt.minute
            hour = dt.hour

        if hour == 0:
            speak += "minwi"
        elif hour == 12:
            speak += "midi"
        elif hour == 1 or hour == 13:
            speak += "inè"
        elif hour < 13:
            speak = pronounce_number_fr(hour) + " è"
        else:
            speak = pronounce_number_fr(hour-12) + " è"

        if minute != 0:
            if minute == 15:
                speak += " é ka"
            elif minute == 30:
                speak += " é dèmi"
            elif minute == -15:
                speak += " mwen-l-ka"
            else:
                speak += " " + pronounce_number_gcf(minute)

        if use_ampm:
            if hour > 17:
                speak += " d-swa"
            elif hour > 12:
                speak += " dè lapré-midi"
            elif hour > 0 and hour < 12:
                speak += " d-maten"

    return speak
