# Popis Komponenty

## Základní koncept

Cílem této části projektu je vytvořit třídu, která bude schopna uložit stav šachovnice (pozice všech figurek, který hráč je na řadě).
Dále pro každou figurku bude schopna najít množinu všech validních tahů. 
Program obdrží tah ve tvaru 2 pozic na šachovnici, kde 1. pozice představuje pozici figurky se kterou se bude táhnout a 2. pozice místo kam se bude táhnout.
Program pak musí být schopen určit zda je tento tah provést. Dále jej provede a změni tak stav šachovnice.

## Příklad použití
### is_move_valid(move)
* Program dostance vstup ((2, 1), (2, 3)).
* vrátí True/False v závislosti na validitě tahu v daném stavu.
### do_move(move)
* Program dostance vstup ((2, 1), (2, 3)).
* posune figurku.
### get_all_valid_moves(position)
* Program dostance pozici figurky.
* vráti seznam všech pozic na které může figurka v daný moment táhnout.

## Obecné rady
* Vytvořit třídu pro Hrací desku, která bude obsahovat 2d pole se všemi figurkami a také výše zmíněné metody.
* Vytvořit třídu pro obecnou figurku a z ní dědit pro ostatní specifické figurky.
