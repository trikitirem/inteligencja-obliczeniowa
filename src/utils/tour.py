import random
from typing import List

from utils.data_types import DistanceMatrix, Tour


def random_tour(n: int) -> Tour:
    """Losowa permutacja miast 0..n-1."""
    tour = list(range(n))
    random.shuffle(tour)
    return tour

def tour_length(tour: Tour, distance_matrix: DistanceMatrix) -> float:
    """Długość cyklu TSP dla danej trasy (zamkniętej)."""
    n = len(tour)
    total = 0.0
    for i in range(n):
        a = tour[i]
        b = tour[(i + 1) % n]  # powrót do miasta startowego
        total += distance_matrix[a][b]
    return total