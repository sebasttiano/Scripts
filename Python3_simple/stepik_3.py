'''
Input a single character and change its register. That is, if the lowercase letter has been entered – make it uppercase,
and vice versa. Characters that are not Latin ones need to stay unchanged.

Another answers:
import string
S = input()
if S in string.ascii_letters:
    S = S.swapcase()
print(S)
'''



import re
character = input()
print(character.swapcase()) if re.search('[a-z]|[A-Z]', character) else print(character)