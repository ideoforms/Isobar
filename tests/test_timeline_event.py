""" Unit tests for events """

import isobar as iso
import pytest
from . import dummy_timeline

def test_event_degree(dummy_timeline):
    dummy_timeline.schedule({
        iso.EVENT_DEGREE: iso.PSequence([0, 1, 2, 3, None, 7, -1], 1),
        iso.EVENT_DURATION: 1.0,
        iso.EVENT_TRANSPOSE: 12
    })
    dummy_timeline.run()
    assert dummy_timeline.output_device.events == [
        [0, 'note_on', 12, 64, 0], [1, 'note_off', 12, 0],
        [1, 'note_on', 14, 64, 0], [2, 'note_off', 14, 0],
        [2, 'note_on', 16, 64, 0], [3, 'note_off', 16, 0],
        [3, 'note_on', 17, 64, 0], [4, 'note_off', 17, 0],
        [5, 'note_on', 24, 64, 0], [6, 'note_off', 24, 0],
        [6, 'note_on', 11, 64, 0], [7, 'note_off', 11, 0]
    ]

def test_event_octave(dummy_timeline):
    dummy_timeline.schedule({
        iso.EVENT_DEGREE: iso.PSequence([0, 1, 2, 3], 1),
        iso.EVENT_DURATION: 1.0,
        iso.EVENT_OCTAVE: iso.PSequence([2, 4])
    })
    dummy_timeline.run()
    assert dummy_timeline.output_device.events == [
        [0, 'note_on', 24, 64, 0], [1, 'note_off', 24, 0],
        [1, 'note_on', 50, 64, 0], [2, 'note_off', 50, 0],
        [2, 'note_on', 28, 64, 0], [3, 'note_off', 28, 0],
        [3, 'note_on', 53, 64, 0], [4, 'note_off', 53, 0]
    ]

def test_event_note_octave(dummy_timeline):
    dummy_timeline.schedule({
        iso.EVENT_NOTE: iso.PSequence([0, 1, 2, 3], 1),
        iso.EVENT_DURATION: 1.0,
        iso.EVENT_OCTAVE: iso.PSequence([2, 4])
    })
    dummy_timeline.run()
    assert dummy_timeline.output_device.events == [
        [0, 'note_on', 24, 64, 0], [1, 'note_off', 24, 0],
        [1, 'note_on', 49, 64, 0], [2, 'note_off', 49, 0],
        [2, 'note_on', 26, 64, 0], [3, 'note_off', 26, 0],
        [3, 'note_on', 51, 64, 0], [4, 'note_off', 51, 0]
    ]

def test_event_key(dummy_timeline):
    dummy_timeline.schedule({
        iso.EVENT_DEGREE: iso.PSequence([0, 1, 2, 3], 1),
        iso.EVENT_KEY: iso.PSequence([iso.Key("C", "major"), iso.Key("F", "major")]),
        iso.EVENT_TRANSPOSE: 12
    })
    dummy_timeline.run()
    assert dummy_timeline.output_device.events == [
        [0, 'note_on', 12, 64, 0], [1, 'note_off', 12, 0],
        [1, 'note_on', 19, 64, 0], [2, 'note_off', 19, 0],
        [2, 'note_on', 16, 64, 0], [3, 'note_off', 16, 0],
        [3, 'note_on', 22, 64, 0], [4, 'note_off', 22, 0]
    ]

def test_event_scale(dummy_timeline):
    dummy_timeline.schedule({
        iso.EVENT_DEGREE: iso.PSequence([0, 1, 2, 3], 1),
        iso.EVENT_SCALE: iso.PSequence([iso.Scale.major, iso.Scale.chromatic]),
        iso.EVENT_TRANSPOSE: 36
    })
    dummy_timeline.run()
    assert dummy_timeline.output_device.events == [
        [0, 'note_on', 36, 64, 0], [1, 'note_off', 36, 0],
        [1, 'note_on', 37, 64, 0], [2, 'note_off', 37, 0],
        [2, 'note_on', 40, 64, 0], [3, 'note_off', 40, 0],
        [3, 'note_on', 39, 64, 0], [4, 'note_off', 39, 0]
    ]

def test_event_dur(dummy_timeline):
    dummy_timeline.schedule({
        iso.EVENT_NOTE: iso.PSequence([1, 2, 3]),
        iso.EVENT_DURATION: iso.PSequence([1, 1.5, 2, 1.5], 1)
    })
    dummy_timeline.run()
    assert dummy_timeline.output_device.events == [
        [0, 'note_on', 1, 64, 0], [1, 'note_off', 1, 0],
        [1, 'note_on', 2, 64, 0], [2.5, 'note_off', 2, 0],
        [2.5, 'note_on', 3, 64, 0], [4.5, 'note_off', 3, 0],
        [4.5, 'note_on', 1, 64, 0], [6, 'note_off', 1, 0]
    ]

def test_event_gate(dummy_timeline):
    dummy_timeline.schedule({
        iso.EVENT_NOTE: iso.PSequence([1, 2, 3, 4, 5], 1),
        iso.EVENT_DURATION: iso.PSequence([1, 2]),
        iso.EVENT_GATE: iso.PSequence([0.5, 1, 1.5]),
    })
    dummy_timeline.run()
    assert dummy_timeline.output_device.events == [
        [0, 'note_on', 1, 64, 0], [0.5, 'note_off', 1, 0],
        [1, 'note_on', 2, 64, 0], [3, 'note_off', 2, 0],
        [3, 'note_on', 3, 64, 0],
        [4, 'note_on', 4, 64, 0],
        [4.5, 'note_off', 3, 0],
        [5, 'note_off', 4, 0],
        [6, 'note_on', 5, 64, 0], [7, 'note_off', 5, 0],
    ]

def test_event_chord(dummy_timeline):
    dummy_timeline.schedule({
        iso.EVENT_NOTE: iso.PSequence([(0, 7), 4, (2, 9, 11), 7], 1),
        iso.EVENT_DURATION: iso.PSequence([1, 2]),
        iso.EVENT_AMPLITUDE: iso.PSequence([10, 20, 30])
    })
    dummy_timeline.run()
    assert dummy_timeline.output_device.events == [
        [0, 'note_on', 0, 10, 0],
        [0, 'note_on', 7, 10, 0],
        [1, 'note_off', 0, 0],
        [1, 'note_off', 7, 0],
        [1, 'note_on', 4, 20, 0],
        [3, 'note_off', 4, 0],
        [3, 'note_on', 2, 30, 0],
        [3, 'note_on', 9, 30, 0],
        [3, 'note_on', 11, 30, 0],
        [4, 'note_off', 2, 0],
        [4, 'note_off', 9, 0],
        [4, 'note_off', 11, 0],
        [4, 'note_on', 7, 10, 0],
        [6, 'note_off', 7, 0],
    ]

def test_event_chord_2(dummy_timeline):
    dummy_timeline.schedule({
        iso.EVENT_NOTE: iso.PSequence([(1, 2, 3), (4, 5, 6)], 1),
        iso.EVENT_GATE: (1, 2, 3),
        iso.EVENT_AMPLITUDE: iso.PSequence([(10, 20, 30), (40, 50, 60)])
    })
    dummy_timeline.run()
    assert dummy_timeline.output_device.events == [
        [0, 'note_on', 1, 10, 0],
        [0, 'note_on', 2, 20, 0],
        [0, 'note_on', 3, 30, 0],
        [1, 'note_off', 1, 0],
        [1, 'note_on', 4, 40, 0],
        [1, 'note_on', 5, 50, 0],
        [1, 'note_on', 6, 60, 0],
        [2, 'note_off', 2, 0],
        [2, 'note_off', 4, 0],
        [3, 'note_off', 3, 0],
        [3, 'note_off', 5, 0],
        [4, 'note_off', 6, 0]
    ]

def test_event_action(dummy_timeline):
    dummy_timeline.event_times = []

    def increment_counter():
        dummy_timeline.event_times.append(dummy_timeline.current_time)
        if len(dummy_timeline.event_times) >= 5:
            raise StopIteration

    dummy_timeline.schedule({
        iso.EVENT_ACTION: increment_counter
    })
    dummy_timeline.run()
    assert len(dummy_timeline.event_times) == 5
    assert dummy_timeline.event_times == pytest.approx([0, 1, 2, 3, 4])

# def test_event_control(dummy_timeline):
#     dummy_timeline.schedule({
#         iso.EVENT_CONTROL: PControlChangeLinear(0, 1, 2)
#     })
