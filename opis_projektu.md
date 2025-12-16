Projekty wykonywane są w grupach liczących od 3 do 5 osób.
Projekty będą bronione na ostatnich zajęciach. Obrona będzie polegała na wyjaśnieniu kodu,
odpowiedzi na pytania z zakresu danego fragmentu kodu/sprawozdania, a także na wyjaśnieniu
metody działania każdego z algorytmów oraz przedstawieniu uzyskanych wyników i wysnutych
wniosków. Obrona będzie odbywać się w grupach, jednak każda osoba z grupy musi posiadać wiedzę
z zakresu przesłanego projektu oraz umieć wyjaśnić działanie danego algorytmu/heurystyki, ponieważ
każda z osób może zostać poproszona o wyjaśnienie danego zagadnienia.
Projekt dotyczy problemu komiwojażera (TSP). Projekt obejmować powinien:

- implementację algorytmów: NN (najbliższego sąsiada), wspinaczki z multistartem (iteracyjna
  wspinaczka - IHC), symulowanego wyżarzania (SA), przeszukiwania Tabu (TS), algorytmy genetyczne
  (GA) oraz dowolnego innego (najlepiej ciekawego) algorytmu wybranego przez daną grupę, jak również
  propozycję minimum dwóch usprawnień dla wybranych algorytmów (z czego minimum jedno musi być
  autorskim dziełem grupy, wymyślonym nie przez Chata) – ważny jest racjonalny pomysł, który jednak
  może się okazać, że w rozważanym przypadku nie pozwala na poprawę uzyskiwanych wyników; kody
  algorytmów muszą znaleźć się w wysyłanych w ramach oddania projektu plikach,
- każdy z algorytmów powinien mieć zaimplementowane przeszukiwanie trzech rodzajów ruchów
  (generowania rozwiązań sąsiednich); algorytmy genetyczny powinny mieć zaimplementowany co
  najmniej trzy rodzaje metod krzyżowania i minimum trzy metody doboru rodziców,
- zestawienie wyników dla danego algorytmu z uwzględnieniem wpływu na wyniki różnych wartości
  parametrów algorytmów (np. liczba iteracji, liczba iteracji bez poprawy, temperatura początkowa,
  szybkość spadku temperatury, długość listy tabu, metoda selekcji, metoda krzyżowania,
  prawdopodobieństwo mutacji, itd.); w przypadku każdego parametru proszę o sprawdzenie (jeżeli to
  możliwe dla danego parametru) przynajmniej 4 różnych wartości tego parametru,
- analizę uzyskanych wyników wraz z wnioskami, gdzie punktem odniesienia do porównania
  efektywności heurystyk będzie wynik uzyskany przez Solver Excela,
- skład grupy.
  Obliczenia dla każdej kombinacji parametrów dla każdej z trzech instancji problemu komiwojażera
  (pliki z instancjami dostępne są do pobrania na Teamsach) powinny zostać wykonane wielokrotnie
  (min. 5 razy) dla algorytmów zawierających elementy losowości (również w przypadku Solvera). W
  zestawieniach proszę przede wszystkim uwzględniać wartości minimalne oraz średnie uzyskane dla
  różnych wartości parametrów. W zestawieniach i wnioskach proszę uwzględnić (zamieścić w
  sprawozdaniu) czas wykonywania danego algorytmu.
  Minimalna liczba parametrów do przetestowania dla każdego z algorytmów (o ile dany algorytm ma
  na tyle parametrów): liczba osób w grupie (nie mniej niż 3). Rodzaj sąsiedztwa można uwzględnić w
  liczbie analizowanych parametrów.
  Najlepsze wyniki dla każdego z algorytmów dla danego przypadku należy w sposób czytelny zawrzeć
  w dodatkowym pliku Excela, wraz z uszeregowaniami, które pozwoliły taki wynik uzyskać (plik z
  szablonem do pobrania w materiałach z zajęć).
  Najlepsze wyniki (spośród wszystkich grup) dla danej instancji problemu, zostaną nagrodzone
  dodatkowymi punktami: +5% do oceny końcowej za najlepszy wynik dla danej instancji problemu (w
  przypadku uzyskania najlepszego wyniku przez kilka grup, dodatkowe punkty zostaną podzielone
  pomiędzy grupy).
  Termin wysyłania sprawozdania zostanie podany na kanale ogólnym. Za każdy rozpoczęty dzień
  opóźnienia maksymalna punktacja zostaje zmniejszona o 25%. Projekt wysyła jedna osoba z danej
  grupy.
  Algorytmy mogą być pisane w dowolnym języku.
  Jeżeli pojawi się konieczność uściślenia wytycznych – informacje o zmianach/uściśleniach będą
  pojawiać się na kanale Teams.
  Dla zainteresowanych możliwe jest podpięcie narzędzia do optymalizacji hiperparametrów modelu
  (typu Optuna) i wykonanie dodatkowych analiz, co pozwoli na podniesienie oceny z projektu.
  Przykładowe parametry algorytmów:
- miasto startowe [NN],
- rodzaj sąsiedztwa [IHC, SA, TS, GA (mutacja)],
- kryterium stopu (np. liczba iteracji, liczba iteracji bez poprawy) [IHC, SA, TS, GA],
- liczba iteracji dla wybranego kryterium stopu [IHC, SA, TS, GA],
- temperatura początkowa, metoda redukcji temperatury, liczba sprawdzanych rozwiązań dla danej
  temperatury [SA],
- długość listy tabu [TS],
- metoda doboru rodziców, prawdopodobieństwo krzyżowania, rodzaj krzyżowania, wielkość
  populacji, metoda tworzenia populacji potomstwa, prawdopodobieństwo mutacji [GA].
  Jako dodatkowy parametr można również potraktować wpływ jakości rozwiązania początkowego (w
  omawianym przypadku będzie to długość trasy komiwojażera) na wielkość uzyskanego rozwiązania.
