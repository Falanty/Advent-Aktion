class Planet:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.distance_to_com = parent.distance_to_com + 1 if parent is not None else 0
        self.children = list()

    def set_parent(self, parent):
        self.parent.children.remove(self) if parent is not None else None
        self.parent = parent
        self.distance_to_com = parent.distance_to_com + 1
        self.update_children()
        parent.children.append(self)

    def update_children(self):
        for orbital in self.children:
            orbital.distance_to_com = self.distance_to_com + 1
            orbital.update_children()


def parse_map_data(filename="data/input_day_06.txt"):
    with open(filename, 'r') as input_file:
        map_data = [tuple(orbit_relation.split(")")) for orbit_relation in list(input_file.read().split("\n"))]
    return map_data


def find_planet_in_system(planet_name, system):
    if planet_name == system.name:
        return system
    if not system.children:
        return None
    for planet in system.children:
        planet_found = find_planet_in_system(planet_name, planet)
        if planet_found is not None:
            return planet_found
    return None


def insert_planet_relation(parent_name, orbital_name, system):
    parent_in_system = find_planet_in_system(parent_name, system)
    orbital_in_system = find_planet_in_system(orbital_name, system)
    if parent_in_system is None:
        parent_in_system = Planet(parent_name, system)
        system.children.append(parent_in_system)
    if orbital_in_system is not None:
        orbital_in_system.set_parent(parent_in_system)
    else:
        parent_in_system.children.append(Planet(orbital_name, parent_in_system))


def build_solar_system(map_data):
    com = Planet("COM", None)
    for parent, orbital in map_data:
        if parent == "COM":
            continue
        insert_planet_relation(parent, orbital, com)
    return com


def get_orbital_distances(system, distances):
    distances.append(system.distance_to_com)
    for orbital in system.children:
        get_orbital_distances(orbital, distances)
    return distances


def calculate_orbital_transfers(start_orbital, end_orbital, transfers_up):
    found_target, transfers = calculate_orbital_transfers_down(start_orbital.parent, end_orbital, 0)
    if found_target:
        return transfers + transfers_up
    return calculate_orbital_transfers(start_orbital.parent, end_orbital, transfers_up + 1) \
        if start_orbital.parent else -1


def calculate_orbital_transfers_down(start_orbital, end_orbital, transfers_down):
    if end_orbital in start_orbital.children:
        return True, transfers_down
    elif start_orbital.children:
        for orbital in start_orbital.children:
            found_target, transfers = calculate_orbital_transfers_down(orbital, end_orbital, transfers_down + 1)
            if found_target:
                return found_target, transfers
    return False, 0


universe = build_solar_system(parse_map_data())
print(sum(get_orbital_distances(universe, [])))
print(calculate_orbital_transfers(find_planet_in_system("YOU", universe), find_planet_in_system("SAN", universe), 0))
