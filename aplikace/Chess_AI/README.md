# Popis Komponenty

## Základní koncept

Cílem této části projektu je vytvořit třídu, která bude schopna zpracovat vstup z mikrofonu a za využití některého ze speech to text API tento vstup převést na text.
Následně pak tento text převede na jednotlivé šachové tahy.

## Příklad použití
* Uživate vysloví "C2 na C4".
* Program vrátí tuple dvojice 2D souřadnic v podobě ((2, 1), (2, 3)).
Tvar souřadnic: (x, y) kde (0 - 7, 0 - 7) = (A - H, 1 - 8)
