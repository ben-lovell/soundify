import statistics
from Note_References import Notes
import numpy as np

"""A midi keyboard has 87 notes starting at #21 and going to #108 with #60 being middle C

    This program maps a given array to this keyboard, BUT for the basic module will only take data 84 points,
    corresponding to 7 full octaves from the lowest C (#24) to the highest B (#108)

    Octave range (set as an array) corresponds to the Midi keyboard, such that an octave value of
    1 = the lowest 7 notes and an octave value of 7 will equal the highest 7 notes

    Future structuring will use different instruments
"""

class Map_Data(object):
    def __init__(self, IorC, dataset, dataset1, dataset2, dataset3, dataset4, dataset5, octaves, scale, mapping):
        self.IorC = IorC
        self.dataset = dataset
        self.dataset1 = dataset1
        self.dataset2 = dataset2
        self.dataset3 = dataset3
        self.dataset4 = dataset4
        self.dataset5 = dataset5
        self.octaves = octaves
        self.scale = scale
        self.mapping = mapping

    @staticmethod
    def chunks(l, n):
        """Yield successive n-sized chunks from l."""
        for i in range(0, len(l), n):
            yield l[i:i+n]

    @staticmethod
    def find_nearest(array,value):
        idx = (np.abs(array-value)).argmin()
        return array[idx]

    @staticmethod
    def create_keyboard(octaves, scale):
        #creates midi keyboard octaves
        midi_keyboard = []

        chord = Notes.makescale(scale)
        check_val = chord[0] - 1

        chunk = []
        for x in chord:
            if x - check_val < 12:
                chunk.append(x)
            else:
                midi_keyboard.append(chunk)
                chunk = []
                check_val = x
                chunk.append(check_val)
        midi_keyboard.append(chunk)

        #Find center of chosen octaves

        keyboard = []
        for n in octaves:
            keyboard.extend(midi_keyboard[n])
        median = float(statistics.median(keyboard))

        #remove off key (non whole numbers)
        if float.is_integer(median):
            median
        else:
            median = median + .5

        return keyboard, median

    @staticmethod
    def check_keyboard(octaves):
        #check octaves
        for o in octaves:
            if (o >= 0 and o <= 7 and len(octaves) <= 8):
                return True
            else:
                print "please either enter octave values between 0 and 7, no more than 7 values and no repeats"

    @staticmethod
    def note_normalizer(arr, mapping):


        if mapping == 'median' or mapping == 'MMmedian':
            median_val = statistics.median(arr)
            upper = []
            lower = []

            for n in arr:
                if n >= median_val:
                    upper.append(n)
                else:
                    lower.append(n)

            umax_val = max(upper)
            lmin_val = min(lower)
            diff = umax_val - lmin_val


            normalized = []

            for n in arr:
                if n in upper:
                    normalized.append(((n - median_val) / float(diff)) +.5)
                elif n in lower:
                    normalized.append(abs(((median_val - n) / float(diff)) - .5))

            return normalized

        elif mapping == 'normalized' or mapping == 'MMnormalized':
            max_value = max(arr)
            min_value = min(arr)
            difference = max_value - min_value
            normalizer = []
            for n in arr:
                normalizer.append((n - min_value) / float((difference)))

            return normalizer

        #sorts a list in a cyclical fashion. For example, if using a database of most common words, the most common
        # word will be put at the center (0.5), and each successive word will be placed alternating to the right and then left
        # of the center word. (eg.    5th, 3rd most common word, 1st most common word, 2nd most common word, 4th)
        elif mapping == 'wrapped' or mapping == 'MMwrapped':
            max_value = max(arr)
            min_value = min(arr)
            difference = max_value - min_value
            normalizer = []

            for n in arr:
                normalizer.append((n - min_value) / float(difference))

            wrapper = []
            for value in normalizer:
                if normalizer.index(value) % 2 != 0:
                    wrapper.append((value * 0.5) + .5)
                else:
                    wrapper.append(abs((value * 0.5) - .5))

            return wrapper

        elif mapping[0:7] == 'grouped' or mapping[0:9] == 'MMgrouped':

            combined_datasets = []
            for dataset in arr:
                combined_datasets += dataset

            max_val = max(combined_datasets)
            min_val = min(combined_datasets)
            diff = max_val - min_val


            normalized = []

            for n in combined_datasets:
                normalized.append(abs(((n - min_val) / float(diff))))

            regrouped_data = []
            for dataset in arr:
                d_set = []
                for data in dataset:
                    d_set.append(normalized[0])
                    del normalized[0]
                regrouped_data.append(d_set)


            return regrouped_data

    @staticmethod
    def key_mapper(arr, octaves, scale, mapping):
        keyboard = Map_Data.create_keyboard(octaves, scale)

        major_keyboard = Map_Data.create_keyboard(octaves, ['All Major'])
        minor_keyboard = Map_Data.create_keyboard(octaves, ['All Minor'])

        full_keyboard = Map_Data.create_keyboard(octaves, ['Full'])

        full_key_map = []

        if mapping[0:2] == 'MM':
            if mapping[2:9] == 'grouped':
                combined_datasets = []
                for dataset in arr:
                    combined_datasets += dataset

                for n in combined_datasets:
                    if len(octaves) == 7:
                        full_key_map.append(int(n * (87) + full_keyboard[0][0]))
                    else:
                        full_key_map.append(int(n * (len(octaves) * 12) + full_keyboard[0][0]))
            else:
                for n in arr:
                    if len(octaves) == 7:
                        full_key_map.append(int(n * (87) + full_keyboard[0][0]))
                    else:
                        full_key_map.append(int(n * (len(octaves) * 12) + full_keyboard[0][0]))

            diff_map = np.diff(full_key_map)
            key_map = []

            for note in full_key_map:
                if diff_map[full_key_map.index(note)] < 0:
                    if note in major_keyboard[0]:
                        key_map.append([note])
                    else:
                        v = Map_Data.find_nearest(np.array(major_keyboard[0]), note)
                        key_map.append([v])
                elif diff_map[full_key_map.index(note)] >= 0:
                    if note in minor_keyboard[0]:
                        key_map.append([note])
                    else:
                        v = Map_Data.find_nearest(np.array(minor_keyboard[0]), note)
                        key_map.append([v])

            if mapping[2:9] == 'grouped':
                regrouped_data = []
                for dataset in arr:
                    d_set = []
                    for data in dataset:
                        d_set.append(key_map[0])
                        del key_map[0]
                    regrouped_data.append(d_set)
                    del d_set

                return regrouped_data

            else:
                return key_map

        elif mapping[0:7] == 'grouped':
            combined_datasets = []
            for dataset in arr:
                combined_datasets += dataset

            for n in combined_datasets:
                if len(octaves) == 7:
                    full_key_map.append(int(n * (87) + full_keyboard[0][0]))
                else:
                    full_key_map.append(int(n * (len(octaves) * 12) + full_keyboard[0][0]))

            select_keys = np.array(keyboard[0])

            key_map = []
            for note in full_key_map:
                if note in keyboard[0]:
                    key_map.append([note])
                else:
                    v = Map_Data.find_nearest(select_keys, note)
                    key_map.append([v])

            regrouped_data = []

            for dataset in arr:
                d_set = []
                for data in dataset:
                    d_set.append(key_map[0])
                    del key_map[0]
                regrouped_data.append(d_set)
                del d_set

            return regrouped_data

        else:
            for n in arr:
                if len(octaves) == 7:
                    full_key_map.append(int(n * (87) + full_keyboard[0][0]))
                else:
                    full_key_map.append(int(n * (len(octaves) * 12) + full_keyboard[0][0]))
            select_keys = np.array(keyboard[0])

            key_map = []
            for note in full_key_map:
                if note in keyboard[0]:
                    key_map.append([note])
                else:
                    v = Map_Data.find_nearest(select_keys, note)
                    key_map.append([v])
            return key_map

    @staticmethod
    def note_mapping(IorC, dataset, octaves, scale, mapping):
        Map_Data.check_keyboard(octaves)
        normalizer = Map_Data.note_normalizer(dataset, mapping)

        key_map = Map_Data.key_mapper(normalizer, octaves, scale, mapping)

        if IorC[0:9] == 'Incomplete':
            subtract = 6
            x = 0
            while x < subtract:
                del key_map[-1]
                x += 1
            print key_map
            return key_map

        elif IorC == 'Word Document':
            for value in key_map:
                one_next_val = key_map[key_map.index(value) + 1][0]
                two_next_val = key_map[key_map.index(value) + 2][0]
                three_next_val = key_map[key_map.index(value) + 3][0]
                four_next_val = key_map[key_map.index(value) + 4][0]

                if value[0] == one_next_val and value == two_next_val and value == three_next_val and value == four_next_val:
                    del one_next_val, two_next_val, three_next_val, four_next_val
                elif value[0] == one_next_val and value == two_next_val and value == three_next_val:
                    del one_next_val, two_next_val, three_next_val
                elif value[0] == one_next_val and value == two_next_val:
                    del one_next_val, two_next_val
                elif value[0] == one_next_val:
                    del one_next_val

            print key_map
            return key_map

        else:
            print key_map
            return key_map

    @staticmethod
    def chord_mapping(IorC, dataset1, dataset2, dataset3, dataset4, dataset5, dataset6, octaves, scale, mapping):
        Map_Data.check_keyboard(octaves)

        dataset_list = [dataset1, dataset2, dataset3, dataset4, dataset5, dataset6]

        for dataset in dataset_list:
            if dataset == 0:
                del dataset

        keys = []

        if mapping[0:7] == 'grouped' or mapping[2:9] == 'grouped':
            map1 = Map_Data.note_normalizer(dataset_list, mapping)
            keys1 = Map_Data.key_mapper(map1, octaves, scale, mapping)
            for dataset in dataset_list:
                if IorC[dataset_list.index(dataset)] == 'Incomplete':
                    subtract = 6
                    x = 0
                    while x < subtract:
                        del keys1[-1]
                        x += 1

            keys = keys1

        else:
            for dataset in dataset_list:
                map1 = Map_Data.note_normalizer(dataset, mapping)
                keys1 = Map_Data.key_mapper(map1, octaves, scale, mapping)

                if IorC[dataset_list.index(dataset)] == 'Incomplete':
                    subtract = 6
                    x = 0
                    while x < subtract:
                        del keys1[-1]
                        x += 1

                keys.append(keys1)



        keyboard_mapper = zip(*[key for key in keys])

        #possible mapping for using datasets of unequal length
        #for i in (filter(None, pair) for pair in itertools.izip_longest(key for key in keys)): keyboard_mapper.append(i)

        final = []
        for n in keyboard_mapper:
            if len(n) == 6:
                final.append([n[0][0], n[1][0], n[2][0], n[3][0], n[4][0], n[5][0]])
            if len(n) == 5:
                final.append([n[0][0], n[1][0], n[2][0], n[3][0], n[4][0]])
            if len(n) == 4:
                final.append([n[0][0], n[1][0], n[2][0], n[3][0]])
            if len(n) == 3:
                final.append([n[0][0], n[1][0], n[2][0]])
            elif len(n) == 2:
                final.append([n[0][0], n[1][0]])
            elif len(n) == 1:
                final.append(n[0][0])

        print final
        return final



data = []

class Map_Live_Data(object):
    def __init__(self):
        self.__dict__.update(data)

    @staticmethod
    def chunks(l, n):
        """Yield successive n-sized chunks from l."""
        for i in range(0, len(l), n):
            yield l[i:i+n]

    @staticmethod
    def find_nearest( array,value):
        idx = (np.abs(array-value)).argmin()
        return array[idx]

    @staticmethod
    def create_keyboard(octaves, scale):
        #creates midi keyboard octaves
        midi_keyboard = []

        chord = Notes.makescale(scale)
        check_val = chord[0] - 1

        chunk = []
        for x in chord:
            if x - check_val < 12:
                chunk.append(x)
            else:
                midi_keyboard.append(chunk)
                chunk = []
                check_val = x
                chunk.append(check_val)
        midi_keyboard.append(chunk)

        #Find center of chosen octaves

        keyboard = []
        for n in octaves:
            keyboard.extend(midi_keyboard[n])
        median = float(statistics.median(keyboard))

        #remove off key (non whole numbers)
        if float.is_integer(median):
            median
        else:
            median = median + .5

        return keyboard, median

    @staticmethod
    def check_keyboard(octaves):
        #check octaves
        for o in octaves:
            if (o >= 0 and o <= 7 and len(octaves) <= 8):
                return True
            else:
                print "please either enter octave values between 0 and 7, no more than 7 values and no repeats"

    @staticmethod
    def note_normalizer(arr, mapping):
        if mapping == 'median' or mapping == 'MMmedian':
            median_val = statistics.median(arr)
            upper = []
            lower = []

            for n in arr:
                if n >= median_val:
                    upper.append(n)
                else:
                    lower.append(n)

            umax_val = max(upper)
            umin_val = min(upper)
            udiff = umax_val - umin_val


            lmax_val = max(lower)
            lmin_val = min(lower)
            ldiff = lmax_val - lmin_val


            normalized = []

            for n in arr:
                if n in upper:
                    normalized.append(((n - median_val) / float(umax_val - lmin_val)) +.5)
                elif n in lower:
                    normalized.append(abs(((median_val - n) / float(umax_val - lmin_val)) - .5))


            return normalized
        elif mapping == 'normalized' or mapping == 'MMnormalized':
            max_value = max(arr)
            min_value = min(arr)
            difference = max_value - min_value
            normalizer = []
            for n in arr:
                normalizer.append((n - min_value) / float((difference)))

            return normalizer

        #sorts a list in a cyclical fashion. For example, if using a database of most common words, the most common
        # word will be put at the center (0.5), and each successive word will be placed alternating to the right and then left
        # of the center word. (eg.    5th, 3rd most common word, 1st most common word, 2nd most common word, 4th)
        elif mapping == 'wrapped' or mapping == 'MMwrapped':
            max_value = max(arr)
            min_value = min(arr)
            difference = max_value - min_value
            normalizer = []

            for n in arr:
                normalizer.append((n - min_value) / float(difference))

            wrapper = []
            for value in normalizer:
                if normalizer.index(value) % 2 != 0:
                    wrapper.append((value * 0.5) + .5)
                else:
                    wrapper.append(abs((value * 0.5) - .5))

            return wrapper

    @staticmethod
    def live_note_normalizer(arr, stock):
        #This function maps the live data relative to the previous days high and low
        #THe data is first compared to the previous day, and mapped to the middle of the keyboard
        # if the data falls outside of the previous day high and low, it is then mapped to the remaining
        # higher or lower octaves

        data_instance = arr.next()

        prev_day_high = data_instance[1]
        prev_day_low = data_instance[2]

        #artifical max and min are based on the distance from the year average value (arr[5]) to the
        # 1 month max (arr[3]) and min (arr[4]) respectively
        # price IS NOT weighted average, but simple average
        # this is because a weighted average would skew the first notes off the center of the keyboard
        artificial_stock_max = prev_day_high + (data_instance[3] - data_instance[5])
        artificial_stock_min = prev_day_low - (data_instance[5] - data_instance[4])
        difference = artificial_stock_max - artificial_stock_min

        normalizer2 = []
        normalizer2.append(abs(float(stock[len(stock) - 1] - artificial_stock_min) / (difference)))

        return normalizer2

    @staticmethod
    def live_mapping(arr, octaves, scale):
        keyboard = Map_Live_Data.create_keyboard(octaves, scale)
        Map_Live_Data.check_keyboard(octaves)

        data.append(arr.next()[0])

        normalizer = Map_Live_Data.live_note_normalizer(arr, data)
        key_map = [int(((normalizer[0] * (len(octaves) * 12)) + keyboard[0][0]))]

        print key_map
        return key_map