
PROJEKT: DIZAJN I IMPLEMENTACIJA SUSTAVA ZA AUTONOMNO PRETRAŽIVANJE PROSTORA U IGRI "BIJEG IZ SOBE" 

KOLEGIJ: Uvod u umjetnu inteligenciju 

AUTORI: Eva Petrović, Ela Turčec 

DATUM: Siječanj, 2026. 

------------------------------------------------------------

OPIS: 
Aplikacija simulira problem pronalaska puta (pathfinding) u 2D prostoru. 
Agent (AI) mora pronaći optimalan put od starta do cilja, uz opcionalni 
međucilj (ključ) i izbjegavanje prepreka (zidova). 

------------------------------------------------------------ 
PREDUVJETI ZA POKRETANJE 
------------------------------------------------------------ 
Za pokretanje aplikacije potrebno je imati instalirano: 
1. Python (verzija 3.x) 
2. Biblioteku 'pygame' 

------------------------------------------------------------ 
INSTALACIJA POTREBNE BIBLIOTEKE 
------------------------------------------------------- 

Ako nemate instaliranu biblioteku 'pygame', otvorite komandnu liniju 
(Command Prompt / Terminal) i upišite sljedeću naredbu: 

pip install pygame 

------------------------------------------------------------ 
POKRETANJE APLIKACIJE 
------------------------------------------------------------ 
1. Pozicionirajte se u mapu gdje se nalazi ova datoteka. 
2. Pokrenite glavnu skriptu naredbom: 

python escape_room.py 

(Napomena: Ako ste skriptu nazvali drugačije, zamjenite 'escape_room.py' s točnim nazivom vaše datoteke). 

------------------------------------------------------------ 
UPUTE ZA KORIŠTENJE (KONTROLE) 
------------------------------------------------------- 

Interakcija s aplikacijom odvija se pomoću miša i tipkovnice. 

MIŠ: 
* Lijevi klik: Postavljanje elemenata. 
- Prvi klik postavlja START (Narančasta) 
- Drugi klik postavlja CILJ (Zelena/Tirkizna) 
- Treći klik postavlja KLJUČ (Žuta) - opcionalno 
- Daljnji klikovi postavljaju ZIDOVE (Crna) 
* Desni klik: Brisanje elemenata (vraća polje u bijelu boju). 

TIPKOVNICA (Algoritmi i naredbe): 
* SPACE (Razmaknica): Pokreni A* (A-Star) algoritam. 
* B: Pokreni BFS (Breadth-First Search) algoritam. 
* G: Generiraj proceduralnu tamnicu (nasumične sobe). 
* R: Očisti samo putanju (zadržava zidove, start i cilj). 
* C: Očisti sve (potpuni reset mreže). 

------------------------------------------------------------ 
LEGENDA BOJA (VIZUALIZACIJA) 
------------------------------------------------------------ 
* Tirkizna: Otvoreni skup (čvorovi koji se razmatraju) 
* Plava: Zatvoreni skup (posjećeni čvorovi) 
* Ljubičasta: Konačni pronađeni put 
* Crna: Prepreka (Zid)
