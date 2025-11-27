#!/usr/bin/env python
# coding: utf-8
from pprint import pprint

from nrk_former_solver import Brett
from nrk_former_solver import Form
from nrk_former_solver import SimpleSolver, LinearSolver, MaxFirstSolver # noqa

O = Form.ORANGE # noqa
G = Form.GRØN
B = Form.BLÅ
R = Form.RAUD

# The challenge from 27. nov 2025:
brett = [
    [O, R, R, B, B, R, O],
    [R, R, O, O, G, B, G],
    [G, R, R, O, R, R, G],
    [R, R, G, G, G, B, G],
    [O, G, B, B, G, O, O],
    [R, G, O, G, B, G, O],
    [R, R, B, O, R, O, B],
    [O, O, R, B, G, R, O],
    [G, B, O, O, G, R, R],
]

print("NRK Former - demo/test:")

brett = Brett(brett)

# s = SimpleSolver(brett)
# s.solve()
# s = LinearSolver(brett)
s = MaxFirstSolver(brett)
try:
    s.solve()
except KeyboardInterrupt:
    print("Bruker avbraut")

print("Resultat:")
print("Antal runder: %d" % s.counter)
print("Beste løysing funne var på %d steg:" % s.best)
pprint(s.best_log)
