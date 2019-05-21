# Program wyznaczajacy klase dla podanej listy punktow ze zbioru testowego na podstawie
# danych ze zbioru treningowego. Program wykorzystuje algorytm KNN


from math import hypot


# Funkcja read_data przyjmuje jako argument nazwę pliku ze zbiorem danych i zwraca
# listę punktów w postaci list trzy lub dwu elementowych w zależności od typu zbioru.
def read_data(filename):
    try:
        with open(filename, "r") as file:
            data = []
            for line in file.readlines():
                insert = [int(x) for x in line.split(",")]
                data.append(insert)
        return data
    except FileNotFoundError as e:
        print("Nie odnaleziono pliku", filename, "\n", e)
    except NameError as e:
        print("Zmienna z nazwą pliku nie istnieje.", "\n", e)


train = read_data('train.txt')  # Zbior danych do nauki algorytmu
test = read_data('test.txt')  # Zbior punktow do przetestowania  algorytmu.


# Funkcja distance przyjmuje wsp dwoch punktow i zwraca odleglosc pomiedzy nimi.
def distance(x1, y1, x2, y2):

    return hypot(x1 - x2, y1 - y2)


# Funkcja calculate_distances przyjmuje jako argumenty współrzędne sprawdzanego punktu i zbiór treningowy.
# Następnie oblicza odległość tego punktu do wszystkich w zbiorze treningowym i zwraca listę skłądającą się z list
# zawierających odległość punktu treningowego od sprawdzanego punktu oraz klasę do jakiej sprawdzany punkt przynależy.
def calculate_distances(point, train):
    distances = []  # [distance, label]
    for p in train:
        insert = [distance(point[0], point[1], p[0], p[1]), p[2]]
        distances.append(insert)

    return distances
    # return [[distance(point[0], point[1], p[0], p[1]), p[2]] for p in train] - Rozwiązanie alternatywne jednolinijkowe


# Funkcja predict definiuje klase dla punktu testowego na podstawie k jego najblizszych sasiadow.
def predict(point, train, k=3):
    distances = calculate_distances(point, train)
    distances.sort()
    distances = distances[:k]               # Obciecie posortowanej listy do k najmniejszych odleglosci.
    class_list = [x[1] for x in distances]  # Utworzenie listy k elementowej, zawierajacej jedynie numer klasy.
    category = round(sum(class_list) / k)   # Na podstawie średniej arytmetycznej wyznacza klase dla badanego punktu.

    return category


# Tworzenie listy punktów ze zbioru testowego, wraz z przypisaniem im odpowiedniej klasy.
results = []
for point in test:
    results.append(predict(point, read_data('train.txt'), k=3))


# Funkcja wczytuje listę punktów testowych oraz listę przypisanych klas
# i zapisuje dane do pliku results.txt.
def write_results(test_points, results):
    with open('results.txt', 'w') as file:
        insert = [str(test_points[i][0]) + "," + str(test_points[i][1]) + ","
                  + str(results[i]) + "\n" for i in range(len(results))]

        try:
            file.writelines(insert)
        except IOError:
            print("Blad przy zapisywaniu danych do pliku.")


write_results(test, results)
