class Notes(object):

    @staticmethod
    def scales(scale):
        if scale == 'Full':
            return [21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108]
        if scale == 'C Major':
            return [21,23,24,26,28,29,31,33,35,36,38,40,41,43,45,47,48,50,52,53,55,57,59,60,62,64,65,67,69,71,72,74,76,77,79,81,83,84,86,88,89,91,93,95,96,98,100,101,103,105,107,108]
        if scale == 'D Major':
            return [21, 23, 25, 26, 28, 30, 31, 33, 35, 37, 38, 40, 42, 43, 45, 47, 49, 50, 52, 54, 55, 57, 59, 61, 62, 64, 66, 67, 69, 71, 73, 74, 76, 78, 79, 81, 83, 85, 86, 88, 90, 91, 93, 95, 97, 98, 100, 102, 103, 105, 107]
        if scale == 'E Major':
            return [21, 23, 25, 27, 28, 30, 32, 33, 35, 37, 39, 40, 42, 44, 45, 47, 49, 51, 52, 54, 56, 57, 59, 61, 63, 64, 66, 68, 69, 71, 73, 75, 76, 78, 80, 81, 83, 85, 87, 88, 90, 92, 93, 95, 97, 99, 100, 102, 104, 105, 107]
        if scale == 'F Major':
            return [21, 22, 24, 26, 28, 29, 31, 33, 34, 36, 38, 40, 41, 43, 45, 46, 48, 50, 52, 53, 55, 57, 58, 60, 62, 64, 65, 67, 69, 70, 72, 74, 76, 77, 79, 81, 82, 84, 86, 88, 89, 91, 93, 94, 96, 98, 100, 101, 103, 105, 106, 108]
        if scale == 'G Major':
            return [21,23,24,26,28,30,31,33,35,36,38,40,42,43,45,47,48,50,52,54,55,57,59,60,62,64,66,67,69,71,72,74,76,78,79,81,83,84,86,88,90,91,93,95,96,98,100,102,103,105,107,108]
        if scale == 'A Major':
            return [21, 23, 25, 26, 28, 30, 32, 33, 35, 37, 38, 40, 42, 44, 45, 47, 49, 50, 52, 54, 56, 57, 59, 61, 62, 64, 66, 68, 69, 71, 73, 74, 76, 78, 80, 81, 83, 85, 86, 88, 90, 92, 93, 95, 97, 98, 100, 102, 104, 105, 107]
        if scale == 'B Major':
            return [22, 23, 25, 27, 28, 30, 32, 34, 35, 37, 39, 40, 42, 44, 46, 47, 49, 51, 52, 54, 56, 58, 59, 61, 63, 64, 66, 68, 70, 71, 73, 75, 76, 78, 80, 82, 83, 85, 87, 88, 90, 92, 94, 95, 97, 99, 100, 102, 104, 106, 107]

        if scale == 'C Minor':
            return [22, 24, 26, 27, 29, 31, 32, 34, 36, 38, 39, 41, 43, 44, 46, 48, 50, 51, 53, 55, 56, 58, 60, 62, 63, 65, 67, 68, 70, 72, 74, 75, 77, 79, 80, 82, 84, 86, 87, 89, 91, 92, 94, 96, 98, 99, 101, 103, 104, 106, 108]
        if scale == 'D Minor':
            return [21, 22, 24, 26, 28, 29, 31, 33, 34, 36, 38, 40, 41, 43, 45, 46, 48, 50, 52, 53, 55, 57, 58, 60, 62, 64, 65, 67, 69, 70, 72, 74, 76, 77, 79, 81, 82, 84, 86, 88, 89, 91, 93, 94, 96, 98, 100, 101, 103, 105, 106, 108]
        if scale == 'E Minor':
            return [21, 23, 24, 26, 28, 30, 31, 33, 35, 36, 38, 40, 42, 43, 45, 47, 48, 50, 52, 54, 55, 57, 59, 60, 62, 64, 66, 67, 69, 71, 72, 74, 76, 78, 79, 81, 83, 84, 86, 88, 90, 91, 93, 95, 96, 98, 100, 102, 103, 105, 107, 108]
        if scale == 'F Minor':
            return [22, 24, 25, 27, 29, 31, 32, 34, 36, 37, 39, 41, 43, 44, 46, 48, 49, 51, 53, 55, 56, 58, 60, 61, 63, 65, 67, 68, 70, 72, 73, 75, 77, 79, 80, 82, 84, 85, 87, 89, 91, 92, 94, 96, 97, 99, 101, 103, 104, 106, 108]
        if scale == 'G Minor':
            return [21, 22, 24, 26, 27, 29, 31, 33, 34, 36, 38, 39, 41, 43, 45, 46, 48, 50, 51, 53, 55, 57, 58, 60, 62, 63, 65, 67, 69, 70, 72, 74, 75, 77, 79, 81, 82, 84, 86, 87, 89, 91, 93, 94, 96, 98, 99, 101, 103, 105, 106, 108]
        if scale == 'A Minor':
            return [21, 23, 24, 26, 28, 29, 32, 33, 35, 36, 38, 40, 41, 44, 45, 47, 48, 50, 52, 53, 56, 57, 59, 60, 62, 64, 65, 68, 69, 71, 72, 74, 76, 77, 80, 81, 83, 84, 86, 88, 89, 92, 93, 95, 96, 98, 100, 101, 104, 105, 107, 108]
        if scale == 'B Minor':
            return [21, 23, 25, 26, 28, 30, 31, 33, 35, 37, 38, 40, 42, 43, 45, 47, 49, 50, 52, 54, 55, 57, 59, 61, 62, 64, 66, 67, 69, 71, 73, 74, 76, 78, 79, 81, 83, 85, 86, 88, 90, 91, 93, 95, 97, 98, 100, 102, 103, 105, 107]

        if scale == 'All Major': #that don't share the same key signature with a minor chord
            majors = set(Notes.scales('C Major') + Notes.scales('E Major') + Notes.scales('F Major') +
                   Notes.scales('A Major') + Notes.scales('B Major'))
            return list(majors)

        if scale == 'All Minor': #that don't share the same key signature with a major chord
            minors = set(Notes.scales('C Minor') + Notes.scales('E Minor') + Notes.scales('F Minor') + Notes.scales('G Minor')
                         + Notes.scales('B Minor'))
            return list(minors)

    @staticmethod
    def makescale (scale):
        if len(scale) == 1:
            return Notes.scales(scale[0])
        elif len(scale) == 2:
            chord1 = Notes.scales(scale[0])
            chord2 = Notes.scales(scale[1])
            return list(set(chord1) | set(chord2))
        elif len(scale) == 3:
            chord1 = Notes.scales(scale[0])
            chord2 = Notes.scales(scale[1])
            chord3 = Notes.scales(scale[2])
            return list(set(chord1) | set(chord2) | set(chord3))
        elif len(scale) == 4:
            chord1 = Notes.scales(scale[0])
            chord2 = Notes.scales(scale[1])
            chord3 = Notes.scales(scale[2])
            chord4 = Notes.scales(scale[3])
            return list(set(chord1) | set(chord2) | set(chord3) | set(chord4))

    @staticmethod
    def createchord():
        'A A# B C C# D D# E F F# G G#'
        '0 1  2 3 4  5 6  7 8 9 10 11'

        'A B C# D E F# G'

        pattern = [0,2,4,5,7,9,10]

        chord = Notes.makescale(['Full'])
        check_val = chord[0]
        keyboard = []
        chunk = []
        for x in chord:
            if x - check_val < 12:
                chunk.append(x)
            else:
                keyboard.append(chunk)
                chunk = []
                check_val = x
                chunk.append(check_val)
        keyboard.append(chunk)

        test = []
        counter = 0
        for x in keyboard:
            if len(x) == 12:
                while counter <= 6:
                    test.append(x[pattern[counter]])
                    counter += 1
            if len(x) == 4:
                for y in x:
                    if pattern[counter] <= len(x) - 1:
                            test.append(x[pattern[counter]])
                            counter += 1
            else:
                counter = 0

        print test