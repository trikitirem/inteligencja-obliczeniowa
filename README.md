# System Monitorowania Algorytmów TSP

System oparty na Pythonie do monitorowania i analizowania algorytmów Problemu Komiwojażera (TSP) z kompleksowymi możliwościami ładowania danych i śledzenia wyników.

## Szybki Start

### Wymagania

- Python 3.8+ (pobierz z [python.org](https://www.python.org/downloads/))

### Instalacja i Uruchomienie

1. **Zainstaluj zależności** (jeśli są):

   ```bash
   pip install -r requirements.txt
   ```

   Uwaga: Ten projekt używa tylko standardowej biblioteki Pythona, więc nie są wymagane żadne zewnętrzne zależności.

2. **Uruchom projekt**:

   ```bash
   python main.py
   ```

3. **Uruchom poszczególne moduły**:
   ```bash
   # Test modułu ładowania danych
   python data_loader.py
   ```

## Struktura Projektu

```
/
├── main.py              # Główny punkt wejścia aplikacji
├── data_loader.py       # Funkcjonalność ładowania danych TSP
├── monitoring.py        # System monitorowania wyników algorytmów
├── requirements.txt     # Zależności Pythona (obecnie puste - używamy stdlib)
├── dane/                # Pliki zbiorów danych TSP
│   ├── TSP_48.csv      # Zbiór danych 48 miast
│   ├── TSP-76.csv      # Zbiór danych 76 miast
│   └── TSP_127.csv     # Zbiór danych 127 miast
├── wyniki/             # Katalog wyników algorytmów (tworzony automatycznie)
└── README.md           # Ten plik
```

## Funkcje

### 1. Moduł Ładowania Danych (`data_loader.py`)

Moduł ładowania danych zapewnia solidną funkcjonalność do ładowania macierzy odległości TSP z plików CSV.

#### Kluczowe Funkcje

- **Parsowanie CSV**: Obsługuje pliki CSV rozdzielane średnikami z przecinkami jako separatorami dziesiętnymi
- **Zarządzanie Zbiorami Danych z Bezpieczeństwem Typów**: Wybór zbioru danych oparty na enumach zapobiega błędom ścieżek plików
- **Automatyczna Walidacja Danych**: Weryfikuje właściwości macierzy (symetria, zera na przekątnej)
- **Kompleksowa Obsługa Błędów**: Czytelne komunikaty błędów do debugowania

#### Dostępne Zbiory Danych

| Zbiór Danych           | Miasta | Ścieżka Pliku        | Opis                                          |
| ---------------------- | ------ | -------------------- | --------------------------------------------- |
| `TspDataset.TSP_48`    | 48     | `dane/TSP_48.csv`    | Mały zbiór danych do szybkiego testowania      |
| `TspDataset.TSP_76`    | 76     | `dane/TSP-76.csv`    | Średni zbiór danych do rozwoju algorytmów      |
| `TspDataset.TSP_127`   | 127    | `dane/TSP_127.csv`   | Duży zbiór danych do testów wydajnościowych    |

#### Przykłady Użycia

```python
from data_loader import load_tsp_dataset, TspDataset

# Załaduj konkretny zbiór danych
dataset = TspDataset.TSP_48
distance_matrix = load_tsp_dataset(dataset)

# Uzyskaj dostęp do odległości między miastami
distance = distance_matrix[0][1]  # Odległość z miasta 0 do miasta 1

# Pobierz informacje o zbiorze danych
print(f"Dataset: {dataset.name()} - {dataset.city_count()} cities")
print(f"File path: {dataset.file_path()}")

# Załaduj różne zbiory danych
small_matrix = load_tsp_dataset(TspDataset.TSP_48)
large_matrix = load_tsp_dataset(TspDataset.TSP_127)
```

#### Struktura Danych

Macierz odległości jest reprezentowana jako `DistanceMatrix` (alias typu dla `List[List[float]]`), gdzie:

- `matrix[i][j]` = odległość z miasta `i` do miasta `j`
- Macierz jest symetryczna: `matrix[i][j] == matrix[j][i]`
- Elementy na przekątnej są zerami: `matrix[i][i] == 0.0`

Typ `DistanceMatrix` jest zdefiniowany w `data_loader.py` i może być importowany do użycia w innych modułach:

```python
from data_loader import DistanceMatrix
```

### 2. Moduł Monitorowania (`monitoring.py`)

System monitorowania zapewnia kompleksowe śledzenie i analizę wyników algorytmów TSP.

#### Kluczowe Funkcje

- **Przechowywanie Wyników**: Trwałe przechowywanie wyników w formacie JSON z znacznikami czasu
- **Metryki Wydajności**: Śledzenie czasu wykonania i iteracji
- **Śledzenie Parametrów**: Logowanie konfiguracji algorytmu
- **Niestandardowe Metryki**: Elastyczny system rejestrowania metryk
- **Śledzenie Zbiorów Danych**: Automatyczne rejestrowanie rozmiaru i nazwy zbioru danych
- **Analiza Wyników**: Wbudowane listowanie i porównywanie wyników

#### Główne Komponenty

##### Klasa `AlgorithmResult`

Reprezentuje wynik pojedynczego wykonania algorytmu z następującymi polami:

```python
@dataclass
class AlgorithmResult:
    algorithm_name: str                    # Nazwa algorytmu
    parameters: Dict[str, str]             # Parametry algorytmu
    route_length: float                    # Najlepsza znaleziona długość trasy
    route: List[int]                       # Najlepsza znaleziona trasa
    execution_time_ms: int                 # Czas wykonania w milisekundach
    iterations: int                        # Liczba wykonanych iteracji
    start_timestamp: datetime              # Kiedy algorytm został uruchomiony
    additional_metrics: Dict[str, float]  # Niestandardowe metryki wydajności
    dataset_size: int                      # Liczba miast w zbiorze danych
    dataset_name: str                      # Czytelna dla człowieka nazwa zbioru danych
```

##### Klasa `ResultMonitor`

Zarządza zbieraniem i trwałym przechowywaniem wyników algorytmów:

```python
class ResultMonitor:
    def __init__(self, results_dir: str = "wyniki")
    def save_result(self, result: AlgorithmResult) -> str
    def list_results(self) -> List[str]
```

#### Przykłady Użycia

```python
from monitoring import AlgorithmResult, ResultMonitor
from data_loader import TspDataset

# Utwórz monitor wyników
monitor = ResultMonitor()

# Utwórz wynik algorytmu z informacjami o zbiorze danych
result = (AlgorithmResult.new("Genetic Algorithm")
    .with_dataset(TspDataset.TSP_48)  # Określ użyty zbiór danych
    .with_parameter("population_size", "100")
    .with_parameter("mutation_rate", "0.01")
    .with_metric("fitness_improvement", 0.85)
    .set_result(1234.56, [0, 5, 12, 3, 8, 1, 9, 4, 7, 2, 6, 10, 11])
    .set_execution_time(1500)
    .set_iterations(1000))

# Zapisz wynik
filename = monitor.save_result(result)
print(f"Result saved to: {filename}")

# Wyświetl wszystkie wyniki
results = monitor.list_results()
for result_info in results:
    print(result_info)
```

#### Przechowywanie Wyników

Wyniki są automatycznie zapisywane do plików JSON w katalogu `wyniki/` zgodnie z następującą konwencją nazewnictwa:

```
wyniki/algorithm_name_XXcities_YYYYMMDD_HHMMSS_fff.json
```

Gdzie:

- `algorithm_name` to nazwa algorytmu
- `XXcities` wskazuje rozmiar zbioru danych (np. `48cities`, `76cities`, `127cities`)
- `YYYYMMDD_HHMMSS_fff` to znacznik czasu z milisekundami

Przykładowy plik wyniku:

```json
{
  "algorithm_name": "Genetic Algorithm",
  "parameters": {
    "population_size": "100",
    "mutation_rate": "0.01"
  },
  "route_length": 1234.56,
  "route": [0, 5, 12, 3, 8, 1, 9, 4, 7, 2, 6, 10, 11],
  "execution_time_ms": 1500,
  "iterations": 1000,
  "start_timestamp": "2024-01-15T10:30:45.123+00:00",
  "additional_metrics": {
    "fitness_improvement": 0.85
  },
  "dataset_size": 48,
  "dataset_name": "TSP 48 Cities"
}
```

## Zależności

Projekt używa tylko modułów ze standardowej biblioteki Pythona:

- **`csv`**: Parsowanie i zapisywanie CSV
- **`json`**: Serializacja/deserializacja JSON
- **`datetime`**: Obsługa daty i czasu
- **`pathlib`**: Manipulacja ścieżkami
- **`enum`**: Obsługa wyliczeń
- **`dataclasses`**: Obsługa klas danych
- **`typing`**: Adnotacje typów

Nie są wymagane żadne zewnętrzne zależności.

## Rozwój

### Dodawanie Nowych Zbiorów Danych

Aby dodać nowy zbiór danych TSP:

1. Dodaj plik CSV do katalogu `dane/`
2. Dodaj nowy wariant do enum `TspDataset` w `data_loader.py`:
   ```python
   TSP_NEW = "TSP_NEW"  # Nowy wariant zbioru danych
   ```
3. Zaktualizuj metodę `file_path()`, aby zawierała nową ścieżkę pliku
4. Zaktualizuj metodę `city_count()` z poprawną liczbą miast
5. Zaktualizuj metodę `name()` z opisową nazwą

### Uruchamianie Testów

Możesz testować moduły indywidualnie:

```bash
# Test modułu ładowania danych
python data_loader.py

# Test głównej aplikacji
python main.py
```

### Jakość Kodu

Projekt przestrzega najlepszych praktyk Pythona:

- Kompleksowa obsługa błędów
- Adnotacje typów dla lepszej czytelności kodu
- Czytelna dokumentacja
- Bezpieczeństwo typów z enumami
- Klasy danych dla ustrukturyzowanych danych

## Przykładowy Przepływ Pracy

Oto typowy przepływ pracy przy użyciu systemu:

```python
from data_loader import load_tsp_dataset, TspDataset
from monitoring import AlgorithmResult, ResultMonitor
import time

def main():
    # 1. Załaduj dane TSP
    dataset = TspDataset.TSP_48
    distance_matrix = load_tsp_dataset(dataset)

    # 2. Uruchom swój algorytm TSP
    start_time = time.time()
    best_route, best_length = your_tsp_algorithm(distance_matrix)
    execution_time_ms = int((time.time() - start_time) * 1000)

    # 3. Zapisz wyniki z informacjami o zbiorze danych
    monitor = ResultMonitor()
    result = (AlgorithmResult.new("Your Algorithm")
        .with_dataset(dataset)  # Uwzględnij informacje o zbiorze danych
        .set_result(best_length, best_route)
        .set_execution_time(execution_time_ms))

    filename = monitor.save_result(result)
    print(f"Result saved to: {filename}")

    # 4. Analizuj wyniki
    all_results = monitor.list_results()
    print(f"All results: {all_results}")

if __name__ == "__main__":
    main()
```

## Rozwiązywanie Problemów

### Częste Problemy

1. **Błędy nieznalezionego pliku**: Upewnij się, że pliki CSV znajdują się w katalogu `dane/`
2. **Błędy parsowania**: Sprawdź, czy pliki CSV używają średników jako separatorów i przecinków jako separatorów dziesiętnych
3. **Błędy uprawnień**: Upewnij się, że masz uprawnienia do zapisu w katalogu `wyniki/`

### Tryb Debugowania

Uruchom z wyjściem debugowania Pythona:

```bash
python -v main.py
```

## Licencja

Ten projekt jest częścią akademickiego kursu dotyczącego algorytmów inteligencji obliczeniowej.
