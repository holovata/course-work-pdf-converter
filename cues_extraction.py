import fitz  # PyMuPDF
import re


def clean_pdf_text(source_pdf_path, output_txt_path, start_page, end_page):
    # Відкриття PDF файлу з PyMuPDF
    document = fitz.open(source_pdf_path)

    # Витягування тексту з вказаних сторінок
    text = ""
    for page_num in range(start_page - 1, end_page):  # Перетворення до 0-індексації
        page = document[page_num]
        text += page.get_text()

    # Закриття документу
    document.close()

    refined_text = ""
    for line in text.splitlines():
        # Перетворення до нижнього регістру
        line = line.lower()

        # Видалення всього від "[бутенко" до кінця рядка
        line = re.sub(r"\[\s*бутенко.*$", "", line, flags=re.IGNORECASE)
        # Видалення вмісту в квадратних дужках і дужках
        line = re.sub(r"\[.*?\]", "", line, flags=re.DOTALL)  # Видалення вмісту в квадратних дужках, включаючи багаторядковий
        line = re.sub(r"\(.*?\)", "", line, flags=re.DOTALL)  # Видалення вмісту в дужках, включаючи багаторядковий

        # Очищення рядка
        line = re.sub(r",\s*", " ", line)  # Очищення пробілів після ком
        line = re.sub(r"\s+\d+", "", line)  # Видалення кінцевих чисел
        line = re.sub(r"\s{2,}", " ", line)  # Замінення декількох пробілів на один
        line = re.sub(r"\s+[.,;:]?\s*$", "", line)  # Видалення кінцевих знаків пунктуації та пробілів

        # Перевірка, чи рядок відповідає формату (число). (слова)
        if re.match(r"^\d+\.\s+\w+", line):
            refined_text += line + "\n"

    # Збереження очищеного тексту у новий текстовий файл
    with open(output_txt_path, "w", encoding="utf-8") as file:
        file.write(refined_text)


def extract_numbers(pdf_path, start_page, end_page):
    # Відкриття PDF файлу
    doc = fitz.open(pdf_path)

    # Створення текстового файлу для запису результатів
    output_file = open('output/numbers1.txt', 'w')

    # Регулярний вираз для пошуку чисел у форматі число/число
    pattern = re.compile(r'\b\d+ \s*\/\s* \d+\b')

    # Проходження по сторінках від 29 до 345
    for page_number in range(28, 345):  # Сторінки у fitz починаються з 0
        page = doc.load_page(page_number)
        text = page.get_text()
        results = pattern.findall(text)
        if results:
            output_file.write('\n'.join(results) + '\n')

    # Закриття файлів
    output_file.close()
    doc.close()

    print("Числа витягнені і записані у файл 'numbers1.txt'.")


def insert_line_in_file(file_path, line_number, text_to_insert):
    """
    Вставка рядка на певний номер у файлі.

    Args:
    file_path (str): Шлях до файлу, де буде вставлено рядок.
    line_number (int): Номер рядка, на який буде вставлено новий рядок (1-індексація).
    text_to_insert (str): Текст для вставки як новий рядок.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Вставка рядка на вказану позицію, враховуючи, що line_number з 1
    lines.insert(line_number - 1, text_to_insert + "\n")

    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(lines)

    print(f"Рядок '{text_to_insert}' вставлено на рядок {line_number} у {file_path}.")


def merge_files(words_file_path, numbers_file_path, output_file_path):
    """
    Об'єднання рядків з текстового файлу з числами з іншого файлу.
    Args:
    words_file_path (str): Шлях до файлу, що містить слова.
    numbers_file_path (str): Шлях до файлу, що містить числа.
    output_file_path (str): Шлях до файлу для збереження об'єднаного результату.
    """
    with open(words_file_path, 'r', encoding='utf-8') as words_file, \
            open(numbers_file_path, 'r', encoding='utf-8') as numbers_file, \
            open(output_file_path, 'w', encoding='utf-8') as output_file:

        words_lines = words_file.readlines()
        numbers_lines = numbers_file.readlines()

        # Переконання, що обидва файли мають однакову кількість рядків
        if len(words_lines) != len(numbers_lines):
            print("Error: Files have different lengths.")
            return

        # Об'єднання рядків з відповідними числами
        for word_line, number_line in zip(words_lines, numbers_lines):
            merged_line = f"{word_line.strip()} [{number_line.strip()}]\n"
            output_file.write(merged_line)

        print(f"Об'єднаний файл створено у {output_file_path}")


# Витягуємо числа
titles = extract_numbers("source/ukr_slovnik1.pdf", 29, 345)
# Вставляємо правильний рядок
insert_line_in_file('output/numbers1.txt', 571, '228 / 101')
# Витягуємо список стимулів
clean_pdf_text("source/ukr_slovnik1.pdf", "output/slovnik1.txt", 19, 28)
merge_files('output/slovnik1.txt', 'output/numbers1.txt', 'output/merged1.txt')
