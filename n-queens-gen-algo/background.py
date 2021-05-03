"""
        Application:    N-Queens Puzzle
          File Name:    background.py
  GitHub Repository:    https://github.com/dguido1/n-queens-gen-algo
             Course:    CPSC 481 A.I.
           Semester:    Spring 21'
           Due Date:    May 18
            Authors:    David Guido   |   GitHub: @DGuido1   |   Email: dguido1@csu.fullerton.edu
                        Trong Pham
                        Jacqueline Kubiak

        *******************
        *  background.py  *
        **********************************************************************************
            Provides an easy-to-use background object for our solution to render on top of
"""""


import pygame as pg


class Background(pg.sprite.Sprite):

    def __init__(self, image_file, location):

        pg.sprite.Sprite.__init__(self)             # Call sprite initializer
        self.image = pg.image.load(image_file)      # Set bg image property to an image file
        self.rect = self.image.get_rect()           # Set bg rect property to the rect of the imported image
        self.rect.left, self.rect.top = location    # Position this (Background) obj

    def set_new_image(self, image_file):
        self.image = pg.image.load(image_file)      # Set bg image property to an image file

