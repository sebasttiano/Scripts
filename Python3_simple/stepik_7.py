'''
Given a string. Find whether it is a palindrome, i.e. it reads the same both left-to-right and right-to-left.
Output “yes” if the string is a palindrome and “no” otherwise.

Another answers:
str = input()
print(['no','yes'][str == str[::-1]])

s = input()
print('yes' if s == s[::-1] else 'no')
'''

word = input()
print('yes') if word[::-1] == word else print('no')
