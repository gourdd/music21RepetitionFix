from music21 import *
from testMeasures import *
from collections import Counter

def hangingDynamics(test_score):
    dynamic_list = []
    for element in test_score.recurse():
        if type(element) == dynamics.Dynamic:
            dynamic_list.append(element)
            if not len(dynamic_list) == 1:
                last_dynamic = dynamic_list[-2].value
                if last_dynamic == element.value:
                    element.activeSite.remove(element)

def dynamicsSignature(measure):
    return tuple((d.getOffsetInHierarchy(measure), d.value)
                 for d in measure.recurse().getElementsByClass(dynamics.Dynamic))

def fixDynamics(test_score, duplicates_list):
    parts = test_score.getElementsByClass([stream.Part, stream.PartStaff])
    for part, part_duplicates in zip(parts, duplicates_list):
        for pattern in part_duplicates:
            measures = [part.measure(n) for n in pattern]
            measures = [m for m in measures if m is not None]
            signatures = [dynamicsSignature(m) for m in measures]

            mode, second_mode = strongMode(signatures)
            if mode is None:
                continue
            if len(mode) == 0 and len(second_mode) > 0:
                mode = second_mode
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
def findRepeatingMeasures(test_score):
    return_measure_numbers = []
    for part in test_score.getElementsByClass([stream.Part, stream.PartStaff]):
        measures = part.recurse().getElementsByClass(stream.Measure).stream()
        return_measure_numbers_part = []
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
                return_measure_numbers_part.append(match_list)
        return_measure_numbers.append(return_measure_numbers_part)
    return return_measure_numbers

def strongMode(data, threshold=0.0):
    if not data:
        return None, []
    counts = Counter(tuple(item) for item in data)
    ranked = counts.most_common(2)
    value, count = ranked[0]
    second = list(ranked[1][0]) if len(ranked) > 1 else []
    if count / len(data) < threshold:
        return None, second
    return list(value), second

def compareMeasures(measure_one, measure_two):
    if list(measure_one.recurse().notesAndRests) == list(measure_two.recurse().notesAndRests):
        return True
    else:
        return False










    