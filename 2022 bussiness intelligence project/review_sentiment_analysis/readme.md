1. PRACOWNIA  
**1-18.10.2022**  
- [x] Research dot. metod przetwarzania języka naturalnego oraz analizy sentymentu  
  
**19.10.2022**  
- [x] Konfiguracja środowiska, instalacje wymaganego oprogramowania, sklonowanie repozytorium lokalnie  
- [x] Ustalenia dot. formatu recenzji, języka oraz formatu dot. wpisu do bazy danych  
- [x] Znalezienie ogólnodostępnej bazy danych rezenzji książek  
  
**26.10.2022**  
- [x] Przygotowanie readme  
- [x] Rozpoczęcie pracy praktycznej  
- [x] Przygotowanie przykładowej recenzji  
- [x] Praca nad tokenizacją tekstu  
- [x] Preprocessing tekstu (zamiana liter na małe, usunięcie stopwords, podział na zdania)  
- [x] Przygotowanie draftu funkcji obliczającej sentyment (VADER)  
- [x] znalezienie zbioru uczącego  
  
**9.11.2022**  
- [x] Ostatnie ustalenia formalne: Brak recencji to None, sentyment negatywny 0 (bool), pozytywny 1 (bool)  
- [x] Dodanie funkcji usuwającej imiona z tesktu  
- [x] Utworzenie zbioru pozytywnych/negatywnych słów  
- [x] Dodanie fukcji zliczającej słowa negatywne/pozytywne  
- [x] Implementacja naiwnego klasyfikatora Bayesa (draft)  
- [x] Porównanie dokładności innych klasyfikatorów (BernoulliNB, ComplementNB, MultinomialNB, KNeighborsClassifier, DecisionTreeClassifier, RandomForestClassifier, LogisticRegression, MLPClassifier, AdaBoostClassifier)  
- [x] Wybór najlepszego klasyfikatora - LogisticRegression
  
**16.11.2022**  
- [x] Uporządkowanie kodu, zorganizowanie go w osobne pliki .py, debugowanie  
- [x] Zapisanie danych treningowych, trening modelu, zapisanie modelu -> skrócenie czasu predykcji z kilku minut do <10 sekund
  
**23.11.2022**  
- [x] Dokumentacja kodu, ostateczne porządkowanie itd  
- [x] szybki kurs htmla  

**30.11.2022**  
- [x] Uporządkowanie importów, stworzenie pliku main  
- [x] Research nt. stworzenia szablonu strony  
  
**7.12.2022**  
- [x] Stworzenie strony (zakładki)
- [x] Połączenie z bazą danych  
- [x] Stworzenie niezbędnych tabel  
  
**PODSUMOWANIE**  
W ramach pracowni został wykonany analizator sentymentu recenzji książek. Tekst jest dzielony na zdania, po czym każde z nich jest analizowane przez funckję *SentimentIntensityAnalyzer()* biblioteki nltk. Następnie tworzony jest słownik cech recenzji, który zostaje przekazany do klasyfikatora. Testowane były różne modele uczenia maszynowego (*BernoulliNB(), ComplementNB(), MultinomialNB(), KNeighborsClassifier(), DecisionTreeClassifier(), RandomForestClassifier(), LogisticRegression(), MLPClassifier(), AdaBoostClassifier()*), po czym wybrano najlepszy z nich - regresję logistyczną. Klasyfikator był wcześniej wytrenowany na zbiorze danych recenzji filmów.  
Gdy logika była gotowa, zajęto się podłączeniem do bazy danych, generacją danych oraz projektem zakładki strony internetowej, a także połączeniem jej z główną funkcjonalnością. Czynności te zostały wykonane z sukcesem.  
  
  
  
2. PROJEKT INŻYNIERSKI  
**1-24.10.2022**  
- [x] Research dotyczący metod przetwarzania obrazów 3D, pracy na nich w sieciach neuronowych, pracy na objętościowych danych, zorganizowanie miejsca do przechowywania objętościowych danych  
- [x] Sporządzenie obszernej listy pytań, konsultacje z promotorem  
- [x] Decyzja o zmianie tematu pracy  
  
**25.10.2022**
- [x] Ustalenia formalne dot. formulacji nowego tematu pracy  
TODO: strona tytułowa, spis treści, 10 stron teorii, literatura (na za 2 tygodnie), strona tytułowa
i spis treści nie liczą się do tych 10 stron teorii  
  
**9.11.2022**  
- [x] Strona tytułowa  
- [x] Spis treści  
- [x] Rozdział AI w medycynie  
- [x] Usunięcie artefaktów (fragmentów tekstu) z danych treningowych  
- [x] Data augmentation  
- [x] Przygotowanie podstwawowych statystyk dot. danych
- [x] Pierwszy model sieci neuronowej - acc=94%  
- [x] Przygotowanie danych do użycia  w uczeniu maszynowym (drzewo decyzyjne)  
  
**16.11.2022**  
- [x] Usunięcie artefaktów z danych testowych  
- [x] Rozszerzenie zbioru o kolejne kategorie danych
- [x] Usunięcie artefaktów (fragmentów tekstu) z dodatkowych danych  
- [x] Model sieci neuronowej przy uwzględnieniu dodatkowych danych - acc=88%  
- [x] Wytrenowanie modeli dla uczenia maszynowego dla podstawowych danych  
- [x] Wytrenowanie modeli dla uczenia maszynowego dla dodatkowych danych  
- [x] Porównanie dokładności modeli dla różnych parametrów (np różna maksymalna głębokość drzewa decyzyjnego itp.)
  
**23.11.2022**  
- [x] Sporządzenie statystyk i wykresów dla modeli ML  
- [x] Napisanie wprowadzenia i celu pracy  
- [x] Napisanie większości teorii (rozdział o chorobach)  
- [x] Praca nad rozdziałem opisującym modele ML  
  
**30.11.2022**  
- [x] Napisany rozdział opisujący modele ML  

**7.12.2022**  
- [x] Napisany rozdział opisujący sieć neuronową  
- [x] Napisany rozdział opisujący zbiór danych oraz preprocessing  
- [x] Nieznaczne modyfikacje architektury sieci i ponowny trening
- [x] Dodanie modelu regresji logistycznej, trening dla różnych parametrów
- [x] Częściowe przygotowanie statystyk dot. ewaluacji modeli
- [x] Przygotowanie prezentacji na obronę
  
