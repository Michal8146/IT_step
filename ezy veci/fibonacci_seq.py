
def fibonacci(opakovani):
    a = 0
    b = 1
    nove = 0

    for i in range(opakovani):
        nove = a + b
        if a < b:
            a = nove
        else:
            b = nove
    return nove

for i in range(20):
    print(fibonacci(i))