import pygame
import sys
import os
import json
import random
import math

pygame.init()
pygame.mixer.init()

# === NASTAVENÍ OKNA ===
SIRKA = 480
VYSKA = 854
FPS = 60
NAZEV = "Lukša - Cesta k Rapové Slávě"

obrazovka = pygame.display.set_mode((SIRKA, VYSKA))
pygame.display.set_caption(NAZEV)
hodiny = pygame.time.Clock()

# === BARVY ===
CERNA       = (0, 0, 0)
BILA        = (255, 255, 255)
ZLATA       = (255, 215, 0)
TMAVE_SEDA  = (30, 30, 30)
SEDA        = (80, 80, 80)
SVETLE_SEDA = (180, 180, 180)
CERVENA     = (220, 50, 50)
ZELENA      = (50, 200, 80)
MODRA       = (50, 100, 220)
ORANZOVA    = (255, 140, 0)
FIALOVA     = (130, 50, 200)
RUZOVA      = (255, 100, 180)
TMAVE_MODRA = (10, 20, 60)

# === ULOŽENÍ / NAČTENÍ ===
SAVE_SOUBOR = "save.json"

def uloz_hru(data):
    with open(SAVE_SOUBOR, "w") as f:
        json.dump(data, f)

def nacti_hru():
    if os.path.exists(SAVE_SOUBOR):
        with open(SAVE_SOUBOR, "r") as f:
            return json.load(f)
    return None

# === NAČÍTÁNÍ TEXTUR ===
def nacti_obrazek(cesta, velikost=None):
    """Načte obrázek nebo vrátí None pokud neexistuje."""
    if os.path.exists(cesta):
        img = pygame.image.load(cesta).convert_alpha()
        if velikost:
            img = pygame.transform.scale(img, velikost)
        return img
    return None

def vytvor_placeholder(velikost, barva, text="?"):
    """Vytvoří barevný placeholder místo chybějící textury."""
    surf = pygame.Surface(velikost, pygame.SRCALPHA)
    surf.fill(barva)
    if text:
        font = pygame.font.SysFont("arial", min(velikost[0], velikost[1]) // 3)
        txt = font.render(text, True, BILA)
        r = txt.get_rect(center=(velikost[0]//2, velikost[1]//2))
        surf.blit(txt, r)
    return surf

class SpravceTextur:
    def __init__(self):
        self.textury = {}
        self._nacti_vse()

    def _nacti_vse(self):
        definice = {
            # Postavy
            "luksa":         ("assets/postavy/luksa.png",          (80, 120)),
            "luksa_vozik":   ("assets/postavy/luksa_vozik.png",     (100, 100)),
            "opicak":        ("assets/postavy/opicak.png",          (80, 120)),
            "stika":         ("assets/postavy/stika.png",           (80, 120)),
            "zakaznik":      ("assets/postavy/zakaznik.png",        (60, 90)),
            # Prostředí
            "pozadi_menu":   ("assets/prostredi/pozadi_menu.png",   (SIRKA, VYSKA)),
            "pozadi_ulice":  ("assets/prostredi/pozadi_ulice.png",  (SIRKA, VYSKA)),
            "pozadi_pokoj":  ("assets/prostredi/pozadi_pokoj.png",  (SIRKA, VYSKA)),
            "pozadi_sklad":  ("assets/prostredi/pozadi_sklad.png",  (SIRKA, VYSKA)),
            "dum":           ("assets/prostredi/dum.png",           (200, 180)),
            "vozik":         ("assets/prostredi/vozik.png",         (90, 70)),
            "noviny":        ("assets/prostredi/noviny.png",        (40, 50)),
            "pocitac":       ("assets/prostredi/pocitac.png",       (120, 100)),
            "mikrofon":      ("assets/prostredi/mikrofon.png",      (50, 80)),
            # UI
            "ui_panel":      ("assets/ui/ui_panel.png",             (SIRKA, 100)),
            "tlacitko":      ("assets/ui/tlacitko.png",             (200, 60)),
            "mince":         ("assets/ui/mince.png",                (30, 30)),
            "xp_ikona":      ("assets/ui/xp_ikona.png",             (30, 30)),
            "srdce":         ("assets/ui/srdce.png",                (30, 30)),
            "logo":          ("assets/ui/logo.png",                 (320, 120)),
            # Ikony
            "ikona_rap":     ("assets/ikony/ikona_rap.png",         (60, 60)),
            "ikona_noviny":  ("assets/ikony/ikona_noviny.png",      (60, 60)),
            "ikona_sklad":   ("assets/ikony/ikona_sklad.png",       (60, 60)),
            "ikona_vikend":  ("assets/ikony/ikona_vikend.png",      (60, 60)),
            # Efekty
            "hvezda":        ("assets/efekty/hvezda.png",           (40, 40)),
            "noty":          ("assets/efekty/noty.png",             (50, 50)),
            "baloncek_rec":  ("assets/efekty/baloncek_rec.png",     (180, 80)),
        }
        placeholdery = {
            "luksa":         (ORANZOVA,  "L"),
            "luksa_vozik":   (ORANZOVA,  "L🛒"),
            "opicak":        (ZELENA,    "🐒"),
            "stika":         (RUZOVA,    "S"),
            "zakaznik":      (SVETLE_SEDA,"Z"),
            "pozadi_menu":   (TMAVE_MODRA,""),
            "pozadi_ulice":  ((30,60,30),""),
            "pozadi_pokoj":  ((50,30,20),""),
            "pozadi_sklad":  ((40,40,60),""),
            "dum":           ((100,60,40),"🏠"),
            "vozik":         (SEDA,      "🛒"),
            "noviny":        (BILA,      "📰"),
            "pocitac":       (TMAVE_SEDA,"💻"),
            "mikrofon":      (CERVENA,   "🎤"),
            "ui_panel":      ((20,20,40),""),
            "tlacitko":      (FIALOVA,   ""),
            "mince":         (ZLATA,     "$"),
            "xp_ikona":      (ZELENA,    "XP"),
            "srdce":         (CERVENA,   "♥"),
            "logo":          (TMAVE_MODRA,"LUKŠA RAP"),
            "ikona_rap":     (FIALOVA,   "🎤"),
            "ikona_noviny":  (BILA,      "📰"),
            "ikona_sklad":   (MODRA,     "📦"),
            "ikona_vikend":  (ZELENA,    "🐒"),
            "hvezda":        (ZLATA,     "★"),
            "noty":          (FIALOVA,   "♪"),
            "baloncek_rec":  (BILA,      ""),
        }

        for klic, (cesta, velikost) in definice.items():
            img = nacti_obrazek(cesta, velikost)
            if img is None:
                bar, txt = placeholdery.get(klic, (SEDA, "?"))
                img = vytvor_placeholder(velikost, bar, txt)
            self.textury[klic] = img

    def get(self, klic):
        return self.textury.get(klic)

# === FONTY ===
def nacti_font(velikost, tucny=False, styl="normal"):
    """
    styl="titulek"  → pro hlavní nadpisy (Lukša, Opičák...) – velký, výrazný
    styl="akce"     → pro akční tlačítka (Připravit noviny...) – čitelný, tučný
    styl="menu"     → pro menu tlačítka – OK, necháme jak bylo
    styl="normal"   → běžný text
    """
    if styl == "titulek":
        # Pro nadpisy: Bebas Neue styl – velká písmena, úzký, street look
        kandidati = ["Bebas Neue", "Impact", "Anton", "Oswald", "Arial Black", "Arial Narrow"]
    elif styl == "akce":
        # Pro akce/tlačítka: čistý tučný bez serify
        kandidati = ["Montserrat", "Nunito", "Trebuchet MS", "Verdana", "Tahoma", "Arial"]
    elif styl == "menu":
        # Menu tlačítka – necháme jak bylo (funguje dobře)
        kandidati = ["Impact", "Arial Black", "Arial"]
    else:
        kandidati = ["Segoe UI", "Trebuchet MS", "Verdana", "Arial"]

    for nazev in kandidati:
        try:
            f = pygame.font.SysFont(nazev, velikost, bold=tucny)
            if f:
                return f
        except:
            continue
    return pygame.font.Font(None, velikost)

# Fonty podle role
font_titulek = nacti_font(58, True,  styl="titulek")   # LUKŠA, OPIČÁK – velké nadpisy
font_velky   = nacti_font(46, True,  styl="titulek")   # Sekce titulky
font_stredni = nacti_font(30, True,  styl="akce")      # Akce, tlačítka aktivit
font_maly    = nacti_font(22, False, styl="normal")     # Popisky
font_mini    = nacti_font(17, False, styl="normal")     # Drobný text
font_menu    = nacti_font(24, True,  styl="menu")       # Menu tlačítka (bylo dobré)

# === POMOCNÉ FUNKCE ===
def kresli_text(povrch, text, x, y, font, barva=BILA, stred=False, stit=True):
    if stit:
        stit_txt = font.render(text, True, CERNA)
        r = stit_txt.get_rect()
        if stred:
            r.centerx = x
            r.centery = y + 2
        else:
            r.topleft = (x+2, y+2)
        povrch.blit(stit_txt, r)
    txt = font.render(text, True, barva)
    r2 = txt.get_rect()
    if stred:
        r2.centerx = x
        r2.centery = y
    else:
        r2.topleft = (x, y)
    povrch.blit(txt, r2)

def kresli_obdel_zaobleny(povrch, barva, rect, polomer=12, alpha=255):
    surf = pygame.Surface((rect[2], rect[3]), pygame.SRCALPHA)
    pygame.draw.rect(surf, (*barva, alpha), (0, 0, rect[2], rect[3]), border_radius=polomer)
    povrch.blit(surf, (rect[0], rect[1]))

def kresli_tlacitko(povrch, text, rect, barva_zak, barva_txt=BILA, aktivni=True, font=None):
    if font is None:
        font = font_maly
    alfa = 255 if aktivni else 120
    kresli_obdel_zaobleny(povrch, barva_zak, rect, 10, alfa)
    pygame.draw.rect(povrch, BILA if aktivni else SEDA,
                     rect, 2, border_radius=10)
    kresli_text(povrch, text, rect[0]+rect[2]//2, rect[1]+rect[3]//2,
                font, barva_txt, stred=True)

def blikani(cas, interval=500):
    return (cas // interval) % 2 == 0

# === HERNÍ STAV ===
class HerniStav:
    def __init__(self):
        self.vynuluj()

    def vynuluj(self):
        self.penize = 0
        self.cil_pocitac = 8000
        self.xp = 0
        self.uroven = 1
        self.den = 1
        self.vikend = False
        self.opicak_navsteva = False
        self.stika_rada = 0

        # Dovednosti
        self.dovednost_rap     = 1
        self.dovednost_roznos  = 1
        self.dovednost_sklad   = 1

        # Statistiky dne
        self.noviny_sklady = 0
        self.noviny_doneseny = 0
        self.energie = 100
        self.nastejleni = False  # noviny připraveny?

        # Příběh / dialogy
        self.dialog_fronta = []
        self.dialog_aktivni = False
        self.dialog_index = 0

        # Fáze dne
        self.faze = "rano"  # rano, sklad, roznos, vecer, noc

        # Rap kariéra
        self.tracky = 0
        self.fans = 0
        self.rap_session_dnes = False

    def ziskej_xp_pro_uroven(self):
        return self.uroven * 100

    def pridej_xp(self, mnozstvi):
        self.xp += mnozstvi
        if self.xp >= self.ziskej_xp_pro_uroven():
            self.xp -= self.ziskej_xp_pro_uroven()
            self.uroven += 1
            return True
        return False

    def je_vikend(self):
        return self.den % 7 in (0, 6)

    def jako_slovnik(self):
        return self.__dict__.copy()

    def nacti_ze_slovniku(self, d):
        for k, v in d.items():
            setattr(self, k, v)

# =============================
#   SCÉNY
# =============================

class Scena:
    def __init__(self, hra):
        self.hra = hra

    def zpracuj_udalost(self, udalost): pass
    def aktualizuj(self, dt): pass
    def kresli(self, povrch): pass


# === MENU ===
class ScenaMenu(Scena):
    def __init__(self, hra):
        super().__init__(hra)
        self.cas = 0
        self.tlacitka = [
            ("🎤  NOVÁ HRA",    FIALOVA,  self._nova_hra),
            ("💾  POKRAČOVAT",  MODRA,    self._pokracovat),
            ("ℹ️   O HŘE",       SEDA,     self._o_hre),
        ]

    def _nova_hra(self):
        self.hra.stav.vynuluj()
        self.hra.zmen_scenu("uvod")

    def _pokracovat(self):
        data = nacti_hru()
        if data:
            self.hra.stav.nacti_ze_slovniku(data)
            self.hra.zmen_scenu("mapa")
        else:
            self.hra.zprava = "Žádná uložená hra!"

    def _o_hre(self):
        self.hra.zmen_scenu("o_hre")

    def zpracuj_udalost(self, udalost):
        if udalost.type == pygame.MOUSEBUTTONDOWN:
            mx, my = udalost.pos
            for i, (text, barva, akce) in enumerate(self.tlacitka):
                rect = (SIRKA//2 - 160, 420 + i*90, 320, 65)
                if (rect[0] <= mx <= rect[0]+rect[2] and
                    rect[1] <= my <= rect[1]+rect[3]):
                    akce()

    def aktualizuj(self, dt):
        self.cas += dt

    def kresli(self, povrch):
        povrch.fill(TMAVE_MODRA)
        # Animované hvězdy v pozadí
        random.seed(42)
        for i in range(60):
            x = random.randint(0, SIRKA)
            y = random.randint(0, VYSKA)
            r = random.randint(1, 3)
            jas = int(128 + 127 * math.sin(self.cas/800 + i))
            pygame.draw.circle(povrch, (jas, jas, jas), (x, y), r)

        # Logo
        logo = self.hra.textury.get("logo")
        povrch.blit(logo, (SIRKA//2 - logo.get_width()//2, 80))

        # Titulek
        kresli_text(povrch, "LUKŠA", SIRKA//2, 200, font_titulek, ZLATA, stred=True)
        kresli_text(povrch, "Cesta k Rapové Slávě", SIRKA//2, 262, font_maly, SVETLE_SEDA, stred=True)

        # Postavička Lukši
        luksa = self.hra.textury.get("luksa")
        scale = 0.9 + 0.1 * math.sin(self.cas / 600)
        w, h = int(luksa.get_width()*scale), int(luksa.get_height()*scale)
        luksa_s = pygame.transform.scale(luksa, (w, h))
        povrch.blit(luksa_s, (SIRKA//2 - w//2, 300))

        # Tlačítka
        for i, (text, barva, _) in enumerate(self.tlacitka):
            rect = (SIRKA//2 - 160, 420 + i*90, 320, 65)
            kresli_tlacitko(povrch, text, rect, barva, font=font_menu)

        if self.hra.zprava:
            kresli_text(povrch, self.hra.zprava, SIRKA//2, VYSKA-40,
                        font_maly, CERVENA, stred=True)


# === ÚVOD / PŘÍBĚH ===
class ScenaUvod(Scena):
    DIALOGY = [
        ("Lukša", "Jsem Lukša. Rap je můj život, bro."),
        ("Lukša", "Ale k nahrávání potřebuju počítač..."),
        ("Lukša", "Stojí 8000 Kč. Budu muset vydělat!"),
        ("Lukša", "Mám vozík. Budu roznášet noviny!"),
        ("Lukša", "Každý večer musím noviny připravit..."),
        ("Lukša", "Složit, seřadit, naskládat do vozíku."),
        ("Lukša", "A pak ráno je rozvést!"),
        ("Opičák", "Heeey! Přijedu za tebou na víkend!"),
        ("Lukša", "Opičák! Vždycky vítaný, bro!"),
        ("Opičák", "Jedu za Štikou, ale přespím u tebe 😄"),
        ("Lukša", "Pojďme na to. Rap kariéra čeká!"),
    ]

    def __init__(self, hra):
        super().__init__(hra)
        self.index = 0
        self.cas = 0
        self.zobrazeny_text = ""
        self.psani_cas = 0
        self.psani_index = 0

    def zpracuj_udalost(self, udalost):
        if udalost.type in (pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN):
            if self.psani_index < len(self.DIALOGY[self.index][1]):
                self.psani_index = len(self.DIALOGY[self.index][1])
            else:
                self.index += 1
                if self.index >= len(self.DIALOGY):
                    self.hra.zmen_scenu("mapa")
                else:
                    self.psani_index = 0

    def aktualizuj(self, dt):
        self.cas += dt
        if self.index < len(self.DIALOGY):
            cil = self.DIALOGY[self.index][1]
            if self.psani_index < len(cil):
                self.psani_cas += dt
                if self.psani_cas >= 35:
                    self.psani_cas = 0
                    self.psani_index += 1

    def kresli(self, povrch):
        povrch.fill(TMAVE_MODRA)
        if self.index >= len(self.DIALOGY):
            return

        mluvci, text = self.DIALOGY[self.index]
        zobrazeny = text[:self.psani_index]

        # Pozadí
        kresli_obdel_zaobleny(povrch, (10,10,40), (0,0,SIRKA,VYSKA), 0, 255)

        # Postava
        if mluvci == "Lukša":
            img = self.hra.textury.get("luksa")
            barva_jmena = ZLATA
        elif mluvci == "Opičák":
            img = self.hra.textury.get("opicak")
            barva_jmena = ZELENA
        else:
            img = self.hra.textury.get("luksa")
            barva_jmena = BILA

        # Animace vstupu postavy
        cil_x = SIRKA//2 - img.get_width()//2
        povrch.blit(img, (cil_x, 200))

        # Dialog box
        kresli_obdel_zaobleny(povrch, (20,20,60), (20, VYSKA-260, SIRKA-40, 220), 16, 230)
        pygame.draw.rect(povrch, ZLATA, (20, VYSKA-260, SIRKA-40, 220), 2, border_radius=16)

        kresli_text(povrch, mluvci, 50, VYSKA-245, font_titulek, barva_jmena)

        # Zalamování textu
        slova = zobrazeny.split(" ")
        radky = []
        radek = ""
        for slovo in slova:
            test = radek + " " + slovo if radek else slovo
            if font_maly.size(test)[0] < SIRKA - 80:
                radek = test
            else:
                radky.append(radek)
                radek = slovo
        if radek:
            radky.append(radek)

        for i, r in enumerate(radky[:4]):
            kresli_text(povrch, r, 40, VYSKA-200 + i*30, font_maly)

        # Pokračovat
        if self.psani_index >= len(text) and blikani(self.cas):
            kresli_text(povrch, "▶ Klepni pro pokračování",
                        SIRKA-20, VYSKA-50, font_mini, SVETLE_SEDA,
                        stred=False)

        # Číslo dialogu
        kresli_text(povrch, f"{self.index+1}/{len(self.DIALOGY)}",
                    SIRKA//2, VYSKA-40, font_mini, SEDA, stred=True)


# === MAPA / VÝBĚR AKTIVITY ===
class ScenaMapa(Scena):
    def __init__(self, hra):
        super().__init__(hra)
        self.cas = 0
        self._postav_akce()

    def _postav_akce(self):
        st = self.hra.stav
        self.akce = []

        if st.faze == "rano":
            self.akce = [
                {
                    "text": "📦 Připravit noviny",
                    "popis": "Složit a naskládat noviny do vozíku",
                    "barva": MODRA,
                    "ikona": "ikona_sklad",
                    "scena": "sklad",
                    "dostupna": not st.nastejleni,
                },
                {
                    "text": "🛒 Roznést noviny",
                    "popis": f"Doručit noviny zákazníkům ({st.noviny_doneseny}/10)",
                    "barva": ZELENA,
                    "ikona": "ikona_noviny",
                    "scena": "roznos",
                    "dostupna": st.nastejleni and st.noviny_doneseny < 10,
                },
            ]
        if st.faze in ("rano", "vecer"):
            self.akce.append({
                "text": "🎤 Rappovat",
                "popis": "Trénuj dovednosti a piš texty",
                "barva": FIALOVA,
                "ikona": "ikona_rap",
                "scena": "rap",
                "dostupna": st.energie > 10,
            })

        if st.je_vikend():
            self.akce.append({
                "text": "🐒 Opičák přijel!",
                "popis": "Povídej si s Opičákem a Štikou",
                "barva": ORANZOVA,
                "ikona": "ikona_vikend",
                "scena": "navsteva",
                "dostupna": True,
            })

        self.akce.append({
            "text": "😴 Jít spát",
            "popis": "Další den (obnoví energii)",
            "barva": TMAVE_SEDA,
            "ikona": None,
            "scena": None,
            "dostupna": True,
        })

    def zpracuj_udalost(self, udalost):
        if udalost.type == pygame.MOUSEBUTTONDOWN:
            mx, my = udalost.pos
            for i, akce in enumerate(self.akce):
                rect = (20, 180 + i * 110, SIRKA - 40, 95)
                if (rect[0] <= mx <= rect[0]+rect[2] and
                    rect[1] <= my <= rect[1]+rect[3] and akce["dostupna"]):
                    if akce["scena"] is None:
                        self._dalsi_den()
                    else:
                        self.hra.zmen_scenu(akce["scena"])

    def _dalsi_den(self):
        st = self.hra.stav
        st.den += 1
        st.energie = 100
        st.nastejleni = False
        st.noviny_doneseny = 0
        st.noviny_sklady = 0
        st.faze = "rano"
        st.rap_session_dnes = False
        st.opicak_navsteva = st.je_vikend()
        uloz_hru(st.jako_slovnik())
        self._postav_akce()

    def aktualizuj(self, dt):
        self.cas += dt
        self._postav_akce()

    def kresli(self, povrch):
        st = self.hra.stav
        bg = self.hra.textury.get("pozadi_pokoj")
        povrch.blit(bg, (0, 0))

        # Tmavý overlay
        overlay = pygame.Surface((SIRKA, VYSKA), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        povrch.blit(overlay, (0, 0))

        # Hlavička
        kresli_obdel_zaobleny(povrch, (10,10,40), (0, 0, SIRKA, 170), 0, 220)
        kresli_text(povrch, f"DEN {st.den}", SIRKA//2, 12, font_velky, ZLATA, stred=True)

        # Lukša
        luksa = self.hra.textury.get("luksa")
        povrch.blit(luksa, (10, 15))

        # Statistiky
        mince = self.hra.textury.get("mince")
        povrch.blit(mince, (100, 20))
        kresli_text(povrch, f"{st.penize} / {st.cil_pocitac} Kč",
                    135, 22, font_maly, ZLATA)

        # Progress bar peněz
        prog = min(st.penize / st.cil_pocitac, 1.0)
        pygame.draw.rect(povrch, SEDA, (100, 52, SIRKA-120, 16), border_radius=8)
        if prog > 0:
            pygame.draw.rect(povrch, ZLATA, (100, 52, int((SIRKA-120)*prog), 16), border_radius=8)
        kresli_text(povrch, "💻 Cíl: počítač", 100, 70, font_mini, SVETLE_SEDA)

        # Energie
        e_barva = ZELENA if st.energie > 50 else ORANZOVA if st.energie > 20 else CERVENA
        pygame.draw.rect(povrch, SEDA, (100, 95, SIRKA-120, 14), border_radius=7)
        pygame.draw.rect(povrch, e_barva, (100, 95, int((SIRKA-120) * st.energie/100), 14), border_radius=7)
        kresli_text(povrch, f"⚡ Energie: {st.energie}%", 100, 112, font_mini, e_barva)

        # Fáze dne
        faze_txt = {"rano": "🌅 Ráno", "vecer": "🌙 Večer", "noc": "🌑 Noc"}.get(st.faze, "")
        kresli_text(povrch, faze_txt, SIRKA-10, 140, font_mini, SVETLE_SEDA, stred=False)

        # Akce
        for i, akce in enumerate(self.akce):
            y = 180 + i * 110
            barva = akce["barva"] if akce["dostupna"] else SEDA
            alfa = 255 if akce["dostupna"] else 140
            kresli_obdel_zaobleny(povrch, barva, (20, y, SIRKA-40, 95), 14, alfa)
            pygame.draw.rect(povrch, BILA if akce["dostupna"] else SEDA,
                             (20, y, SIRKA-40, 95), 2, border_radius=14)

            if akce["ikona"]:
                ik = self.hra.textury.get(akce["ikona"])
                povrch.blit(ik, (30, y + 17))
                kresli_text(povrch, akce["text"], 100, y+16, font_stredni,
                            BILA if akce["dostupna"] else SVETLE_SEDA)
            else:
                kresli_text(povrch, akce["text"], 30, y+16, font_stredni,
                            BILA if akce["dostupna"] else SVETLE_SEDA)

            kresli_text(povrch, akce["popis"], 30, y+56, font_mini,
                        SVETLE_SEDA if akce["dostupna"] else SEDA)

        # Výhra - koupili jsme počítač!
        if st.penize >= st.cil_pocitac:
            self.hra.zmen_scenu("vyhral")


# === SKLAD - Příprava novin ===
class ScenaSklad(Scena):
    CELKEM_NOVIN = 50
    BONUS_ZA_RYCHLOST = 5

    def __init__(self, hra):
        super().__init__(hra)
        self.cas = 0
        self.noviny = []
        self.cas_skladani = 0
        self.sklozene = 0
        self.cil = self.CELKEM_NOVIN
        self.hotovo = False
        self.cas_hotovo = 0
        self._generuj_noviny()

    def _generuj_noviny(self):
        self.noviny = []
        for i in range(self.cil):
            x = random.randint(30, SIRKA - 70)
            y = random.randint(200, VYSKA - 150)
            uhel = random.randint(-30, 30)
            self.noviny.append({
                "x": x, "y": y, "uhel": uhel,
                "vybrana": False, "animace": 0
            })

    def zpracuj_udalost(self, udalost):
        if self.hotovo:
            if udalost.type == pygame.MOUSEBUTTONDOWN:
                self.hra.stav.nastejleni = True
                self.hra.stav.energie -= 20
                self.hra.stav.noviny_sklady = self.sklozene
                self.hra.stav.faze = "rano"
                xp_bonus = max(0, (self.CELKEM_NOVIN - self.cas_skladani // 1000) * 2)
                self.hra.stav.pridej_xp(30 + xp_bonus)
                self.hra.zmen_scenu("mapa")
            return

        if udalost.type == pygame.MOUSEBUTTONDOWN:
            mx, my = udalost.pos
            for n in reversed(self.noviny):
                if not n["vybrana"]:
                    r = pygame.Rect(n["x"]-20, n["y"]-25, 40, 50)
                    if r.collidepoint(mx, my):
                        n["vybrana"] = True
                        n["animace"] = 0
                        self.sklozene += 1
                        pygame.event.post(pygame.event.Event(pygame.USEREVENT,
                                                              {"akce": "noviny_klik"}))
                        if self.sklozene >= self.cil:
                            self.hotovo = True
                            self.cas_hotovo = self.cas
                        break

    def aktualizuj(self, dt):
        self.cas += dt
        if not self.hotovo:
            self.cas_skladani += dt
        for n in self.noviny:
            if n["vybrana"]:
                n["animace"] = min(n["animace"] + dt / 200, 1.0)

    def kresli(self, povrch):
        bg = self.hra.textury.get("pozadi_sklad")
        povrch.blit(bg, (0, 0))

        overlay = pygame.Surface((SIRKA, VYSKA), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 100))
        povrch.blit(overlay, (0, 0))

        # Hlavička
        kresli_obdel_zaobleny(povrch, (10,10,50), (0, 0, SIRKA, 70), 0, 220)
        kresli_text(povrch, "PŘÍPRAVA NOVIN", SIRKA//2, 10, font_velky, ZLATA, stred=True)
        kresli_text(povrch, f"Naskládáno: {self.sklozene} / {self.cil}",
                    SIRKA//2, 42, font_maly, BILA, stred=True)

        # Progress
        prog = self.sklozene / self.cil
        pygame.draw.rect(povrch, SEDA, (20, 75, SIRKA-40, 18), border_radius=9)
        if prog > 0:
            pygame.draw.rect(povrch, MODRA, (20, 75, int((SIRKA-40)*prog), 18), border_radius=9)

        # Noviny
        noviny_img = self.hra.textury.get("noviny")
        for n in self.noviny:
            if not n["vybrana"]:
                surf = pygame.transform.rotate(noviny_img, n["uhel"])
                povrch.blit(surf, (n["x"] - surf.get_width()//2,
                                   n["y"] - surf.get_height()//2))
            elif n["animace"] < 1.0:
                scale = 1.0 - n["animace"]
                w = max(1, int(noviny_img.get_width() * scale))
                h = max(1, int(noviny_img.get_height() * scale))
                surf = pygame.transform.scale(noviny_img, (w, h))
                povrch.blit(surf, (n["x"] - w//2, n["y"] - h//2))

        # Navigace / vozík cíl
        vozik = self.hra.textury.get("vozik")
        povrch.blit(vozik, (SIRKA - 110, VYSKA - 90))
        kresli_text(povrch, "👆 Klikej na noviny!", SIRKA//2,
                    VYSKA - 50, font_maly, SVETLE_SEDA, stred=True)

        # Hotovo overlay
        if self.hotovo:
            kresli_obdel_zaobleny(povrch, (0,80,0), (40, VYSKA//2-80, SIRKA-80, 160), 20, 230)
            pygame.draw.rect(povrch, ZELENA, (40, VYSKA//2-80, SIRKA-80, 160), 3, border_radius=20)
            kresli_text(povrch, "✅ HOTOVO!", SIRKA//2, VYSKA//2-50,
                        font_velky, ZELENA, stred=True)
            kresli_text(povrch, f"Naskládal jsi {self.sklozene} novin!",
                        SIRKA//2, VYSKA//2, font_maly, BILA, stred=True)
            cas_s = self.cas_skladani // 1000
            kresli_text(povrch, f"Čas: {cas_s}s", SIRKA//2, VYSKA//2+35, font_maly, SVETLE_SEDA, stred=True)
            if blikani(self.cas):
                kresli_text(povrch, "▶ Klepni pro pokračování",
                            SIRKA//2, VYSKA//2+80, font_mini, ZLATA, stred=True)


# === ROZNOS NOVIN ===
class ScenaRoznos(Scena):
    ZAKAZNIKU = 10
    ODMENA_ZA_NOVINY = 60   # Kč za doručení jednoho zákazníka
    DETEKCE_RADIUS = 70     # px – kolik stačí k doručení
    RYCHLOST = 220          # px/s

    def __init__(self, hra):
        super().__init__(hra)
        self.cas = 0
        # Lukša startuje dole uprostřed, ale může se pohybovat po celé obrazovce
        self.luksa_x = float(SIRKA // 2)
        self.luksa_y = float(VYSKA - 160)
        self.cilova_x = self.luksa_x
        self.cilova_y = self.luksa_y
        self.pohybuje_se = False
        self.zakaznici = self._generuj_zakazniky()
        self.animace_penez = []
        self.hotovo = False
        self.celkem_vydelano = 0

    def _generuj_zakazniky(self):
        """Zákazníci jsou rozmístěni po celé hrací ploše pod HUD (pod y=80)."""
        zak = []
        # Rozděl obrazovku na zóny pro rovnoměrné rozmístění
        for i in range(self.ZAKAZNIKU):
            zona_x = (i % 5)
            zona_y = (i // 5)
            x = 50 + zona_x * 80 + random.randint(-20, 20)
            y = 120 + zona_y * 260 + random.randint(-40, 40)
            x = max(40, min(SIRKA - 60, x))
            y = max(110, min(VYSKA - 100, y))
            zak.append({"x": x, "y": y, "dorucleno": False})
        return zak

    def zpracuj_udalost(self, udalost):
        if self.hotovo:
            if udalost.type == pygame.MOUSEBUTTONDOWN:
                self.hra.zmen_scenu("mapa")
            return
        if udalost.type == pygame.MOUSEBUTTONDOWN:
            # Cíl = kde kliknul hráč (2D pohyb)
            self.cilova_x = float(udalost.pos[0])
            self.cilova_y = float(udalost.pos[1])
            self.pohybuje_se = True

    def aktualizuj(self, dt):
        self.cas += dt
        if self.hotovo:
            return

        # Pohyb Lukši ve 2D
        if self.pohybuje_se:
            dx = self.cilova_x - self.luksa_x
            dy = self.cilova_y - self.luksa_y
            dist_cil = math.hypot(dx, dy)
            if dist_cil > 5:
                krok = self.RYCHLOST * dt / 1000
                self.luksa_x += (dx / dist_cil) * krok
                self.luksa_y += (dy / dist_cil) * krok
            else:
                self.luksa_x = self.cilova_x
                self.luksa_y = self.cilova_y
                self.pohybuje_se = False

        # Kontrola doručení – porovnáváme střed Lukši se středem zákazníka
        st = self.hra.stav
        for z in self.zakaznici:
            if not z["dorucleno"]:
                dist = math.hypot(self.luksa_x - z["x"], self.luksa_y - z["y"])
                if dist < self.DETEKCE_RADIUS:
                    z["dorucleno"] = True
                    st.noviny_doneseny += 1
                    odmena = self.ODMENA_ZA_NOVINY + int(st.dovednost_roznos) * 5
                    st.penize += odmena
                    self.celkem_vydelano += odmena
                    st.pridej_xp(15)
                    self.animace_penez.append({
                        "x": float(z["x"]), "y": float(z["y"]),
                        "text": f"+{odmena} Kč",
                        "cas": 0
                    })

        # Animace peněz
        for ap in self.animace_penez[:]:
            ap["cas"] += dt
            ap["y"] -= 60 * dt / 1000
            if ap["cas"] > 1400:
                self.animace_penez.remove(ap)

        # Všichni doručeni?
        if all(z["dorucleno"] for z in self.zakaznici):
            self.hotovo = True
            st.faze = "vecer"
            st.energie -= 25

    def kresli(self, povrch):
        bg = self.hra.textury.get("pozadi_ulice")
        povrch.blit(bg, (0, 0))

        # Domy v pozadí
        dum = self.hra.textury.get("dum")
        for i in range(3):
            povrch.blit(dum, (i * 170 - 10, 60))

        # Zákazníci
        zak_img = self.hra.textury.get("zakaznik")
        noviny_img = self.hra.textury.get("noviny")
        for z in self.zakaznici:
            if not z["dorucleno"]:
                # Detekční kruh (ladicí helper – odkomentuj pokud chceš vidět)
                # pygame.draw.circle(povrch, (255,255,0,80),
                #                    (int(z["x"]), int(z["y"])), self.DETEKCE_RADIUS, 1)
                povrch.blit(zak_img, (int(z["x"]) - zak_img.get_width()//2,
                                      int(z["y"]) - zak_img.get_height()//2))
                # Noviny nad zákazníkem + blikání
                if blikani(self.cas, 600):
                    povrch.blit(noviny_img, (int(z["x"]) - noviny_img.get_width()//2,
                                              int(z["y"]) - zak_img.get_height()//2 - 45))
            else:
                # Zelená fajfka po doručení
                kresli_text(povrch, "✓", int(z["x"]), int(z["y"]) - 30,
                            font_stredni, ZELENA, stred=True, stit=True)

        # Lukša s vozíkem
        lv = self.hra.textury.get("luksa_vozik")
        lx = int(self.luksa_x) - lv.get_width()//2
        ly = int(self.luksa_y) - lv.get_height()//2
        povrch.blit(lv, (lx, ly))

        # Čára k cíli
        if self.pohybuje_se:
            pygame.draw.line(povrch, (*ZLATA, 80),
                             (int(self.luksa_x), int(self.luksa_y)),
                             (int(self.cilova_x), int(self.cilova_y)), 2)
            pygame.draw.circle(povrch, ZLATA,
                               (int(self.cilova_x), int(self.cilova_y)), 6)

        # Animace peněz
        for ap in self.animace_penez:
            alfa = max(0, int(255 * (1 - ap["cas"] / 1400)))
            surf = font_stredni.render(ap["text"], True, ZLATA)
            surf.set_alpha(alfa)
            povrch.blit(surf, (int(ap["x"]) - surf.get_width()//2, int(ap["y"])))

        # HUD nahoře
        kresli_obdel_zaobleny(povrch, (10, 10, 40), (0, 0, SIRKA, 72), 0, 215)
        kresli_text(povrch, "ROZNÁŠKA NOVIN", SIRKA//2, 8,
                    font_stredni, ZLATA, stred=True)
        kresli_text(povrch, f"Doručeno: {self.hra.stav.noviny_doneseny} / {self.ZAKAZNIKU}",
                    SIRKA//2, 38, font_maly, BILA, stred=True)
        prog = self.hra.stav.noviny_doneseny / self.ZAKAZNIKU
        pygame.draw.rect(povrch, SEDA, (20, 62, SIRKA - 40, 10), border_radius=5)
        if prog > 0:
            pygame.draw.rect(povrch, ZELENA,
                             (20, 62, int((SIRKA - 40) * prog), 10), border_radius=5)

        kresli_text(povrch, "Klepni kam jít", SIRKA//2, VYSKA - 28,
                    font_mini, SVETLE_SEDA, stred=True)

        # Hotovo overlay
        if self.hotovo:
            kresli_obdel_zaobleny(povrch, (0, 70, 0), (30, VYSKA//2 - 90, SIRKA - 60, 180), 20, 235)
            pygame.draw.rect(povrch, ZELENA,
                             (30, VYSKA//2 - 90, SIRKA - 60, 180), 3, border_radius=20)
            kresli_text(povrch, "HOTOVO!", SIRKA//2, VYSKA//2 - 65,
                        font_velky, ZELENA, stred=True)
            kresli_text(povrch, f"Vydělal jsi {self.celkem_vydelano} Kč",
                        SIRKA//2, VYSKA//2 - 15, font_stredni, ZLATA, stred=True)
            kresli_text(povrch, f"Celkem úspory: {self.hra.stav.penize} Kč",
                        SIRKA//2, VYSKA//2 + 25, font_maly, SVETLE_SEDA, stred=True)
            if blikani(self.cas):
                kresli_text(povrch, "▶ Klepni pro pokračování",
                            SIRKA//2, VYSKA//2 + 65, font_mini, BILA, stred=True)


# === RAP SESSION ===
class ScenaRap(Scena):
    TEXTY_INTRO = [
        "Flow je smooth jak máslo...",
        "Bro, tohle bude banger!",
        "Jeden slok. Jeden záběr.",
        "Rýmy mi tečou jak Nisa...",
        "Vozík a rýmy, to je môj life.",
    ]
    RADY_OPICAKA = [
        "Opičák: Dej tam beat drop, bro!",
        "Opičák: Štika říká, že jsi fire! 🔥",
        "Opičák: Zkus to víc low-key.",
        "Opičák: Banger incoming! 🐒",
    ]

    def __init__(self, hra):
        super().__init__(hra)
        self.cas = 0
        self.faze = "psani"  # psani, nahravani, hotovo
        self.text_index = 0
        self.rady_index = 0
        self.progres = 0
        self.beat_animace = 0
        self.intro = random.choice(self.TEXTY_INTRO)
        self.rada = random.choice(self.RADY_OPICAKA) if self.hra.stav.je_vikend() else ""
        self.kliknuto = 0
        self.cil_kliku = 20

    def zpracuj_udalost(self, udalost):
        if self.faze == "hotovo":
            if udalost.type == pygame.MOUSEBUTTONDOWN:
                self.hra.zmen_scenu("mapa")
            return
        if udalost.type == pygame.MOUSEBUTTONDOWN:
            self.kliknuto += 1
            self.progres = self.kliknuto / self.cil_kliku
            if self.kliknuto >= self.cil_kliku:
                self._dokoncit_rap()

    def _dokoncit_rap(self):
        st = self.hra.stav
        bonus = 1 + st.dovednost_rap * 0.2
        xp_gain = int(25 * bonus)
        fans_gain = int(st.dovednost_rap * 3 * bonus)
        st.tracky += 1
        st.fans += fans_gain
        st.energie -= 20
        st.dovednost_rap = min(10, st.dovednost_rap + 0.1)
        st.rap_session_dnes = True
        st.pridej_xp(xp_gain)
        self.faze = "hotovo"
        self.gain_fans = fans_gain
        self.gain_xp = xp_gain

    def aktualizuj(self, dt):
        self.cas += dt
        self.beat_animace = math.sin(self.cas / 200) * 10

    def kresli(self, povrch):
        bg = self.hra.textury.get("pozadi_pokoj")
        povrch.blit(bg, (0, 0))
        overlay = pygame.Surface((SIRKA, VYSKA), pygame.SRCALPHA)
        overlay.fill((30, 0, 60, 160))
        povrch.blit(overlay, (0, 0))

        # Titulek
        kresli_obdel_zaobleny(povrch, (50,0,80), (0, 0, SIRKA, 70), 0, 220)
        kresli_text(povrch, "RAP SESSION", SIRKA//2, 15, font_velky, FIALOVA, stred=True)

        # Lukša s mikrofonem - animace
        luksa = self.hra.textury.get("luksa")
        bop_y = int(self.beat_animace)
        povrch.blit(luksa, (SIRKA//2 - luksa.get_width()//2 - 40, 100 + bop_y))
        mik = self.hra.textury.get("mikrofon")
        povrch.blit(mik, (SIRKA//2 + 10, 120 + bop_y))

        # Noty kolem
        nota = self.hra.textury.get("noty")
        for i in range(5):
            angle = self.cas/500 + i * 1.2
            nx = int(SIRKA//2 + math.cos(angle) * 80)
            ny = int(250 + math.sin(angle) * 40)
            povrch.blit(nota, (nx, ny))

        # Aktuální text
        kresli_text(povrch, f'"{self.intro}"', SIRKA//2, 320,
                    font_maly, SVETLE_SEDA, stred=True)

        # Opičák rada
        if self.rada:
            kresli_obdel_zaobleny(povrch, (0,80,0), (20, 370, SIRKA-40, 55), 12, 200)
            kresli_text(povrch, self.rada, SIRKA//2, 385, font_mini, ZELENA, stred=True)

        # Progress bar
        y_prog = 450
        kresli_text(povrch, f"Klikej pro rappování! ({self.kliknuto}/{self.cil_kliku})",
                    SIRKA//2, y_prog, font_maly, BILA, stred=True)
        pygame.draw.rect(povrch, SEDA, (30, y_prog+30, SIRKA-60, 22), border_radius=11)
        if self.progres > 0:
            pygame.draw.rect(povrch, FIALOVA, (30, y_prog+30, int((SIRKA-60)*self.progres), 22), border_radius=11)

        # BIG BUTTON
        btn_rect = (SIRKA//2 - 120, 520, 240, 80)
        pulse = int(10 * abs(math.sin(self.cas/300)))
        kresli_obdel_zaobleny(povrch, FIALOVA,
                               (btn_rect[0]-pulse//2, btn_rect[1]-pulse//2,
                                btn_rect[2]+pulse, btn_rect[3]+pulse), 18)
        kresli_text(povrch, "🎤 TAP!", SIRKA//2, 560, font_velky, BILA, stred=True)

        # Stats
        kresli_text(povrch, f"Tracky: {self.hra.stav.tracky}  |  Fans: {self.hra.stav.fans}",
                    SIRKA//2, VYSKA-50, font_mini, SVETLE_SEDA, stred=True)

        # Hotovo
        if self.faze == "hotovo":
            kresli_obdel_zaobleny(povrch, (60,0,100), (30, VYSKA//2-100, SIRKA-60, 200), 20, 240)
            pygame.draw.rect(povrch, FIALOVA, (30, VYSKA//2-100, SIRKA-60, 200), 3, border_radius=20)
            kresli_text(povrch, "🎤 TRACK HOTOV!", SIRKA//2, VYSKA//2-75, font_stredni, ZLATA, stred=True)
            kresli_text(povrch, f"+{self.gain_fans} nových fans!", SIRKA//2, VYSKA//2-35, font_maly, ZELENA, stred=True)
            kresli_text(povrch, f"+{self.gain_xp} XP", SIRKA//2, VYSKA//2, font_maly, FIALOVA, stred=True)
            kresli_text(povrch, f"Dovednost rapu: {self.hra.stav.dovednost_rap:.1f}/10",
                        SIRKA//2, VYSKA//2+40, font_mini, SVETLE_SEDA, stred=True)
            if blikani(self.cas):
                kresli_text(povrch, "▶ Klepni pro pokračování",
                            SIRKA//2, VYSKA//2+85, font_mini, RUZOVA, stred=True)


# === NÁVŠTĚVA OPIČÁKA ===
class ScenaNavsteva(Scena):
    DIALOGY_VIKEND = [
        [
            ("Opičák", "Heeey Lukša! Jsem tady! 🐒"),
            ("Lukša",  "Bro! Jak se má Štika?"),
            ("Opičák", "Dobře, dobře. Přišel jsem za ní,\nale první zastavka u tebe!"),
            ("Lukša",  "Máš u mě vždy místo, bro."),
            ("Opičák", "Dneska večer zkusíme dát track?"),
            ("Lukša",  "Na to jsem čekal! Připravuju beat!"),
        ],
        [
            ("Opičák", "Štika říká pozdravy! 🐟"),
            ("Lukša",  "Super! Jak ten vztah?"),
            ("Opičák", "Bro, ona je úžasná."),
            ("Opičák", "Přijede si tě poslechnout na koncert!"),
            ("Lukša",  "Musím se pořádně připravit pak!"),
        ],
        [
            ("Opičák", "Viděls kolik followerů máš? 🐒"),
            ("Lukša",  "Jo! {fans} fanoušků bro!"),
            ("Opičák", "Ještě trochu a vydáš EP!"),
            ("Lukša",  "Nejdřív ten počítač..."),
            ("Opičák", "Já věřím! Vozík tě dostane tam!"),
        ],
    ]

    def __init__(self, hra):
        super().__init__(hra)
        self.cas = 0
        self.dialog_set = self.DIALOGY_VIKEND[hra.stav.den % len(self.DIALOGY_VIKEND)]
        self.index = 0
        self.psani_index = 0
        self.psani_cas = 0

    def zpracuj_udalost(self, udalost):
        if udalost.type in (pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN):
            cil_text = self.dialog_set[self.index][1].replace("{fans}", str(self.hra.stav.fans))
            if self.psani_index < len(cil_text):
                self.psani_index = len(cil_text)
            else:
                self.index += 1
                if self.index >= len(self.dialog_set):
                    self.hra.stav.xp += 20
                    self.hra.zmen_scenu("mapa")
                else:
                    self.psani_index = 0

    def aktualizuj(self, dt):
        self.cas += dt
        if self.index < len(self.dialog_set):
            cil = self.dialog_set[self.index][1].replace("{fans}", str(self.hra.stav.fans))
            if self.psani_index < len(cil):
                self.psani_cas += dt
                if self.psani_cas >= 35:
                    self.psani_cas = 0
                    self.psani_index += 1

    def kresli(self, povrch):
        bg = self.hra.textury.get("pozadi_pokoj")
        povrch.blit(bg, (0, 0))
        overlay = pygame.Surface((SIRKA, VYSKA), pygame.SRCALPHA)
        overlay.fill((0, 20, 0, 140))
        povrch.blit(overlay, (0, 0))

        if self.index >= len(self.dialog_set):
            return

        mluvci, text = self.dialog_set[self.index]
        text = text.replace("{fans}", str(self.hra.stav.fans))
        zobrazeny = text[:self.psani_index]

        # Postavy
        if mluvci == "Opičák":
            img = self.hra.textury.get("opicak")
            barva = ZELENA
            x_postava = SIRKA//2 - 60
        else:
            img = self.hra.textury.get("luksa")
            barva = ZLATA
            x_postava = SIRKA//2 - img.get_width()//2 + 60

        povrch.blit(img, (x_postava, 180))

        # Štika občas
        stika = self.hra.textury.get("stika")
        povrch.blit(stika, (SIRKA - stika.get_width() - 10, 250))
        kresli_text(povrch, "Štika", SIRKA - 50, 375, font_mini, RUZOVA, stred=True)

        # Dialog
        kresli_obdel_zaobleny(povrch, (10,30,10), (20, VYSKA-270, SIRKA-40, 230), 16, 230)
        pygame.draw.rect(povrch, ZELENA, (20, VYSKA-270, SIRKA-40, 230), 2, border_radius=16)
        kresli_text(povrch, mluvci, 50, VYSKA-255, font_titulek, barva)

        radky = []
        radek = ""
        for cast in zobrazeny.split("\n"):
            slova = cast.split(" ")
            for slovo in slova:
                test = radek + " " + slovo if radek else slovo
                if font_maly.size(test)[0] < SIRKA - 80:
                    radek = test
                else:
                    radky.append(radek)
                    radek = slovo
            radky.append(radek)
            radek = ""

        for i, r in enumerate(radky[:5]):
            kresli_text(povrch, r, 40, VYSKA-210 + i*30, font_maly)

        if self.psani_index >= len(text) and blikani(self.cas):
            kresli_text(povrch, "▶ Klepni", SIRKA-20, VYSKA-35,
                        font_mini, SVETLE_SEDA, stred=False)


# === VÝHRA ===
class ScenaVyhral(Scena):
    def __init__(self, hra):
        super().__init__(hra)
        self.cas = 0
        self.hvezdy = [(random.randint(0, SIRKA), random.randint(0, VYSKA),
                        random.random()*2+1) for _ in range(80)]

    def zpracuj_udalost(self, udalost):
        if udalost.type == pygame.MOUSEBUTTONDOWN:
            self.hra.zmen_scenu("menu")

    def aktualizuj(self, dt):
        self.cas += dt

    def kresli(self, povrch):
        povrch.fill((10, 0, 30))

        # Padající hvězdy
        for hx, hy, rychl in self.hvezdy:
            jas = int(128 + 127 * math.sin(self.cas/400 + hx))
            pygame.draw.circle(povrch, (jas, jas, 50), (hx, hy), 3)

        pocitac = self.hra.textury.get("pocitac")
        scale = 1.0 + 0.05 * math.sin(self.cas/400)
        w = int(pocitac.get_width() * scale * 2)
        h = int(pocitac.get_height() * scale * 2)
        pc_big = pygame.transform.scale(pocitac, (w, h))
        povrch.blit(pc_big, (SIRKA//2 - w//2, 150))

        kresli_text(povrch, "🎉 CONGRATULATIONS! 🎉",
                    SIRKA//2, 80, font_stredni, ZLATA, stred=True)
        kresli_text(povrch, "LUKŠA KOUPIL POČÍTAČ!",
                    SIRKA//2, 380, font_velky, BILA, stred=True)
        kresli_text(povrch, "Rapová kariéra může začít!",
                    SIRKA//2, 440, font_stredni, FIALOVA, stred=True)

        st = self.hra.stav
        kresli_text(povrch, f"Dny: {st.den}  |  Fans: {st.fans}  |  Tracky: {st.tracky}",
                    SIRKA//2, 510, font_maly, SVETLE_SEDA, stred=True)

        luksa = self.hra.textury.get("luksa")
        povrch.blit(luksa, (SIRKA//2 - luksa.get_width()//2, 580))

        if blikani(self.cas, 700):
            kresli_text(povrch, "▶ Klepni pro návrat do menu",
                        SIRKA//2, VYSKA - 50, font_maly, SVETLE_SEDA, stred=True)


# === O HŘE ===
class ScenaOHre(Scena):
    def __init__(self, hra):
        super().__init__(hra)
        self.cas = 0

    def zpracuj_udalost(self, udalost):
        if udalost.type == pygame.MOUSEBUTTONDOWN:
            self.hra.zmen_scenu("menu")

    def aktualizuj(self, dt):
        self.cas += dt

    def kresli(self, povrch):
        povrch.fill(TMAVE_MODRA)
        kresli_text(povrch, "O HŘE", SIRKA//2, 40, font_velky, ZLATA, stred=True)

        info = [
            "Lukša sní o rapové kariéře.",
            "K nahrávání potřebuje počítač (8000 Kč).",
            "",
            "Každý den:",
            "📦 Připrav noviny (klikej na ně)",
            "🛒 Roznes noviny zákazníkům",
            "🎤 Rappuj a získávej fans",
            "",
            "Na víkend přijede Opičák 🐒",
            "za svou přítelkyní Štikou 🐟",
            "a přespí u Lukši.",
            "",
            "Vydělej 8000 Kč a kup počítač!",
        ]
        for i, r in enumerate(info):
            barva = ZLATA if r.startswith("Lukša") or r.startswith("Vydělej") else BILA
            if r == "":
                continue
            kresli_text(povrch, r, 30, 110 + i * 34, font_mini, barva)

        if blikani(self.cas):
            kresli_text(povrch, "▶ Zpět do menu", SIRKA//2, VYSKA-50,
                        font_maly, SVETLE_SEDA, stred=True)


# === HLAVNÍ HRA ===
class Hra:
    def __init__(self):
        self.textury = SpravceTextur()
        self.stav = HerniStav()
        self.zprava = ""
        self.zprava_cas = 0

        self.sceny = {
            "menu":     ScenaMenu(self),
            "uvod":     ScenaUvod(self),
            "mapa":     ScenaMapa(self),
            "sklad":    ScenaSklad(self),
            "roznos":   ScenaRoznos(self),
            "rap":      ScenaRap(self),
            "navsteva": ScenaNavsteva(self),
            "vyhral":   ScenaVyhral(self),
            "o_hre":    ScenaOHre(self),
        }
        self.aktualni_scena = "menu"

    def zmen_scenu(self, nova_scena):
        # Znovu-inicializuj scény co se mění pokaždé
        obnovit = {"mapa", "sklad", "roznos", "rap", "navsteva", "vyhral"}
        if nova_scena in obnovit:
            konstruktory = {
                "mapa":     ScenaMapa,
                "sklad":    ScenaSklad,
                "roznos":   ScenaRoznos,
                "rap":      ScenaRap,
                "navsteva": ScenaNavsteva,
                "vyhral":   ScenaVyhral,
            }
            if nova_scena in konstruktory:
                self.sceny[nova_scena] = konstruktory[nova_scena](self)
        self.aktualni_scena = nova_scena

    def spust(self):
        bezi = True
        while bezi:
            dt = hodiny.tick(FPS)
            scena = self.sceny[self.aktualni_scena]

            for udalost in pygame.event.get():
                if udalost.type == pygame.QUIT:
                    bezi = False
                elif udalost.type == pygame.KEYDOWN:
                    if udalost.key == pygame.K_ESCAPE:
                        if self.aktualni_scena != "menu":
                            self.zmen_scenu("mapa" if self.aktualni_scena != "mapa" else "menu")
                scena.zpracuj_udalost(udalost)

            scena.aktualizuj(dt)
            scena.kresli(obrazovka)

            # Zprávy
            if self.zprava:
                self.zprava_cas += dt
                kresli_text(obrazovka, self.zprava, SIRKA//2, VYSKA//2,
                            font_stredni, CERVENA, stred=True)
                if self.zprava_cas > 2500:
                    self.zprava = ""
                    self.zprava_cas = 0

            pygame.display.flip()

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    hra = Hra()
    hra.spust()
