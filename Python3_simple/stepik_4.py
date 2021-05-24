'''
Desks
Some school have decided to create three new math groups and equip classrooms for them with the new desks.
Only two students may sit at any desk. The number of students in each of the three groups is known.
Output the smallest amount of desks, which will need to be purchased. Each new group sits in its own classroom.
Input data format

The program receives the input of the three non-negative integers: the number of students in each of the three classes
(the numbers do not exceed 1000).
'''

lst = []
for i in range(3):
    amount = int(input())
    lst.append(amount // 2 + amount % 2) if amount in range(0, 1000) else exit(1)
print(sum(lst))
