#!/usr/bin/env python
# coding: utf-8

import nrk_former_solver
from nrk_former_solver import Solver, print_brett

print("NRK Former - demo/test:")

#tilf = nrk_former_solver.lag_tilfeldig_brett()
#print_brett(tilf)
#b = nrk_former_solver.Brett(tilf)
#b.fjern(2, 2)
#print_brett(b.brett)
#b.graviter()
#print_brett(b.brett)
s = Solver()
s.solve()
