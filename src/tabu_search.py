import random
from typing import Callable, Dict, List, Literal, Optional, Tuple

from utils.data_types import AlgorithmName, DistanceMatrix, Tour
from utils.tour import random_tour, tour_length
from utils.data_loader import load_tsp_dataset, TspDataset
from utils.monitoring import AlgorithmResult, ResultMonitor
from utils.timing import measure_execution_time

Neighborhood = Literal["swap", "insert", "two_opt"]
Move = Tuple[Neighborhood, int, int]
TabuList = Dict[Move, int]


def _apply_swap(tour: Tour, i: int, j: int) -> Tour:
    neighbor = tour.copy()
    neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
    return neighbor


def _apply_insert(tour: Tour, i: int, j: int) -> Tour:
    if i == j:
        return tour.copy()
    neighbor = tour.copy()
    city = neighbor.pop(i)
    neighbor.insert(j, city)
    return neighbor


def _apply_two_opt(tour: Tour, i: int, j: int) -> Tour:
    if i >= j:
        return tour.copy()
    neighbor = tour.copy()
    neighbor[i : j + 1] = reversed(neighbor[i : j + 1])
    return neighbor


def _move_generator(
    n: int,
    neighborhood: Neighborhood,
    rng: random.Random,
    max_candidates: Optional[int],
) -> List[Tuple[int, int]]:
    """Generate (i, j) move pairs.

    If max_candidates is provided, it samples that many unique move pairs (or fewer if impossible).
    This is practical for larger instances to control runtime in parameter sweeps.
    """
    all_pairs: List[Tuple[int, int]] = []

    if neighborhood in ("swap", "two_opt"):
        # i < j
        if max_candidates is None:
            for i in range(n - 1):
                for j in range(i + 1, n):
                    all_pairs.append((i, j))
            return all_pairs

        seen = set()
        target = min(max_candidates, (n * (n - 1)) // 2)
        attempts = 0
        attempt_cap = target * 50 + 100
        while len(seen) < target and attempts < attempt_cap:
            i = rng.randrange(0, n - 1)
            j = rng.randrange(i + 1, n)
            seen.add((i, j))
            attempts += 1
        return list(seen)

    if max_candidates is None:
        for i in range(n):
            for j in range(n):
                if i != j:
                    all_pairs.append((i, j))
        return all_pairs

    seen = set()
    target = min(max_candidates, n * (n - 1))
    attempts = 0
    attempt_cap = target * 50 + 100
    while len(seen) < target and attempts < attempt_cap:
        i = rng.randrange(0, n)
        j = rng.randrange(0, n)
        if i != j:
            seen.add((i, j))
        attempts += 1
    return list(seen)


def _best_admissible_neighbor(
    tour: Tour,
    distance_matrix: DistanceMatrix,
    tabu_list: TabuList,
    iteration: int,
    best_overall_len: float,
    neighborhood: Neighborhood,
    rng: random.Random,
    max_candidates: Optional[int],
) -> Tuple[Optional[Tour], float, Optional[Move]]:
    """Select best neighbor under tabu + aspiration.

    Aspiration criterion: allow tabu move if it improves the global best.
    """
    n = len(tour)
    apply_fn: Callable[[Tour, int, int], Tour]
    if neighborhood == "swap":
        apply_fn = _apply_swap
    elif neighborhood == "insert":
        apply_fn = _apply_insert
    else:  # two_opt
        apply_fn = _apply_two_opt

    best_tour: Optional[Tour] = None
    best_len = float("inf")
    best_move: Optional[Move] = None

    candidates = _move_generator(n, neighborhood, rng, max_candidates)
    for i, j in candidates:
        move: Move = (neighborhood, i, j)
        expires_at = tabu_list.get(move, -1)
        is_tabu = expires_at > iteration

        neighbor = apply_fn(tour, i, j)
        neighbor_len = tour_length(neighbor, distance_matrix)

        # Tabu unless aspiration triggers.
        if is_tabu and neighbor_len >= best_overall_len:
            continue

        if neighbor_len < best_len:
            best_len = neighbor_len
            best_tour = neighbor
            best_move = move

    return best_tour, best_len, best_move


def tabu_search(
    distance_matrix: DistanceMatrix,
    *,
    neighborhood: Neighborhood = "two_opt",
    max_iters: int = 2000,
    max_no_improve: Optional[int] = 400,
    tabu_tenure: int = 20,
    start_tour: Optional[Tour] = None,
    seed: Optional[int] = None,
    max_candidates: Optional[int] = None,
) -> Tuple[Tour, float, int]:
    """Tabu Search for TSP.

    Project-aligned features:
    - 3 neighborhoods: swap / insert / two_opt (parameter: neighborhood)
    - tabu list with tenure (parameter: tabu_tenure)
    - aspiration criterion (tabu move allowed if it improves the global best)
    - stop criteria: max_iters and/or max_no_improve (parameter: max_no_improve)
    - optional candidate sampling (parameter: max_candidates) for runtime control
    """
    if max_iters <= 0:
        raise ValueError("max_iters must be > 0")
    if tabu_tenure <= 0:
        raise ValueError("tabu_tenure must be > 0")
    if max_no_improve is not None and max_no_improve <= 0:
        raise ValueError("max_no_improve must be > 0 when provided")

    n = len(distance_matrix)
    rng = random.Random(seed)

    current_tour = start_tour if start_tour is not None else random_tour(n)
    current_len = tour_length(current_tour, distance_matrix)

    best_tour = current_tour
    best_len = current_len

    tabu_list: TabuList = {}
    no_improve = 0
    iterations = 0

    for iteration in range(max_iters):
        iterations = iteration + 1

        expired = [m for m, exp in tabu_list.items() if exp <= iteration]
        for m in expired:
            del tabu_list[m]

        neighbor_tour, neighbor_len, move = _best_admissible_neighbor(
            current_tour,
            distance_matrix,
            tabu_list,
            iteration,
            best_len,
            neighborhood,
            rng,
            max_candidates,
        )

        if neighbor_tour is None or move is None:
            break

        current_tour = neighbor_tour
        current_len = neighbor_len
        tabu_list[move] = iteration + tabu_tenure

        if current_len < best_len:
            best_len = current_len
            best_tour = current_tour
            no_improve = 0
        else:
            no_improve += 1
            if max_no_improve is not None and no_improve >= max_no_improve:
                break

    return best_tour, best_len, iterations


def run_tabu(
    dataset: TspDataset = TspDataset.TSP_48,
    max_iters: int = 500,
    tabu_tenure: int = 10,
) -> AlgorithmResult:
    """
    Uruchamia Tabu Search i zapisuje wyniki.

    Args:
        dataset: Zbior danych TSP do przetworzenia
        max_iters: Maksymalna liczba iteracji algorytmu
        tabu_tenure: Dlugosc trwania tabu dla ruchu
    """
    distance_matrix = load_tsp_dataset(dataset)

    result = AlgorithmResult.new(AlgorithmName.TABU.value)
    result.with_dataset(dataset)
    result.with_parameter("max_iters", str(max_iters))
    result.with_parameter("tabu_tenure", str(tabu_tenure))

    print("Uruchamianie algorytmu tabu search...")

    (best_tour, best_len, iterations), execution_time_s = measure_execution_time(
        lambda: tabu_search(distance_matrix, max_iters=max_iters, tabu_tenure=tabu_tenure)
    )

    print("Algorytm tabu search zakończony.")

    result.set_result(best_len, best_tour)
    result.set_execution_time(execution_time_s)
    result.set_iterations(iterations)

    monitor = ResultMonitor()
    filename = monitor.save_result(result)
    print(f"Wyniki zapisane do: {filename}")
    print(f"Najlepsza długość trasy: {best_len:.2f}")
    print(f"Czas wykonania: {execution_time_s:.3f} s")


if __name__ == "__main__":
    for dataset in (TspDataset.TSP_48, TspDataset.TSP_76, TspDataset.TSP_127):
        run_tabu(dataset)
