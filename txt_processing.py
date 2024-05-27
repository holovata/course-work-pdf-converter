import re

def format_reaction(reaction_line):
    # Розділяємо назву реакції і список стимулів
    reaction, stimuli_part = reaction_line.split(':', 1)
    stimuli = stimuli_part.split(';')
    formatted_stimuli = []
    last_number = '1'  # Початкове значення для стимулів без явно вказаного числа

    # Перебираємо стимули справа наліво
    for i, stimulus in enumerate(reversed(stimuli)):
        stimulus = stimulus.strip()
        if not stimulus:
            continue
        parts = stimulus.rsplit(' ', 1)
        if len(parts) > 1 and parts[1].isdigit():
            # Стимул вже має число
            last_number = parts[1]  # Оновлюємо останнє відоме число
            formatted_stimuli.append(f"{parts[0]} &{last_number}")
        else:
            # Перевіряємо, чи є елемент дробом (останній елемент у списку)
            if i == 0 and '/' in parts[0]:
                formatted_stimuli.append(parts[0])  # Додаємо як є, без числа
            else:
                # Присвоюємо стимулу останнє відоме число
                formatted_stimuli.append(f"{stimulus} &{last_number}")

    # Так як ми обробили стимули у зворотному порядку, треба їх перевернути назад
    formatted_stimuli.reverse()

    # Додаємо "; 1/1", якщо в кінці немає дробу
    if not re.search(r'/\d+$', formatted_stimuli[-1]):
        formatted_stimuli.append('1/1')

    return f"{reaction}: {'; '.join(formatted_stimuli)}"


def process_file(filename, output_filename):
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    reaction_data = []
    current_reaction = ""

    for line in lines:
        if "подоброму" in line:
            line = line.replace("подоброму", "по-доброму")

        line = line.strip()
        if not line:
            continue

        if ':' in line:
            if current_reaction:
                processed_reaction = format_reaction(current_reaction.rstrip('- '))
                reaction_data.append(processed_reaction)
            current_reaction = line
        else:
            if current_reaction.endswith('-'):
                current_reaction = current_reaction[:-1] + line
            else:
                current_reaction += " " + line

    if current_reaction:
        processed_reaction = format_reaction(current_reaction.rstrip('- '))
        reaction_data.append(processed_reaction)

    with open(output_filename, 'w', encoding='utf-8') as file:
        for reaction in reaction_data:
            file.write(reaction + "\n")

# Обробка файлу
process_file('output/slovnik2.txt', 'output/processed2.txt')
