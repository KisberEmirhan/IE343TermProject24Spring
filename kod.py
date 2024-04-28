import random
import matplotlib.pyplot as plt
from Facility import Facility
from Point import Point
from Operators import Operators

def main():
    operator = Operators()

    candidate_facility_number = 10
    point_amount = 50
    facs_coordinates = operator.create_distance_matrix(candidate_facility_number, 2)
    points_coordinates = operator.create_distance_matrix(point_amount, 2)
    facs = [Facility(i, facs_coordinates[i][0], facs_coordinates[i][1], 20 * random.random() + 50) for i in range(candidate_facility_number)]
    points = [Point(i, points_coordinates[i][0], points_coordinates[i][1], 2 * random.random() + 1) for i in range(point_amount)]
    distance_matrix = operator.distance_matrix(facs, points)
    
    # Store opened facilities and other lists, you need to use these arrays.
    opened_facilities = []
    unopened_facilities = facs.copy()
    unassigned_points = []


    # Number of facilities to open
    open_p_num_of_facs = 3
    total_distance = 0
    min_value = float('inf')
    index_of = 0
    previous_min = -1
    max_val = 0

    # Find a huge value to set min_value for comparison
    for y in range(len(facs)):
        total_distance = sum(distance_matrix[y])
        if max_val < total_distance:
            max_val = total_distance
    min_value = max_val + 1

    #Start coding here

    # Plot facilities and assigned points
    plot_facilities_and_points(opened_facilities, unopened_facilities, points)

def plot_facilities_and_points(opened_facilities, unopened_facilities, points):
    colors = {}
    color_list = ['blue', 'red', 'green', 'purple', 'orange', 'cyan', 'pink', 'yellow', 'brown', 'linen']
    for i, fac in enumerate(opened_facilities):
        colors[fac.id] = color_list[i % len(color_list)]

    for fac in unopened_facilities:
        plt.scatter(fac.x, fac.y, c='black', marker='^')

    for fac in opened_facilities:
        plt.scatter(fac.x, fac.y, c=colors[fac.id], marker='^')

    for point in points:
        if point.assigned_facility_id is not None:
            plt.scatter(point.x, point.y, c=colors[point.assigned_facility_id], marker='o')

    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.title('Facilities and Assigned Points')

    plt.show()

if __name__ == "__main__":
    main()