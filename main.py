from math import floor, log2
from random import randint
import numpy as np


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


def generate_batch(cols, rows):
    """
    Given the number of columns and rows, returns a random pixel array with 2 + (rows * cols) elements

    The first two elements are the image dimensions as specified in the document
    """

    return [cols, rows] + [randint(0, 256) for _ in range(rows * cols)]


def print_image(ram):
    """
    Given a list representing ram values, visualizes the image before and after the equalization.

    Not needed for generation purposes.
    """
    
    image = np.array(ram[2:-len(ram)//2 + 1])
    image = image.reshape(ram[1], ram[0])

    print(image)

    image = np.array(ram[2 + len(ram)//2 - 1:])
    image = image.reshape(ram[1], ram[0])

    print(image)


def generate_ram(cols, rows):
    """
    Generates ram values for a random test case
    """

    batch = generate_batch(cols, rows)
    return batch + solve_batch(batch)


cols, rows = 4, 3

def examples():
    """
    Prints example batches + solves from specification document
    """

    # example batch 1
    batch = [4, 3, 76, 131, 109, 89, 46, 121, 62, 59, 46, 77, 68, 94]

    print('\n\nbatch 1\n')
    ram = batch + solve_batch(batch)
    print_image(ram)

    # example batch 2
    batch = [4, 3, 0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 120]

    print('\n\nbatch 2\n')
    ram = batch + solve_batch(batch)
    print_image(ram)

    # example batch 3
    batch = [4, 3, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133]

    print('\n\nbatch 3\n')
    ram = batch + solve_batch(batch)
    print_image(ram)


def main():
    """
    Generates 'TESTS' new tests, in the file tests.txt

    Every test is a row with the test index, a closed bracket, and ram values for the test
    """

    TESTS = 100

    with open('tests.txt', 'w') as test_file:
        for i in range(TESTS):
            cols, rows = randint(1, 129), randint(1, 129)

            ram = generate_ram(cols, rows)
            test_file.write(f'{i + 1}) {" ".join([str(x) for x in ram])}\n')


if __name__ == '__main__':
    # UNCOMMENT THIS TO SHOW EXAMPLE
    # examples() 
    
    main()

