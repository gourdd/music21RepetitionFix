from music21 import *

def getTestScore():
    measure_one = stream.Measure(number=1)
    measure_two = stream.Measure(number=2)
    measure_three = stream.Measure(number=3)
    measure_four = stream.Measure(number=4)
    measure_five = stream.Measure(number=5)
    measure_six = stream.Measure(number=6)
    measure_seven = stream.Measure(number=7)
    measure_eight = stream.Measure(number=8)
    measure_nine = stream.Measure(number=9)

    note_one = note.Note("C4", type="whole")
    note_two = note.Note("C4", type="whole")
    note_three = note.Note("D4", type="half")
    note_four = note.Note("E4", type="half")
    note_five = note.Note("C4",type="whole")
    note_six = note.Note("D4", type="half")
    note_seven = note.Note("E4", type="half")

    note_eight = chord.Chord(["C4", "G4", "C5"], type="quarter")
    note_nine = chord.Chord(["D5", "A4"], type="quarter")
    note_ten = note.Rest(type="half")

    note_eleven = note.Note("A3", type="whole")

    note_twelve = chord.Chord(["C4", "G4", "C5"], type="quarter")
    note_thirteen = chord.Chord(["D5", "A4"], type="quarter")
    note_fourteen = note.Rest(type="half")
    note_fifteen = note.Note("C4", type="whole")

    dynamic_one = dynamics.Dynamic("mp")
    dynamic_two = dynamics.Dynamic("pp")
    dynamic_three = dynamics.Dynamic("mp")
    dynamic_four = dynamics.Dynamic("p")
    dynamic_five = dynamics.Dynamic("pp")
    dynamic_six = dynamics.Dynamic("mp")
    dynamic_seven = dynamics.Dynamic("mp")

    measure_one.append(note_one)
    measure_two.append(note_two)
    measure_three.append([note_three, note_four])
    measure_four.append(note_five)
    measure_five.append([note_six, note_seven])

    measure_six.append([note_eight, note_nine, note_ten])
    measure_seven.append(note_eleven)
    measure_eight.append([note_twelve, note_thirteen, note_fourteen])
    measure_nine.append(note_fifteen)

    measure_one.insert(offsetOrItemOrList=0.0, itemOrNone=dynamic_one)
    measure_two.insert(offsetOrItemOrList=0.0, itemOrNone=dynamic_three)
    measure_four.insert(offsetOrItemOrList=0.0, itemOrNone=dynamic_four)
    measure_nine.insert(offsetOrItemOrList=0.0, itemOrNone=dynamic_seven)

    test_part = stream.Part()
    test_part.append([measure_one, measure_two, measure_three, measure_four, measure_five, measure_six, measure_seven, measure_eight, measure_nine])

    

    test_score = stream.Score()
    test_score.append(test_part)

    return test_score
