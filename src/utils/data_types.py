"""
Moduł definiujący typy danych używane w projekcie TSP.
"""

from enum import Enum
from typing import List

# Typ dla macierzy odległości TSP
DistanceMatrix = List[List[float]]

# Typ dla trasy (listy miast)
Tour = List[int]


class AlgorithmName(Enum):
    """Enum reprezentujący nazwy dostępnych algorytmów TSP."""
    
    # Iterative Hill Climbing
    IHC = "ihc"

