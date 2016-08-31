from MIDI_Reader import fileio
import statistics

def full_set_maker(group, dataset):
    full_set = [list(dataset) for dataset in zip( * [iter(dataset)] * group)]
    return full_set

def train_set_maker(group, dataset):
    train_set = [list(dataset) for dataset in zip( * [iter(dataset)] * group)][:-5]
    return train_set

def test_set_maker(group, dataset):
    full_set = full_set_maker(group, dataset)
    test_set = [list(dataset) for dataset in zip( * [iter(dataset)] * group)][(len(full_set) - 5):]
    return test_set

def average_per_group(dataset):
    avg = []
    for x in dataset:
        avg.append(statistics.mean(x))

    overall_avg = statistics.mean(avg)


    grouped_y = []
    for x in avg:
        if x > overall_avg:
            grouped_y.append(1)
        elif x <= overall_avg:
            grouped_y.append(0)

    return grouped_y

def up_or_down_movement(dataset, type):
    if type == 'Per Note':
        grouped_y = []
        previous_val = 0
        for x in dataset:
            if x > previous_val:
                grouped_y.append(1)
                previous_val = x
            elif x <= previous_val:
                grouped_y.append(0)
                previous_val = x
        return grouped_y

    if type == 'Rolling Average':
        avg = []
        for x in dataset:
            avg.append(statistics.mean(x))

        grouped_y = []
        previous_val = 0
        for x in avg:
            if x > previous_val:
                grouped_y.append(1)
                previous_val = x
            elif x <= previous_val:
                grouped_y.append(0)
                previous_val = x

        return grouped_y
    if type == 'Sum of Group':
        sum_movement = []
        for x in dataset:
            group_movement = []
            previous_val = x[0]
            for note in x:
                group_movement.append(note - previous_val)
                previous_val = note
            sum_movement.append(sum(group_movement))

        grouped_y = []
        for x in sum_movement:
            if x > 0:
                grouped_y.append(1)
            elif x <= 0:
                grouped_y.append(0)

        return grouped_y

def min_max_group(dataset):
    minmax = []
    for x in dataset:
        difference = max(x) - min(x)
        minmax.append(difference)

    overall_avg = statistics.mean(minmax)

    grouped_y = []
    for x in minmax:
        difference = max(minmax) - min(minmax)
        if difference > overall_avg:
            grouped_y.append(1)
        elif difference <= overall_avg:
            grouped_y.append(0)

    return grouped_y

def reverse_sonify_test(midifile, group, yvalue):
    converted_file = fileio.return_notes(midifile)

    maxmidi = max(converted_file)
    minmidi= min(converted_file)


    normalized = []
    for x in converted_file:
        normalized.append((float(x) - minmidi) / (maxmidi - minmidi))


    test_set = test_set_maker(group, normalized)
    full_set = full_set_maker(group, normalized)

    if yvalue == 'Average of Groups':
        actual = average_per_group(full_set)[(len(full_set) - 5):]
        return test_set, actual
    elif yvalue == 'Up or Down Per Note':
        # Can be "Per Note", "Rolling Average" or "Sum of Group"
        actual = up_or_down_movement(full_set, 'Per Note')[(len(full_set) - 5):]
        return test_set, actual
    elif yvalue == 'Up or Down Rolling Average':
        # Can be "Per Note", "Rolling Average" or "Sum of Group"
        actual = up_or_down_movement(full_set, 'Rolling Average')[(len(full_set) - 5):]
        return test_set, actual
    elif yvalue == 'Up or Down Sum of Group':
        # Can be "Per Note", "Rolling Average" or "Sum of Group"
        actual = up_or_down_movement(full_set, 'Sum of Group')[(len(full_set) - 5):]
        return test_set, actual
    elif yvalue == 'Group Min Max':
        actual = min_max_group(full_set)[(len(full_set) - 5):]
        return test_set, actual

def reverse_sonify_train(midifile, group, yvalue):

    # THIS SECTION REVERSES THE MIDI NOTES INTO NORMALIZED VALUES BETWEEN 0 AND 1
    all_files = []
    for file in midifile:
        converted_file = fileio.return_notes(file)
        all_files += converted_file


    median_val = statistics.median(all_files)
    upper = []
    lower = []

    for n in all_files:
        if n >= median_val:
            upper.append(n)
        else:
            lower.append(n)


    umax_val = max(upper)
    umin_val = min(upper)
    lmax_val = max(lower)
    lmin_val = min(lower)
    udiff = umax_val - umin_val
    ldiff = lmax_val - lmin_val


    # THIS SECTION SPLITS THE BASS NOTES FROM THE TREBLE NOTES
    normalizedu = []
    normalizedl = []
    for n in upper:
        normalizedu.append(((n - umin_val) / float(udiff)))
    for n in lower:
        normalizedl.append(abs(((n - lmin_val) / float(ldiff))))


    maxmidi = max(all_files)
    minmidi= min(all_files)

    normalized2 = []
    for x in all_files:
        normalized2.append((float(x) - minmidi) / (maxmidi - minmidi))



    test_set = test_set_maker(group, normalizedu)
    train_set = train_set_maker(group, normalizedu)
    full_set = full_set_maker(group, normalizedu)

    if yvalue == 'Average of Groups':
        average_of_groups = average_per_group(train_set)
        actual = average_per_group(full_set)[(len(full_set) - 5):]
        return train_set, average_of_groups, test_set, actual
    elif yvalue == 'Up or Down Per Note':
        # Can be "Per Note", "Rolling Average" or "Sum of Group"
        up_or_down_groups = up_or_down_movement(train_set, 'Per Note')
        actual = up_or_down_movement(full_set, 'Per Note')[(len(full_set) - 5):]
        return train_set, up_or_down_groups, test_set, actual
    elif yvalue == 'Up or Down Rolling Average':
        # Can be "Per Note", "Rolling Average" or "Sum of Group"
        up_or_down_groups = up_or_down_movement(train_set, 'Rolling Average')
        actual = up_or_down_movement(full_set, 'Rolling Average')[(len(full_set) - 5):]
        return train_set, up_or_down_groups, test_set, actual
    elif yvalue == 'Up or Down Sum of Group':
        # Can be "Per Note", "Rolling Average" or "Sum of Group"
        up_or_down_groups = up_or_down_movement(train_set, 'Sum of Group')
        actual = up_or_down_movement(full_set, 'Sum of Group')[(len(full_set) - 5):]
        return train_set, up_or_down_groups, test_set, actual
    elif yvalue == 'Group Min Max':
        min_max_of_groups = min_max_group(train_set)
        actual = min_max_group(full_set)[(len(full_set) - 5):]
        return train_set, min_max_of_groups, test_set, actual
    elif yvalue == 'Grouped Notes':
        XValues = []
        YValues = []
        song_norm = full_set_maker(group, normalized2)
        song_notes = full_set_maker(group, all_files)
        for norm, notes in zip(song_norm, song_notes):
            if song_norm.index(norm) % 2 == 0:
                XValues.append(norm)
            else:
                YValues.append(notes)
        return XValues, YValues

#train_dataset_source = ['/Users/BenLovell/Documents/Creaitive/Soundify/Musical_Neural_Net/Music_Training_Datasets/5thsymphony.mid']
#print reverse_sonify_train(train_dataset_source, 10, 'Grouped Notes')[0]
#print reverse_sonify_train(train_dataset_source, 10, 'Grouped Notes')[1]