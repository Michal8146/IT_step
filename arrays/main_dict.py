
db = {"Cesko": "Praha", "Slovensko": "Bratislava"}

def add_country(key, value):
    db[key] = value


def main():
    while True:
        print("""
        [1] vypis databazi
        [2] pridej zem a mesto""")

        choice = input("Volba: ")

        if choice == "1":
            print(db)
        elif choice == "2":
            zeme = input("Zeme: ")
            mesto = input("Mesto: ")
            add_country(zeme, mesto)
        else:
            print("nezspustily se")


main()