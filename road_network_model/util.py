import math

def get_euclidean_distance(coor1, coor2):
    distance = math.sqrt(
        ((coor1[0]-coor2[0]) ** 2) +
        ((coor1[1]-coor2[1]) ** 2)
    )

    return distance

def is_opposite_direction(current_direction, destination_direction):
    if current_direction == '<' and destination_direction == '>':
        return True
    if current_direction == '>' and destination_direction == '<':
        return True
    if current_direction == '^' and destination_direction == 'v':
        return True
    if current_direction == 'v' and destination_direction == '^':
        return True
    return False

def get_next_direction(current_direction, current_coor, destination_direction, destination_coor):
    if current_direction == destination_direction:
        return current_direction

    if is_opposite_direction(current_direction, destination_direction):
        return '_'

    if current_direction == '<' or current_direction == '>':
        if current_coor[0] != destination_coor[0]:
            return current_direction
        return destination_direction

    if current_direction == '^' or current_direction == 'v':
        if current_coor[1] != destination_coor[1]:
            return current_direction
        return destination_direction

    return '_'