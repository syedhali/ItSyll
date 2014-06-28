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

# The following function opens up the sonority file and parses it using configparser. The file is organized as follows:

# [Segments]
# A = a, 26, V
#
# This is the information that will be stored in each weighted letter object, along with the original letter.
# Thus, fetch_lexicon("c") -> c, k, 1, O   // where 1 is the sonority value, and O stands for Occlusive
def fetch_lexicon(input_string):
    sonfile = "sonorityfile.txt"
    config = configparser.ConfigParser()
    config.read(sonfile)
    try:
        value = config.get("Segments", input_string)
        if value != None:
            return input_string + ", " + value
        else:
            return False
    except Exception:
        return False

# This function takes a single word as its input and returns a list of WeightedLetter objects for each letter in that word.
def input_transpose(input_string):
    ph_sequence = []
    input_string = list(input_string)
    for index, segment in enumerate(input_string):
        if fetch_lexicon(segment):
            letter = (fetch_lexicon(segment))
            ph_sequence.append(WeightedLetter(letter.split(',')))
    return ph_sequence

# This function takes as its input a list of WeightedLetter objects. It then determines syllable boundaries based on
# a sonority hierarchy. The output will be the original word with a '.' placed at each syllable boundary.
# Originally the boundaries list was used for something else, and I left it in in case I need to
# do something else with it later. 
def syllabify(sequence):
    boundaries = []

# Since the for loop begins on sequence[1], the final output phrase should begin with the first letter of the word.
    phrase = [sequence[0].original]
# A null segment is added to the end of the list to prevent any indexing errors.
    null_segment = WeightedLetter(['0', '0', '0', '0'])
    sequence.append(null_segment)
    len_sequence = len(sequence)
# The sonority hierarchy is incredibly simple. Syllable boundaries are marked based on sonority minimums. That is, place a 
# syllable boundary if either 1) the letter under analysis has a sonority value less than the preceding letter and less than the 
# following letter, or 2) the letter under analysis has the same sonority value as the preceding letter.
# i.e. if (x-1 > x < x+1) or (x-1 == x)  ---> boundary | x
# Each letter and boundary marker are then simply appended to the final output string.
    for i in range(1, len_sequence - 1):
            if (sequence[i-1].son > sequence[i].son  and \
            sequence[i+1].son > sequence[i].son) or \
            sequence[i-1].son == sequence[i].son:
                boundaries.append(i)
                phrase.append('.')
                phrase.append(sequence[i].original)
            else:
                phrase.append(sequence[i].original)
# Remove the null sequence before returning the string.
    sequence = sequence[:-1]
    return ''.join(phrase)


# This function is a rather rudimentary method for analyzing a sentence and returning that same sentence with syllables marked.
def syllable_sequencer(phrase):
    sequence = []
    final = []
    phrase = phrase.split()
    for word in phrase:
        sequence.append(input_transpose(word))
    for segment in sequence:
        final.append(syllabify(segment))
    return ' '.join(final)

# And lastly, a rudimentary function for reading a .txt file, reading and syllabizing each line, and then writing a new file.
def file_syllable(file):
    newfile = file.replace(".txt", "_syllables.txt")
    data = open(file, "r").readlines()
    with open(newfile, "w") as f:
        for line in data:
            print(syllable_sequencer(line))
            f.write(syllable_sequencer(line) + "\n")
    print("Done.")

file_syllable("petrarca2_wordlist.txt")
