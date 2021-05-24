'''
Write a simple calculator that reads the three input lines: the first number, the second number and the operation,
after which it applies the operation to the entered numbers ("first number" "operation" "second number") and outputs
the result to the screen. Note that the numbers can be real.

Supported operations: +, -, /, *, mod, pow, div; where
mod — taking the residue,
pow — exponentiation,
div — integer division.

If a user performs the division and the second number is 0, it is necessary to output the line "Division by 0!".
'''


first_number = float(input())
second_number= float(input())
action = input()
if second_number == 0 and action in ('/', 'div', 'mod', '%'):
    print('Division by0 !')
    exit(0)


def operation(first, second, action):
    if action == '+':
        result = first + second
    elif action == '-':
        result = first - second
    elif action == '*':
        result = first * second
    elif action == '/':
        result = first / second
    elif action == 'mod':
        result = first % second
    elif action == 'pow':
        result = first ** second
    elif action == 'div':
        result = int(first // second)
    return result

print(operation(first_number, second_number, action))