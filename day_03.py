import numpy as np


class Line:
    def __init__(self, *args, **kwargs):
        if len(args) == 0:
            original = kwargs.get('original')
            self.range = original.range
            self.steps = original.steps
            self.direction = original.direction
        else:
            self.range = args[0]
            self.steps = args[1]
            self.direction = args[2]


class HorizontalLine(Line):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if len(args) == 0:
            self.y = kwargs.get('original').y
        else:
            self.y = args[3]


class VerticalLine(Line):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if len(args) == 0:
            self.x = kwargs.get('original').x
        else:
            self.x = args[3]


def parse_paths(filename="data/input_day_03.txt"):
    with open(filename, 'r') as input_file:
        result = list()
        for line in input_file:
            wire_path = [(move[0], int(move[1:])) for move in line.split(",")]
            parsed_path = list()
            current_x = 0
            current_y = 0
            steps = 0
            for move_type, distance in wire_path:
                if move_type == "R" or move_type == "L":
                    new_x = current_x + distance if move_type == "R" else current_x - distance
                    steps += abs(distance)
                    parsed_path.append(HorizontalLine(range(current_x, new_x) if new_x > current_x
                                                       else range(new_x, current_x), steps, move_type, current_y))
                    current_x = new_x
                else:
                    new_y = current_y + distance if move_type == "U" else current_y - distance
                    steps += abs(distance)
                    parsed_path.append(VerticalLine(range(current_y, new_y) if new_y > current_y
                                                     else range(new_y, current_y), steps, move_type, current_x))
                    current_y = new_y
            result.append(parsed_path)
        return result


def get_intersections(wire_paths):
    result = list()
    horizontals = [line for line in wire_paths[0] if isinstance(line, HorizontalLine)]
    verticals = [line for line in wire_paths[0] if isinstance(line, VerticalLine)]
    for line in wire_paths[1]:
        if isinstance(line, VerticalLine):
            intersections = [(VerticalLine(original=line), HorizontalLine(original=h_line)) for h_line in horizontals
                             if h_line.y in line.range and line.x in h_line.range]
            result.extend(intersections) if len(intersections) != 0 else None
        else:
            intersections = [(VerticalLine(original=v_line), HorizontalLine(original=line)) for v_line in verticals
                             if v_line.x in line.range and line.y in v_line.range]
            result.extend(intersections) if len(intersections) > 0 else None
    for v_line, h_line in result:
        if v_line.direction == "U":
            v_line.steps -= (v_line.range.stop - h_line.y)
        else:
            v_line.steps -= (h_line.y - v_line.range.start)
        if h_line.direction == "R":
            h_line.steps -= (h_line.range.stop - v_line.x)
        else:
            h_line.steps -= (v_line.x - h_line.range.start)
    return result


def get_closest_intersection_to_port(intersections):
    inters = [(v_line.x, h_line.y) for v_line, h_line in intersections if v_line.x != 0 or h_line.y != 0]
    inters.sort(key=lambda tup: abs(tup[0]) + abs(tup[1]))
    return sum(inters[0]) if len(inters) > 0 else None


def get_intersection_with_shortest_path(intersections):
    inters = [(v_line.steps, h_line.steps) for v_line, h_line in intersections if v_line.x != 0 or h_line.y != 0]
    inters.sort(key=lambda tup: tup[0] + tup[1])
    return sum(inters[0]) if len(inters) > 0 else None


print(get_closest_intersection_to_port(get_intersections(parse_paths())))
print(get_intersection_with_shortest_path(get_intersections(parse_paths())))
