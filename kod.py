import random
import matplotlib.pyplot as plt
from Facility import Facility
from Point import Point
from Operators import Operators

facs_coordinates_global = [
    (41.08394267984579, 28.225010755222666),
    (41.04750293183692, 28.42321073814882),
    (41.0936471214164, 28.87669948742291),
    (41.109217956770486, 28.286938832629417),
    (41.06219218196853, 28.22979721943807),
    (41.04186379748036, 28.705355288103362),
    (41.02265359696839, 28.398837650686648),
    (41.08498844377795, 28.744941480603217),
    (41.04204406220407, 28.789265683875907),
    (41.10094304566778, 28.20649875967806)
]


points_coordinates_global = [
    (41.08394267984579, 28.225010755222666),
    (41.04750293183692, 28.42321073814882),
    (41.0936471214164, 28.87669948742291),
    (41.109217956770486, 28.286938832629417),
    (41.06219218196853, 28.22979721943807),
    (41.04186379748036, 28.705355288103362),
    (41.02265359696839, 28.398837650686648),
    (41.08498844377795, 28.744941480603217),
    (41.04204406220407, 28.789265683875907),
    (41.10094304566778, 28.20649875967806),
    (41.100581925183285, 28.898139394988227),
    (41.054025051651806, 28.355479499811782),
    (41.11572130722068, 28.536594545112624),
    (41.02927458433802, 28.296716376833462),
    (41.10474943663475, 28.80372603136689),
    (41.10071282732744, 28.929731786693818),
    (41.073622809145476, 29.17311576397937),
    (41.05785343772084, 28.752040631273225),
    (41.1029404664253, 28.818519752364246),
    (41.10617069003108, 28.77735214525676),
    (41.090457183621496, 28.245824383655663),
    (41.04278982756516, 28.489387963602105),
    (41.02797919769237, 28.43279088636103),
    (41.030100142940974, 28.47797360311009),
    (41.08356844442644, 28.564832178970082),
    (41.057018096711694, 28.409507030771486),
    (41.046697782204916, 29.136654587712492),
    (41.08480353852466, 28.809131005666988),
    (41.037113864819815, 28.92912679795035),
    (41.036340249376195, 28.57945544175765),
    (41.11895233506366, 28.83999975985409),
    (41.07569497437747, 28.884614250989873),
    (41.104285192018985, 28.975999911546243),
    (41.042904807196415, 28.232100243904036),
    (41.05154530480591, 28.467740875975704),
    (41.04109828435863, 29.142909714335055),
    (41.10763676264727, 28.514677880798477),
    (41.08554386652949, 28.595631901060663),
    (41.111454758974055, 28.658851852587397),
    (41.04648801664981, 28.446627507693982),
    (41.07613681341632, 28.462741608522933),
    (41.078458599022355, 29.097822883602475),
    (41.059940050514044, 28.419320759157284),
    (41.119753760649516, 28.709526293676465),
    (41.02909094121738, 28.247116375424735),
    (41.03096491303507, 28.82744604170309),
    (41.0992079364363, 28.622159966799682),
    (41.0263527706152, 28.581619286506537),
    (41.11961213802401, 28.729114345099138),
    (41.11710783776137, 29.0607797022345)
]


def main():
    operator = Operators()

    candidate_facility_number = 10
    point_amount = 50
    facs_coordinates =  facs_coordinates_global # operator.create_distance_matrix(candidate_facility_number, 2)
    points_coordinates =  points_coordinates_global# operator.create_distance_matrix(point_amount, 2)
    facs = [Facility(i, facs_coordinates[i][0], facs_coordinates[i][1], 20 * random.random() + 50) for i in range(candidate_facility_number)]
    points = [Point(i, points_coordinates[i][0], points_coordinates[i][1], 2 * random.random() + 1) for i in range(point_amount)]
    distance_matrix = operator.distance_matrix(facs, points)
    
    # Store opened facilities and other lists, you need to use these arrays.
    opened_facilities = []
    unopened_facilities = facs.copy()
    unassigned_points = points.copy()

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
    while len(opened_facilities) < open_p_num_of_facs:
        for y in range(len(facs)):
            total_distance = sum(distance_matrix[y])
            if total_distance < min_value and facs[y] not in opened_facilities:
                min_value = total_distance
                index_of = y

        opened_facilities.append(facs[index_of])
        unopened_facilities.remove(facs[index_of])
        previous_min = min_value
        min_value = max_val + 1

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
        else:
            unassigned_points.append(point)

    # Calculate total distance
    total_distance = calculate_total_distance(points, opened_facilities, operator)
    print(f"Total Distance: {total_distance}")

    # Plot facilities and assigned points
    plot_facilities_and_points(opened_facilities, unopened_facilities, points)

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
