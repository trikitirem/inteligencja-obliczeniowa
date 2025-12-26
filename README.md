# System Monitorowania Algorytmów TSP

Projekt w Pythonie do monitorowania i analizowania algorytmów Problemu Komiwojażera (TSP)

## Autorzy

- Paweł Przetacznik
- Natalia Możdżeń
- Amadeusz Bistram
- Łukasz Michalik

## Szybki Start

**Uruchom przykładowy algorytm**:

```bash
# Przykład algorytmu wspinaczki z multistartem
python src/ihc.py

# Przykład algorytmu Tabu Search
python src/tabu_search.py
```

## Struktura Projektu

```
/
├── src/                 # Kod źródłowy projektu
│   ├── main.py         # Główny punkt wejścia aplikacji
│   ├── ihc.py          # Implementacja algorytmu wspinaczki z multistartem
│   ├── tabu_search.py  # Implementacja algorytmu Tabu Search
│   └── utils/          # Moduły pomocnicze
│       ├── data_loader.py    # Ładowanie danych TSP z plików CSV
│       ├── data_types.py     # Definicje typów danych (DistanceMatrix, Tour, AlgorithmName)
│       ├── monitoring.py      # System monitorowania i zapisywania wyników
│       ├── timing.py          # Funkcje do mierzenia czasu wykonania
│       └── tour.py            # Funkcje pomocnicze do pracy z trasami
├── dane/                # Pliki zbiorów danych TSP
│   ├── TSP_48.csv      # Zbiór danych 48 miast
│   ├── TSP-76.csv      # Zbiór danych 76 miast
│   └── TSP_127.csv     # Zbiór danych 127 miast
├── wyniki/             # Katalog wyników algorytmów (tworzony automatycznie)
└── README.md           # Ten plik
```

> **⚠️ Uwaga:** Folder `src/utils/` jest w pełni wygenerowany przez AI i zawiera wyłącznie pomocnicze funkcje. Kod w tym folderze służy jako infrastruktura wspierająca implementację algorytmów TSP.
