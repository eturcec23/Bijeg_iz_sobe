#  PROJEKT: Dizajn i implementacija sustava za autonomno pretraživanje prostora  
##  Igra: Bijeg iz sobe

*Kolegij:* Uvod u umjetnu inteligenciju  
*Autori:* Eva Petrović, Ela Turčec  
*Datum:* Siječanj, 2026.

---

##  Opis projekta

Aplikacija simulira problem *pronalaženja puta (pathfinding)* u *2D prostoru*.  
Agent (AI) mora pronaći *optimalan put* od početne točke do cilja, uz mogućnost:

- prolaska kroz *međucilj (ključ)*  
- *izbjegavanja prepreka (zidova)*  

Projekt demonstrira rad osnovnih algoritama pretraživanja prostora.

---

##  Preduvjeti za pokretanje

Za pokretanje aplikacije potrebno je imati instalirano:

1. *Python* (verzija 3.x)
2. *pygame* biblioteku

---

##  Instalacija potrebne biblioteke

Ako nemate instaliranu biblioteku 'pygame', otvorite komandnu liniju 
(Command Prompt / Terminal) i upišite sljedeću naredbu: 

pip install pygame 

##  Pokretanje aplikacije

1. Pozicionirajte se u mapu gdje se nalazi projektna datoteka  
2. Pokrenite glavnu skriptu naredbom:


##  Upute za korištenje (kontrole)

Interakcija s aplikacijom odvija se pomoću *miša i tipkovnice*.

---

###  Miš

- *Lijevi klik* – postavljanje elemenata:
  - *Prvi klik:* START (narančasta)
  - *Drugi klik:* CILJ (zelena / tirkizna)
  - *Treći klik:* KLJUČ (žuta) – opcionalno
  - *Daljnji klikovi:* ZIDOVI (crna)

- *Desni klik* – brisanje elemenata  
  (polje se vraća u bijelu boju)

---

###  Tipkovnica (algoritmi i naredbe)

- *SPACE (razmaknica):* Pokreni *A\** (A-Star) algoritam
- *B:* Pokreni *BFS* (Breadth-First Search) algoritam
- *G:* Generiraj *proceduralnu tamnicu* (nasumične sobe)
- *R:* Očisti samo *putanju*  
  (zadržava zidove, start i cilj)
- *C:* Očisti sve  
  (potpuni reset mreže)

---

##  Legenda boja (vizualizacija)

- *Tirkizna:* Otvoreni skup (čvorovi koji se razmatraju)
- *Plava:* Zatvoreni skup (posjećeni čvorovi)
- *Ljubičasta:* Konačni pronađeni put
- *Crna:* Prepreka (zid)
