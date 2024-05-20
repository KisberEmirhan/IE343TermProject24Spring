import random
import matplotlib.pyplot as plt
from Facility import Facility
from Point import Point
from Operators import Operators
from kod import points_coordinates_global, facs_coordinates_global

def main():
    operator = Operators()

    candidate_facility_number = 10
    point_amount = 50
    facs_coordinates =  facs_coordinates_global # operator.create_distance_matrix(candidate_facility_number, 2)
    facs = [Facility(i, facs_coordinates[i][0], facs_coordinates[i][1], 20 * random.random() + 50) for i in range(candidate_facility_number)]
    points_coordinates =  points_coordinates_global# operator.create_distance_matrix(point_amount, 2)    facs = [Facility(i, facs_coordinates[i][0], facs_coordinates[i][1], 20 * random.random() + 50) for i in range(candidate_facility_number)]
    points = [Point(i, points_coordinates[i][0], points_coordinates[i][1], 2 * random.random() + 1) for i in range(point_amount)]
    
    # Store opened facilities and other lists, you need to use these arrays.
    opened_facilities = []
    unopened_facilities = facs.copy()
    unassigned_points = points.copy()

    # Number of facilities to open
    open_p_num_of_facs = 3

    # Improved heuristic start with k-means like approach
    for _ in range(open_p_num_of_facs):
        best_facility = None
        min_total_distance = float('inf')

        for fac in unopened_facilities:
            current_total_distance = 0
            for point in unassigned_points:
                dist = operator.distance_from(fac.x, fac.y, point.x, point.y)
                current_total_distance += dist

            if current_total_distance < min_total_distance:
                min_total_distance = current_total_distance
                best_facility = fac

        if best_facility:
            opened_facilities.append(best_facility)
            unopened_facilities.remove(best_facility)
            newly_assigned_points = []

            for point in unassigned_points:
                min_distance = float('inf')
                assigned_facility = None
                for fac in opened_facilities:
                    dist = operator.distance_from(point.x, point.y, fac.x, fac.y)
                    if dist < min_distance:
                        min_distance = dist
                        assigned_facility = fac

                if assigned_facility:
                    point.assigned_facility_id = assigned_facility.id
                    newly_assigned_points.append(point)

            for point in newly_assigned_points:
                unassigned_points.remove(point)

    # Refinement step
    refine_assignments(points, opened_facilities, operator)

    # Calculate total distance
    total_distance = calculate_total_distance(points, opened_facilities, operator)
    print(f"Total Distance: {total_distance}")

    # Plot facilities and assigned points
    plot_facilities_and_points(opened_facilities, unopened_facilities, points)

def refine_assignments(points, opened_facilities, operator):
    for _ in range(10):  # Number of refinement iterations
        for point in points:
            min_distance = float('inf')
            assigned_facility = None
            for fac in opened_facilities:
                dist = operator.distance_from(point.x, point.y, fac.x, fac.y)
                if dist < min_distance:
                    min_distance = dist
                    assigned_facility = fac
            if assigned_facility:
                point.assigned_facility_id = assigned_facility.id

def calculate_total_distance(points, opened_facilities, operator):
    total_distance = 0
    for point in points:
        assigned_facility = next((fac for fac in opened_facilities if fac.id == point.assigned_facility_id), None)
        if assigned_facility:
            total_distance += operator.distance_from(point.x, point.y, assigned_facility.x, assigned_facility.y)
    return total_distance

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
