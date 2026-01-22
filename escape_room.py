import pygame
import math
import random
from queue import PriorityQueue
from collections import deque
import sys

# konfiguracija
SIRINA = 600
REDOVI = 40
INFO_PANEL = 60
VISINA_PROZORA = SIRINA + INFO_PANEL

# boje
BIJELA = (255, 255, 255)      # Prolaz 
CRNA = (20, 20, 20)           # Zid
SIVA = (50, 50, 50)           # Linije mreze
CRVENA = (255, 0, 0)          # Pocetak
ZELENA = (0, 255, 0)          # Cilj 
ZUTA = (255, 255, 0)          # Kljuc
LJUBICASTA = (128, 0, 128)    # Putanja
NARANCASTA = (255, 165, 0)    # Startna pozicija 
TIRKIZNA = (64, 224, 208)     # Otvoreni skup
PLAVA = (0, 100, 255)         # Posjeceni 

class Soba:
    """ Pomoćna klasa za generiranje soba bez preklapanja """
    def __init__(self, x, y, sirina, visina):
        self.x = x
        self.y = y
        self.sirina = sirina
        self.visina = visina
        self.srediste = (x + sirina // 2, y + visina // 2)

    def sijece(self, druga):
        # provjerava preklapanje s drugom sobom
        return (self.x <= druga.x + druga.sirina + 1 and self.x + self.sirina + 1 >= druga.x and
                self.y <= druga.y + druga.visina + 1 and self.y + self.visina + 1 >= druga.y)

class Cvor:
    def __init__(self, red, stup, sirina, ukupno_redova):
        self.red = red
        self.stup = stup
        self.x = red * sirina
        self.y = stup * sirina
        self.boja = BIJELA
        self.susjedi = []
        self.sirina = sirina
        self.ukupno_redova = ukupno_redova

    def dohvati_poziciju(self):
        return self.red, self.stup

    def je_zatvoren(self): return self.boja == PLAVA
    def je_otvoren(self): return self.boja == TIRKIZNA
    def je_prepreka(self): return self.boja == CRNA
    def je_pocetak(self): return self.boja == CRVENA
    def je_kraj(self): return self.boja == ZELENA
    def je_kljuc(self): return self.boja == ZUTA
    def je_put(self): return self.boja == LJUBICASTA

    def resetiraj(self): self.boja = BIJELA
    def postavi_pocetak(self): self.boja = CRVENA
    def postavi_zatvoreno(self): self.boja = PLAVA
    def postavi_otvoreno(self): self.boja = TIRKIZNA
    def postavi_prepreku(self): self.boja = CRNA
    def postavi_kraj(self): self.boja = ZELENA
    def postavi_kljuc(self): self.boja = ZUTA
    def postavi_put(self): self.boja = LJUBICASTA

    def nacrtaj(self, prozor):
        pygame.draw.rect(prozor, self.boja, (self.x, self.y, self.sirina, self.sirina))

    def azuriraj_susjede(self, mreza):
        self.susjedi = []
        if self.red < self.ukupno_redova - 1 and not mreza[self.red + 1][self.stup].je_prepreka():
            self.susjedi.append(mreza[self.red + 1][self.stup])
        if self.red > 0 and not mreza[self.red - 1][self.stup].je_prepreka():
            self.susjedi.append(mreza[self.red - 1][self.stup])
        if self.stup < self.ukupno_redova - 1 and not mreza[self.red][self.stup + 1].je_prepreka():
            self.susjedi.append(mreza[self.red][self.stup + 1])
        if self.stup > 0 and not mreza[self.red][self.stup - 1].je_prepreka():
            self.susjedi.append(mreza[self.red][self.stup - 1])

    def __lt__(self, drugi):
        return False

class RjesavacIgre:
    @staticmethod
    def heuristika(p1, p2):
        x1, y1 = p1; x2, y2 = p2
        return abs(x1 - x2) + abs(y1 - y2)

    @staticmethod
    def ocisti_vizuale_pretrage(mreza, funkcija_crtanja):
        """
        Briše plava/tirkizna polja (pretragu), ali ČUVA PUT (ljubičasto).
        Ovo se koristi NA KRAJU pretrage da se vidi rješenje.
        """
        for red in mreza:
            for tocka in red:
                if (tocka.je_zatvoren() or tocka.je_otvoren()) and not tocka.je_put():
                    tocka.resetiraj()
        funkcija_crtanja()

    @staticmethod
    def rekonstruiraj_put(dosao_od, trenutni, funkcija_crtanja):
        duljina_puta = 0
        while trenutni in dosao_od:
            trenutni = dosao_od[trenutni]
            trenutni.postavi_put()
            duljina_puta += 1
            funkcija_crtanja()
        return duljina_puta

    @staticmethod
    def algoritam_bfs(funkcija_crtanja, mreza, pocetak, kraj):
        red_cekanja = deque([pocetak])
        posjeceni = {pocetak}
        dosao_od = {}
        broj_cvorova = 0
        while red_cekanja:
            for dogadjaj in pygame.event.get():
                if dogadjaj.type == pygame.QUIT: pygame.quit(); sys.exit()
            trenutni = red_cekanja.popleft()
            broj_cvorova += 1
            
            if trenutni == kraj:
                RjesavacIgre.rekonstruiraj_put(dosao_od, kraj, funkcija_crtanja)
                # brišemo nered (plavo), ostavljamo put
                RjesavacIgre.ocisti_vizuale_pretrage(mreza, funkcija_crtanja)
                kraj.postavi_kraj(); pocetak.postavi_pocetak()
                return True, broj_cvorova
            
            for susjed in trenutni.susjedi:
                if susjed not in posjeceni:
                    posjeceni.add(susjed)
                    dosao_od[susjed] = trenutni
                    red_cekanja.append(susjed)
                    susjed.postavi_otvoreno()
            funkcija_crtanja()
            if trenutni != pocetak: trenutni.postavi_zatvoreno()
        return False, broj_cvorova

    @staticmethod
    def algoritam_astar(funkcija_crtanja, mreza, pocetak, kraj):
        brojac = 0
        otvoreni_skup = PriorityQueue()
        otvoreni_skup.put((0, brojac, pocetak))
        dosao_od = {}
        g_trosak = {tocka: float("inf") for red in mreza for tocka in red}
        g_trosak[pocetak] = 0
        f_trosak = {tocka: float("inf") for red in mreza for tocka in red}
        f_trosak[pocetak] = RjesavacIgre.heuristika(pocetak.dohvati_poziciju(), kraj.dohvati_poziciju())
        otvoreni_skup_hash = {pocetak}
        broj_cvorova = 0

        while not otvoreni_skup.empty():
            for dogadjaj in pygame.event.get():
                if dogadjaj.type == pygame.QUIT: pygame.quit(); sys.exit()
            trenutni = otvoreni_skup.get()[2]
            otvoreni_skup_hash.remove(trenutni)
            broj_cvorova += 1
            
            if trenutni == kraj:
                RjesavacIgre.rekonstruiraj_put(dosao_od, kraj, funkcija_crtanja)
                # brišemo nered (plavo), ostavljamo put
                RjesavacIgre.ocisti_vizuale_pretrage(mreza, funkcija_crtanja)
                kraj.postavi_kraj(); pocetak.postavi_pocetak()
                return True, broj_cvorova
            
            for susjed in trenutni.susjedi:
                privremeni_g = g_trosak[trenutni] + 1
                if privremeni_g < g_trosak[susjed]:
                    dosao_od[susjed] = trenutni
                    g_trosak[susjed] = privremeni_g
                    f_trosak[susjed] = privremeni_g + RjesavacIgre.heuristika(susjed.dohvati_poziciju(), kraj.dohvati_poziciju())
                    if susjed not in otvoreni_skup_hash:
                        brojac += 1
                        otvoreni_skup.put((f_trosak[susjed], brojac, susjed))
                        otvoreni_skup_hash.add(susjed)
                        susjed.postavi_otvoreno()
            funkcija_crtanja()
            if trenutni != pocetak: trenutni.postavi_zatvoreno()
        return False, broj_cvorova

# generiranje sobe
def primijeni_sobu_na_mrezu(mreza, soba):
    for x in range(soba.x, soba.x + soba.sirina):
        for y in range(soba.y, soba.y + soba.visina):
            mreza[x][y].resetiraj() 

def stvori_h_tunel(mreza, x1, x2, y):
    for x in range(min(x1, x2), max(x1, x2) + 1):
        mreza[x][y].resetiraj()

def stvori_v_tunel(mreza, y1, y2, x):
    for y in range(min(y1, y2), max(y1, y2) + 1):
        mreza[x][y].resetiraj()

def generiraj_tamnicu(mreza):
    for red in mreza:
        for tocka in red:
            tocka.postavi_prepreku()

    sobe = []
    MAX_SOBA = 25
    MIN_VELICINA = 5
    MAX_VELICINA = 10
    POKUSAJI = 150

    for _ in range(POKUSAJI):
        sirina = random.randint(MIN_VELICINA, MAX_VELICINA)
        visina = random.randint(MIN_VELICINA, MAX_VELICINA)
        x = random.randint(1, REDOVI - sirina - 1)
        y = random.randint(1, REDOVI - visina - 1)
        
        nova_soba = Soba(x, y, sirina, visina)
        
        neuspjelo = False
        for druga in sobe:
            if nova_soba.sijece(druga):
                neuspjelo = True
                break
        
        if not neuspjelo:
            primijeni_sobu_na_mrezu(mreza, nova_soba)
            if len(sobe) > 0:
                prethodna = sobe[-1].srediste
                trenutna = nova_soba.srediste
                if random.randint(0, 1) == 1:
                    stvori_h_tunel(mreza, prethodna[0], trenutna[0], prethodna[1])
                    stvori_v_tunel(mreza, prethodna[1], trenutna[1], trenutna[0])
                else:
                    stvori_v_tunel(mreza, prethodna[1], trenutna[1], prethodna[0])
                    stvori_h_tunel(mreza, prethodna[0], trenutna[0], trenutna[1])
            sobe.append(nova_soba)
            if len(sobe) >= MAX_SOBA:
                break

# pomoćne funkcije
def napravi_mrezu(redovi, sirina):
    mreza = []
    razmak = sirina // redovi
    for i in range(redovi):
        mreza.append([])
        for j in range(redovi):
            tocka = Cvor(i, j, razmak, redovi)
            mreza[i].append(tocka)
    return mreza

def ocisti_samo_put(mreza, pocetak, kraj, kljuc):
    """ Briše sve boje (putanje, open, closed) osim zidova i glavnih točaka """
    for red in mreza:
        for tocka in red:
            if tocka in [pocetak, kraj, kljuc] or tocka.je_prepreka():
                continue
            tocka.resetiraj()

def nacrtaj_linije_mreze(prozor, redovi, sirina):
    razmak = sirina // redovi
    for i in range(redovi):
        pygame.draw.line(prozor, SIVA, (0, i * razmak), (sirina, i * razmak))
        for j in range(redovi):
            pygame.draw.line(prozor, SIVA, (j * razmak, 0), (j * razmak, sirina))

def nacrtaj_prozor(prozor, mreza, redovi, sirina, osnovni_tekst, algo_tekst):
    prozor.fill(BIJELA)
    for red in mreza:
        for tocka in red:
            tocka.nacrtaj(prozor)
    nacrtaj_linije_mreze(prozor, redovi, sirina)
    
    pygame.draw.rect(prozor, CRNA, (0, SIRINA, SIRINA, INFO_PANEL))
    tekst_1 = FONT.render(osnovni_tekst, True, BIJELA)
    prozor.blit(tekst_1, tekst_1.get_rect(center=(SIRINA/2, SIRINA + 20)))
    tekst_2 = FONT.render(algo_tekst, True, ZUTA)
    prozor.blit(tekst_2, tekst_2.get_rect(center=(SIRINA/2, SIRINA + 45)))
    pygame.display.update()

def dohvati_kliknutu_poziciju(pozicija, redovi, sirina):
    razmak = sirina // redovi
    y, x = pozicija
    red = y // razmak; stup = x // razmak
    return red, stup

# glavni program
def glavna_funkcija(prozor, sirina):
    mreza = napravi_mrezu(REDOVI, sirina)
    pocetak = None; kraj = None; kljuc = None
    radi = True
    
    bazni_tekst = "Lijevi klik: Postavi | Desni klik: Briši | G: Generiraj | R: Očisti Put | C: Resetiraj"
    algo_tekst = "RAZMAKNICA: A* Algoritam | B: BFS Algoritam"
    status_tekst = algo_tekst

    while radi:
        nacrtaj_prozor(prozor, mreza, REDOVI, sirina, bazni_tekst, status_tekst)

        for dogadjaj in pygame.event.get():
            if dogadjaj.type == pygame.QUIT: radi = False

            if pygame.mouse.get_pressed()[0]:
                poz = pygame.mouse.get_pos()
                if poz[1] < sirina:
                    red, stup = dohvati_kliknutu_poziciju(poz, REDOVI, sirina)
                    tocka = mreza[red][stup]
                    if not pocetak and tocka != kraj and tocka != kljuc and not tocka.je_prepreka():
                        pocetak = tocka; pocetak.postavi_pocetak()
                    elif not kraj and tocka != pocetak and tocka != kljuc and not tocka.je_prepreka():
                        kraj = tocka; kraj.postavi_kraj()
                    elif not kljuc and tocka != pocetak and tocka != kraj and not tocka.je_prepreka():
                        kljuc = tocka; kljuc.postavi_kljuc()
                    elif tocka != kraj and tocka != pocetak and tocka != kljuc:
                        tocka.postavi_prepreku()

            elif pygame.mouse.get_pressed()[2]:
                poz = pygame.mouse.get_pos()
                if poz[1] < sirina:
                    red, stup = dohvati_kliknutu_poziciju(poz, REDOVI, sirina)
                    tocka = mreza[red][stup]
                    tocka.resetiraj()
                    if tocka == pocetak: pocetak = None
                    if tocka == kraj: kraj = None
                    if tocka == kljuc: kljuc = None

            if dogadjaj.type == pygame.KEYDOWN:
                if dogadjaj.key == pygame.K_c:
                    pocetak = None; kraj = None; kljuc = None
                    mreza = napravi_mrezu(REDOVI, sirina)
                    status_tekst = "Prazna mreža."

                if dogadjaj.key == pygame.K_r:
                    ocisti_samo_put(mreza, pocetak, kraj, kljuc)
                    if pocetak: pocetak.postavi_pocetak()
                    if kraj: kraj.postavi_kraj()
                    if kljuc: kljuc.postavi_kljuc()
                    status_tekst = "Put očišćen."

                if dogadjaj.key == pygame.K_g:
                    pocetak = None; kraj = None; kljuc = None
                    generiraj_tamnicu(mreza)
                    status_tekst = "Nove sobe generirane! Postavi elemente."

                if pocetak and kraj:
                    for red in mreza:
                        for tocka in red: tocka.azuriraj_susjede(mreza)
                    
                    ime_algoritma = ""; posjeceni = 0; uspjeh = False
                    
                    # logika pokretanja
                    if dogadjaj.key == pygame.K_SPACE:
                        ime_algoritma = "A*"
                        ocisti_samo_put(mreza, pocetak, kraj, kljuc)
                        if kljuc:
                            # 1. Pocetak -> Kljuc
                            uspjeh1, posjeceni1 = RjesavacIgre.algoritam_astar(lambda: nacrtaj_prozor(prozor, mreza, REDOVI, sirina, bazni_tekst, "A*: Tražim ključ..."), mreza, pocetak, kljuc)
                            if uspjeh1:
                                # brišemo put do ključa prije nego krenemo na izlaz
                                ocisti_samo_put(mreza, pocetak, kraj, kljuc)
                                kljuc.postavi_kljuc(); pocetak.postavi_pocetak(); kraj.postavi_kraj()
                                
                                # 2. Kljuc -> Kraj
                                uspjeh2, posjeceni2 = RjesavacIgre.algoritam_astar(lambda: nacrtaj_prozor(prozor, mreza, REDOVI, sirina, bazni_tekst, "A*: Idem van..."), mreza, kljuc, kraj)
                                uspjeh = uspjeh2; posjeceni = posjeceni1 + posjeceni2
                        else:
                            uspjeh, posjeceni = RjesavacIgre.algoritam_astar(lambda: nacrtaj_prozor(prozor, mreza, REDOVI, sirina, bazni_tekst, "A*: Tražim izlaz..."), mreza, pocetak, kraj)

                    elif dogadjaj.key == pygame.K_b:
                        ime_algoritma = "BFS"
                        ocisti_samo_put(mreza, pocetak, kraj, kljuc)
                        if kljuc:
                            # 1. Pocetak -> Kljuc
                            uspjeh1, posjeceni1 = RjesavacIgre.algoritam_bfs(lambda: nacrtaj_prozor(prozor, mreza, REDOVI, sirina, bazni_tekst, "BFS: Tražim ključ..."), mreza, pocetak, kljuc)
                            if uspjeh1:
                                # brišemo put do ključa
                                ocisti_samo_put(mreza, pocetak, kraj, kljuc)
                                kljuc.postavi_kljuc(); pocetak.postavi_pocetak(); kraj.postavi_kraj()
                                
                                # 2. Kljuc -> Kraj
                                uspjeh2, posjeceni2 = RjesavacIgre.algoritam_bfs(lambda: nacrtaj_prozor(prozor, mreza, REDOVI, sirina, bazni_tekst, "BFS: Idem van..."), mreza, kljuc, kraj)
                                uspjeh = uspjeh2; posjeceni = posjeceni1 + posjeceni2
                        else:
                            uspjeh, posjeceni = RjesavacIgre.algoritam_bfs(lambda: nacrtaj_prozor(prozor, mreza, REDOVI, sirina, bazni_tekst, "BFS: Tražim izlaz..."), mreza, pocetak, kraj)

                    if ime_algoritma:
                        status_tekst = f"{ime_algoritma}: Gotov! {posjeceni} čvorova." if uspjeh else f"{ime_algoritma}: Nema puta!"

    pygame.quit()

if __name__ == "__main__":
    pygame.init()
    pygame.font.init()
    FONT = pygame.font.SysFont('Arial', 16, bold=True)
    PROZOR = pygame.display.set_mode((SIRINA, VISINA_PROZORA))
    pygame.display.set_caption("Bijeg iz sobe")
    glavna_funkcija(PROZOR, SIRINA)