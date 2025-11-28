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

# The challenge from 28. nov 2025:
brett = [
    [O, R, B, O, O, R, B],
    [B, O, O, O, R, O, G],
    [O, R, G, R, B, G, B],
    [B, G, O, B, O, R, G],
    [G, R, R, B, B, R, G],
    [G, R, R, R, O, B, B],
    [O, R, R, O, R, O, B],
    [R, G, G, O, R, O, B],
    [B, G, R, R, B, B, R],
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
