"""
Write a program the input of which is the list of numbers in one line. For each elements of this list,
the program should output the sum of its two neighbouring numbers. For list item that is first or last,
an element from the opposite end of the list is considered in place of a missing neighbour.
For example, if the input list is "1 3 5 6 10", the expected output list is "13 6 9 15 7" (without quotation marks).
If only one number serves as input, the output shall display the same one number.
The output must contain one line with the numbers from the new list, separated by space.

Best practice:

lst = list(map(int, input().split()))
len_lest = len(lst)
print(*[lst[i-1] + lst[(i+1)%len_lest] for i in range(len_lest)]) if len_lest>1 else print(lst[0])
"""

numbers = list(int(number) for number in input().split(' '))
length = len(numbers)
result_list = []
if length == 1:
    print(str(numbers[0]))
else:
    result_list = []
    for i in range(length):
        if i == 0:
            result_list.append(str(numbers[1] + numbers[-1]))
            continue
        if i == length - 1:
            result_list.append(str(numbers[length-2] + numbers[0]))
            continue
        result_list.append(str(numbers[i-1] + numbers[i+1]))
    print(' '.join(result_list))