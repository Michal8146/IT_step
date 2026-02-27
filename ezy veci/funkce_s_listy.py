
seznam = [10,5,-2,8,2,-9, "2", True]

def seznam_soucet(seznam):
    if type(seznam) == list:
        soucet = 0
        for cislo in seznam:
            if type(cislo) == int or type(cislo) == float:
                soucet += cislo
        return soucet
    
print(seznam_soucet(seznam))

def najdi_negativni(seznam):
    if type(seznam) == list:
        negativni_cisla = []
        for cislo in seznam:
            if (type(cislo) == int or type(cislo) == float) and cislo < 0:
                negativni_cisla.append(cislo)
        return negativni_cisla
    
print(najdi_negativni(seznam))
    