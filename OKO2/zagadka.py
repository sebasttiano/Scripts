# #!/usr/bin/env python
# -*- coding: utf-8 -*
"""Генерирует все слова из 3-х букв, у которых 1 и 3 буквы одинаковые. Кириллица. Кроме ь. ъ"""


letters = [chr(x) for x in range(1072, 1104) if x not in (1098, 1100)]

for char in letters:
    for second_char in letters:
        if char != second_char:
            print(char, second_char, char, sep='')