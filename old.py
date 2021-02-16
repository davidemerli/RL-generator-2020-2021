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

    return [cols, rows] + [randint(0, 255) for _ in range(rows * cols)]


def generate_ram(cols, rows):
    """
    Generates ram values for a random test case
    """

    batch = generate_batch(cols, rows)
    return batch + solve_batch(batch)


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


def pretty_print_ram(ram, num_test, cols, rows):
    """
    Pretty prints a single ram configuration into 'tests.txt' and 'solution.txt'.
    VHDL code snippets are written, to be copied and pasted into a test-bench file in Vivado.
    """

    test_file = open(f'test{num_test}.txt', 'w')
    sol_file = open(f'solution{num_test}.txt', 'w')

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

    print(f'Generated "test{num_test}.txt" and "solution{num_test}.txt" for a test cols:{cols} and rows:{rows}.')


def generate_vhd_testbench(ram, num_test, cols, rows):
    """
    Automatically generate a .vhd test bench that can be imported in Vivado
    """

    test_bench = open(f'test{num_test}.vhd', 'w')
    bytes_length = int(len(ram) / 2 - 1)

    test_bench.write("library ieee;\n")
    test_bench.write("use ieee.std_logic_1164.all;\n")
    test_bench.write("use ieee.numeric_std.all;\n")
    test_bench.write("use ieee.std_logic_unsigned.all;\n")
    test_bench.write("entity project_tb is\n")
    test_bench.write("end project_tb;\n")
    test_bench.write("architecture projecttb of project_tb is\n")
    test_bench.write("constant c_CLOCK_PERIOD         : time := 15 ns;\n")
    test_bench.write("signal   tb_done                : std_logic;\n")
    test_bench.write("signal   mem_address            : std_logic_vector (15 downto 0) := (others => '0');\n")
    test_bench.write("signal   tb_rst                 : std_logic := '0';\n")
    test_bench.write("signal   tb_start               : std_logic := '0';\n")
    test_bench.write("signal   tb_clk                 : std_logic := '0';\n")
    test_bench.write("signal   mem_o_data,mem_i_data  : std_logic_vector (7 downto 0);\n")
    test_bench.write("signal   enable_wire            : std_logic;\n")
    test_bench.write("signal   mem_we                 : std_logic;\n")
    test_bench.write("type ram_type is array (65535 downto 0) of std_logic_vector(7 downto 0);\n")
    test_bench.write("signal RAM: ram_type := (\n")

    for element_position in range(bytes_length + 2):
        test_bench.write(f'\t\t\t{element_position} => std_logic_vector(to_unsigned({ram[element_position]}, 8)),\n')

    test_bench.write("\t\t\tothers => (others => '0'));\n")

    test_bench.write("component project_reti_logiche is\n")
    test_bench.write("port (\n")
    test_bench.write("      i_clk         : in  std_logic;\n")
    test_bench.write("      i_rst         : in  std_logic;\n")
    test_bench.write("      i_start       : in  std_logic;\n")
    test_bench.write("      i_data        : in  std_logic_vector(7 downto 0);\n")
    test_bench.write("      o_address     : out std_logic_vector(15 downto 0);\n")
    test_bench.write("      o_done        : out std_logic;\n")
    test_bench.write("      o_en          : out std_logic;\n")
    test_bench.write("      o_we          : out std_logic;\n")
    test_bench.write("      o_data        : out std_logic_vector (7 downto 0)\n")
    test_bench.write("      );\n")
    test_bench.write("end component project_reti_logiche;\n")
    test_bench.write("begin\n")
    test_bench.write("UUT: project_reti_logiche\n")
    test_bench.write("port map (\n")
    test_bench.write("          i_clk      	=> tb_clk,\n")
    test_bench.write("          i_rst      	=> tb_rst,\n")
    test_bench.write("          i_start       => tb_start,\n")
    test_bench.write("          i_data    	=> mem_o_data,\n")
    test_bench.write("          o_address  	=> mem_address,\n")
    test_bench.write("          o_done      	=> tb_done,\n")
    test_bench.write("          o_en   	=> enable_wire,\n")
    test_bench.write("          o_we 		=> mem_we,\n")
    test_bench.write("          o_data    	=> mem_i_data\n")
    test_bench.write("          );\n\n")
    test_bench.write("p_CLK_GEN : process is\n")
    test_bench.write("begin\n")
    test_bench.write("    wait for c_CLOCK_PERIOD/2;\n")
    test_bench.write("    tb_clk <= not tb_clk;\n")
    test_bench.write("end process p_CLK_GEN;\n")
    test_bench.write("MEM : process(tb_clk)\n")
    test_bench.write("begin\n")
    test_bench.write("    if tb_clk'event and tb_clk = '1' then\n")
    test_bench.write("        if enable_wire = '1' then\n")
    test_bench.write("            if mem_we = '1' then\n")
    test_bench.write("                RAM(conv_integer(mem_address))  <= mem_i_data;\n")
    test_bench.write("                mem_o_data                      <= mem_i_data after 1 ns;\n")
    test_bench.write("            else\n")
    test_bench.write("                mem_o_data <= RAM(conv_integer(mem_address)) after 1 ns;\n")
    test_bench.write("            end if;\n")
    test_bench.write("        end if;\n")
    test_bench.write("    end if;\n")
    test_bench.write("end process;\n")
    test_bench.write("test : process is\n")
    test_bench.write("begin \n")
    test_bench.write("    wait for 100 ns;\n")
    test_bench.write("    wait for c_CLOCK_PERIOD;\n")
    test_bench.write("    tb_rst <= '1';\n")
    test_bench.write("    wait for c_CLOCK_PERIOD;\n")
    test_bench.write("    wait for 100 ns;\n")
    test_bench.write("    tb_rst <= '0';\n")
    test_bench.write("    wait for c_CLOCK_PERIOD;\n")
    test_bench.write("    wait for 100 ns;\n")
    test_bench.write("    tb_start <= '1';\n")
    test_bench.write("    wait for c_CLOCK_PERIOD;\n")
    test_bench.write("    wait until tb_done = '1';\n")
    test_bench.write("    wait for c_CLOCK_PERIOD;\n")
    test_bench.write("    tb_start <= '0';\n")
    test_bench.write("    wait until tb_done = '0';\n")
    test_bench.write("    wait for 100 ns;\n")

    for element_position in range(bytes_length + 2, 2 * bytes_length + 2):
        test_bench.write(
            f'\tassert RAM({element_position}) = std_logic_vector(to_unsigned({ram[element_position]}, 8))')
        test_bench.write(f' report \"TEST FALLITO (WORKING ZONE). ')
        test_bench.write(f'Expected  {ram[element_position]}  ')
        test_bench.write(f'found \" & integer\'image(to_integer(unsigned(RAM({element_position}))))  ')
        test_bench.write(f'severity failure;\n')

    test_bench.write("    assert false report \"Simulation Ended! TEST PASSATO\" severity failure;\n")
    test_bench.write("end process test;\n")
    test_bench.write("end projecttb;\n")

    print(f'Generated "test{num_test}.vhd" for a test cols:{cols} and rows:{rows}.')


def main():
    # UNCOMMENT TO GENERATE RAW TESTS
    # generate_raw_tests()

    # Generate a single random test
    num_tests = int(input("How many tests do you want to generate?: "))
    mode = input("Automatically generate importable test benches? Yes or No? ")

    for i in range(1, num_tests + 1):
        cols, rows = randint(1, 128), randint(1, 128)
        ram = generate_ram(cols, rows)

        if mode == "Yes":
            # Create the whole test bench
            generate_vhd_testbench(ram, i, cols, rows)

        if mode == "No":
            # Pretty print into VHDL code snippets
            pretty_print_ram(ram, i, cols, rows)


if __name__ == '__main__':
    main()
