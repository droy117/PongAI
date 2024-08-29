import neat.config
import pygame, neat, os, pickle
from pong_module import Game

FPS = 60

width, height = 800, 600
window = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

font = pygame.font.Font(None, 74)
font_sm = pygame.font.Font(None, 54)

class PongGame:
    def __init__(self, window, width, height):
        self.game = Game(window, width, height)
        self.left_paddle = self.game.left_paddle
        self.right_paddle = self.game.right_paddle
        self.ball = self.game.ball

    def test_ai(self, genome, config):
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        run = True
        while run:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

            keys = pygame.key.get_pressed()

            if keys[pygame.K_x]:
                run = False
                intro_screen(config)

            if keys[pygame.K_w]:
                self.game.move_paddle(left=True, up=True)
            if keys[pygame.K_s]:
                self.game.move_paddle(left=True, up=False)

            output = net.activate((self.right_paddle.y, self.ball.y, abs(self.right_paddle.x-self.ball.x)))
            decision = output.index(max(output))

            if decision == 0:
                pass
            elif decision == 1:
                self.game.move_paddle(left=False, up=True)
            else:
                self.game.move_paddle(left=False, up=False)

            game_info = self.game.loop()

            # print(game_info.left_hits, game_info.left_score, game_info.right_hits, game_info.right_score)
            self.game.draw(left_player="Player", right_player="AI")
            pygame.display.update()

            if(game_info.left_score == 5):
                player_win_text = font.render("Player WON!", True, Game.GREEN)
                window.blit(player_win_text, (width//2 - player_win_text.get_width()//2, 200))
                pygame.display.update()
                pygame.time.delay(3000)
                self.game.reset()

            elif(game_info.right_score == 5):
                ai_win_text = font.render("AI WON!", True, Game.RED)
                window.blit(ai_win_text, (width//2 - ai_win_text.get_width()//2, 200))
                pygame.display.update()
                pygame.time.delay(3000)
                self.game.reset()

        pygame.quit()

    def player_vs_player(self, config):
        run = True
        while run:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

            keys = pygame.key.get_pressed()

            if keys[pygame.K_x]:
                run = False
                intro_screen(config)

            if keys[pygame.K_w]:
                self.game.move_paddle(left=True, up=True)
            if keys[pygame.K_s]:
                self.game.move_paddle(left=True, up=False)

            if keys[pygame.K_UP]:
                self.game.move_paddle(left=False, up=True)
            if keys[pygame.K_DOWN]:
                self.game.move_paddle(left=False, up=False)

            game_info = self.game.loop()

            self.game.draw(left_player="Player 1", right_player="Player 2")
            pygame.display.update()

            if(game_info.left_score == 5):
                player_win_text = font.render("Player 1 WON!", True, Game.BLACK)
                window.blit(player_win_text, (width//2 - player_win_text.get_width()//2, 200))
                pygame.display.update()
                pygame.time.delay(3000)
                self.game.reset()

            elif(game_info.right_score == 5):
                ai_win_text = font.render("Player 2 WON!", True, Game.BLACK)
                window.blit(ai_win_text, (width//2 - ai_win_text.get_width()//2, 200))
                pygame.display.update()
                pygame.time.delay(3000)
                self.game.reset()

        pygame.quit()

    def ai_vs_ai(self, genome, config):
        net_1 = neat.nn.FeedForwardNetwork.create(genome, config)
        net_2 = neat.nn.FeedForwardNetwork.create(genome, config)
        run = True
        while run:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

            keys = pygame.key.get_pressed()

            if keys[pygame.K_x]:
                run = False
                intro_screen(config)

            output_1 = net_1.activate((self.left_paddle.y, self.ball.y, abs(self.left_paddle.x-self.ball.x)))
            decision_1 = output_1.index(max(output_1))

            if decision_1 == 0:
                pass
            elif decision_1 == 1:
                self.game.move_paddle(left=True, up=True)
            else:
                self.game.move_paddle(left=True, up=False)

            output_2 = net_2.activate((self.right_paddle.y, self.ball.y, abs(self.right_paddle.x-self.ball.x)))
            decision_2 = output_2.index(max(output_2))

            if decision_2 == 0:
                pass
            elif decision_2 == 1:
                self.game.move_paddle(left=False, up=True)
            else:
                self.game.move_paddle(left=False, up=False)

            game_info = self.game.loop()

            # print(game_info.left_hits, game_info.left_score, game_info.right_hits, game_info.right_score)
            self.game.draw(left_player="AI 1", right_player="AI 2")
            pygame.display.update()

            if(game_info.left_score == 5):
                player_win_text = font.render("AI 1 WON!", True, Game.RED)
                window.blit(player_win_text, (width//2 - player_win_text.get_width()//2, 200))
                pygame.display.update()
                pygame.time.delay(3000)
                self.game.reset()

            elif(game_info.right_score == 5):
                ai_win_text = font.render("AI 2 WON!", True, Game.RED)
                window.blit(ai_win_text, (width//2 - ai_win_text.get_width()//2, 200))
                pygame.display.update()
                pygame.time.delay(3000)
                self.game.reset()

        pygame.quit()


    def train_ai(self, genome1, genome2, config):
        net1 = neat.nn.FeedForwardNetwork.create(genome1, config)
        net2 = neat.nn.FeedForwardNetwork.create(genome2, config)

        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            output1 = net1.activate((self.left_paddle.y, self.ball.y, abs(self.left_paddle.x-self.ball.x)))
            decision1 = output1.index(max(output1))
            output2 = net2.activate((self.right_paddle.y, self.ball.y, abs(self.right_paddle.x-self.ball.x)))
            decision2 = output2.index(max(output2))

            if decision1 == 0:
                pass
            elif decision1 == 1:
                self.game.move_paddle(left=True, up=True)
            else:
                self.game.move_paddle(left=True, up=False)

            if decision2 == 0:
                pass
            elif decision2 == 1:
                self.game.move_paddle(left=False, up=True)
            else:
                self.game.move_paddle(left=False, up=False)

            game_info = self.game.loop()
            self.game.draw(draw_score=False, draw_hits=True)
            pygame.display.update()

            if game_info.left_score >=1 or game_info.right_score >=1 or game_info.left_hits > 50:
                self.calculate_fitness(genome1, genome2, game_info)
                break

    def calculate_fitness(self, genome1, genome2, game_info):
        genome1.fitness += game_info.left_hits
        genome2.fitness += game_info.right_hits

def eval_genomes(genomes, config):
    for i, (genomes_id1, genome1) in enumerate(genomes):
        if i == len(genomes)-1:
            break
        genome1.fitness = 0
        for genome_id2, genome2 in genomes[i+1:]:
            genome2.fitness = 0 if genome2.fitness == None else genome2.fitness
            game = PongGame(window, width, height)
            game.train_ai(genome1, genome2, config)

def run_neat(config):
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1))

    winner = p.run(eval_genomes, 50)
    with open("best.pickle", "wb") as f:
        pickle.dump(winner, f)

def get_ai(config):
    with open("best.pickle", "rb") as f:
        winner = pickle.load(f)

    game = PongGame(window, width, height)
    game.test_ai(winner, config)

def play_player_vs_player(config):
    game = PongGame(window, width, height)
    game.player_vs_player(config)

def play_ai_vs_ai(config):
    with open("best.pickle", "rb") as f:
        winner = pickle.load(f)

    game = PongGame(window, width, height)
    game.ai_vs_ai(winner, config)

def intro_screen(config):
    pygame.init()
    run = True
    while run:
        window.fill(Game.BROWN)
        
        title_text = font.render("PONG", True, Game.WHITE)
        desc_text = font_sm.render("Press 1, 2 or 3 to start!", True, Game.WHITE)
        p_vs_ai_text = font.render("1. Player vs AI", True, Game.WHITE)
        p_vs_p_text = font.render("2. Player vs Player", True, Game.WHITE)
        ai_vs_ai_text = font.render("3. AI vs AI", True, Game.WHITE)
        intro_screen_return_text = font_sm.render("Press X anytime to return to the menu!", True, Game.BLACK)
        
        window.blit(title_text, (width//2 - title_text.get_width()//2, 50))
        window.blit(desc_text, (width//2 - desc_text.get_width()//2, 150))
        window.blit(p_vs_ai_text, (width//2 - p_vs_ai_text.get_width()//2, 250))
        window.blit(p_vs_p_text, (width//2 - p_vs_p_text.get_width()//2, 350))
        window.blit(ai_vs_ai_text, (width//2 - ai_vs_ai_text.get_width()//2, 450))
        window.blit(intro_screen_return_text, (width//2 - intro_screen_return_text.get_width()//2, 550))
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    get_ai(config)  
                elif event.key == pygame.K_2:
                    play_player_vs_player(config)  
                elif event.key == pygame.K_3:
                    play_ai_vs_ai(config)  

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
    
    intro_screen(config)  
