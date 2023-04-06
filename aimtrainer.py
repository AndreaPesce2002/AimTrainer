from re import M
import string
import threading
import time
import pygame
import sys
import random
import os

# -------------- CLASSI ----------------------
class condown(threading.Thread):

    def __init__(self, tempo):
        threading.Thread.__init__(self)
        self.tempo = tempo
        self.gioco = False

    def run(self):
        threadLock = threading.Lock()
        print("avviato partita")
        # Acquisizione del lock
        threadLock.acquire()
        time.sleep(self.tempo)
        print(
            f"fine partita: {punteggio} colpiti, {mancati} mancati in {tempo} secondi")
        self.gioco = False

        # Rilascio del lock
        threadLock.release()


class errore(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        threadLock = threading.Lock()
        # Acquisizione del lock
        threadLock.acquire()

        for i in reversed(range(200)):
            s = pygame.image.load('images\cross.png').convert_alpha()
            s.set_alpha(i)
            screen.blit(s, r2)

        # Rilascio del lock
        threadLock.release()

def path_to(img):
    # ottieni il percorso assoluto della cartella del tuo script
    script_dir = os.path.dirname(__file__)

    # concatena il nome del file alla fine del percorso della cartella
    return os.path.join(script_dir, 'images', img)
# ----------- VARIABILI ------------
screen_altezza = 800
screen_largezza = 600
w = 30
punteggio = 0
mancati = 0
record = [0,0,0,0]
difficola=1

tempo = 10  # int(input("inserisci il tempo per ogni raund: "))

# --------------- SCERMATA ---------------
pygame.init()
screen = pygame.display.set_mode((screen_altezza, screen_largezza))
pygame.display.set_caption('Aim Trainer 2.0 by Peke')

# new type, "color" cursor
surf = pygame.Surface((30, 25), pygame.SRCALPHA)
pygame.draw.rect(surf, (0, 255, 0), [13, 0, 3, 30])
pygame.draw.rect(surf, (0, 255, 0), [0, 10, 30, 3])
cursors = pygame.cursors.Cursor((10, 10), surf)
pygame.mouse.set_cursor(cursors)

# ------------------- COLORI ----------------
CYAN = (41, 41, 41)
RED = (255, 28, 28)
VIOLA = (0, 0, 0)

# ------------------- PYGAME ----------------
r1 = pygame.Rect(400, 400, w, w)
r2 = pygame.Rect(100, 300, 10, 10)
sotto = pygame.Rect(0, screen_largezza-100, 1000, 1000)

buttonReset = pygame.Rect(50, screen_largezza-60, 100, 40)
buttonFacile = pygame.Rect(200, screen_largezza-60, 100, 40)
buttonMedio = pygame.Rect(350, screen_largezza-60, 100, 40)
buttonDifficile = pygame.Rect(500, screen_largezza-60, 100, 40)
buttonPazzia = pygame.Rect(650, screen_largezza-60, 100, 40)

fnt = pygame.font.SysFont("", 40)
vittoria = fnt.render("BENVENUTO", True, "green")

# --------------- FUNZIONI -------------


def area(mouse, zona):
    return mouse.pos[0] > zona.topleft[0] and mouse.pos[1] > zona.topleft[1] and mouse.pos[0] < zona.bottomright[0] and mouse.pos[1] < zona.bottomright[1]


# ----------- inisio gioco ----------------
c = condown(tempo)
while True:

    if not c.gioco:
        if record[difficola] < punteggio:
            record[difficola] = punteggio
        vittoria = fnt.render(f"FINISH: {punteggio} colpiti, {mancati} mancati in {tempo} secondi RECORD: {record[difficola]}", True, "green")
        
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:  # chiousura del gioco
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:  # gioco

            quadrato = area(event, r1)

            if (not c.gioco) and quadrato:
                c = condown(tempo)
                c.start()
                c.gioco = True
                punteggio = 0
                mancati = 0

            if c.gioco:
                vittoria = fnt.render(f"", True, "green")
                if quadrato:
                    punteggio += 1

                    if difficola==3:
                        w=random.randint(10,40)
                        r1 = pygame.Rect(400, 400, w, w)

                    r1 = pygame.Rect(0, 0, w, w)
                    r1 = r1.move(random.randint(0, screen_altezza-50),random.randint(0, screen_largezza-120))

                else:
                    if not area(event, sotto):
                        mancati += 1
                        r2 = pygame.Rect(-30, -30, 10, 10)
                        r2 = r2.move(event.pos)
                        errore().start()
            
            if area(event, buttonReset):
                c.tempo = 0
                c.gioco = False
            
            if area(event, buttonFacile):
                w=60
                r1 = pygame.Rect(400, 400, w, w)
                difficola=0
                c.tempo = 0
                c.gioco = False
            
            if area(event, buttonMedio):
                w=40
                r1 = pygame.Rect(400, 400, w, w)
                difficola=1                
                c.tempo = 0
                c.gioco = False

            if area(event, buttonDifficile):
                w=20
                r1 = pygame.Rect(400, 400, w, w)
                difficola=2
                c.tempo = 0
                c.gioco = False

            if area(event, buttonPazzia):
                w=random.randint(5,20)
                r1 = pygame.Rect(400, 400, w, w)
                difficola=3
                c.tempo = 0
                c.gioco = False

# ------------ creazione  elementi in scermata -----------
    screen.fill(CYAN)

    m = pygame.Surface((1000, 1000))
    m.fill(VIOLA)
    screen.blit(m, sotto)

    b = pygame.image.load(path_to('restart.png')).convert_alpha()
    screen.blit(b, buttonReset)

    b1 = pygame.image.load(path_to('facile.png')).convert_alpha()
    screen.blit(b1, buttonFacile)

    b2 = pygame.image.load(path_to('medio.png')).convert_alpha()
    screen.blit(b2, buttonMedio)

    b3 = pygame.image.load(path_to('difficile.png')).convert_alpha()
    screen.blit(b3, buttonDifficile)

    b4 = pygame.image.load(path_to('pazzia.png')).convert_alpha()
    screen.blit(b4, buttonPazzia)


    s = pygame.Surface((w, w))
    s.fill(RED)
    screen.blit(s, r1)

    screen.blit(vittoria, (50, screen_altezza-300))

    pygame.display.update()

