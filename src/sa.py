import math
import random
from typing import Tuple

from utils.data_types import AlgorithmName, DistanceMatrix, Tour
from utils.tour import tour_length, random_tour
from utils.data_loader import load_tsp_dataset, TspDataset
from utils.monitoring import AlgorithmResult, ResultMonitor
from utils.timing import measure_execution_time


def neighbor_swap(tour: Tour) -> Tour:
    """Sąsiad: zamiana dwóch losowych miast (swap)."""
    i, j = random.sample(range(len(tour)), 2)
    new_tour = tour.copy()
    new_tour[i], new_tour[j] = new_tour[j], new_tour[i]
    return new_tour


def simulated_annealing(
    distance_matrix: DistanceMatrix,
    T_start: float = 1000.0,
    T_end: float = 1e-3,
    alpha: float = 0.995,
    iters_per_T: int = 100,
    start_tour: Tour = None,
) -> Tuple[Tour, float]:
    """
    Algorytm symulowanego wyżarzania dla problemu TSP.
    
    Args:
        distance_matrix: Macierz odległości między miastami
        T_start: Temperatura początkowa
        T_end: Temperatura końcowa (kryterium stopu)
        alpha: Współczynnik chłodzenia (temperatura *= alpha w każdej iteracji)
        iters_per_T: Liczba iteracji dla każdej wartości temperatury
        start_tour: Opcjonalna trasa startowa (jeśli None, losowa)
    
    Returns:
        Tuple[Tour, float]: Najlepsza znaleziona trasa i jej długość
    """
    n = len(distance_matrix)
    
    # Rozwiązanie początkowe
    if start_tour is None:
        current = random_tour(n)
    else:
        current = start_tour.copy()
    
    current_cost = tour_length(current, distance_matrix)
    
    best = current.copy()
    best_cost = current_cost
    
    T = T_start
    
    while T > T_end:
        for _ in range(iters_per_T):
            candidate = neighbor_swap(current)
            candidate_cost = tour_length(candidate, distance_matrix)
            dE = candidate_cost - current_cost  # chcemy minimalizować
            
            if dE < 0:
                # Lepsze rozwiązanie – akceptuj bezwarunkowo
                current, current_cost = candidate, candidate_cost
            else:
                # Gorsze – akceptuj z prawdopodobieństwem exp(-dE / T)
                if random.random() < math.exp(-dE / T):
                    current, current_cost = candidate, candidate_cost
            
            # Aktualizacja najlepszego znalezionego
            if current_cost < best_cost:
                best, best_cost = current.copy(), current_cost
        
        # Chłodzenie (redukcja temperatury – schemat geometryczny)
        T *= alpha
    
    return best, best_cost


def run_sa(
    dataset: TspDataset = TspDataset.TSP_48,
    T_start: float = 1000.0,
    T_end: float = 1e-3,
    alpha: float = 0.995,
    iters_per_T: int = 100,
    start_tour: Tour = None,
) -> AlgorithmResult:
    """
    Uruchamia algorytm symulowanego wyżarzania i zapisuje wyniki.
    
    Args:
        dataset: Zbiór danych TSP do przetworzenia
        T_start: Temperatura początkowa
        T_end: Temperatura końcowa
        alpha: Współczynnik chłodzenia
        iters_per_T: Liczba iteracji dla każdej wartości temperatury
        start_tour: Opcjonalna trasa startowa
    
    Returns:
        AlgorithmResult: Wynik wykonania algorytmu
    """
    distance_matrix = load_tsp_dataset(dataset)
    
    result = AlgorithmResult.new(AlgorithmName.SA.value)
    result.with_dataset(dataset)
    result.with_parameter("T_start", str(T_start))
    result.with_parameter("T_end", str(T_end))
    result.with_parameter("alpha", str(alpha))
    result.with_parameter("iters_per_T", str(iters_per_T))
    
    print("Uruchamianie algorytmu symulowanego wyżarzania...")
    print(f"  Parametry: T_start={T_start}, T_end={T_end}, alpha={alpha}, "
          f"iters_per_T={iters_per_T}")
    
    (best_tour, best_len), execution_time_s = measure_execution_time(
        lambda: simulated_annealing(
            distance_matrix,
            T_start=T_start,
            T_end=T_end,
            alpha=alpha,
            iters_per_T=iters_per_T,
            start_tour=start_tour,
        )
    )
    
    print("Algorytm symulowanego wyżarzania zakończony.")
    
    # Oblicz przybliżoną liczbę iteracji
    estimated_iterations = int(math.ceil(math.log(T_end / T_start) / math.log(alpha)) * iters_per_T)
    
    result.set_result(best_len, best_tour)
    result.set_execution_time(execution_time_s)
    result.set_iterations(estimated_iterations)
    
    monitor = ResultMonitor()
    filename = monitor.save_result(result)
    print(f"Wyniki zapisane do: {filename}")
    print(f"Najlepsza długość trasy: {best_len:.2f}")
    print(f"Czas wykonania: {execution_time_s:.3f} s")
    


if __name__ == "__main__":
    run_sa(
        dataset=TspDataset.TSP_48,
        T_start=1000.0,
        T_end=1e-3,
        alpha=0.995,
        iters_per_T=100,
    )
