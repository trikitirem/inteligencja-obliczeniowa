"""
Moduł ładowania danych dla macierzy odległości TSP.

Ten moduł zapewnia funkcjonalność do ładowania macierzy odległości TSP z plików CSV.
"""

from enum import Enum
from typing import List
import csv
from pathlib import Path

from utils.data_types import DistanceMatrix

class TspDataset(Enum):
    """Enum reprezentujący dostępne pliki zbiorów danych TSP."""
    
    # Zbiór danych 48 miast
    TSP_48 = "TSP_48"
    # Zbiór danych 76 miast
    TSP_76 = "TSP_76"
    # Zbiór danych 127 miast
    TSP_127 = "TSP_127"
    
    def file_path(self) -> str:
        """Zwraca ścieżkę pliku dla zbioru danych."""
        # Ścieżka do katalogu głównego projektu (poziom wyżej niż src/)
        project_root = Path(__file__).parent.parent.parent
        mapping = {
            TspDataset.TSP_48: project_root / "dane" / "TSP_48.csv",
            TspDataset.TSP_76: project_root / "dane" / "TSP-76.csv",
            TspDataset.TSP_127: project_root / "dane" / "TSP_127.csv",
        }
        return str(mapping[self])
    
    def city_count(self) -> int:
        """Zwraca liczbę miast w zbiorze danych."""
        mapping = {
            TspDataset.TSP_48: 48,
            TspDataset.TSP_76: 76,
            TspDataset.TSP_127: 127,
        }
        return mapping[self]
    
    def name(self) -> str:
        """Zwraca czytelną dla człowieka nazwę zbioru danych."""
        mapping = {
            TspDataset.TSP_48: "TSP 48 Cities",
            TspDataset.TSP_76: "TSP 76 Cities",
            TspDataset.TSP_127: "TSP 127 Cities",
        }
        return mapping[self]


def load_tsp_data(file_path: str) -> DistanceMatrix:
    """
    Ładuje macierz odległości TSP z pliku CSV.
    
    Args:
        file_path: Ścieżka do pliku CSV zawierającego macierz odległości
        
    Returns:
        DistanceMatrix: Lista 2D, gdzie matrix[i][j] to odległość z miasta i do miasta j
        
    Raises:
        FileNotFoundError: Jeśli plik nie może zostać otwarty
        ValueError: Jeśli CSV nie może zostać sparsowany lub wartości nie mogą zostać przekonwertowane na float
    """
    matrix = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file, delimiter=';')
            
            for row in csv_reader:
                processed_row = []
                for field in row:
                    # Zamień przecinek na kropkę jako separator dziesiętny
                    normalized_field = field.replace(',', '.')
                    try:
                        value = float(normalized_field)
                        processed_row.append(value)
                    except ValueError as e:
                        raise ValueError(f"Failed to parse '{field}' as float: {e}")
                
                matrix.append(processed_row)
        
        return matrix
    
    except FileNotFoundError:
        raise FileNotFoundError(f"Failed to open file: {file_path}")
    except Exception as e:
        raise ValueError(f"Failed to parse CSV file {file_path}: {e}")


def load_tsp_dataset(dataset: TspDataset) -> DistanceMatrix:
    """
    Ładuje macierz odległości TSP z predefiniowanego zbioru danych.
    
    Args:
        dataset: Zbiór danych TSP do załadowania
        
    Returns:
        DistanceMatrix: Lista 2D, gdzie matrix[i][j] to odległość z miasta i do miasta j
        
    Raises:
        FileNotFoundError: Jeśli plik nie może zostać otwarty
        ValueError: Jeśli CSV nie może zostać sparsowany lub wartości nie mogą zostać przekonwertowane na float
    """
    return load_tsp_data(dataset.file_path())


if __name__ == "__main__":
    # Kod testowy
    import sys
    
    # Test z TSP_48
    try:
        matrix = load_tsp_dataset(TspDataset.TSP_48)
        print(f"Loaded {len(matrix)} cities from {TspDataset.TSP_48.name()}")
        print(f"Distance from city 5 to city 10: {matrix[5][10]:.2f}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

