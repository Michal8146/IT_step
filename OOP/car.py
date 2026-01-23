class Car:
    def __init__(self, brand, model, year):
        self.brand = brand
        self.model = model
        self.__year = year

    def carInfo(self):
        print(f"Značka: {self.brand}, Model: {self.model}, Rok: {self.__year}")

    def getYear(self):
        return self.__year
    
    def getAge(self):
        return 2025 - self.__year



car_1 = Car(brand="Koegnisegg", model="Agera r", year= 2013)
cas_2 = Car(brand="Toyota", model="Mirai", year = 2025)

car_1.carInfo()
print(car_1.getYear(), car_1.getAge())

