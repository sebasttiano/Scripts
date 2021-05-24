'''
Purchase pies
A pie costs A dollars and B cents. Find how many dollars and cents you need to pay for N pies.
Input data format
The program gets three numbers as input: A, B, N - integers, positive, don't exceed 10000.
Output data format
The program should output two numbers separated by a space: cost of the purchase in dollars and cents.
'''

(dollars, cents, amount) = (int(input()) for i in range(3))
cost = (dollars * 100 + cents) * amount
print(cost // 100, cost % 100)