"""
Moduł monitorowania wyników algorytmów TSP.

Ten moduł zapewnia kompleksowe śledzenie i analizę wyników algorytmów TSP.
"""

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List

from utils.data_loader import TspDataset


@dataclass
class AlgorithmResult:
    """Reprezentuje wynik pojedynczego wykonania algorytmu."""

    algorithm_name: str
    parameters: Dict[str, str] = field(default_factory=dict)
    route_length: float = 0.0
    route: List[int] = field(default_factory=list)
    execution_time_ms: int = 0
    iterations: int = 0
    start_timestamp: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    additional_metrics: Dict[str, float] = field(default_factory=dict)
    dataset_size: int = 0
    dataset_name: str = ""

    @classmethod
    def new(cls, algorithm_name: str) -> "AlgorithmResult":
        """Tworzy nowy AlgorithmResult z podaną nazwą algorytmu."""
        return cls(algorithm_name=algorithm_name)

    def with_dataset(self, dataset: TspDataset) -> "AlgorithmResult":
        """Ustawia informacje o zbiorze danych."""
        self.dataset_size = dataset.city_count()
        self.dataset_name = dataset.name()
        return self

    def with_parameter(self, key: str, value: str) -> "AlgorithmResult":
        """Dodaje parametr."""
        self.parameters[key] = value
        return self

    def with_metric(self, key: str, value: float) -> "AlgorithmResult":
        """Dodaje dodatkową metrykę."""
        self.additional_metrics[key] = value
        return self

    def set_result(self, route_length: float, route: List[int]) -> "AlgorithmResult":
        """Ustawia wynik (długość trasy i trasę)."""
        self.route_length = route_length
        self.route = route
        return self

    def set_execution_time(self, time_ms: int) -> "AlgorithmResult":
        """Ustawia czas wykonania w milisekundach."""
        self.execution_time_ms = time_ms
        return self

    def set_iterations(self, iterations: int) -> "AlgorithmResult":
        """Ustawia liczbę iteracji."""
        self.iterations = iterations
        return self

    def to_dict(self) -> dict:
        """Konwertuje do słownika do serializacji JSON."""
        return {
            "algorithm_name": self.algorithm_name,
            "parameters": self.parameters,
            "route_length": self.route_length,
            "route": self.route,
            "execution_time_ms": self.execution_time_ms,
            "iterations": self.iterations,
            "start_timestamp": self.start_timestamp.isoformat(),
            "additional_metrics": self.additional_metrics,
            "dataset_size": self.dataset_size,
            "dataset_name": self.dataset_name,
        }


class ResultMonitor:
    """Zarządza zbieraniem i trwałym przechowywaniem wyników algorytmów."""

    def __init__(self, results_dir: str = "wyniki"):
        """
        Inicjalizuje ResultMonitor.

        Args:
            results_dir: Katalog do przechowywania plików wyników
        """
        # Jeśli ścieżka nie jest bezwzględna, oblicz ją względem katalogu głównego projektu
        results_path = Path(results_dir)
        if not results_path.is_absolute():
            # Ścieżka do katalogu głównego projektu (poziom wyżej niż src/)
            project_root = Path(__file__).parent.parent.parent
            results_path = project_root / results_dir
        self.results_dir = str(results_path)

    def save_result(self, result: AlgorithmResult) -> str:
        """
        Zapisuje wynik algorytmu do pliku JSON.

        Args:
            result: AlgorithmResult do zapisania

        Returns:
            str: Nazwa pliku zapisanego wyniku

        Raises:
            IOError: Jeśli plik nie może zostać zapisany
        """
        # Upewnij się, że katalog wyników istnieje
        Path(self.results_dir).mkdir(parents=True, exist_ok=True)

        # Utwórz nazwę pliku z nazwą algorytmu, rozmiarem zbioru danych i znacznikiem czasu
        timestamp = result.start_timestamp.strftime("%Y%m%d_%H%M%S_%f")[
            :-3
        ]  # milisekundy
        filename = (
            f"{result.algorithm_name}_{result.dataset_size}cities_{timestamp}.json"
        )
        filepath = Path(self.results_dir) / filename

        # Konwertuj do słownika i serializuj do JSON
        result_dict = result.to_dict()
        json_str = json.dumps(result_dict, indent=2, ensure_ascii=False)

        # Zapisz do pliku
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(json_str)

        return filename

    def list_results(self) -> List[str]:
        """
        Wyświetla listę wszystkich plików wyników w katalogu wyników.

        Returns:
            List[str]: Lista nazw plików wyników, posortowana alfabetycznie
        """
        results_path = Path(self.results_dir)

        if not results_path.exists():
            return []

        files = []
        for entry in results_path.iterdir():
            if entry.is_file() and entry.suffix == ".json":
                files.append(entry.name)

        files.sort()
        return files
