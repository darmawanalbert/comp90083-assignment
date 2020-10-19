import math

def get_euclidean_distance(coor1, coor2):
    distance = math.sqrt(
        ((coor1[0]-coor2[0]) ** 2) +
        ((coor1[1]-coor2[1]) ** 2)
    )

    return distance