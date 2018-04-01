import pygame
import time
from pygame.locals import  *

class Drawer():
    def __init__(self):
        pass
    def init(self, w, h, r):
        pygame.init()
        self.virus_radius = r
        self.screen = pygame.display.set_mode((w, h), 0, 32)
        self.surface = pygame.Surface(self.screen.get_size())
        self.surface = self.surface.convert()
        self.surface.fill((255,255,255))
        self.circles = []
        # font = pygame.font.Font(None, 36)
        # text = font.render(str(snake.length), 1, (10, 10, 10))



    def add(self, x,y,r):

        self.circles.append((x,y,r))

        
            

    def draw(self, fs, es, vs, ps):
        
        self.surface.fill((255,255,255))


        for f in fs: 
            pygame.draw.circle(self.surface, (255,100,0), f.pos, 2)
        for e in es: 
            pygame.draw.circle(self.surface, (0,200,0), (int(e.pos[0]),int(e.pos[1])), int(e.radius))
        for v in vs: 
            pygame.draw.circle(self.surface, (5,0,0), v.pos, self.virus_radius, 1)                        
        for me in ps:
            pygame.draw.circle(self.surface, (120,120,120), (int(me.pos[0]),int(me.pos[1])), int(me.radius)       )                             
        text = 'no'
        if len(self.circles)>0:
            for c in self.circles:
                pygame.draw.circle(self.surface, (0,255,0), (int(c[0]),int(c[1])), int(c[2]))            
            text =str(len(self.circles))                
        

        self.circles.clear()
        self.screen.blit(self.surface, (0,0))

        
        myfont = pygame.font.SysFont('Comic Sans MS', 30)
        textsurface = myfont.render(text, False, (0, 0, 0))
        self.screen.blit(textsurface,(0,0))


        pygame.display.flip()
        pygame.display.update()

        # import time
        # time.sleep(0.1)

        # while self.pause:
        #     for event in pygame.event.get():
        #         if event.type == KEYUP:
        #             if pygame.key.name == K_SPACE:
        #                 self.pause = not self.pause
        #             if pygame.key.name == K_RIGHT:
        #                 self.pause = True
        #                 return

            



