
a = (2, 4, 1, 10, 7, 11, 5, -2, 4, 1, 4, 13)

def find_min_max(numbers):
    min_num = numbers[0]
    max_num = numbers[0]
    for num in numbers[1:]:
        if num < min_num:
            min_num = num
        elif num > max_num:
            max_num = num
    
    return min_num, max_num

print(find_min_max(a))

def count_occurrences(numbers, target):
    counter = 0
    if target in numbers:
        for num in numbers:
            if num == target:
                counter += 1
    return counter

print(count_occurrences(a, 4))
