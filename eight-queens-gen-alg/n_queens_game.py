"""
        Application:    N-Queens Puzzle
          File Name:    n_queens_game.py
             Course:    CPSC 481 A.I.
           Semester:    Spring 21'
           Due Date:    May 18
            Authors:    David Guido         |   dguido1@csu.fullerton.edu
                        Trong Pham          |   ...@csu.fullerton.edu
                        Jacqueline kubiak   |   ...@csu.fullerton.edu

        **********************
        *  n_queens_game.py  *
        **********************************************
        *  1.) main() initializes Game class variable:
               game = Game()
        *  2.) main() calls function game_loop on that variable:
               game.game_loop()

        ******************
        *  Instructions  *
        *************************************************************************
        > Write a program to solve the N-Queens puzzle for any given value for N.
        > The N-Queens puzzle is to place N chess queens on an N×N chessboard so that no two queens threaten each other;
              i.e, a placement where no two queens share the same row, column, or diagonal.

            > This can be solved using a Genetic algorithm as described in class.
            > Write a Python program that computes a solution to solve this puzzle and display the result graphically.

            > Note: The `Genetic Algorithm` is already implemented in the textbook code (genetic_search() in search.py)
                    and one state representation is also given (class NQueensProblem in search.py).

            Thus, the main tasks are:
                1. Put these together, with any required modifications, to solve the puzzle.
                2. Try different values for the different algorithm hyperparameters (such as mutation probability,
                   size of population) to get the best results (i.e., solves it fast and finds a solution).
                3. Create a simple GUI. You can use your own choice of graphics library. One choice is PyGame.
"""

import pygame as pg
from background import Background
from search import *


class Game:

    WIDTH = 900                             # Width of game window
    HEIGHT = 630                            # Height of game window

    def __init__(self):

        pg.init()                                                                 # Initialize pygame
        self.screen = pg.display.set_mode((Game.WIDTH, Game.HEIGHT))              # Set window dimensions
        pg.display.set_caption('N-Queens Puzzle')                                 # Set name of the game
        self.bg = Background('images/chess_8.png', (0, 60))             # Background Image obj
        self.BG_COLOR = (0, 0, 0)                                                 # Set background to black

        self.last_key = None                        # Last key the user inputted
        self.start_screen = True                    # Start screen conditional var

        self.find_soln_pressed = False              # Find solution button pressed conditional var
        self.new_scene_buffer = False               # New scene buffer conditional var (0.1 sec timer expired)

        self.white = (255, 255, 255)                # Color def (White, green, blue)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 128)

        self.play_button = True                     # Buttons & their rectangles
        self.play_button_rect = None
        self.find_soln_button = False
        self.find_soln_button_rect = None
        self.return_menu_button = False
        self.return_menu_button_rect = None
        self.restart_button = False
        self.restart_button_rect = None
        self.n_up_button = False                    # N - buttons
        self.n_up_button_rect = None
        self.n_down_button = False
        self.n_down_button_rect = None
        self.ngen_up_button = False                 # NGen - buttons
        self.ngen_up_button_rect = None
        self.ngen_down_button = False
        self.ngen_down_button_rect = None
        self.mut_up_button = False                  # mut - buttons
        self.mut_up_button_rect = None
        self.mut_down_button = False
        self.mut_down_button_rect = None

        self.CLOCK = pg.time.Clock()                # Universal animation clock

        self.n_value = 8
        self.ngen_value = 118
        self.mut_value = 0.6

        self.scene_rendered = False                 # Conditional var, has the scene been rendered?
        self.results_rendered = False               # Conditional var, have the results been rendered?

        # picture = pygame.transform.scale(picture, (1280, 720))
        self.up_image = pg.image.load('images/up.png')
        self.down_image = pg.image.load('images/down.png')
        self.up_image = pg.transform.scale(self.up_image, (16, 16))
        self.down_image = pg.transform.scale(self.down_image, (16, 16))

        self.n_up_button = self.up_image
        self.n_down_button = self.down_image
        self.ngen_up_button = self.up_image
        self.ngen_down_button = self.down_image
        self.mut_up_button = self.up_image
        self.mut_down_button = self.down_image

        self.n_up_button_rect = self.n_up_button.get_rect()
        self.n_down_button_rect = self.n_down_button.get_rect()
        self.ngen_up_button_rect = self.ngen_up_button.get_rect()
        self.ngen_down_button_rect = self.ngen_down_button.get_rect()
        self.mut_up_button_rect = self.mut_up_button.get_rect()
        self.mut_down_button_rect = self.mut_down_button.get_rect()

        self.n_up_button_rect.center = (280, 390)
        self.n_down_button_rect.center = (280, 410)
        self.ngen_up_button_rect.center = (280, 430)
        self.ngen_down_button_rect.center = (280, 450)
        self.mut_up_button_rect.center = (280, 470)
        self.mut_down_button_rect.center = (280, 490)

        self.results_loading = True
        self.results = []

        self.total_iter = 0
        self.curr_iter = 0

        self.crown_image = pg.image.load('images/crown.png')

    """"
    Function Game Loop:
        *   1.) Display start scene
        *   2.) Display find solution scene
        *  2a.) Display find solution scene w/ results
    """""""""
    def game_loop(self):
        start_ticks = pg.time.get_ticks()                             # Used for future instantaneous time reference

        while self.start_screen:                                      # While start screen is being shown

            self.process_events()                                     # Get user input

            if not self.scene_rendered:                               # If menu scene hasn't already been rendered
                self.render_menu_scene()                               # Go ahead and render it

        while not self.start_screen and not self.new_scene_buffer:  # Wait .1 second then jump to next while (Main Scn)

            seconds = (pg.time.get_ticks() - start_ticks) / 1000    # Calculate seconds since new (main) scene started

            if seconds > 0.05:                                       # More than .1 sec have passed
                self.scene_rendered = False
                self.new_scene_buffer = True

        while not self.start_screen and not self.find_soln_pressed:

            self.process_events()                                           # Get user input

            if not self.scene_rendered:                                     # If main scene hasn't already been rendered
                self.render_soln_scene()                                    # Go ahead and render it

            self.CLOCK.tick(60)                                             # Limit display rate

            if self.find_soln_pressed and not self.results_rendered:        # Render results once
                self.display_soln_found()
                self.results_rendered = True

    def process_events(self):

        for event in pg.event.get():

            if event.type == pg.QUIT:
                sys.exit()

            # Mouse event: Check for collision and for render changes .. i.e. text updates
            elif event.type == pg.MOUSEBUTTONDOWN:
                x, y = event.pos
                print("Mouse input received. X-Coord: " + str(x) + ", Y-Coord: " + str(y))

                if not self.new_scene_buffer:
                    if self.play_button_rect.collidepoint(x, y):
                        self.start_screen = False
                elif self.find_soln_pressed:
                    if self.restart_button_rect.collidepoint(x, y):
                        self.reset_game()
                else:
                    if self.find_soln_button_rect.collidepoint(x, y):
                        self.find_soln_pressed = True
                    elif self.return_menu_button_rect.collidepoint(x, y):
                        self.reset_game()
                    elif self.n_up_button_rect.collidepoint(x, y):
                        if self.n_value < 10:
                            self.n_value += 1
                    elif self.n_down_button_rect.collidepoint(x, y):
                        if self.n_value > 4:
                            self.n_value -= 1
                    elif self.ngen_up_button_rect.collidepoint(x, y):
                        if self.ngen_value < 120:
                            self.ngen_value += 10
                        print("Ngen up Pressed")
                    elif self.ngen_down_button_rect.collidepoint(x, y):
                        if self.ngen_value > 20:
                            self.ngen_value -= 10
                        print("Ngen down Pressed")
                    elif self.mut_up_button_rect.collidepoint(x, y):
                        if self.mut_value < 0.9:
                            self.mut_value = round(self.mut_value + 0.1, 1)
                        print("Mut up Pressed")
                    elif self.mut_down_button_rect.collidepoint(x, y):
                        if self.mut_value > 0.1:
                            self.mut_value -= 0.1
                        print("Mut down Pressed")

                self.render_soln_scene()

    def render_menu_scene(self):
        start_font = pg.font.Font('Gameplay.ttf', 18)
        welcome_font = pg.font.Font('Gameplay.ttf', 12)
        credit_font = pg.font.Font('Gameplay.ttf', 10)

        start_prompt = start_font.render('Start', True, self.white)  # PLAY Text
        welcome_prompt00 = welcome_font.render('Welcome to the N-Queens puzzle', True, self.white)
        welcome_prompt01 = welcome_font.render('solution generator', True, self.white)
        credit = credit_font.render('Project by David Guido, Trong Pham & Jacqueline Kubiak', True, self.white)

        welcome_msg_rect = welcome_prompt00.get_rect()
        welcome_msg_rect01 = welcome_prompt01.get_rect()
        self.play_button_rect = start_prompt.get_rect()
        credit_rect = credit.get_rect()

        welcome_msg_rect.center = ((self.WIDTH // 2), 360)
        welcome_msg_rect01.center = ((self.WIDTH // 2), 380)
        self.play_button_rect.center = ((self.WIDTH // 2), 425)
        credit_rect.center = ((self.WIDTH // 2), self.HEIGHT - 40)

        self.screen.fill(self.BG_COLOR)  # Render BG
        self.clear_screen()  # Render the background

        self.screen.blit(start_prompt, self.play_button_rect)
        self.screen.blit(welcome_prompt00, welcome_msg_rect)
        self.screen.blit(welcome_prompt01, welcome_msg_rect01)
        self.screen.blit(credit, credit_rect)

        pg.display.update()
        self.scene_rendered = True

    def render_soln_scene(self):

        self.clear_screen()

        label_font = pg.font.Font('freesansbold.ttf', 16)
        text_font = pg.font.Font('freesansbold.ttf', 22)

        rtn_prompt = label_font.render('Return to Menu', True, self.white)
        find_soln_prompt = label_font.render('Find Solution', True, self.white)
        n_label = label_font.render('Number of non-attacking queens           ', True, self.white)
        ngen_label = label_font.render('Max number of states generated           ', True, self.white)
        mut_label = label_font.render('Mutation ratio of algorithm randomization', True, self.white)
        n_text = text_font.render(str(self.n_value), True, self.white)
        ngen_text = text_font.render(str(self.ngen_value), True, self.white)
        mut_text = text_font.render(str(self.mut_value), True, self.white)

        self.return_menu_button_rect = rtn_prompt.get_rect()
        self.find_soln_button_rect = find_soln_prompt.get_rect()
        text_rect00 = n_label.get_rect()
        text_rect01 = n_text.get_rect()
        text_rect02 = ngen_label.get_rect()
        text_rect03 = ngen_text.get_rect()
        text_rect04 = mut_label.get_rect()
        text_rect05 = mut_text.get_rect()

        self.return_menu_button_rect.center = (self.WIDTH / 6, 25)
        self.find_soln_button_rect.center = (self.WIDTH / 2, 550)
        text_rect00.center = (375, 400)
        text_rect00.left = 375
        text_rect01.center = (325, 400)
        text_rect02.center = (375, 440)
        text_rect02.left = 375
        text_rect03.center = (325, 440)
        text_rect04.center = (375, 480)
        text_rect04.left = 375
        text_rect05.center = (325, 480)

        self.screen.blit(rtn_prompt, self.return_menu_button_rect)
        self.screen.blit(find_soln_prompt, self.find_soln_button_rect)
        self.screen.blit(n_label, text_rect00)
        self.screen.blit(n_text, text_rect01)
        self.screen.blit(ngen_label, text_rect02)
        self.screen.blit(ngen_text, text_rect03)
        self.screen.blit(mut_label, text_rect04)
        self.screen.blit(mut_text, text_rect05)
        self.screen.blit(self.up_image, self.n_up_button_rect)
        self.screen.blit(self.down_image, self.n_down_button_rect)
        self.screen.blit(self.up_image, self.ngen_up_button_rect)
        self.screen.blit(self.down_image, self.ngen_down_button_rect)
        self.screen.blit(self.up_image, self.mut_up_button_rect)
        self.screen.blit(self.down_image, self.mut_down_button_rect)

        pg.display.update()
        self.scene_rendered = True

    def display_soln_found(self):

        pg.display.update()

        # Logic
        myNQueen = NQueensProblem(self.n_value)
        self.results = genetic_search(myNQueen, self.ngen_value, self.mut_value, self.n_value, self)
        self.total_iter = self.curr_iter

        self.results_loading = False
        self.clear_screen()

        label_font = pg.font.Font('freesansbold.ttf', 16)
        text_font = pg.font.Font('freesansbold.ttf', 22)
        n_label = label_font.render('Number of non-attacking queens           ', True, self.white)
        ngen_label = label_font.render('Max number of states generated           ', True, self.white)
        mut_label = label_font.render('Mutation ratio of algorithm randomization', True, self.white)
        n_text = text_font.render(str(self.n_value), True, self.white)
        ngen_text = text_font.render(str(self.ngen_value), True, self.white)
        mut_text = text_font.render(str(self.mut_value), True, self.white)
        text_rect00 = n_label.get_rect()
        text_rect01 = n_text.get_rect()
        text_rect02 = ngen_label.get_rect()
        text_rect03 = ngen_text.get_rect()
        text_rect04 = mut_label.get_rect()
        text_rect05 = mut_text.get_rect()
        text_rect00.center = (375, 400)
        text_rect00.left = 375
        text_rect01.center = (325, 400)
        text_rect02.center = (375, 440)
        text_rect02.left = 375
        text_rect03.center = (325, 440)
        text_rect04.center = (375, 480)
        text_rect04.left = 375
        text_rect05.center = (325, 480)
        self.screen.blit(n_label, text_rect00)
        self.screen.blit(n_text, text_rect01)
        self.screen.blit(ngen_label, text_rect02)
        self.screen.blit(ngen_text, text_rect03)
        self.screen.blit(mut_label, text_rect04)
        self.screen.blit(mut_text, text_rect05)

        font = pg.font.Font('Gameplay.ttf', 14)
        restart_font = pg.font.Font('Gameplay.ttf', 12)

        text = font.render('Solution: ' + str(self.results), True, self.white)
        iter_text = font.render('Total Iterations: ' + str(self.total_iter), True, self.white)
        self.restart_button = restart_font.render('Return to main menu', True, (205, 204, 0), self.blue)

        text_rect = text.get_rect()
        iter_text_rect = iter_text.get_rect()
        self.restart_button_rect = self.restart_button.get_rect()

        text_rect.center = (self.WIDTH // 2, 525)
        iter_text_rect.center = (self.WIDTH // 2, 555)
        self.restart_button_rect.center = (self.WIDTH // 2, 600)

        self.screen.blit(text, text_rect)
        self.screen.blit(iter_text, iter_text_rect)
        self.screen.blit(self.restart_button, self.restart_button_rect)

        self.render_queens()
        pg.display.update()

        while self.find_soln_pressed:
            self.CLOCK.tick(15)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    sys.exit()
                elif event.type == pg.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if self.restart_button_rect.collidepoint(x, y):
                        self.reset_game()

    def render_queens(self):

        for n in self.results:

            queen_rect = self.crown_image.get_rect()
            queen_rect.centerx = 340 + (n * 31.5)
            queen_rect.centery = 39 + (self.results[n] * 32)

            self.screen.blit(self.crown_image, queen_rect)

    def clear_screen(self):

        self.screen.fill(self.BG_COLOR)                 # Set background color to black

        if self.n_value == 4:
            self.bg.set_new_image('images/chess_4.png')
        elif self.n_value == 5:
            self.bg.set_new_image('images/chess_5.png')
        elif self.n_value == 6:
            self.bg.set_new_image('images/chess_6.png')
        elif self.n_value == 7:
            self.bg.set_new_image('images/chess_7.png')
        elif self.n_value == 8:
            self.bg.set_new_image('images/chess_8.png')
        elif self.n_value == 9:
            self.bg.set_new_image('images/chess_9.png')
        else:
            self.bg.set_new_image('images/chess_10.png')

        self.bg.rect.center = (self.WIDTH // 2, 150)
        self.screen.blit(self.bg.image, self.bg.rect)

    def update_loading(self, curr_iter):
        self.curr_iter = curr_iter

        self.clear_screen()

        label_font = pg.font.Font('freesansbold.ttf', 16)
        text_font = pg.font.Font('freesansbold.ttf', 22)
        n_label = label_font.render('Number of non-attacking queens           ', True, self.white)
        ngen_label = label_font.render('Max number of states generated           ', True, self.white)
        mut_label = label_font.render('Mutation ratio of algorithm randomization', True, self.white)
        n_text = text_font.render(str(self.n_value), True, self.white)
        ngen_text = text_font.render(str(self.ngen_value), True, self.white)
        mut_text = text_font.render(str(self.mut_value), True, self.white)
        text_rect00 = n_label.get_rect()
        text_rect01 = n_text.get_rect()
        text_rect02 = ngen_label.get_rect()
        text_rect03 = ngen_text.get_rect()
        text_rect04 = mut_label.get_rect()
        text_rect05 = mut_text.get_rect()
        text_rect00.center = (375, 400)
        text_rect00.left = 375
        text_rect01.center = (325, 400)
        text_rect02.center = (375, 440)
        text_rect02.left = 375
        text_rect03.center = (325, 440)
        text_rect04.center = (375, 480)
        text_rect04.left = 375
        text_rect05.center = (325, 480)
        self.screen.blit(n_label, text_rect00)
        self.screen.blit(n_text, text_rect01)
        self.screen.blit(ngen_label, text_rect02)
        self.screen.blit(ngen_text, text_rect03)
        self.screen.blit(mut_label, text_rect04)
        self.screen.blit(mut_text, text_rect05)

        font = pg.font.Font('Gameplay.ttf', 14)
        wait_text = font.render('Please wait..', True, self.white)
        text = font.render('Current Iteration: ' + str(curr_iter), True, self.white)
        text_rect = text.get_rect()
        wait_text_rect = wait_text.get_rect()
        text_rect.center = (self.WIDTH // 2, 555)
        wait_text_rect.center = (self.WIDTH // 2, 525)
        self.screen.blit(text, text_rect)
        self.screen.blit(wait_text, wait_text_rect)

        restart_font = pg.font.Font('Gameplay.ttf', 12)
        self.restart_button = restart_font.render('Cancel search', True, (205, 204, 0), self.blue)
        self.restart_button_rect = self.restart_button.get_rect()
        self.restart_button_rect.center = (self.WIDTH // 2, 600)
        self.screen.blit(self.restart_button, self.restart_button_rect)
        pg.display.update()

    def reset_game(self):
        self.__init__()
        self.game_loop()


def main():
    game = Game()
    game.game_loop()


if __name__ == '__main__':
    main()
