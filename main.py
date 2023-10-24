import pygame
import random
import sys

LARGURA = 1200
ALTURA = 650

BG = 'assets/imgs/fundo.png'
FONTE = 'assets/fonts/PixelGameFont.ttf'
ALVO ='assets/imgs/pomba.png'
MIRA = 'assets/imgs/mouse.png'
DISPARO = 'assets/audio/disparo.mp3'

PONTOS = 0
RECORDE = 0

TIMER = 600  

GAME_PAUSED = False
FINALIZAR = False

# Classe para representar os alvos no jogo
class Alvo(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__() 
        self.image = pygame.image.load(ALVO).convert_alpha()
        self.image = pygame.transform.scale(self.image, (100,100))
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]
        
# Classe para representar a mira do jogador
class Mira(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(MIRA).convert_alpha()
        self.image = pygame.transform.scale(self.image, (50,50))
        self.rect = self.image.get_rect()
        self.sound = pygame.mixer.Sound(DISPARO)
    
    def update(self): 
        self.rect.center = pygame.mouse.get_pos()
    
    def shoot(self):
        global PONTOS
        self.sound.play()
        
        colisions = pygame.sprite.spritecollide(mira,grupo_de_alvos, False)
        for colision in colisions:
            PONTOS +=1
            colision.kill()
            alvo = Alvo(random.randrange(0,LARGURA),random.randrange(0,ALTURA)) 
            grupo_de_alvos.add(alvo)

# Inicializar o pygame
pygame.init()

# Configurar a janela do jogo
screen = pygame.display.set_mode((LARGURA,ALTURA))

# Carregar a imagem de fundo
bg =  pygame.image.load(BG).convert() 
bg = pygame.transform.scale(bg, (LARGURA,ALTURA))

# Configurar o relógio do jogo
clock = pygame.time.Clock()

# Carregar a fonte para exibir a pontuação
font = pygame.font.Font(FONTE, 30)

pygame.display.set_caption("Tiro ao alvo")

# Criar um grupo de sprites para os alvos
grupo_de_alvos = pygame.sprite.Group()

# Criar a mira do jogador
for i in range(15):
    alvo = Alvo(random.randrange(0,LARGURA),random.randrange(0,ALTURA)) 
    grupo_de_alvos.add(alvo)
    
mira = Mira()
mira_group = pygame.sprite.Group()
mira_group.add(mira)


while not FINALIZAR:
    if not GAME_PAUSED:
        pygame.mouse.set_visible(False)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: 
                    GAME_PAUSED = not GAME_PAUSED
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                mira.shoot()        
                    
        screen.blit(bg, (0,0))   
        grupo_de_alvos.draw(screen)
        
        mira_group.draw(screen)
        
        mira_group.update()
        
        score = font.render(f' Pontos: {int(PONTOS)} ', True, (0,0,0))
        screen.blit(score, (25,30)) 
        
        tempo = font.render(f'Tempo: {TIMER/60:.1f} s',True, (0,0,0))
        screen.blit(tempo, (30,70))                               

        TIMER -=1
        if TIMER < 0:
            TIMER = 600
            
            if PONTOS > RECORDE:
                RECORDE = PONTOS
                PONTOS = 0
            GAME_PAUSED = not GAME_PAUSED
            
            if PONTOS < RECORDE:
                PONTOS = 0
            
    else:
        screen.fill((252, 132, 3))
        pygame.mouse.set_visible(True)
        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    GAME_PAUSED = not GAME_PAUSED

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        pause = font.render(f"PRESSIONE ESC PARA INICIAR   ",True, (0,0,0))
        points = font.render(f"RECORDE: {RECORDE} ",True, (0,0,0))

        pause_rect = pause.get_rect(center = (LARGURA/2, ALTURA/2))
        points_rect = points.get_rect(center = (LARGURA/2, ALTURA/2-50))
        
        screen.blit(pause, pause_rect)
        screen.blit(points,points_rect)
                
                
    pygame.display.flip()
    clock.tick(60)                