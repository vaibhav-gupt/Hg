#!/usr/bin/env python3

"""Wahrscheinlichkeiten für Mindestwürfe in einem Pool-System"""

augenzahlen = [1, 2, 3, 4, 5, 6]
ergebnis = {}
max_würfel = 5
max_mindestwurf = 24

for anzahl_würfel in range(max_würfel):
    ergebnis[anzahl_würfel+1] = []
    # erster würfel
    ergebnis[anzahl_würfel+1].extend(augenzahlen)
    for würfel in range(anzahl_würfel):
        erg = []
        for i in ergebnis[anzahl_würfel+1]:
            for j in augenzahlen:
                erg.append(i+j)
        ergebnis[anzahl_würfel+1] = erg
        

erg = []
for mw in range(max_mindestwurf):
    for würfel in ergebnis:
        erg.append(((würfel, mw+1), len([i for i in ergebnis[würfel] if i >= mw+1]) / len(ergebnis[würfel])))

erg.sort()

for würfel_mw, Wahrscheinlichkeit in erg:
    print (würfel_mw[0], würfel_mw[1], Wahrscheinlichkeit)
