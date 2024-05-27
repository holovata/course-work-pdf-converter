import pandas as pd


def create_cues_list(cues_txt_file):
    """
    Створює список стимулів із зазначеного текстового файлу.
    """
    cues_list = []
    with open(cues_txt_file, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split('.')
            if len(parts) < 2:
                continue
            cue = parts[1].split('[')[0].strip()  # Відокремлює назву до дужки
            cues_list.append(cue)
    return cues_list


def add_root_to_csv(input_csv_file, node_mapping_file, cues_list, output_csv_file):
    """
    Додає вузол ROOT до CSV-файлу зі вказаними даними.
    """
    # Завантаження існуючого CSV файлу
    df = pd.read_csv(input_csv_file)

    # Завантаження відображення вузлів для пошуку числових ID
    node_mapping = pd.read_csv(node_mapping_file)

    # Фільтрація відображення вузлів, щоб включати лише ті стимули, що присутні у cues_list
    filtered_node_mapping = node_mapping[node_mapping['Name'].isin(cues_list)]

    # Визначення ID ROOT з існуючого списку вузлів (припускається, що це 841)
    root_id = 841
    print(f"Використовується призначений ROOT ID: {root_id}")

    # Видалення зв'язків, де Source і Target однакові
    df = df[df['Source'] != df['Target']]

    # Визначення загальної кількості унікальних стимулів з filtered_node_mapping
    N = filtered_node_mapping.shape[0]

    # Знаходження максимального ваги у існуючих зв'язках та встановлення ваги для ROOT зв'язку
    max_weight = df['Weight'].max() + 20

    # Створення нових зв'язків для ROOT з кожним стимулом у filtered_node_mapping
    links = [{'Source': root_id, 'Target': row['Id'], 'SourceWord': 'ROOT', 'TargetWord': row['Name'], 'R': 1, 'N': root_id, 'Weight': max_weight, 'Label': f'1 / {root_id}'} for index, row in filtered_node_mapping.iterrows()]

    # Створення DataFrame з нових зв'язків
    links_df = pd.DataFrame(links)

    # Додавання нових зв'язків до існуючого DataFrame
    df = pd.concat([df, links_df], ignore_index=True)

    # Збереження оновленого DataFrame до нового CSV файлу
    df.to_csv(output_csv_file, index=False)

if __name__ == "__main__":
    cues = create_cues_list('output/merged1.txt')
    node_mapping_file = 'csvs/nodes12_list.csv'
    input_csv_file = 'csvs/cue1_response2_str_filtered.csv'
    output_csv_file = 'csvs/cue1_response2_str_filtered_ROOT.csv'
    add_root_to_csv(input_csv_file, node_mapping_file, cues, output_csv_file)
