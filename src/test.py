import os

os.chdir('data/pomysl-grand-prix/tournaments')
files = os.listdir()

# Otwórz plik i wczytaj dane jako string z sekwencjami \uXXXX
for filename in files:
    print(filename)
    with open(filename, "r", encoding="utf-8") as f:
        data = f.read()

    if 'ł' in data:
        continue

    # Zdekoduj unicode escape
    data = data.replace('\\"', '__QUOTE__')
    decoded = data.encode("utf-8").decode("unicode_escape")
    decoded = decoded.replace('__QUOTE__', '\\"')

    # Zapisz do nowego pliku jako zwykły tekst
    with open(filename, "w", encoding="utf-8") as f:
        f.write(decoded)
