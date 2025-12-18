"""
Moduł do mierzenia czasu wykonania funkcji.

Ten moduł zapewnia narzędzia do precyzyjnego mierzenia czasu wykonania kodu.
"""

import time
from typing import Callable, Tuple, TypeVar

# TypeVar do zachowania typu zwracanego przez funkcję
T = TypeVar('T')


def measure_execution_time(func: Callable[[], T]) -> Tuple[T, float]:
    """
    Wykonuje funkcję i mierzy czas jej wykonania.
    
    Args:
        func: Funkcja do wykonania (lambda lub callable bez argumentów).
              Użyj lambda aby opakować funkcję z argumentami, np.:
              lambda: my_function(arg1, arg2)
        
    Returns:
        Tuple[T, float]: Krotka zawierająca:
            - wynik funkcji (dowolny typ)
            - czas wykonania w sekundach (float)
    
    Example:
        >>> result, time_s = measure_execution_time(lambda: compute_something(data))
        >>> print(f"Obliczenia zajęły {time_s:.3f} s")
        >>> print(f"Wynik: {result}")
    """
    start_time = time.perf_counter()
    result = func()
    end_time = time.perf_counter()
    
    # Czas w sekundach
    execution_time_s = end_time - start_time
    
    return result, execution_time_s

