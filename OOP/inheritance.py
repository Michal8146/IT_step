class Vehicle:
    def __init__(self, brand, speed):
        self.brand = brand
        self.speed = speed

    def describe(self):
        return f"znacka: {self.brand}, rychlost: {self.speed}"
    
class Car(Vehicle):
    def __init__(self, brand, speed, num_doors):
        super().__init__(brand, speed)
        self.num_doors = num_doors
    
    def describe(self):
        return f"znacka: {self.brand}, rychlost: {self.speed}, pocet dveri: {self.num_doors}"
    

class Bike(Vehicle):
    def __init__(self, brand, speed, has_engine):
        super().__init__(brand, speed)
        self.has_engine = has_engine
    
    def describe(self):
        description = f"znacka: {self.brand}, rychlost: {self.speed}, "
        if self.has_engine:
            return description + "ma motor"
        else:
            return description + "nema motor"
        

ponorka = Vehicle("ocean gate", "10 km/h")
print(ponorka.describe())

skodovka = Car("Skoda", "120 km/h", 4)
print(skodovka.describe())

skodovka = Bike("Merida", "80 km/h", True)
print(skodovka.describe())

skodovka = Bike("::", "50 km/h", False)
print(skodovka.describe()) 


