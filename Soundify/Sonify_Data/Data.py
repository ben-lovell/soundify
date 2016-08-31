import numpy as np
import time
import pandas
#from Live_Stream import get_live
class Get_Data():

    @staticmethod
    def data_analysis(arr):
        minr = np.nanmin(arr)
        maxr = np.nanmax(arr)
        length = np.size(arr)
        median = (length / 2)
        average = (sum(arr) / np.size(arr))

        data_stats = [minr, maxr, median, average, length]

        return data_stats

    @staticmethod
    def datasets(dataset_source, dataset):
        if dataset == 0:
            return 0

        elif dataset[0:9] == 'Incomplete':
            dataset = dataset[1:]
            v = pandas.read_csv(dataset_source,  usecols = [dataset])

            clean_dataframe = v.dropna()

            called_set = clean_dataframe[dataset].tolist()
            return called_set

        #use 'r' as the set to read a text file
        elif dataset == 'Word Document':
            most_common_words = '/Users/BenLovell/Documents/Creaitive/Soundify/Sonify_Data/20k.txt'
            common_word_text_file = open(most_common_words, 'r')

            common_lines = common_word_text_file.readlines()
            common_lines = [line[:-1] for line in common_lines]

            doc_words = []
            with open(dataset_source,'r') as f:
                for line in f:
                    for word in line.split():
                        doc_words.append(word.lower())

            matching_index = []
            for word in doc_words:
                if word in common_lines:
                    matching_index.append(common_lines.index(word))
                else:
                    continue

            return matching_index

        else:
            v = pandas.read_csv(dataset_source,  usecols = [dataset])

            clean_dataframe = v.dropna()

            called_set = clean_dataframe[dataset].tolist()
            return called_set



def live_data(dataset_source, dataset, frequency):
    while True:
        del test[0]
        time.sleep(frequency)
        #yields the data point, previous day high, previous day low, previous month high and previous month low and average price
        # could possibly change this to 3 month or year
        # price IS NOT weighted average, but simple average
        yield [test[0], 1250,1200,1500,800, 1100]
