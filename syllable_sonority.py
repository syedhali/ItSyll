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


def input_transpose(input_string):
    ph_sequence = []
    input_string = list(input_string)
    for index, segment in enumerate(input_string):
        if fetch_lexicon(segment):
            letter = (fetch_lexicon(segment))
            ph_sequence.append(WeightedLetter(letter.split(',')))
    return ph_sequence

def syllabify(sequence):
    boundaries = []
    phrase = [sequence[0].original]
    null_segment = WeightedLetter(['0', '0', '0', '0'])
    sequence.append(null_segment)
    len_sequence = len(sequence)
    for i in range(1, len_sequence - 1):
            if (sequence[i-1].son > sequence[i].son  and \
            sequence[i+1].son > sequence[i].son) or \
            sequence[i-1].son == sequence[i].son:
                boundaries.append(i)
                phrase.append('.')
                phrase.append(sequence[i].original)
            else:
                phrase.append(sequence[i].original)
    sequence = sequence[:-1]
    return ''.join(phrase)


def syllable_sequencer(phrase):
    sequence = []
    final = []
    phrase = phrase.split()
    for word in phrase:
        sequence.append(input_transpose(word))
    for segment in sequence:
        final.append(syllabify(segment))
    return ' '.join(final)

def file_syllable(file):
    newfile = file.replace(".txt", "_syllables.txt")
    data = open(file, "r").readlines()
    with open(newfile, "w") as f:
        for line in data:
            print(syllable_sequencer(line))
            f.write(syllable_sequencer(line) + "\n")
    print("Done.")

file_syllable("petrarca2_wordlist.txt")
