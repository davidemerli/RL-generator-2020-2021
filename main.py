from math import floor, log2
from random import randint


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


def generate_raw_tests(to_generate=10):
    """
    Generates 'to_generate' new tests, in the file tests.txt

    Every test is a row with the test index, a closed bracket, and ram values for the test
    """

    with open('tests.txt', 'w') as test_file:
        for i in range(to_generate):
            cols, rows = randint(1, 128), randint(1, 128)

            ram = generate_ram(cols, rows)
            test_file.write(f'{i + 1}) {" ".join([str(x) for x in ram])}\n')


def pretty_print_ram(ram):
    """
    Pretty prints a single ram configuration into 'tests.txt' and 'solution.txt'.
    VHDL code snippets are written, to be copied and pasted into a test-bench file in Vivado.
    """

    test_file = open('test.txt', 'w')
    sol_file = open('solution.txt', 'w')

    bytes_length = int(len(ram) / 2 - 1)
    test_file.write(f'{bytes_length}\n')

    test_file.write("signal RAM: ram_type := (\n")

    for element_position in range(bytes_length + 2):
        test_file.write(f'\t\t\t{element_position} => std_logic_vector(to_unsigned({ram[element_position]}, 8)),\n')

    test_file.write("\t\t\tothers => (others => '0'));\n\n")

    for element_position in range(bytes_length + 2, 2 * bytes_length + 2):
        sol_file.write(f'\tassert RAM({element_position}) = std_logic_vector(to_unsigned({ram[element_position]}, 8))')
        sol_file.write(f' report \"TEST FALLITO (WORKING ZONE). ')
        sol_file.write(f'Expected  {ram[element_position]}  ')
        sol_file.write(f'found \" & integer\'image(to_integer(unsigned(RAM({element_position}))))  ')
        sol_file.write(f'severity failure;\n')

    print(f'Generated "test.txt" and "solution.txt" for a test with {bytes_length} bytes.')


def main():
    # UNCOMMENT TO GENERATE RAW TESTS
    # generate_raw_tests()

    # Generate a single random test
    cols, rows = randint(1, 128), randint(1, 128)
    ram = generate_ram(cols, rows)

    # Pretty print into VHDL code snippets
    pretty_print_ram(ram)


if __name__ == '__main__':
    # UNCOMMENT THIS TO SHOW EXAMPLE
    # examples()

    main()
