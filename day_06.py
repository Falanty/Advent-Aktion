class Orb:
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


def find_orbital_in_system(orb_name, system):
    if orb_name == system.name:
        return system
    if not system.children:
        return None
    for orbital in system.children:
        orbital_found = find_orbital_in_system(orb_name, orbital)
        if orbital_found is not None:
            return orbital_found
    return None


def insert_orbital_relation(parent_name, orbital_name, system):
    parent_in_system = find_orbital_in_system(parent_name, system)
    orbital_in_system = find_orbital_in_system(orbital_name, system)
    if parent_in_system is None:
        parent_in_system = Orb(parent_name, system)
        system.children.append(parent_in_system)
    if orbital_in_system is not None:
        orbital_in_system.set_parent(parent_in_system)
    else:
        parent_in_system.children.append(Orb(orbital_name, parent_in_system))


def build_solar_system(map_data):
    com = Orb("COM", None)
    for parent, orbital in map_data:
        if parent == "COM":
            continue
        insert_orbital_relation(parent, orbital, com)
    return com


def get_orbital_distances(system, distances):
    distances.append(system.distance_to_com)
    for orbital in system.children:
        get_orbital_distances(orbital, distances)
    return distances


def calculate_orbital_transfers(start_orbital, end_orbital, transfers_up=0):
    target_found, transfers = calculate_orbital_transfers_down(start_orbital.parent, end_orbital)
    if target_found:
        return transfers + transfers_up
    return calculate_orbital_transfers(start_orbital.parent, end_orbital, transfers_up + 1) \
        if start_orbital.parent else -1


def calculate_orbital_transfers_down(start_orbital, end_orbital, transfers_down=0):
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
print(calculate_orbital_transfers(find_orbital_in_system("YOU", universe), find_orbital_in_system("SAN", universe)))
