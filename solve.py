#!/usr/bin/env python
# coding: utf-8

import nrk_former_solver

print("NRK Former - demo/test:")

tilf = nrk_former_solver.lag_tilfeldig_brett()
nrk_former_solver.print_brett(tilf)
b = nrk_former_solver.Brett(tilf)
b.fjern(2, 2)
nrk_former_solver.print_brett(tilf)
b.graviter()
nrk_former_solver.print_brett(tilf)
