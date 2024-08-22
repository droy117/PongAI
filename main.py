import pygame
from pong_module import Game

FPS = 60

width, height = 800, 600
window = pygame.display.set_mode((width, height))

class PongGame:
    def __init__(self, widow, width, height):
        self.game = Game(window, width, height)
        self.left_paddle = self.game.left_paddle
        self.right_paddle = self.game.right_paddle
        self.ball = self.game.ball

    def test_ai(self):
        run = True
        clock = pygame.time.Clock()
        while run:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.game.move_paddle(left=True, up=True)
            if keys[pygame.K_s]:
                self.game.move_paddle(left=True, up=False)

            if keys[pygame.K_UP]:
                self.game.move_paddle(left=False, up=True)
            if keys[pygame.K_DOWN]:
                self.game.move_paddle(left=False, up=False)

            game_info = self.game.loop()
            print(game_info.left_hits, game_info.left_score, game_info.right_hits, game_info.right_score)
            self.game.draw()
            pygame.display.update()

        pygame.quit()