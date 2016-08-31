############################################################################
# A sample program to create a single-track MIDI file, add a note,
# and write to disk.
############################################################################

#Import the library
from Midi_Filemaker.MidiFile import MIDIFile
from Data_Mapping import Map_Data, Map_Live_Data
import numpy as np
import os
from Data import Get_Data, live_data

#CD stands for "Conversion Dependencies"
class CD(object):

    @staticmethod
    def normalizer_volume(arr):
        max_value = max(arr)
        min_value = min(arr)
        difference = max_value - min_value

        relator = []

        for n in arr:
            t = (n - min_value) / float(difference)
            relator.append(t)


        volume_mapper = []

        for n in relator:
            volume_mapper.append(int(abs(n * 70) + 57))

        return volume_mapper

    @staticmethod
    def normalizer_note_duration(arr):
        diff_array = abs(np.diff(arr))
        max_value = max(diff_array)
        min_value = min(diff_array)
        difference = max_value - min_value

        relator = []
        for n in diff_array:
            t = (n - min_value) / float((difference))
            relator.append(t)

        relator.insert(0, relator[0])


        note_duration_mapper = []
        for n in relator:
            note_duration_mapper.append(abs(n + .45))

        return note_duration_mapper

    @staticmethod
    def dur_checker(dataset_source, dataset, duration):

        if isinstance(duration, list) != True and isinstance(duration, str) != True:
            note_duration = []
            for x in dataset:
                note_duration.append(duration)
        elif isinstance(duration, str) == True:
                pull_data = Get_Data.datasets(dataset_source, duration)
                note_duration = CD.normalizer_note_duration(pull_data)
        else:
            note_duration = CD.normalizer_note_duration(duration)

        return note_duration

    @staticmethod
    def vol_checker(dataset, volume, mapping):

        if mapping[0:7] == 'grouped' or mapping[2:9] == 'grouped':
            combined_datasets = []
            for data_set in dataset:
                combined_datasets += data_set

            note_volume = CD.normalizer_volume(combined_datasets)

            return note_volume

        else:
            if isinstance(volume, list) != True:
                note_volume = []
                for x in dataset[0]:
                    note_volume.append(volume)
            else:
                note_volume = CD.normalizer_volume(volume)

            return note_volume


class Convert_To_Music():

    @staticmethod
    def convert_note_to_music(dataset, dataset_source, octaves, note_duration, note_volume, mapping, scale, trackname, output_location):
        # Create the MIDIFile Object
        MyMIDI = MIDIFile(1)
        # Add track name and tempo. The first argument to addTrackName and
        # addTempo is the time to write the event.
        track = 0
        time = 0
        MyMIDI.addTrackName(track,time,"Sample Track")
        MyMIDI.addTempo(track,time, 120)

        # this section notmalizes the arrays to MIDI notes
        n = Map_Data.note_mapping(dataset, Get_Data.datasets(dataset_source, dataset), octaves, scale, mapping)
        # this section maps and extends the volume
        v = iter(CD.vol_checker(n, note_volume))
        # this seciton maps and extends the note durations
        d = iter(CD.dur_checker(dataset_source, n, note_duration))


        #while time < length:
        for note, duration, volume in zip(n, d, v):
            MyMIDI.addNote(track,
                                channel =0,
                                pitch = note[0],
                                time = time,
                                duration = duration,
                                volume = volume)
            time += duration

        # And write it to disk.
        binfile = open(os.path.expanduser(output_location) + trackname + ".mid", 'wb')
        MyMIDI.writeFile(binfile)
        binfile.close()

    @staticmethod
    def convert_chord_to_music(dataset_source, dataset1, dataset2, dataset3, dataset4, dataset5, dataset6, separate, octaves, note_duration, note_volume, mapping, scale, trackname, output_location):
        # Create the MIDIFile Object
        MyMIDI = MIDIFile(1)

        # Add track name and tempo. The first argument to addTrackName and
        # addTempo is the time to write the event.
        track = 0
        time = 0
        MyMIDI.addTrackName(track,time,"Sample Track")
        MyMIDI.addTempo(track,time, 120)

        IorC = []
        sets = [dataset1, dataset2, dataset3, dataset4, dataset5, dataset6]
        for x in sets:
            if isinstance(x, str) == True:
                IorC.append(x[0:9])
            else:
                IorC.append(x)

        data_set1 = Get_Data.datasets(dataset_source, dataset1)
        data_set2 = Get_Data.datasets(dataset_source, dataset2)
        data_set3 = Get_Data.datasets(dataset_source, dataset3)
        data_set4 = Get_Data.datasets(dataset_source, dataset4)
        data_set5 = Get_Data.datasets(dataset_source, dataset5)
        data_set6 = Get_Data.datasets(dataset_source, dataset6)

        dataset_list = [data_set1, data_set2, data_set3, data_set4, data_set5, data_set6]

        dataset_counter = 0
        for d in dataset_list:
            if d != 0:
                dataset_counter += 1


        # this section notmalizes the arrays to MIDI notes
        n = Map_Data.chord_mapping(IorC, data_set1, data_set2, data_set3, data_set4, data_set5,data_set6, octaves, scale, mapping)
        # this section maps and extends the volume
        v = CD.vol_checker(dataset_list, note_volume, mapping)
        # this seciton maps and extends the note durations
        d = CD.dur_checker(dataset_source, data_set1, note_duration)

        # the chord mapping section requires a volume and duration for each individual data point
        # this section extends the volume and duration maps to match the number of notes total (not total chords)
        vol = []
        dur = []

        counter = 0
        for chord in n:
            dur.append(d[n.index(chord)])
            mid_vol = []
            for note in chord:
                mid_vol.append(v[counter])
                counter += 1
            vol.append(mid_vol)

        if separate == True:
            length = len(n)
            iteration = 0
            counter = 0
            splitter = []
            for x in xrange(dataset_counter):
                splitter.append([[], [], []])  #one array for note, duration and volume
            while iteration < length:
                notes = n[0]
                volumes = vol[0]
                for note, duration, volume in zip(notes, dur, volumes):
                    splitter[counter][0].append([note])
                    splitter[counter][1].append(duration)
                    splitter[counter][2].append(volume)
                    counter += 1

                del duration
                del vol[0]
                del n[0]
                iteration += 1
                counter = 0

            for split_song in splitter:

                n = split_song[0]
                d = split_song[1]
                v = split_song[2]

                MyMIDI = MIDIFile(1)
                # Add track name and tempo. The first argument to addTrackName and
                # addTempo is the time to write the event.
                track = 0
                time = 0
                MyMIDI.addTrackName(track,time,"Sample Track")
                MyMIDI.addTempo(track,time, 120)

                for note, duration, volume in zip(n, d, v):
                    MyMIDI.addNote(track,
                                channel =0,
                                pitch = note[0],
                                time = time,
                                duration = duration,
                                volume = volume)
                    time += duration

                # And write it to disk.
                binfile = open(os.path.expanduser(output_location) + str(sets[splitter.index(split_song)]) + ".mid", 'wb')
                MyMIDI.writeFile(binfile)
                binfile.close()


        else:
            # length is the sum of all note durations (chord not note)
            length = sum(dur)
            # continues program while the current note is less than the overall length of the song
            while time < length:
                # takes a segment of the dataset to make into a chord
                notes = n[0]
                volumes = vol[0]
                for note, duration, volume in zip(notes, dur, volumes):
                    MyMIDI.addNote(
                                track,
                                channel = 0,
                                pitch = note,
                                time = time,
                                duration = duration,
                                volume = volume)
                time += duration
                # removes chord and restarts on next portion
                dur.remove(duration)
                del vol[0]
                del n[0]
                if len(n) == 0:
                    time += duration


            # And write it to disk.
            binfile = open(os.path.expanduser(output_location) + trackname + ".mid", 'wb')
            MyMIDI.writeFile(binfile)
            binfile.close()

    @staticmethod
    def convert_live_to_music(dataset, dataset_source, frequency, octaves, note_duration, note_volume, mapping, scale, trackname, output_location):
        # Create the MIDIFile Object
        MyMIDI = MIDIFile(1)

        # Add track name and tempo. The first argument to addTrackName and
        # addTempo is the time to write the event.
        track = 0
        time = 0
        MyMIDI.addTrackName(track,time,"Sample Track")
        MyMIDI.addTempo(track,time, 120)

        # this section notmalizes the arrays to MIDI notes
        n = Map_Live_Data.live_mapping(live_data(dataset_source, dataset, frequency), octaves, scale)
        # this section maps and extends the volume
        v = iter(CD.vol_checker(n, note_volume))
        # this seciton maps and extends the note durations
        d = iter(CD.dur_checker(dataset_source, n, note_duration))


        #while time < length:
        for note, duration, volume in zip(n, d, v):
            MyMIDI.addNote(track,
                                channel =0,
                                pitch = note,
                                time = time,
                                duration = duration,
                                volume = volume)
            time += duration

        # And write it to disk.
        binfile = open(os.path.expanduser(output_location) + trackname + ".mid", 'wb')
        MyMIDI.writeFile(binfile)
        binfile.close()