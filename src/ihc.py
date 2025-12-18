import random
from typing import Tuple

from utils.data_types import AlgorithmName, DistanceMatrix, Tour
from utils.tour import tour_length
from utils.data_loader import load_tsp_dataset, TspDataset
from utils.monitoring import AlgorithmResult, ResultMonitor
from utils.timing import measure_execution_time


def random_tour(n: int) -> Tour:
    """Generuje losową trasę (permutację miast od 0 do n-1)."""
    tour = list(range(n))
    random.shuffle(tour)
    return tour

def best_improving_neighbor_swap(
    tour: Tour, distance_matrix: DistanceMatrix
) -> Tuple[Tour, float]:
    """
    Znajdź najlepszego sąsiada typu 'swap' (zamiana dwóch pozycji).
    Zwraca (najlepsza_trasa, długość). Jeżeli brak poprawy, zwraca oryginalną trasę.
    """
    n = len(tour)
    best_tour = tour
    best_len = tour_length(tour, distance_matrix)

    for i in range(n - 1):
        for j in range(i + 1, n):
            neighbor = tour.copy()
            neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
            length_neighbor = tour_length(neighbor, distance_matrix)
            if length_neighbor < best_len:
                best_len = length_neighbor
                best_tour = neighbor

    return best_tour, best_len


def hill_climbing(
    start_tour: Tour, distance_matrix: DistanceMatrix
) -> Tuple[Tour, float]:
    """
    Algorytm wspinaczki: startuje z 'start_tour' i wykonuje lokalne poprawki,
    aż brak lepszego sąsiada.
    """
    current_tour = start_tour
    current_len = tour_length(current_tour, distance_matrix)

    while True:
        neighbor_tour, neighbor_len = best_improving_neighbor_swap(
            current_tour, distance_matrix
        )

        if neighbor_len < current_len:
            current_tour, current_len = neighbor_tour, neighbor_len
        else:
            break

    return current_tour, current_len


def iterative_hill_climbing(
    distance_matrix: DistanceMatrix,
    num_starts: int = 50,
) -> Tuple[Tour, float]:
    """
    Iteracyjna wspinaczka (multistart):
    - num_starts losowych startów
    - dla każdego uruchamiamy hill_climbing
    - zwracamy najlepszy wynik.
    """
    n = len(distance_matrix)
    best_tour_overall = None
    best_len_overall = float("inf")

    for _ in range(num_starts):
        start = random_tour(n)
        local_best_tour, local_best_len = hill_climbing(start, distance_matrix)

        if local_best_len < best_len_overall:
            best_len_overall = local_best_len
            best_tour_overall = local_best_tour

    return best_tour_overall, best_len_overall


def run_ihc(dataset: TspDataset = TspDataset.TSP_48, num_starts: int = 50) -> AlgorithmResult:
    """
    Uruchamia algorytm wspinaczki z multistartem i zapisuje wyniki.
    
    Args:
        dataset: Zbiór danych TSP do przetworzenia
        num_starts: Liczba losowych startów dla algorytmu
    """
    distance_matrix = load_tsp_dataset(dataset)
    
    result = AlgorithmResult.new(AlgorithmName.IHC.value)
    result.with_dataset(dataset)
    result.with_parameter("num_starts", str(num_starts))
    
    print("Uruchamianie algorytmu wspinaczki z multistartem...")

    (best_tour, best_len), execution_time_s = measure_execution_time(
        lambda: iterative_hill_climbing(distance_matrix, num_starts)
    )

    print("Algorytm wspinaczki z multistartem zakończony.")
    
    result.set_result(best_len, best_tour)
    result.set_execution_time(execution_time_s)
    result.set_iterations(num_starts)
    
    monitor = ResultMonitor()
    filename = monitor.save_result(result)
    print(f"Wyniki zapisane do: {filename}")
    print(f"Najlepsza długość trasy: {best_len:.2f}")
    print(f"Czas wykonania: {execution_time_s:.3f} s")



if __name__ == "__main__":
    result = run_ihc(TspDataset.TSP_127)

