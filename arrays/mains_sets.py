numbers = {2, 4, 3, 6}
numbers2 = {1, 2, 3, 4}

def all_even(numbers):
    for num in numbers:
        if num % 2:
            return False
    return True

print(all_even(numbers))

def unique_elements(set1, set2):
    return set1 ^ set2

print(unique_elements(numbers, numbers2))

