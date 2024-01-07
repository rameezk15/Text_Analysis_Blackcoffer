from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import os

def create_output_directory(directory):
    if not os.path.isdir(directory):
        os.makedirs(directory)

def import_input_data():
    input_file_path =  os.path.join(os.getcwd(), "Input", "Input.xlsx")
    return pd.read_excel(input_file_path)


def extract_clean_text(html):
    title = html.find('h1', class_=['entry-title','tdb-title-text'])
    content = html.find('div', class_=['td-post-content tagdiv-type','td_block_wrap tdb_single_content tdi_130 td-pb-border-top td_block_template_1 td-post-content tagdiv-type','td-post-content'])
    clean_text = title.text + "\n" + content.text.strip()
    return clean_text

def save_to_file(file_path, clean_text):
    with open(file_path, 'w') as file:
        file.write(clean_text)

def main():
    output_dir = 'article_data'
    create_output_directory(output_dir)

    data = import_input_data()

    for index, row in data.iterrows():
        url = row['URL']
        url_id = row['URL_ID']

        response = requests.get(url)
        if response.ok:
            web_text = response.text
            html = bs(web_text, 'html.parser')

            clean_text = extract_clean_text(html)

            file_name = f"{url_id}.txt"
            file_path = os.path.join(output_dir, file_name)
            save_to_file(file_path, clean_text)

if __name__ == "__main__":
    main()