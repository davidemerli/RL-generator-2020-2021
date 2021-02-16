from math import floor, log2
from random import randint
from tqdm import tqdm
import click


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

 
@click.command()
@click.option('--size', default=100, show_default=True, help='Number of tests to generate')
@click.option('--limit', default=128, show_default=True, help='Maximum row/col size')
def main(size, limit):
    with open('ram_content.txt', 'w') as ram, open('test_values.txt', 'w') as readable:
        for i in tqdm(range(size), desc='Generating tests', dynamic_ncols=True):
            cols, rows = randint(1, limit), randint(1, limit)
            test = generate_ram(cols, rows)

            for value in test:
                ram.write(f'{value}\n')

            written_ram = ' '.join([str(v) for v in test])
            readable.write(f'{i}) {test[1]} cols, {test[2]} rows: {test[0]} pixels \t\t RAM: {written_ram}\n')


if __name__ == '__main__':
    main()
