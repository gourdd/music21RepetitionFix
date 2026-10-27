from music21 import *
from testMeasures import *
from collections import Counter

def findDifferencesInDynamics(test_score, duplicates_list, dynamics_list):
    for part in test_score.getElementsByClass([stream.Part, stream.PartStaff]):
        for dynamic_set in dynamics_list:
            current_mode = strongMode(dynamic_set)

            print(current_mode)
            if len(current_mode) > 0:
                print(current_mode[0])

            for duplicate_pattern in duplicates_list:
                for duplicate_measure_number in duplicate_pattern:
                    # duplicate_measure_number is the measure number that we want to operate on
                    current_measure_dynamics = list(part.measure(duplicate_measure_number).recurse().getElementsByClass(dynamics.Dynamic))

                    if not current_measure_dynamics == current_mode:
                        if len(current_measure_dynamics) > 0:
                            part.measure(duplicate_measure_number).removeByClass(dynamics.Dynamic)

                        for dynamic in current_mode:
                            dynamic_offset = dynamic.offset
                            new_dynamic = dynamics.Dynamic(value=dynamic.value)
                            part.measure(duplicate_measure_number).insert(dynamic_offset, new_dynamic)
                    
# Take a list, examine each measure. Just iterate first, then we can extract/edit
def findDynamics(test_score, duplicate_list):
    #test_parts = test_score.recurse().getElementsByClass(stream.Part)
    #test_part = test_parts[0].recurse().getElementsByClass(stream.Measure).stream()
    # Get a list of measure numbers which have duplicate notes
    # Check if the measures themselves are true duplicates
    all_pattern_dynamics = []
    for part in test_score.getElementsByClass([stream.Part, stream.PartStaff]):
        for pattern in duplicate_list:
            pattern_dynamics = []
            for measure in pattern:
                # Going through one measure at a time
                current_measure = part.measure(measure)
                current_measure_dynamics = []
                # Extract dynamics
                for dynamic in current_measure.recurse().getElementsByClass(dynamics.Dynamic):
                    current_measure_dynamics.append(dynamic)
                pattern_dynamics.append(current_measure_dynamics)
            all_pattern_dynamics.append(pattern_dynamics)
    return all_pattern_dynamics, duplicate_list

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










    