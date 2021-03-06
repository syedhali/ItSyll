# ItSyl

This program is designed to divide up Italian words into syllables. It uses a modified and reduced version of Luca Iacoponi's Sylli program, which itself uses the Sonority Scale as a basis for syllabification.

Ultimately, this will be part of a larger project to create a program capable of analyzing verses of Itlian poetry and providing important information, such as descriptions of meter, syllabification, and interesting syntactic or phonetic features.

## Example output

The current output of sonority_syllable.py is something like this:

```
Chi crederia che sotto umane forme
e sotto queste pastorali spoglie
fosse nascosto un Dio? non mica un Dio
selvaggio, o de la plebe de gli Dei,
ma tra' grandi e celesti il più potente,
che fa spesso cader di mano a Marte
la sanguinosa spada, ed a Nettuno
scotitor de la terra il gran tridente,
ed i folgori eterni al sommo Giove.


Chi | cre|de|ria | che | sot|to u|ma|ne | for|me   11
e | sot|to | que|ste | pa|sto|ra|li | spo|glie     11
fos|se | na|sco|sto un | Dio? | non | mi|ca un | Dio  10
sel|vag|gio, o | de | la | ple|be | de | gli | Dei,   10
ma | tra' | gran|di e | ce|le|sti il | più | po|ten|te, 11
che | fa | spes|so | ca|der | di | ma|no a | Mar|te   11
la | san|gui|no|sa | spa|da, ed | a | Net|tu|no       11
sco|ti|tor | de | la | ter|ra il | gran | tri|den|te,  11
ed | i | fol|go|ri e|ter|ni al | som|mo | Gio|ve.      11

```

## How it works

Each of the lines is divided into syllables according to Italian metrical rules. Beyond simply dividing up the syllables in words, there also need to be syllable boundaries between words. However, one of the most important aspects of poetic syllabization is that if there is a vowel at the end of one word and another at the beginning of the following word, then they should count as the same syllable. An example from above would be in the first line, "sot|to_u|ma|ne." Note that these vowels are not elided but are pronounced as discrete letters, even though they are counted together metrically. 

## Gotchas and Future Steps

Currently the major problem seems to be figuring out how to deal with diphthongs, or rather when words are NOT diphthongs and should be divided up, such as in the case of the second "Dio" in line 3. It seems that when a word that would normally be counted as a diphthong comes at the end of the line, it is possible to divide it into multiple syllables. 

First order of business needs to be a new set of functions that are capable of providing primary stress on words, and then determining whether or not that word falls at the end of the line.
