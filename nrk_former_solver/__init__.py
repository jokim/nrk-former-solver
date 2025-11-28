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
import math
import random
import time


class Form(enum.Enum):
    ORANGE = 1
    GRØN = 2
    BLÅ = 3
    RAUD = 4


DEBUG: bool = False


def debug(output, *args):
    if DEBUG:
        print(output % args)


class Solver(object):
    def __init__(self, brett=None):
        self.brett = brett
        self.counter: int = 0
        if not self.brett:
            print("Lager tilfeldig brett")
            self.brett = Brett(lag_tilfeldig_brett())


class SimpleSolver(Solver):
    """Løys eit brett berre ein gang - mest ein test"""

    def solve(self):
        """Løys brettet ein gang og print resultat"""
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


class LinearSolver(Solver):
    """Brute force - løys alle muligheter og print løysinga med færrast steg"""

    def solve(self):
        print("Skal løyse denne:")
        print_brett(self.brett)

        self.best: int = self.brett.rader * self.brett.kolonner + 1
        self.best_log = []

        starttid = time.time()

        for rad in range(self.brett.rader):
            for kol in range(self.brett.kolonner):
                b = Brett(copy_brett(self.brett))
                print(f"Dykker ned frå ({kol}, {rad})…")
                self.solve_fjern(b, kol, rad, [])

        print("Ferdig, etter %.3f sekund" % (time.time() - starttid))
        print(f"Beste resultat var {self.best} steg:")
        from pprint import pprint
        pprint(self.best_log)

    def solve_fjern(self, brett, kol, rad, steps):
        """Løys brettet rekursivt.

        Stopp når brettet er tomt eller du har brukt fleire steg enn noverande
        rekord.

        """
        if len(steps) >= self.best:
            return
        self.counter += 1
        if self.counter % 1000000 == 0:
            print(f"{self.counter} runs")
        # print(f" solve_fjern at ({kol}, {rad}), depth=%d, uid={uid}" %
        #                                           len(steps))
        # print_brett(brett)
        verdi = brett.get(kol, rad)
        steps = steps.copy() + [(kol, rad, verdi)]
        brett.fjern(kol, rad)
        brett.graviter()

        if brett.er_tomt():
            if len(steps) < self.best:
                print("Tomt! Steg: %d" % len(steps))
                self.best = len(steps)
                self.best_log = steps
                from pprint import pprint
                pprint(steps)
        else:
            for rad in range(brett.rader):
                for kol in range(brett.kolonner):
                    verdi = brett.get(kol, rad)
                    if not verdi:
                        continue
                    b = Brett(copy_brett(brett))
                    self.solve_fjern(b, kol, rad, steps)


class MaxFirstSolver(Solver):
    """Brute force, der største grupperingane fjernast først.

    Forsøk på ein _litt_ meir effektiv algoritme, enn `LinearSolver`.

    """

    def solve(self):
        print("Skal løyse denne:")
        print_brett(self.brett)

        self.max_solutions = math.factorial(self.brett.rader *
                                            self.brett.kolonner)
        print("Maks mulige løysingar: {:g}".format(self.max_solutions))
        print()

        self.best: int = self.brett.rader * self.brett.kolonner + 1
        self.best_log = []

        self.starttid = time.time()

        # Oversikt over brett som er besøkt, og kor mange steg for å komme dit.
        # Gjer at kan skippe dersom du treff på eit brett og har fleire steg
        # (sidan du då veit at du ikkje klarer slå førre gjennomgang)
        self.besokt = {}

        for (kol, rad, _) in self.get_pos_of_largest_shape(self.brett):
            b = Brett(copy_brett(self.brett))
            print(f"Dykker ned frå ({kol}, {rad})…")
            self.solve_fjern(b, kol, rad, ())

        print("Ferdig, etter %.3f sekund" % (time.time() - self.starttid))
        print(f"Beste resultat var {self.best} steg:")
        from pprint import pprint
        pprint(self.best_log)

    def get_pos_of_largest_shape(self, brett):
        """Returner liste av `(kol, rad)` utfrå største grupperingane.

        Med grupperinga meinast former som er naboar med like former, slik at å
        fjerne ein vil fjerne flest mogleg.

        """
        ret = []
        seen = set()
        for rad in range(brett.rader):
            for kol in range(brett.kolonner):
                if (kol, rad) in seen:
                    continue
                naboer = brett.get_naboer(kol, rad)
                if len(naboer) > 0:
                    ret.append((kol, rad, len(naboer)))
                for nabo in naboer:
                    seen.add((nabo[0], nabo[1]))
        return sorted(ret, reverse=True, key=lambda x: x[2])

    def heartbeat(self):
        """Print status"""
        brukttid = time.time() - self.starttid
        print(
            f"{self.counter} løysingar (%.6f%%) - %d l/sek" % (
                  (100 * self.counter / self.max_solutions),
                  self.counter / brukttid,
            )
        )

    def solve_fjern(self, brett, kol, rad, steps):
        """Løys brettet rekursivt, men start med største formene først.

        Stopp når brettet er tomt eller du har brukt fleire steg enn noverande
        rekord.

        """
        if len(steps) >= self.best:
            debug(" Gir opp, for mange steg")
            # Dette blir ikkje korrekt, men eit anslag
            self.counter += 1
            return
        brett_tuple = brett.get_hash_base()
        if self.besokt.get(brett_tuple, 9999) < len(steps):
            self.counter += 1
            if DEBUG:
                print(f"solve_fjern({kol}, {rad}), steg=%d" % len(steps))
                print(" Gir opp, har vore her før, og med færre steg")
                print_brett(brett)
            return
        self.besokt[brett_tuple] = len(steps)

        if self.counter % 100000 == 0:
            self.heartbeat()
        if DEBUG:
            debug(f"solve_fjern({kol}, {rad}), steg=%d", len(steps))
            print_brett(brett)
            input()

        verdi = brett.get(kol, rad)
        steps = steps + ((kol, rad, verdi),)
        brett.fjern(kol, rad)
        brett.graviter()

        if brett.er_tomt():
            self.counter += 1
            debug(" tomt!")
            if len(steps) < self.best:
                print("Ny beste: %d steg" % len(steps))
                self.best = len(steps)
                self.best_log = steps
                from pprint import pprint
                pprint(steps)
        else:
            for (kol, rad, _) in self.get_pos_of_largest_shape(brett):
                debug(" sjekk shape i (%d, %d)", kol, rad)
                verdi = brett.get(kol, rad)
                if not verdi:
                    debug(" felt tomt, skipper")
                    continue
                b = Brett(copy_brett(brett))
                self.solve_fjern(b, kol, rad, steps)


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


def copy_brett(brett):
    """Deeper copy av eit brett"""
    if isinstance(brett, Brett):
        brett = brett.brett
    ret = []
    for b in brett:
        ret.append(b.copy())
    return ret


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
        # assert len(data) == self.rader
        # assert len(data[0]) == self.kolonner
        self.brett = data

    def get(self, kolnr, radnr) -> Form:
        assert kolnr >= 0
        assert radnr >= 0
        return self.brett[radnr][kolnr]

    def set(self, kolnr, radnr, verdi: Form):
        assert kolnr >= 0
        assert radnr >= 0
        self.brett[radnr][kolnr] = verdi

    def count(self) -> int:
        """Returner antal former på brettet"""
        ret: int = 0
        for rad in self.brett:
            for kol in rad:
                if kol is not None:
                    ret += 1
        return ret

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

    def tell_naboer(self, kolnr, radnr, sti=()) -> int:
        """Tell naboer som er like med gitt felt"""
        form = self.get(kolnr, radnr)
        if form is None:
            return 0
        sti = sti + ((kolnr, radnr),)
        ret = 1

        # Sjå oppover:
        if (kolnr, radnr - 1) not in sti:
            if radnr > 0 and self.get(kolnr, radnr - 1) == form:
                ret += self.tell_naboer(kolnr, radnr - 1, sti)

        # Sjå nedover
        if (kolnr, radnr + 1) not in sti:
            if radnr + 1 < self.rader and self.get(kolnr, radnr + 1) == form:
                ret += self.tell_naboer(kolnr, radnr + 1, sti)

        # Sjå til venstre
        if (kolnr - 1, radnr) not in sti:
            if kolnr > 0 and self.get(kolnr - 1, radnr) == form:
                ret += self.tell_naboer(kolnr - 1, radnr, sti)

        # Sjå til høgre
        if (kolnr + 1, radnr) not in sti:
            if kolnr + 1 < self.kolonner:
                if self.get(kolnr + 1, radnr) == form:
                    ret += self.tell_naboer(kolnr + 1, radnr, sti)

        return ret

    def get_naboer(self, kolnr, radnr, sti=()):
        """Gi liste over naboer som er like med gitt felt"""
        form = self.get(kolnr, radnr)
        if form is None:
            return ()
        sti = sti + ((kolnr, radnr),)
        ret = ()

        # Sjå oppover:
        if (kolnr, radnr - 1) not in sti:
            if radnr > 0 and self.get(kolnr, radnr - 1) == form:
                ret += self.get_naboer(kolnr, radnr - 1, sti)

        # Sjå nedover
        if (kolnr, radnr + 1) not in sti:
            if radnr + 1 < self.rader and self.get(kolnr, radnr + 1) == form:
                ret += self.get_naboer(kolnr, radnr + 1, sti)

        # Sjå til venstre
        if (kolnr - 1, radnr) not in sti:
            if kolnr > 0 and self.get(kolnr - 1, radnr) == form:
                ret += self.get_naboer(kolnr - 1, radnr, sti)

        # Sjå til høgre
        if (kolnr + 1, radnr) not in sti:
            if kolnr + 1 < self.kolonner:
                if self.get(kolnr + 1, radnr) == form:
                    ret += self.get_naboer(kolnr + 1, radnr, sti)

        return sti + ret

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

    def get_hash_base(self):
        """Returner tuple som kan brukast som hash for set og dict"""
        return tuple(tuple(r) for r in self.brett)
