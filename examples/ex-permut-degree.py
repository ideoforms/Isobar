#!/usr/bin/env python

# import vital classes from isobar namespace
from isobar import *
import random

# create a pitch line comprised of multiple permutations on a pelog scale
ppitch = PShuffle([ random.randint(-6, 6) for n in range(6) ])
ppitch = PPermut(ppitch)
ppitch = PDegree(ppitch, Key("F#", "pelog"))

# create permuted sets of durations and amplitudes
# different lengths mean poly-combinations
pdur = PShuffle([ 1, 1, 2, 2, 4 ], 1)
pdur  = PPermut(pdur) * 0.25

pamp = PShuffle([ 10, 15, 20, 35 ], 2)
pamp = PPermut(pamp)

# schedule on a 60bpm timeline and send to MIDI output
timeline = Timeline(60)
timeline.sched({ 'note': ppitch + 60, 'dur': pdur, 'channel': 0, 'gate': 1, 'amp': pamp })
timeline.sched({ 'note': ppitch + 24, 'dur': pdur * 4, 'channel': 1, 'gate': 2, 'amp': pamp })
timeline.sched({ 'note': ppitch + 72, 'dur': pdur / 2, 'channel': 1, 'gate': 1, 'amp': pamp / 2 })

# add some continuous warping
warp = PWInterpolate(PBrown(-0.1, 0.01, -0.15, -0.05), 2)
timeline.warp(warp)

# go!
timeline.run()
