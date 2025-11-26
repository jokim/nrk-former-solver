#!/usr/bin/env python
# coding: utf-8
"""Solver for NRK sitt minispill *Former*

Funksjonalitet for å finne beste løysingane på minispillet.

Former er eit brett med sju kolonner og 9 rader. Kvar plass inneheld ei av fire
former (oransje, grøn, blå og raud). Du velger ein av formene, som gjer at alle
naboplasser (over, under, venstre og høgre, men ikkje diagnoalt) med same form
forsvinner. Ledige plasser gjer at formene over faller ned. Målet er å fjerne
alle former med færrast mogeleg trykk.

Formene, gjer det enkelt med str i starten:

- 'O' - oransje
- 'G' - grøn
- 'B' - blå
- 'R' - raud

"""

import enum
import random


class Form(enum.Enum):
    ORANGE = 1
    GRØN = 2
    BLÅ = 3
    RAUD = 4


class Solver(object):
    pass


def print_brett(brett):
    """Vis lett lesbart brett"""
    for rad in brett:
        for kol in rad:
            if kol is None:
                print("{:^6}".format("-"), end=" ")
            else:
                print(f"{kol.name:^6}", end=" ")
        print()
    print()


def lag_tilfeldig_brett():
    ret = []
    for i in range(Brett.rader):
        rad = []
        for j in range(Brett.kolonner):
            rad.append(random.choice(list(Form)))
        ret.append(rad)
    return ret


class Brett(object):
    """Oppstilling av formene"""

    rader = 9
    kolonner = 7

    def __init__(self, oppstartsdata=None):
        if oppstartsdata:
            self.brett = oppstartsdata
        else:
            self.brett = self.tomt_brett()

    def tomt_brett(self):
        ret = []
        for i in range(self.rader):
            ret.append([None] * self.kolonner)

        print_brett(ret)
        return ret

    def get(self, kolonnenr, radnr) -> Form:
        assert kolonnenr >= 0
        assert radnr >= 0
        return self.brett[radnr][kolonnenr]

    def set(self, kolonnenr, radnr, verdi: Form):
        assert kolonnenr >= 0
        assert radnr >= 0
        self.brett[radnr][kolonnenr] = verdi

    def _fjern(self, kolonnenr, radnr):
        """Fjern enkelt-punkt, ikkje dei rundt"""
        self.brett[radnr][kolonnenr] = None

    def er_tomt(self) -> bool:
        for rad in range(self.rader):
            for kol in range(self.kolonner):
                if self.get(kol, rad) is not None:
                    return False
        return True

    def fjern(self, kolnr, radnr):
        """Fjern ei form frå brettet, og fjern like former rundt.

        Går gjennom rekursivt.

        """
        form = self.get(kolnr, radnr)
        self._fjern(kolnr, radnr)

        # Sjå oppover:
        if radnr > 0 and self.get(kolnr, radnr - 1) == form:
            self.fjern(kolnr, radnr - 1)

        # Sjå nedover
        if radnr < self.rader and self.get(kolnr, radnr + 1) == form:
            self.fjern(kolnr, radnr + 1)

        # Sjå til venstre
        if kolnr > 0 and self.get(kolnr - 1, radnr) == form:
            self.fjern(kolnr - 1, radnr)

        # Sjå til høgre
        if kolnr < self.kolonner and self.get(kolnr + 1, radnr) == form:
            self.fjern(kolnr + 1, radnr)

    def graviter(self):
        """Gå gjennom kolonnene og flytt former nedover om det er tomme"""
        for kol in range(self.kolonner):
            movement: bool = True
            while movement:
                movement = False
                rad = self.rader
                while rad > 0:
                    rad -= 1
                    if self.get(kol, rad) is None:
                        if rad == 0:
                            self.set(kol, rad, None)
                        else:
                            verdi = self.get(kol, rad - 1)
                            self.set(kol, rad, verdi)
                            if verdi:
                                movement = True
                            self._fjern(kol, rad - 1)
