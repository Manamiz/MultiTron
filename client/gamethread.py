from threading import Thread
import threading
import utils
import commands
import pygame
import random
import math
import os
import time
from pygame.locals import *

class GameThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        
    def run(self):
        while True:
            try:
                command = utils.recv_data(utils.Global.sock_game)
            except Exception as e:
                break
                
            if command == None:
                break

            if command == commands.CMD_LAUNCH_GAME:
                id = utils.recv_data(utils.Global.sock_game)

                map = utils.recv_data(utils.Global.sock_game)

                colors = utils.recv_data(utils.Global.sock_game)
                players = utils.recv_data(utils.Global.sock_game)

                screen = pygame.display.set_mode((700, 480))
                pygame.display.set_caption("Multitron")

                background = pygame.Surface(screen.get_size())
                background = background.convert()
                background.fill((10, 198, 198))

                wallImage = pygame.image.load("images/wall.png").convert()

                DOWN = 1
                RIGHT = 2
                LEFT = 3
                UP = 4

                PLAYER_SIZE = 5
                WALL_SIZE = 30

                clock = pygame.time.Clock()

                playersGrid = []
                for i in range(96):
                    playersGrid.append([])
                    for j in range(96):
                        playersGrid[i].append(0)

                playerImage = pygame.image.load("images/player.png").convert()
                x = random.randint(10, 85) * 5
                y = random.randint(10, 85) * 5
                tmpY = math.floor(y / WALL_SIZE)
                tmpX = math.floor(x / WALL_SIZE)

                while map[tmpY][tmpX] != 0:
                    x = random.randint(10, 85) * 5
                    y = random.randint(10, 85) * 5
                    tmpY = math.floor(y / WALL_SIZE)
                    tmpX = math.floor(x / WALL_SIZE)

                direction = DOWN

                #random.seed(1)

                pygame.font.init()
                myfont = pygame.font.Font(None, 50)
                myfontScore = pygame.font.Font(None, 40)
                fontPlayerss = pygame.font.Font(None, 25)
                lose = False
                win = False
                score = 0

                idEnemy = -1
                running = True
                wait = True

                pygame.mixer.init()
                son = pygame.mixer.Sound("sounds/music.wav")
                son.play()

                while running:
                    clock.tick(utils.fps)

                    tmpX = math.floor(x / PLAYER_SIZE)
                    tmpY = math.floor(y / PLAYER_SIZE)
                    if not lose and not win:
                        playersGrid[tmpX][tmpY] = id

                        if direction == DOWN:
                            y += PLAYER_SIZE 
                        elif direction == RIGHT:
                            x += PLAYER_SIZE
                        elif direction == LEFT:
                            x -= PLAYER_SIZE
                        elif direction == UP:
                            y -= PLAYER_SIZE

                        # Check wall collision
                        tmpY = math.floor(y / WALL_SIZE)
                        tmpX = math.floor(x / WALL_SIZE)
                        if map[tmpY][tmpX] == 1:
                            lose = True
                            score = score - 150

                        # Check tail collision
                        tmpY = math.floor(y / PLAYER_SIZE)
                        tmpX = math.floor(x / PLAYER_SIZE)
                        if playersGrid[tmpX][tmpY] == id:
                            lose = True
                            score = score - 200
                        # Check players collision
                        elif playersGrid[tmpX][tmpY] != 0:
                            lose = True
                            score = score - 100
                            idEnemy = playersGrid[tmpX][tmpY]

                        for event in pygame.event.get():
                            if event.type == QUIT:
                                pygame.quit()
                            if event.type == KEYDOWN:
                                if event.key == K_RIGHT and direction != LEFT:
                                    direction = RIGHT
                                if event.key == K_LEFT and direction != RIGHT:
                                    direction = LEFT
                                if event.key == K_UP and direction != DOWN:
                                    direction = UP
                                if event.key == K_DOWN and direction != UP:
                                    direction = DOWN

                        if not lose and not win:
                            screen.blit(background, (0, 0))

                            # Draw wall
                            for i in range(len(map)):
                                for j in range(len(map[i])):
                                    if map[i][j] == 1:
                                        screen.blit(wallImage, (j * WALL_SIZE, i * WALL_SIZE))

                            screen.blit(playerImage, (x, y))

                    # Draw players
                    for i in range(len(playersGrid)):
                        for j in range(len(playersGrid[i])):
                            if playersGrid[i][j] != 0:
                                pygame.draw.rect(screen, colors[playersGrid[i][j] - 1], (i * PLAYER_SIZE, j * PLAYER_SIZE, PLAYER_SIZE, PLAYER_SIZE))

                    for i in range(len(players)):
                        label = fontPlayerss.render(players[i], 1, colors[i])
                        screen.blit(label, (520, 20 + (i * 40)))

                    if lose:
                        wait = False
                        label = myfont.render("Vous avez perdu !", 1, (255,0,0))
                        screen.blit(label, (100, 100))
                        labelScore = myfontScore.render("Score : " + str(score), 2, (255,255,255))
                        screen.blit(labelScore, (115, 135))
                        pygame.display.flip()
                    elif win:
                        wait = False
                        label = myfont.render("Vous avez gagne !", 1, (0,255,0))
                        screen.blit(label, (100, 100))
                        labelScore = myfontScore.render("Score : " + str(score), 1, (255,255,255))
                        screen.blit(labelScore, (115, 135))
                        pygame.display.flip()

                    pygame.display.flip()

                    utils.send_data(utils.Global.sock_game, idEnemy)
                    idEnemy = -1

                    utils.send_data(utils.Global.sock_game, lose)

                    utils.send_data(utils.Global.sock_game, playersGrid)

                    allKills = utils.recv_data(utils.Global.sock_game)

                    for i in allKills:
                        if i == id and not win and not lose:
                            score = score + 100

                    allLost = utils.recv_data(utils.Global.sock_game)

                    nbPlayer = len(allLost)
                    nbLost = 0
                    for i in allLost:
                        if i == True:
                            nbLost = nbLost + 1

                        if nbLost == (nbPlayer-1) and not lose and not win:
                            win = True
                            score = score + 300

                    playersGrid = utils.recv_data(utils.Global.sock_game)

                    utils.send_data(utils.Global.sock_game, score)

                    if wait:
                        utils.send_data(utils.Global.sock_game, False)
                    else:
                        utils.send_data(utils.Global.sock_game, True)

                    finish = utils.recv_data(utils.Global.sock_game)
                    if finish:
                        if win:
                            label = myfont.render("Vous avez gagne !", 1, (0,255,0))
                            screen.blit(label, (100, 100))
                            labelScore = myfontScore.render("Score : " + str(score), 1, (255,255,255))
                            screen.blit(labelScore, (115, 135))
                            pygame.display.flip()
                        time.sleep(2)
                        running = False
                        son.stop()
                        pygame.display.quit()