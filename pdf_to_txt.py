import fitz  # PyMuPDF


def extract_and_convert(pdf_path, output_path, start_page, end_page):
    document = fitz.open(pdf_path)

    # Перевірка, чи кінцева сторінка не виходить за межі документа
    if end_page > len(document):
        end_page = len(document)

    # Ініціалізація вмісту тексту
    text_content = []

    # Проходження по кожній сторінці
    for page_num in range(start_page - 1, end_page):  # Нумерація сторінок з 0
        # Отримання сторінки
        page = document[page_num]

        # Витягування тексту зі сторінки
        text = page.get_text()

        # Додавання витягнутого тексту до списку
        text_content.append(text)

    # Закриття PDF документа
    document.close()

    # Об'єднання тексту в один рядок
    full_text = "\n".join(text_content)

    # Збереження витягнутого тексту у .txt файл
    with open(output_path, "w", encoding="utf-8") as output_file:
        output_file.write(full_text)


bad_encoding_signs = []
characters = "ÀÂ"

# Додавання кожного унікального символу з нової строки, якщо його ще немає в списку
for char in characters:
    if char not in bad_encoding_signs:
        bad_encoding_signs.append(char)


# Функція для перевірки, чи містить строка символи неправильного кодування
def contains_bad_encoding(line, signs):
    return any(sign in line for sign in signs)


def clean(text_file):
    with open(text_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    output_lines = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line == "":
            print(f"Skipping empty line and next two at index {i}")  # Відладочний вихід
            i += 3  # Пропуск порожнього рядка і наступних двох рядків
        elif len(line) == 1:
            print(f"Skipping line because it contains only one character at index {i}: {line}")  # Відладочний вихід
            i += 1  # Пропуск рядків, що містять лише один символ
        elif '*' in line:
            print(f"Skipping line due to '*' character at index {i}: {line}")  # Відладочний вихід
            i += 1  # Пропуск рядків, що містять '*'
        elif contains_bad_encoding(line, bad_encoding_signs):
            print(f"Skipping line due to bad encoding at index {i}: {line}")  # Відладочний вихід
            i += 1  # Пропуск рядка з неправильним кодуванням
        else:
            output_lines.append(lines[i])  # Додавання рядка, якщо він проходить усі перевірки
            i += 1

    # Запис очищених рядків назад у файл
    with open(text_file, 'w', encoding='utf-8') as file:
        file.writelines(output_lines)

    print(f"Cleaned content written to {text_file}")


def pdf_to_txt(pdf_path, output_path, start_page, end_page):
    extract_and_convert(pdf_path, output_path, start_page, end_page)
    clean(output_path)


pdf_to_txt("source/ukr_slovnik4.pdf", "output/slovnik4.txt", 8, 635)
pdf_to_txt("source/ukr_slovnik2.pdf", "output/slovnik2.txt", 10, 460)
print("Ready")