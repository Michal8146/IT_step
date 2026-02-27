
jmena = ["michal", "martin", "nela", "nikol", "honza"]

jmena 

for i in range(len(jmena)):
    print(f"{i + 1}. {jmena[i]}", end=", ")

for i, jmeno in enumerate(jmena):
    print(f"{i + 1}. {jmeno}", end=", ")