from music21 import *
from testMeasures import *
from collections import Counter

def dynamicsSignature(measure):
    return tuple((d.getOffsetInHierarchy(measure), d.value)
                 for d in measure.recurse().getElementsByClass(dynamics.Dynamic))

def fixDynamics(test_score, duplicates_list):
    for part in test_score.getElementsByClass([stream.Part, stream.PartStaff]):
        for pattern in duplicates_list:
            measures = [part.measure(n) for n in pattern]
            measures = [m for m in measures if m is not None]
            signatures = [dynamicsSignature(m) for m in measures]

            mode = strongMode(signatures)
            if mode is None:
                continue
            mode = tuple(mode)

            for m, sig in zip(measures, signatures):
                if sig == mode:
                    continue
                for d in list(m.recurse().getElementsByClass(dynamics.Dynamic)):
                    m.remove(d, recurse=True)
                for offset, value in mode:
                    m.insert(offset, dynamics.Dynamic(value))

# Returns a list of lists. Each list contains measure numbers that contain duplicate notes
# [[1, 2, 4, 9], [3, 5], [6, 8]]
def findRepeatingMeasures(test_score, error_margin=0.0):
    #test_parts = test_score.recurse().getElementsByClass(stream.Part)
    #test_measures = test_parts[0].recurse().getElementsByClass(stream.Measure).stream()
    for part in test_score.getElementsByClass([stream.Part, stream.PartStaff]):
        measures = part.recurse().getElementsByClass(stream.Measure).stream()
        return_measure_numbers = []
        found_patterns = []
        for measure_one in measures:
            match_list = []
            pattern_index = []
            measure_one_number = measure_one.number
            for measure_two in measures:
                measure_two_number = measure_two.number
                if compareMeasures(measure_one, measure_two) and not measure_one_number == measure_two_number and not list(measure_two.recurse().notesAndRests) in found_patterns:
                    pattern_index.append(measure_two_number)
            if len(pattern_index) > 0:
                found_patterns.append(list(measure_one.recurse().notesAndRests))
                match_list.append(measure_one_number)
                for match_index in pattern_index:
                    match_list.append(match_index)
                return_measure_numbers.append(match_list)
    return return_measure_numbers

def strongMode(data, threshold=0.0):
    if not data:
        return None
    counts = Counter(tuple(item) for item in data)   # lists can't be dict keys, tuples can
    value, count = counts.most_common(1)[0]
    if count / len(data) >= threshold:
        return list(value)                           # hand back a list, like the input items
    return None

def compareMeasures(measure_one, measure_two):
    if list(measure_one.recurse().notesAndRests) == list(measure_two.recurse().notesAndRests):
        return True
    else:
        return False










    