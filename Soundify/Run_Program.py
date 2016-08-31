import os
from Sonify_Data.Make_MIDI import Convert_To_Music
from Play_Soundify.Player import play
import time

#octaves = input('Which octaves would you like the data to span?')

#data set source
dataset_source = '/Users/BenLovell/Documents/UnanimousAI/Data/BernieMeme/Excel_Data/Data_Per_Choice.csv'

#single dataset number
#PUT "Incomplete" TO HAVE THE LAST 6 NOTES REMOVED
# PUT "Word Document" if looking at a text file
dataset = 0


#multiple datasets, make sure ALL DATASETS are equal in length
#WRITE IN AS INTEGER OF DATASET
#dataset1 is used for volume/duration mapping
dataset1 = 'The Candidate of the People'
dataset2 = 'The Mile-High Socialist Club'
dataset3 = 'Do they serve Trump Steak on this flight?'
dataset4 = 'Of the people... for the people!'
dataset5 = 'Nobody would give Bernie an aisle seat?'
dataset6 = 'Is that a high-school varsity jacket?'

separate = False


#LIVE DATASET (same parameters as single dataset), insert number for frequency in seconds
livedata = 0
frequency = 2

#time between notes
#single number or dataset for note length
#DO NOT USE DATASET FOR LIVEDATA YET
duration = .25

#how loud a note is played
#single integer (between 1 - 127) or dataset for note volume
# when marking GROUPED under MAPPING, this variable will be ignored and volume will automatically be set normalized to the entire dataset
volume = 100

#select which octaves to map the data within
#0 = bottom-most octave on piano, 6 = top-most octave
octaves = [0,1,2,3,4,5,6,7]

#map the data by either normalizing the whole set 'normalized' OR
# map the data in relation to the median of the dataset 'median' OR
# wrap the dataset around the median value (alternating left and right)
# add 'MM' to the front of a mapping to map the values going up to major, and down to minor
# add 'grouped' to front if mapping chords that don't need to be seperately normalized (but after 'MM' if included)
mapping = 'MMgroupedmedian'

#can be 'Full' for entire keyboard, or specific scale for shortened range
#currently able to do all major and minor keys (eg 'B Major)
scale = ['Full']

trackname = 'wtfffff'
output_location = '~/Code/Soundify/Play_Soundify/Outputs/'

#sc = HARMONIC_MINOR_SCALE
#scale = [x for x in buildScale(sc, 24, 108)]

output = output_location + trackname + '.wav '
sf2 = '~/Code/Soundify/Play_Soundify/Soundfonts/MotifES6ConcertPiano.sf2 '
midi = output_location + trackname + '.mid'
play_file = output_location + trackname + '.wav'



if dataset != 0:
    Convert_To_Music.convert_note_to_music(dataset, dataset_source, octaves, duration, volume, mapping, scale, trackname, output_location)
    play(os.path.expanduser(output), os.path.expanduser(sf2), os.path.expanduser(midi), os.path.expanduser(play_file))

elif dataset1 != 0:
    Convert_To_Music.convert_chord_to_music(dataset_source, dataset1, dataset2, dataset3, dataset4, dataset5, dataset6, separate, octaves, duration, volume, mapping, scale, trackname, output_location)
    play(os.path.expanduser(output), os.path.expanduser(sf2), os.path.expanduser(midi), os.path.expanduser(play_file))

elif livedata != 0:
    while True:
        Convert_To_Music.convert_live_to_music(livedata, dataset_source, frequency, octaves, duration, volume, mapping, scale, trackname, output_location)
        play(os.path.expanduser(output), os.path.expanduser(sf2), os.path.expanduser(midi), os.path.expanduser(play_file))
        time.sleep(frequency)