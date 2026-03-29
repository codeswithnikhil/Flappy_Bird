# Module that want for game
import pygame
import random


# Opps is the all part of flappy bird
class Flappy_Bird:
    def __init__(self,caption,width,height):
        # game windows variable
        self.caption = caption
        self.width = width
        self.height = height
        self.game_over = False
        # Making game windows
        pygame.init()
        self.game_window = pygame.display.set_mode((self.width,self.height))
        pygame.display.set_caption(self.caption)
        self.clock = pygame.time.Clock()
        # Game main variable
        self.speed = 2
        self.score = 0
        self.last_score_time = pygame.time.get_ticks()
        # Bird variavle
        self.bird_y = self.height//2
        self.bird_x = 250
        self.bird_gravity = 5
        self.bird_jump = 10
        self.bird = pygame.image.load("bird.png")
        self.bird = pygame.transform.scale(self.bird,(80,80)).convert_alpha()
        # Obsciticals list
        self.obsciticals = []
    # This function display high score and score and save high score and update score
    def auto_score_and_high_score(self):
        pygame.draw.rect(self.game_window,(20, 40, 80),(0,0,self.width,50))
        if self.game_over:
            return
        current_time = pygame.time.get_ticks()
        if current_time - self.last_score_time >= 2000/self.speed:
            self.score += 1
            self.last_score_time = current_time
        self.add_text(f"Score: {self.score}", (255,255,255), 10, 10, 50)
        with open("score.txt","r") as f:
            data = f.readlines()[0]
        if int(data)<self.score:
            with open("score.txt","w") as f:
                f.write(str(self.score))
        self.add_text(f"High Score: {data}", (255,255,255), 540, 10, 50)
    # this function increase speed if score is increse
    def game_harder(self):
        if self.score>20:
            self.speed = self.score/20 * 2
    # This is start game windows
    def Start_game(self):
        while True:
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            if keys[pygame.K_SPACE]:
                break
            else:
                self.game_window.fill((135, 206, 235))
                self.add_text("Welcome in Flappy Bird Game",(0,0,0),120,280,55)
                pygame.display.update()
    # This function add tetx in game screen
    def add_text(self,text,colour,x,y,font_size):
        self.text = text
        self.colour = colour
        self.x = x
        self.y = y
        self.font_size = font_size
        self.font = pygame.font.SysFont(None,self.font_size)
        self.screen = self.font.render(self.text,True,self.colour)
        self.game_window.blit(self.screen,[x,y])
    # This gunction create bird
    def Create_bird(self):
        self.game_window.blit(self.bird, (self.bird_x, self.bird_y))
        self.bird_rect = pygame.Rect(self.bird_x, self.bird_y, 80, 80)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.bird_y -= self.bird_jump
            
        self.bird_y += self.bird_gravity
    # This function create obscitacl
    def create_obscitacl(self,gap,next_pip_time):
        self.next_pip_time = next_pip_time
        self.gap = gap
        self.upper_y = random.randint(100,self.height-self.gap-150)
        self.obscitical = {
            "x" : self.width,
            "u_y" : self.upper_y,
            "b_y" : self.upper_y + self.gap
        }
        self.obsciticals.append(self.obscitical)
    # This function reste the the game afte game over
    def reset(self):
        self.score = 0
        self.speed = 2
        self.obsciticals = []
        self.create_obscitacl(150,250)
        self.bird_y = self.height//2
        self.bird_x = 250
        self.game_over = False
    # This function display the game over screen
    def game_over_screen(self):
        while self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            self.game_window.fill((135, 206, 235))
            self.add_text("Game Over",(10,250,10),250,280,60)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_TAB]:
                self.reset()
            pygame.display.update()
    # This function add obscitacl at the real time game
    def add_obscitacl(self,size):
        self.size = size
        for obscitical in self.obsciticals:
            pygame.draw.rect(self.game_window,(0, 200, 0),(obscitical["x"] , 0 , self.size , obscitical["u_y"]))
            pygame.draw.rect(self.game_window,(0, 200, 0),(obscitical["x"] , obscitical["b_y"] , self.size , self.height-obscitical["b_y"]))
            obscitical["x"] -= self.speed
            if obscitical["x"]<0-self.size:
                self.obsciticals.remove(obscitical)
            if self.obsciticals[-1]["x"]<self.width - self.next_pip_time:
                    self.create_obscitacl(self.gap , self.next_pip_time)
            upper_rect = pygame.Rect(obscitical["x"]+15, -20, self.size-30, obscitical["u_y"])
            bottom_rect = pygame.Rect(obscitical["x"]+15, obscitical["b_y"]+30,self.size-30, self.height - obscitical["b_y"])
            if self.bird_rect.colliderect(upper_rect) or self.bird_rect.colliderect(bottom_rect):
                self.game_over = True
            if self.bird_y<0 or self.bird_y>self.height:
                self.game_over = True

                
  



        
        
        






# This is main function for the game executing
def main():
    window = Flappy_Bird("Flappy Bird",800,600)
    window.Start_game()
    window.create_obscitacl(150,250)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        window.game_window.fill((135, 206, 235))
        window.Create_bird()
        window.add_obscitacl(50)
        window.game_harder()
        window.game_over_screen()
        window.auto_score_and_high_score()
        pygame.display.update()
        window.clock.tick(50)





# --------------------Main----------------------
if __name__ == "__main__":
    main()




pygame.quit()