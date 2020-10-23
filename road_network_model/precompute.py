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

REV_DIRECTION = {
    "^": [0,-1],
    "v": [0,1],
    "<": [1,0],
    ">": [-1,0]
}

def get_successors(current_coor, prev_direction, prev_coor, map_instance):
    delta_x = [0,1,0,-1]
    delta_y = [1,0,-1,0]

    successors_list = []  #coordinates of neighbours
    current_direction = map_instance.layout[current_coor[0]][current_coor[1]]
    if (current_direction in INTERSECTION.values()):
        print("current_coor:", current_coor, ", prev_direction:", prev_direction,", current_direction:", current_direction)
        exit_points = map_instance.get_exit_point(current_coor, prev_direction, current_direction)
        successors_list = [x[0] for x in exit_points]

    elif (current_direction == 'x'):
        next_direction = get_next_direction(prev_direction, prev_coor, current_direction, current_coor)
        print("next_direction:", next_direction)

        new_x = current_coor[0] + DIRECTION[next_direction][0]
        new_y = current_coor[1] + DIRECTION[next_direction][1]

        successors_list.append((new_x, new_y))
        #successors_list = [x[0] for x in exit  _points]

    elif (current_direction in BUILDING):
        successors_list.append(map_instance.get_fringes(current_coor[0], current_coor[1])[0][0])

    else: # current_coor is in road, only one way to go
        new_x = current_coor[0] + DIRECTION[current_direction][0]
        new_y = current_coor[1] + DIRECTION[current_direction][1]

        successors_list.append((new_x, new_y))
        #for i in range(4):
        #    new_x = current_coor[0] + delta_x[i]
        #    new_y = current_coor[1] + delta_y[i]
        #    if map_instance.layout[new_x][new_y] == map_instance.layout[current_coor[0]][current_coor[1]]:
        #        successors_list = i

    return successors_list


def precompute(residence_list, office_list, entertainment_list, map_instance):
    delta_x = [0,1,0,-1]
    delta_y = [1,0,-1,0]
    all_pairs_shortest_path = dict()
    # Merge Office list and Entertainment, since it is a bipartite match (residence and office/entertainment)
    office_entertainment_list = office_list + entertainment_list

    delta_x = []
    # Perform BFS (Residence -> Office Entertainment)
    for residence in residence_list:
        all_pairs_shortest_path[residence] = []
        for office_entertainment in office_entertainment_list:
            queue = list()
            exit_direction = map_instance.get_fringes(residence[0], residence[1])[0][1] ## get direction.
            queue.append((residence, exit_direction, (residence[0], residence[1])))
            visited = [[-1 for j in range(GRID_WIDTH)] for i in range(GRID_HEIGHT)]
            while (len(queue) > 0):
                coordinate, path, coordinate_list = queue.pop()
                visited[coordinate[0]][coordinate[1]] = 1
                if(coordinate == office_entertainment):
                    break

                next_coordinate_list = get_successors(coordinate, path[len(path) - 1], coordinate_list[len(coordinate_list) - 1], map_instance)
                print("YOYOYOYO")
                print(next_coordinate_list)
                for next_coordinate in next_coordinate_list:
                    if (next_coordinate[0] > 0 and next_coordinate[0] < GRID_WIDTH and next_coordinate[1] > 0 and next_coordinate[1] < GRID_HEIGHT):
                        if (visited[next_coordinate[0]][next_coordinate[1]] == -1):
                            new_path = path + map_instance.layout[next_coordinate[0]][next_coordinate[1]]
                            new_coordinate = coordinate + next_coordinate
                            queue.append((next_coordinate, new_path, new_coordinate))

            all_pairs_shortest_path[residence].append({ office_entertainment: path})

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
