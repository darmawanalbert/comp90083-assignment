from map_dummy import MapGenerator
from util import get_next_direction

# TODO: Change the import later
GRID_WIDTH = 100
GRID_HEIGHT = 100
INTERSECTION = {
    "AVE_AVE": 'T',
    "AVE_ST": 't',
    "ST_AVE": '+',
    "ST_ST": '#',
    "ALL_LA": '*'
}

BUILDING = {
    "O": 'OFFICE',
    "R": 'RESIDENCE',
    "E": 'ENTERTAINMENT'
}

DIRECTION = {
    "^": [0,1],
    "v": [0,-1],
    "<": [-1,0],
    ">": [1,0]
}

def get_next_direction_list(current_direction, current_coor, destination_direction, destination_coor):
    next_direction_list = []
    if current_direction == '<' or current_direction == '>':
        next_direction_list += [current_direction for i in range(abs(current_coor[0] - destination_coor[0]))]
        next_direction_list += [destination_direction for i in range(abs(current_coor[1] - destination_coor[1]))]
    if current_direction == '^' or current_direction == 'v':
        next_direction_list += [current_direction for i in range(abs(current_coor[1] - destination_coor[1]))]
        next_direction_list += [destination_direction for i in range(abs(current_coor[0] - destination_coor[0]))]
    return next_direction_list

def get_successors(current_coordinate, previous_direction, map_instance):
    successors_list = []  #coordinates of neighbours
    current_direction = map_instance.layout[current_coordinate[0]][current_coordinate[1]]
    if (current_direction in INTERSECTION.values()):
        # print("INTERSECTION!")
        exit_points = map_instance.get_exit_point(current_coordinate, previous_direction, current_direction)
        successors_list = [x[0] for x in exit_points]

    elif (current_direction in BUILDING):
        # print("BUILDING")
        successors_list.append(map_instance.get_fringes(current_coordinate[0], current_coordinate[1])[0][0])

    else: # current_coordinate is in road, only one way to go
        # print("ELSE!")
        new_x = current_coordinate[0] + DIRECTION[current_direction][0]
        new_y = current_coordinate[1] + DIRECTION[current_direction][1]

        successors_list.append((new_x, new_y))

    return successors_list


def precompute(residence_list, office_list, entertainment_list, map_instance):
    all_pairs_shortest_path = dict()
    # Merge Office list and Entertainment, since it is a bipartite match (residence and office/entertainment)
    office_entertainment_list = office_list + entertainment_list

    # Perform BFS (Residence -> Office Entertainment)
    for residence in residence_list:
        all_pairs_shortest_path[residence] = []
        for office_entertainment in office_entertainment_list:
            print("Residence: {}\n Office: {}".format(residence, office_entertainment))
            queue = list()
            exit_direction = map_instance.get_fringes(residence[0], residence[1])[0][1] ## get direction.
            queue.append((residence, [exit_direction]))
            # -1 indicates unvisited, 1 indicates visited
            visited = [[-1 for j in range(GRID_WIDTH)] for i in range(GRID_HEIGHT)]
            while (len(queue) > 0):
                coordinate, path = queue.pop()
                # print("Current Queue: {} {}".format(coordinate, path))
                visited[coordinate[0]][coordinate[1]] = 1
                if(coordinate == office_entertainment):
                    break

                next_coordinate_list = get_successors(coordinate, path[-1], map_instance)
                current_direction = map_instance.layout[coordinate[0]][coordinate[1]]
                # print("Next Coordinate List")
                # print(next_coordinate_list)
                for next_coordinate in next_coordinate_list:
                    if (next_coordinate[0] > 0 and next_coordinate[0] < GRID_WIDTH and next_coordinate[1] > 0 and next_coordinate[1] < GRID_HEIGHT):
                        if (visited[next_coordinate[0]][next_coordinate[1]] == -1):
                            next_direction = map_instance.layout[next_coordinate[0]][next_coordinate[1]]
                            if current_direction in INTERSECTION.values():
                                new_path = path + get_next_direction_list(current_direction, coordinate, next_direction, next_coordinate)
                            elif next_direction in INTERSECTION.values():
                                new_path = path + [current_direction]
                            else:
                                new_path = path + [next_direction]
                            queue.append((next_coordinate, new_path))

            all_pairs_shortest_path[residence].append({ office_entertainment: path})
            print(path)

    # Perform BFS (Office Entertainment -> Residence)

    # for office_entertainment in office_entertainment_list:
    #     for residence in residence_list:

    return all_pairs_shortest_path


# Examples
_map = MapGenerator()
residence_list = _map.get_residence_position()
office_list = _map.get_office_position()
entertainment_list = _map.get_entertainment_position()
all_pairs_shortest_path = precompute(residence_list, office_list, entertainment_list, _map)
print(all_pairs_shortest_path)
