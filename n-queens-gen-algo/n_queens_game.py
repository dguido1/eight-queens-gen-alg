"""
        Application:    N-Queens Puzzle
          File Name:    n_queens_game.py
  GitHub Repository:    https://github.com/dguido1/n-queens-gen-algo
             Course:    CPSC 481 A.I.
           Semester:    Spring 21'
           Due Date:    May 18
            Authors:    David Guido   |   GitHub: @DGuido1   |   Email: dguido1@csu.fullerton.edu
                        Trong Pham
                        Jacqueline Kubiak

        **********************
        *  n_queens_game.py  *
        ***********************************************
            1.) main() initializes Game class variable:
                game = Game()
            2.) main() calls function game_loop on that variable:
                game.game_loop()
"""""

import pygame as pg
from background import Background
from search import *


class Game:

    WIDTH = 900     # Width of game window
    HEIGHT = 630    # Height of game window

    """"
    __init__() -- Called once before the menu scene is rendered to the screen
        * Automatically initializes built in modules
        * Initializes each custom pygame module by hand for use later
    """""
    def __init__(self):

        pg.init()                                                                 # Initialize pygame
        self.screen = pg.display.set_mode((Game.WIDTH, Game.HEIGHT))              # Set window dimensions
        pg.display.set_caption('N-Queens Puzzle')                                 # Set name of the game
        self.bg = Background('images/chess_8.png', (0, 60))                       # Background Image obj
        self.BG_COLOR = (0, 0, 0)                                                 # Set background to black

        self.last_key = None                        # Last key the user inputted
        self.start_screen = True                    # Start screen conditional var

        self.find_soln_pressed = False              # Find solution button pressed conditional var
        self.new_scene_buffer = False               # New scene buffer conditional var (0.1 sec timer expired)

        self.white = (255, 255, 255)                # Color def (White, green, blue)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 128)

        # Buttons & their rectangles
        self.start_button = True                    # Start button
        self.start_button_rect = None
        self.find_soln_button = False               # Find solution button
        self.find_soln_button_rect = None
        self.return_menu_button = False             # Return to menu button (first)
        self.return_menu_button_rect = None
        self.restart_button = False                 # Return to menu button (second)
        self.restart_button_rect = None
        self.n_up_button = False                    # N up
        self.n_up_button_rect = None
        self.n_down_button = False                  # N down
        self.n_down_button_rect = None
        self.ngen_up_button = False                 # NGen up
        self.ngen_up_button_rect = None
        self.ngen_down_button = False               # NGen down
        self.ngen_down_button_rect = None
        self.mut_up_button = False                  # Mut up
        self.mut_up_button_rect = None
        self.mut_down_button = False                # Mut down
        self.mut_down_button_rect = None

        self.CLOCK = pg.time.Clock()                # Universal clock reference for scene

        self.n_value = 8                  # Big N value, how many non attacking queens to find (User inputted)
        self.ngen_value = 118             # N Gen value, max number sequences are generated per (User inputted)
        self.mut_value = 0.6              # Mut ratio value, "how much" to alter the generated sequence (User inputted)

        self.scene_rendered = False                 # Conditional var, has the scene been rendered?
        self.results_rendered = False               # Conditional var, have the results been rendered?

        self.up_image = pg.image.load('images/up.png')                      # Up arrow image reference
        self.down_image = pg.image.load('images/down.png')                  # Down arrow image reference
        self.up_image = pg.transform.scale(self.up_image, (16, 16))         # Scaled up arrow image
        self.down_image = pg.transform.scale(self.down_image, (16, 16))     # Scaled down arrow image

        self.n_up_button = self.up_image                    # Set n up button to reference up image
        self.n_down_button = self.down_image                # Set n down button to reference down image
        self.ngen_up_button = self.up_image                 # Set ngen up button to reference up image
        self.ngen_down_button = self.down_image             # Set ngen down button to reference down image
        self.mut_up_button = self.up_image                  # Set mut up button to reference up image
        self.mut_down_button = self.down_image              # Set mut down button to reference down image

        self.n_up_button_rect = self.n_up_button.get_rect()             # Set N, NGen and Mut button rectangles
        self.n_down_button_rect = self.n_down_button.get_rect()         # to their appropriate regions
        self.ngen_up_button_rect = self.ngen_up_button.get_rect()
        self.ngen_down_button_rect = self.ngen_down_button.get_rect()
        self.mut_up_button_rect = self.mut_up_button.get_rect()
        self.mut_down_button_rect = self.mut_down_button.get_rect()

        self.n_up_button_rect.center = (280, 390)                       # Set N, NGen and Mut buttons
        self.n_down_button_rect.center = (280, 410)                     # to render locations
        self.ngen_up_button_rect.center = (280, 430)
        self.ngen_down_button_rect.center = (280, 450)
        self.mut_up_button_rect.center = (280, 470)
        self.mut_down_button_rect.center = (280, 490)

        self.results_loading = True     # Are the results loading?
        self.results = []               # The returned results

        self.total_iter = 0             # Total iterations in corresponding parse
        self.curr_iter = 0              # Current iteration in corresponding parse

        self.crown_image = pg.image.load('images/crown.png')        # Crown image reference

        self.myNQueen = None

    """"
    game_loop
       * Get user input
       * Display start scene
       * Display find solution scene
       * Display find solution scene w/ results
    """""
    def game_loop(self):
        start_ticks = pg.time.get_ticks()                             # Used for future instantaneous time reference

        while self.start_screen:                                      # While start screen is being shown

            self.process_events()                                     # Get user input

            if not self.scene_rendered:                                # If menu scene hasn't already been rendered
                self.render_menu_scene()                               # ==> Go ahead and render it

        while not self.start_screen and not self.new_scene_buffer:  # Wait .1 second then jump to next while (Main Scn)

            seconds = (pg.time.get_ticks() - start_ticks) / 1000    # Calculate seconds since new (main) scene started

            if seconds > 0.05:                                       # More than .1 sec has passed
                self.scene_rendered = False
                self.new_scene_buffer = True

        while not self.start_screen and not self.find_soln_pressed:     # While find solution scene & no solution found

            self.process_events()                                       # Get user input

            if not self.scene_rendered:                                 # If main scene hasn't already been rendered
                self.render_solution_scene()                            # Go ahead and render it

            self.CLOCK.tick(60)                                           # Limit display rate

            if self.find_soln_pressed and not self.results_rendered:      # If results haven't already been rendered
                self.find_solution()                                      # Find the corresponding solution
                self.render_solution_results()                            # ==> Go ahead and render it
                self.results_rendered = True                              # Set render var to true

    """"
    process_events
       * Get user input
       * Respond appropriately
    """""
    def process_events(self):

        for event in pg.event.get():

            if event.type == pg.QUIT:       # User pressed the exit button on the upper right corner of window
                sys.exit()

            elif event.type == pg.MOUSEBUTTONDOWN:  # User pressed the exit button on the upper right corner of window
                x, y = event.pos

                if not self.new_scene_buffer:                            # If set time (.1 sec) has not passed
                    if self.start_button_rect.collidepoint(x, y):        # If Start button pressed
                        self.start_screen = False                        # Set current scene to find solution scene
                elif self.find_soln_pressed:                             # If user presses find solution
                    if self.restart_button_rect.collidepoint(x, y):      # If user presses return to menu button
                        self.reset_game()                                # Reset the game
                else:                                                       # Buffer time up, find solution not pressed
                    if self.find_soln_button_rect.collidepoint(x, y):       # If find solution button pressed
                        self.find_soln_pressed = True
                    elif self.return_menu_button_rect.collidepoint(x, y):   # If return to menu button pressed
                        self.reset_game()
                    elif self.n_up_button_rect.collidepoint(x, y):              # If n up button pressed
                        if self.n_value < 10:                                   # If new value is in bounds
                            self.n_value += 1                                   # Increment n value
                    elif self.n_down_button_rect.collidepoint(x, y):            # If n down button pressed
                        if self.n_value > 4:                                    # If new value is in bounds
                            self.n_value -= 1                                   # Increment n value
                    elif self.ngen_up_button_rect.collidepoint(x, y):           # If ngen up button pressed
                        if self.ngen_value < 120:                               # If new value is in bounds
                            self.ngen_value += 10                               # Increment ngen value
                    elif self.ngen_down_button_rect.collidepoint(x, y):         # If ngen down button pressed
                        if self.ngen_value > 20:                                # If new value is in bounds
                            self.ngen_value -= 10                               # Increment ngen value
                    elif self.mut_up_button_rect.collidepoint(x, y):            # If mut up button pressed
                        if self.mut_value < 0.9:                                # If new value is in bounds
                            self.mut_value = round(self.mut_value + 0.1, 1)     # Increment mut value
                    elif self.mut_down_button_rect.collidepoint(x, y):          # If mut down button pressed
                        if self.mut_value > 0.1:                                # If new value is in bounds
                            self.mut_value -= 0.1                               # Increment mut value

                self.render_solution_scene()    # Call render solution scene after ANY input event

    """"
    render_menu_scene
        * Render main menu scenes current state to the screen
    """""
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
        self.start_button_rect = start_prompt.get_rect()
        credit_rect = credit.get_rect()

        welcome_msg_rect.center = ((self.WIDTH // 2), 360)
        welcome_msg_rect01.center = ((self.WIDTH // 2), 380)
        self.start_button_rect.center = ((self.WIDTH // 2), 425)
        credit_rect.center = ((self.WIDTH // 2), self.HEIGHT - 40)

        self.screen.fill(self.BG_COLOR)  # Render BG
        self.clear_screen()  # Render the background

        self.screen.blit(start_prompt, self.start_button_rect)
        self.screen.blit(welcome_prompt00, welcome_msg_rect)
        self.screen.blit(welcome_prompt01, welcome_msg_rect01)
        self.screen.blit(credit, credit_rect)

        pg.display.update()
        self.scene_rendered = True

    """"
    render_solution_scene
        * Render find solution scenes current state to the screen
    """""
    def render_solution_scene(self):

        self.clear_screen()

        label_font = pg.font.Font('freesansbold.ttf', 16)

        rtn_prompt = label_font.render('Return to Menu', True, self.white)
        find_soln_prompt = label_font.render('Find Solution', True, self.white)

        self.return_menu_button_rect = rtn_prompt.get_rect()
        self.find_soln_button_rect = find_soln_prompt.get_rect()

        self.return_menu_button_rect.center = (self.WIDTH / 6, 25)
        self.find_soln_button_rect.center = (self.WIDTH / 2, 550)

        self.render_input_labels()

        self.screen.blit(rtn_prompt, self.return_menu_button_rect)
        self.screen.blit(find_soln_prompt, self.find_soln_button_rect)

        self.screen.blit(self.up_image, self.n_up_button_rect)
        self.screen.blit(self.down_image, self.n_down_button_rect)
        self.screen.blit(self.up_image, self.ngen_up_button_rect)
        self.screen.blit(self.down_image, self.ngen_down_button_rect)
        self.screen.blit(self.up_image, self.mut_up_button_rect)
        self.screen.blit(self.down_image, self.mut_down_button_rect)

        pg.display.update()
        self.scene_rendered = True

    """"
    find_solution
        * Call search.genetic_search(self.myNQueen, self.ngen_value, self.mut_value, self.n_value, self)
          to find a solution to the corresponding puzzle
    """""
    def find_solution(self):
        self.myNQueen = NQueensProblem(self.n_value)
        self.results = genetic_search(self.myNQueen, self.ngen_value, self.mut_value, self.n_value, self)
        self.total_iter = self.curr_iter

    """"
    render_finding_solution
        * Render an updated state to the screen while finding the solution (i.e. loading..)
        * Called from search.py
    """""
    def render_finding_solution(self, curr_iter):

        self.curr_iter = curr_iter

        self.clear_screen()
        self.render_input_labels()

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

    """"
    render_solution_results
        * Render solution results to the screen
            i.e. Sequence of numbers .. [1,5,3,0,2,4,6,7]
                 1.) Value = Row
                 2.) Index = Column
    """""
    def render_solution_results(self):

        pg.display.update()

        self.results_loading = False
        self.clear_screen()

        self.render_input_labels()

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

    """"
    render_queens
        * Render solution results (Queens on top of board) to the screen
    """""
    def render_queens(self):

        for n in self.results:                                  # For each node in the results
            queen_rect = self.crown_image.get_rect()            # Set the current queen rect to the crown image rect
            queen_rect.centerx = 340 + (n * 31.5)               # Set x value to (340 pixels) + (index + 31.5)
            queen_rect.centery = 39 + (self.results[n] * 32)    # Set y value to  (39 pixels) + (currentRow * yBuffer)

            self.screen.blit(self.crown_image, queen_rect)      # Render the queen to the screen

    """"
    render_input_labels (Helper function, reduces repetitive code)
        * Render user input labels to the screen
    """""
    def render_input_labels(self):

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

    """"
    clear_screen (Helper function, reduces repetitive code)
        * Clear the screen, render a new background
    """""
    def clear_screen(self):

        self.screen.fill(self.BG_COLOR)                         # Set background color to black

        if self.n_value == 4:                                   # Adjust the background image to appropriate size
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

        self.bg.rect.center = (self.WIDTH // 2, 150)                # Set background to appropriate position
        self.screen.blit(self.bg.image, self.bg.rect)               # Render background to the screen

    """"
    reset_game (Helper function, reduces repetitive code)
        * Calls __init__() and game_loop() to reset the game
    """""
    def reset_game(self):
        self.__init__()
        self.game_loop()


def main():
    game = Game()
    game.game_loop()


if __name__ == '__main__':
    main()