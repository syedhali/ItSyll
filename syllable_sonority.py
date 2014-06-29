# This program is designed to take a string of Italian poetry as input and return that string with its syllables marked.
# It is based on the program Sylli written by Luca Iacoponi, with slight modifications to account for peculiarities
# in poetic language, such as strange word morphologies, apostrophes, etc.

# The syllabification process uses the very simple and elegant Sonority Scale to determine the phonetic equivalent of
# syllabic boundaries. Thus the sound of the letters are used to determine the division of the word, rather than a
# brute force, rule-based program that relies on dividing a word into consonants and vowels.

# The values of the Sonority Scale can be found in sonorityfile.txt. These values were taken from the masters thesis of
# Luca Iacoponi, "Dividing CLIPS' Phonemic Layer into Syllables: An SPP Based Syllabification Program with Python/NLTK."

# The thesis can be found here:
# http://eden.rutgers.edu/~li51/php/papers/iacoponi2011clipssyllabification.pdf
#
# He in turn modified the values and algorithm originally created by:
# Cutugno, F., Passaro, G. & Petrillo, M., 2001. Sillabificazione fonologica e sillabificazione fonetica.
#   Dans Atti del XXXIII, Congresso della Società di Linguistica Italiana, Bulzoni Roma. pp. 205–232.


# To begin with, we need an object for each letter that is capable of retaining information regarding natural class
# and sonority level. Each letter is to be assigned it's phonetic equivalent (e.g. "c" -> "k"), it's sonority value,
# and it's natural class. Classes are V-owels, G-lides, S-onorants, N-asals, F-ricatives, A-ffricates, O-cclusives.
# There is also the property 'pclass' which simply returns C or V depending on the letter's status as a vowel
# or a consonant.

import configparser
import re

class WeightedLetter:
    def __init__(self, properties):
        try:
            self.original = properties[0].strip()
            self.phonetic = properties[1].strip()
            self.son = int(properties[2].strip())
            self.pclass = properties[3].strip()
        except IndexError:
            print("Sonority Error")
        if self.pclass == 'V':
            self.cvcv = 'V'
        else:
            self.cvcv = 'C'

class Phrase:

    def __init__(self, phrase):
            self.sentence = (phrase.split())
            self.nopunct = (''.join(re.split('\W', str(self.sentence))))
            self.syllphrase = ''

    def fetch_lexicon(self, input_string):
        config = configparser.ConfigParser()
        config.read("sonorityfile.txt")
        try:
            value = config.get("Segments", input_string)
            if value != None:
                return input_string + ", " + value
            else:
                return False
        except Exception:
            return False

    def Transpose(self, input_string):
        ph_sequence = []
        for segment in input_string:
            if self.fetch_lexicon(segment):
                letter = (self.fetch_lexicon(segment))
                ph_sequence.append(WeightedLetter(letter.split(',')))
            else:
                letter = (WeightedLetter([str(segment), '0', '0', '0']))
                ph_sequence.append(letter)
        return ph_sequence

    def Syllabify(self, sequence):
        phrase = [sequence[0].original]
        null_segment = WeightedLetter(['0', '0', '0', '0'])
        sequence.append(null_segment)
        len_sequence = len(sequence)
        for i in range(1, len_sequence - 1):
# If the current sound does not have any sonority (meaning that it is probably punctuation),
# then it should assume the sonority of the preceding letter. Thus, when the loop iterates to
# the next letter, it will compare this value, rather than a value of 0.
            if (sequence[i].son == 0):
                sequence[i].son = sequence[i-1].son
                phrase.append(sequence[i].original)
# If the subsequent character is an apostrophe, its sonority value should equal that of the
# following character.
            elif (sequence[i+1].phonetic == "'" and sequence[i+2].pclass == "V"):
                sequence[i+1].son = sequence[i+2].son
                if (sequence[i-1].son > sequence[i].son and \
                sequence[i+1].son > sequence[i].son) or \
                    (sequence[i-1].son == sequence[i].son and \
                    sequence[i].cvcv != "V"):
                    phrase.append('|')
                    phrase.append(sequence[i].original)
                else:
                    phrase.append(sequence[i].original)
# Always separate A-E
            else:
                if (sequence[i].phonetic == "e") and \
                (sequence[i-1].phonetic == "a"):
                    phrase.append('|')
                    phrase.append(sequence[i].original)
# If there is Dieresis (i.e. the vowels are split up), the first will typically be marked
# with an umlaut. In the sonority file these will be marked as pclass "D." Automatically
# please a syllable boundary.
                elif (sequence[i].pclass == "D"):
                    phrase.append(sequence[i].original)
                    phrase.append('|')
# This is the basic algorithm. If the sonority value of the character under analysis is
# less than both the preceding character and the following character, then it is a sonority
# minimum, and it is therefore a syllable boundary. Alternatively, if its sonority value is
# the same as the previous character's and it is not a vowel, then it is a syllable boundary.
# This is to check for double consonants such as in the word "bello."
                elif (sequence[i-1].son > sequence[i].son  and \
                    sequence[i+1].son > sequence[i].son) or \
                    (sequence[i-1].son == sequence[i].son and \
                    sequence[i].cvcv != "V"):
                        phrase.append('|')
                        phrase.append(sequence[i].original)
                else:
                    phrase.append(sequence[i].original)
        return ''.join(phrase)

    def WordBoundaries(self, sequence):
        output = []
        sequence.append("#")
        for i in range(0, len(sequence) - 1):
# If the last letter of a word is not alphanumeric, take the letter before that. This is to avoid
# counting apostrophes, commas, or other punctuation.
            if (sequence[i][-1].isalpha()):
                lastlett = sequence[i][-1]
            else:
                lastlett = sequence[i][-2]
# If the last letter of a word is a vowel, and the following word begins with a vowel or an H,
# then no syllable boundary is placed, due to elision.
            if (self.is_Vowel(lastlett) == True) and (self.is_Vowel(sequence[i+1][0]) == True) or \
            (sequence[i+1] == "#"):
                output.append(sequence[i])
            elif (sequence[i+1][0].isalpha() == False):
                output.append(sequence[i])
# Otherwise, between two consonants, or a vowel and a consonant, a syllable boundary is placed.
            else:
                sequence[i] = sequence[i] + " |"
                output.append(sequence[i])
        return output


    def is_Vowel(self, segment):
        if segment.lower() in "aeiouàèéìíòùh":
            return True
        else:
            return False


    def Syllables(self):
        output = []
        phrase = self.sentence
        for word in phrase:
            output.append(self.Syllabify(self.Transpose(word)))
        output = self.WordBoundaries((output))
        self.syllphrase = ' '.join((output))
        return self.syllphrase


    def SyllCount(self):
        return len(self.syllphrase.split("|"))


def file_syllable(file):
    data = open(file, "r").readlines()
    newline = []
    for line in data:
        if len(line) > 1:
            newline = (Phrase(line))
            print(newline.Syllables(), " ", newline.SyllCount())
        else:
            print("")

file_syllable("aminta.txt")
