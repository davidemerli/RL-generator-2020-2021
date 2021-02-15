import random
from math import floor, log2
from random import randint
import numpy as np

# Generatore di test per l'anno 2020/2021 - per gli anni successivi andra' modificato in funzione delle specifiche di progetto

def generate_batch(cols, rows):
    """
    Given the number of columns and rows, returns a random pixel array with 2 + (rows * cols) elements
    The first two elements are the image dimensions as specified in the document
    """

    return [cols, rows] + [randint(0, 255) for _ in range(rows * cols)]

def solve_batch(batch):
    """
    Given a list with a structure like
    [cols, rows, PIXEL_1, ..., PIXEL_(ROWS*COLS)]
    returns a list of pixels equalized with the given algorithm
    """

    image = batch[2:]
    min_pixel_value, max_pixel_value = min(image), max(image)
    delta_value = max_pixel_value - min_pixel_value
    shift_level = 8 - floor(log2(delta_value + 1))

    def equalize(pixel):
        temp_pixel = (pixel - min_pixel_value) << shift_level
        return min(255, temp_pixel)

    return [equalize(x) for x in image]

def generate_ram(cols, rows):
    """
    Generates ram values for a random test case
    """

    batch = generate_batch(cols, rows)
    return [cols*rows] + batch + solve_batch(batch)
            
def main():
    test = []
    for _ in range(1, 31): #Genera 30 test
        cols, rows = randint(1, 128), randint(1, 128)
        new_test = generate_ram(cols, rows)
        test.append(new_test)

    with open('ram_content.txt','w') as w:
        for each_test in test:
            for elem in each_test:
                w.write(str(elem)+"\n")

if __name__ == '__main__':

    main()
