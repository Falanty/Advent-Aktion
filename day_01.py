import numpy as np


def fuel_calculation(weight):
    return np.floor(weight / 3) - 2


def total_fuel(weight):
    """
    Returns fuel.

    >>> total_fuel(1969.0)
    966.0
    """
    fuel_needed = fuel_calculation(weight)
    result = 0
    while fuel_needed > 0:
        result += fuel_needed
        fuel_needed = fuel_calculation(fuel_needed)
    return result


def fuel_for_modules(fuel_calculator, filename="data/input_day_01.txt"):
    with open(filename, 'r') as input_file:
        return np.sum([fuel_calculator(float(line)) for line in input_file])


print(fuel_for_modules(fuel_calculation))
print(fuel_for_modules(total_fuel))
