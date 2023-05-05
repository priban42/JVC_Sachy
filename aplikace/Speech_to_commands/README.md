# Popis Komponenty

## Základní koncept

Cílem této části projektu je vytvořit třídu, která bude schopna zpracovat vstup z mikrofonu a za využití některého ze speech to text API tento vstup převést na text.
Následně pak tento text převede na jednotlivé šachové tahy.

## Příklad použití
* Uživate vysloví "C2 na C4".
* Program vrátí tuple dvojice 2D souřadnic v podobě ((2, 1), (2, 3)).<br/>
Tvar souřadnic: (x, y) kde (0 - 7, 0 - 7) = (A - H, 1 - 8)

# How to use
* Commands are given in english, can be said anything containing the two coordinates FIRST where we start SECOND where we go
* E.g. "move this from A3 to maybe A4" will return ((0, 2), (0, 3))

## You might need to run these first
* pip install speechrecognition
* sudo apt-get install python3-pyaudio
* pip install pyaudio
* pip install pyttsx3
