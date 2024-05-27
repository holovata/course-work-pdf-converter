import csv
from typing import List, Tuple, Dict


def read_cue_data(filename: str) -> Dict[str, Tuple[str, int, str]]:
    """
    Читає дані стимулів із зазначеного файлу.
    Повертає словник зі стимулами як ключами та кортежами, що містять стимул, число та форматовану деталь як значення.
    Додає вузол 'ROOT' зі зазначеними параметрами і змінює місцями числа в деталі 'СТ [..]'.
    """
    cue_data = {}
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split('[')
            if len(parts) < 2:
                continue
            cue = parts[0].strip().split('.')[1].strip()
            numbers = parts[1].split('/')
            first_number = numbers[0].strip()
            second_number = numbers[1].split(']')[0].strip()
            detail = f"СТ [{second_number} / {first_number}]"  # Заміна чисел місцями
            cue_data[cue] = (cue, int(first_number), detail)

    # Додавання вузла 'ROOT' після обробки всіх рядків
    cue_data['ROOT'] = ('ROOT', 841, "СТ [841 / 841]")
    return cue_data


def read_response_data(filename: str) -> List[Tuple[str, str, int, str]]:
    """
    Читає дані відповідей із зазначеного файлу.
    Повертає список кортежів, що містять відповідь, текст стимулу, кількість та остаточне співвідношення у форматі.
    """
    response_data = []
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if ':' not in line:
                continue
            response, cues_part = line.split(':', 1)
            cues = cues_part.split(';')
            final_ratio = cues[-1].strip()
            final_ratio_formatted = f"РЕ [{final_ratio}]"
            for cue in cues[:-1]:
                if '&' in cue:
                    cue_text, count = cue.rsplit('&', 1)
                    count = count.split('/')[0].strip()
                    response_data.append((response.strip(), cue_text.strip(), int(count), final_ratio_formatted))
    return response_data


def process_data(cue_data: Dict[str, Tuple[str, int, str]], response_data: List[Tuple[str, str, int, str]]) -> List[List]:
    """
    Обробляє дані стимулів та відповідей для розрахунку міцності та форматування для CSV виходу.
    """
    csv_data = []
    for response, cue, count, ratio in response_data:
        cue_info = cue_data.get(cue, (None, 0, ''))
        if cue_info[1] == 0:
            print(f"Skipping cue {cue} as no N data available")
            continue
        N = cue_info[1]
        Strength = N / count
        Label = f"{count} / {N}"
        csv_data.append([cue, response, count, N, Strength, Label])
    return csv_data


def write_csv_new(data: List[List], output_filename: str, node_mapping: Dict[str, int]) -> None:
    """
    Записує дані у CSV файл зі зазначеними заголовками, використовуючи ID вузлів для Source та Target.
    """
    with open(output_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Source', 'Target', 'SourceWord', 'TargetWord', 'R', 'N', 'Weight', 'Label'])
        for source_word, target_word, count, N, strength, label in data:
            source_id = node_mapping.get(source_word)
            target_id = node_mapping.get(target_word)
            writer.writerows([[source_id, target_id, source_word, target_word, count, N, strength, label]])


def generate_nodes_file(cue_data, response_data, output_filename):
    nodes = {}
    # Збір інформації з cue_data
    for cue, data in cue_data.items():
        label = data[2]  # Отримання мітки "СТ [..]"
        if cue in nodes:
            nodes[cue] += " " + label  # Додавання мітки, якщо стимул вже існує в nodes
        else:
            nodes[cue] = label

    # Збір інформації з response_data
    for response, cue, count, ratio in response_data:
        # Форматування "РЕ [..]" з додаванням пробілів
        parts = ratio.split('[')
        numbers = parts[1].replace('/', ' / ')  # Додавання пробілів навколо скісної риски
        ratio_label = f"РЕ [{numbers}"  # Формування остаточної мітки з правильним форматуванням

        if response in nodes:
            if ratio_label not in nodes[response]:  # Перевірка, чи така мітка вже існує
                nodes[response] += " " + ratio_label
        else:
            nodes[response] = ratio_label  # Створення нового запису, якщо відповідь ще не зустрічалася

    with open(output_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Id', 'Name', 'Label'])
        for i, (name, label) in enumerate(nodes.items()):
            writer.writerow([i, name, f"{name} {label}"])  # Використання i як Id та об'єднання name з label для Label


def load_node_mapping(filename: str) -> Dict[str, int]:
    """
    Завантажує дані вузлів з CSV файлу та повертає відображення від імен вузлів до їхніх Id.
    """
    mapping = {}
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Пропуск заголовка
        for row in reader:
            node_id, name = int(row[0]), row[1]
            mapping[name] = node_id
    return mapping


# Завантаження відображення вузлів з файлу
node_mapping = load_node_mapping('csvs/nodes12_list.csv')

# Читання, обробка та запис даних
cue_data = read_cue_data('output/merged1.txt')
response_data = read_response_data('output/processed2_filtered.txt')
csv_data = process_data(cue_data, response_data)
write_csv_new(csv_data, 'csvs/cue1_response2_str_filtered.csv', node_mapping)

# Виклик функції для генерації файлу вузлів
# generate_nodes_file(cue_data, response_data, 'csvs/nodes12_list.csv')

print(f"Number of cues: {len(cue_data)}")
print(f"Number of responses: {len(response_data)}")
print(f"Number of entries in CSV: {len(csv_data)}")
