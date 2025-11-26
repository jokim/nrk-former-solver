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
    """Algoritme(r) for å løyse brett"""

    def __init__(self):
        self.brett = Brett(lag_tilfeldig_brett())

    def solve(self):
        """Løys eitt brett, med enkel algoritme.

        Returner loggen over kva som vart fjerna.

        """
        logg = []
        print("Løyser denne!")
        print_brett(self.brett)
        while not self.brett.er_tomt():
            kol, rad, verdi = self.finn_form()
            logg.append((kol, rad, verdi))
            self.brett.fjern(kol, rad)
            self.brett.graviter()

        print("Resultat: {} steg".format(len(logg)))
        for line in logg:
            print(line)

    def finn_form(self):
        """Finn første form på brettet og returner

        Returnerer:
            (kolonnenr, radnr, verdi)

        """
        for kol in range(self.brett.kolonner):
            for rad in range(self.brett.rader):
                verdi = self.brett.get(kol, rad)
                if verdi is not None:
                    return kol, rad, verdi


def print_brett(brett):
    """Vis lett lesbart brett"""
    if type(brett) is Brett:
        brett = brett.brett
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

    def __init__(self, data):
        assert len(data) == self.rader
        assert len(data[0]) == self.kolonner
        self.brett = data

    def get(self, kolnr, radnr) -> Form:
        assert kolnr >= 0
        assert radnr >= 0
        return self.brett[radnr][kolnr]

    def set(self, kolnr, radnr, verdi: Form):
        assert kolnr >= 0
        assert radnr >= 0
        self.brett[radnr][kolnr] = verdi

    def er_tomt(self) -> bool:
        for rad in range(self.rader):
            for kol in range(self.kolonner):
                if self.get(kol, rad) is not None:
                    return False
        return True

    def _fjern(self, kolnr, radnr):
        """Fjern enkelt-punkt, ikkje dei rundt"""
        self.brett[radnr][kolnr] = None

    def fjern(self, kolnr, radnr, _fra=None):
        """Fjern ei form frå brettet, og fjern like former rundt.

        Går gjennom rekursivt.

        """
        form = self.get(kolnr, radnr)
        self._fjern(kolnr, radnr)

        # Sjå oppover:
        if _fra != (kolnr, radnr - 1):
            if radnr > 0 and self.get(kolnr, radnr - 1) == form:
                self.fjern(kolnr, radnr - 1, _fra=(kolnr, radnr))

        # Sjå nedover
        if _fra != (kolnr, radnr + 1):
            if radnr + 1 < self.rader and self.get(kolnr, radnr + 1) == form:
                self.fjern(kolnr, radnr + 1, _fra=(kolnr, radnr))

        # Sjå til venstre
        if _fra != (kolnr - 1, radnr):
            if kolnr > 0 and self.get(kolnr - 1, radnr) == form:
                self.fjern(kolnr - 1, radnr, _fra=(kolnr, radnr))

        # Sjå til høgre
        if _fra != (kolnr + 1, radnr):
            if kolnr + 1 < self.kolonner:
                if self.get(kolnr + 1, radnr) == form:
                    self.fjern(kolnr + 1, radnr, _fra=(kolnr, radnr))

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
