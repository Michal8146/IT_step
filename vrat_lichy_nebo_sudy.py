
list = [1, 4, 3, 10, -2, -3, 2.4, "a", 16, -10, 111]


def returnOddOrEven(list, return_even):
    new_list = []
    for number in list:
        if type(number) == int:
            if return_even:
                if number % 2 == 0:
                    new_list.append(number)
            else:
                if number % 2:
                    new_list.append(number)
    return new_list

print(returnOddOrEven(list, True))
print(returnOddOrEven(list, False))

