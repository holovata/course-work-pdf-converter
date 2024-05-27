import re

# Завантаження файлу
with open('output/processed2.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()

# Фільтрація рядків
pattern = re.compile(r"; (1/1|1/2|2/2|1/3|2/3|3/3|1/4|2/4|3/4|4/4|1/5|2/5|3/5|4/5|5/5|1/6|2/6|3/6|4/6|5/6|6/6)$")
filtered_lines = [line for line in lines if not pattern.search(line)]

# Збереження результатів у новий файл
with open('output/processed2_filtered.txt', 'w', encoding='utf-8') as file:
    file.writelines(filtered_lines)
