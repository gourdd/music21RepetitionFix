from music21 import *
from testMeasures import *
from collections import Counter

#def findDifferencesInDynamics(test_score, duplicates_list, dynamics_list):




# Take a list, examine each measure. Just iterate first, then we can extract/edit
def findDynamics(test_score, duplicate_list):
    test_parts = test_score.recurse().getElementsByClass(stream.Part)
    test_part = test_parts[0].recurse().getElementsByClass(stream.Measure).stream()
    # Get a list of measure numbers which have duplicate notes
    # Check if the measures themselves are true duplicates
    all_pattern_dynamics = []
    for pattern in duplicate_list:
        pattern_dynamics = []
        for measure in pattern:
            # Going through one measure at a time
            current_measure = test_part.measure(measure)
            current_measure_dynamics = []
            # Extract dynamics
            for dynamic in current_measure.recurse().getElementsByClass(dynamics.Dynamic):
                current_measure_dynamics.append(dynamic.value)
            pattern_dynamics.append(current_measure_dynamics)
        all_pattern_dynamics.append(pattern_dynamics)
    return all_pattern_dynamics, duplicate_list

# Returns a list of lists. Each list contains measure numbers that contain duplicate notes
# [[1, 2, 4, 9], [3, 5], [6, 8]]
def findRepeatingMeasures(test_score, error_margin=0.0):
    test_parts = test_score.recurse().getElementsByClass(stream.Part)
    test_measures = test_parts[0].recurse().getElementsByClass(stream.Measure).stream()
    return_measure_numbers = []
    found_patterns = []
    for measure_one in test_measures:
        match_list = []
        pattern_index = []
        measure_one_number = measure_one.number
        for measure_two in test_measures:
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

def strongMode(data, threshold=0.5):
    if not data:
        return None
    value, count = Counter(data).most_common(1)[0]
    return value if count / len(data) >= threshold else None

def compareMeasures(measure_one, measure_two):
    if list(measure_one.recurse().notesAndRests) == list(measure_two.recurse().notesAndRests):
        return True
    else:
        return False

test_score = getTestScore()
repeating_measures = findRepeatingMeasures(test_score)
test_score.show()

# Expected output [[1, 2, 4], [3, 5]]
print(repeating_measures)
dynamics_list, repeating_measures = findDynamics(test_score, repeating_measures)
print(dynamics_list)









    