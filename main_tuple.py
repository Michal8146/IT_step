
a = (2, 4, 1, 10, 7, 11, 5, -2)

def find_min_max(numbers):
    min_num = numbers[0]
    max_num = numbers[0]
    for num in numbers:
        if num < min_num:
            min_num = num
        elif num > max_num:
            max_num = num
    
    return (min_num, max_num)

print(find_min_max(a))