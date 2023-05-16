# Popis aplikace

## Základní koncept

Cílem této části projektu je vytvořit grafický program ve kterém bude možné hrát šachy.
Jeho součástí bude uchování současného stavu hry v paměti.
Dále je potřeba aby byl schopen říci zda je daný tah podle pravidel možné provézt
(nejlépe aby byl pro každou figurku schopen vrátit množinu všech možných tahů).
Program bude možné ovládat jak myší, tak i hlasem.

## Použité nástroje

* Jazyky: (POUZE!) [**python 3.11**](https://www.python.org/)
* Knihovna pro zobrazování: (autor zvolí, doporučil bych [pygame](https://www.pygame.org/news))
* API pro hlasové ovládání: (autor zvolí)

## Pravida psaní kódu

* Jednotlivé podčásti implementovat do class.
* Co jeden soubor, to jedna class.
* každou funkci okomentujte a určete datové typy argumentů a výstupu (V angličtině pokud možno)

## USED PACKAGES
"pip install pygame"
"pip install stockfish"
"brew install stockfish / (install stockfish engine)"
"pip install chess"
"pip install pyserial"
"pip install speechrecognition"
"brew install portaudio / sudo apt-get install python3-pyaudio"
"pip install pyaudio"
"pip install pyttsx3"


### DO
```
def is_prime(num: int) -> bool:
    """
    This function determines whether a given number is or is not a prime number.
    :param num: non-zero positive integer. 
    For a number too big this might take too long to compute within our lifetime.
    :return: num is a prime -> True, num is not a prime -> False.
    """
    # ... code ...
    return True
```

### DON'T
```
def is_prime(num):
    # ... code ...
    return True
```
