# Politecnico di Milano - Progetto Reti Logiche 2020-2021

## Test Generator

written in python3

### How to install

To install dependencies

```bash
pip3 install -r requirements.txt 
```

or

```bash
pip install -r requirements.txt 
```

depending on system installation

### How to generate tests

```bash
python3 generator.py
```

or

```bash
python generator.py
```

depending on system installation

```txt
Usage: generator.py [OPTIONS]

Options:
  --size INTEGER   Number of tests to generate  [default: 100]
  --limit INTEGER  Maximum row/col size  [default: 128]
  --help           Show this message and exit.
```

```test_values.txt``` will contain all details about every single generated test, for debugging.
```ram_content.txt``` is the file that will be read by Vivado to load the ram values

Example:

```sh
python generator.py --size 1000 --limit 16
```

### How to import in Vivado

You can directly import the ```gen_testbench.vhd``` file as source in Vivado, then modify this file to match the folder containing the generated ram files. Instruction on how to modify it are included in the .vhd file itself.

<!-- #### Example output
test.txt:
```
8
signal RAM: ram_type := (
			0 => std_logic_vector(to_unsigned(4, 8)),
			1 => std_logic_vector(to_unsigned(2, 8)),
			2 => std_logic_vector(to_unsigned(158, 8)),
			3 => std_logic_vector(to_unsigned(26, 8)),
			4 => std_logic_vector(to_unsigned(105, 8)),
			5 => std_logic_vector(to_unsigned(139, 8)),
			6 => std_logic_vector(to_unsigned(79, 8)),
			7 => std_logic_vector(to_unsigned(110, 8)),
			8 => std_logic_vector(to_unsigned(20, 8)),
			9 => std_logic_vector(to_unsigned(242, 8)),
			others => (others => '0'));
```

solution.txt
```
	assert RAM(10) = std_logic_vector(to_unsigned(255, 8)) report "TEST FALLITO (WORKING ZONE). Expected  255  found " & integer'image(to_integer(unsigned(RAM(10))))  severity failure;
	assert RAM(11) = std_logic_vector(to_unsigned(12, 8)) report "TEST FALLITO (WORKING ZONE). Expected  12  found " & integer'image(to_integer(unsigned(RAM(11))))  severity failure;
	assert RAM(12) = std_logic_vector(to_unsigned(170, 8)) report "TEST FALLITO (WORKING ZONE). Expected  170  found " & integer'image(to_integer(unsigned(RAM(12))))  severity failure;
	assert RAM(13) = std_logic_vector(to_unsigned(238, 8)) report "TEST FALLITO (WORKING ZONE). Expected  238  found " & integer'image(to_integer(unsigned(RAM(13))))  severity failure;
	assert RAM(14) = std_logic_vector(to_unsigned(118, 8)) report "TEST FALLITO (WORKING ZONE). Expected  118  found " & integer'image(to_integer(unsigned(RAM(14))))  severity failure;
	assert RAM(15) = std_logic_vector(to_unsigned(180, 8)) report "TEST FALLITO (WORKING ZONE). Expected  180  found " & integer'image(to_integer(unsigned(RAM(15))))  severity failure;
	assert RAM(16) = std_logic_vector(to_unsigned(0, 8)) report "TEST FALLITO (WORKING ZONE). Expected  0  found " & integer'image(to_integer(unsigned(RAM(16))))  severity failure;
	assert RAM(17) = std_logic_vector(to_unsigned(255, 8)) report "TEST FALLITO (WORKING ZONE). Expected  255  found " & integer'image(to_integer(unsigned(RAM(17))))  severity failure;

```

### Main Functions, if you want to hack with the generator:
For example, to create 100 random tests (in raw form, aka as a single output line): 

```python
generate_raw_tests(to_generate=100)
```

To pretty print a test:

```python
# Generate a single random test
cols, rows = randint(1, 128), randint(1, 128)
ram = generate_ram(cols, rows)

# Pretty print into VHDL code snippets
pretty_print_ram(ram)
```
-->

### Credits
Pretty print function by [Daniele Locatelli](https://github.com/locadani)

Importing RAM from outside feature by [Davide Mornatta](https://github.com/davidemornatta)

Original testbench code by [Mark Zampedroni](https://github.com/Mark-Zampedroni) [here](https://github.com/Mark-Zampedroni/multi-TB-progetto-Reti-PoliMi)