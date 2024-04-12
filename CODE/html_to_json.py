import os
import re
from bs4 import BeautifulSoup

def extract_information_from_html(html_file):
    with open(html_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')


        meta_keywords = soup.find_all('meta', attrs={'name': 'keywords'})
        # print(meta_keywords)

        if not meta_keywords:
            meta_keywords = soup.find('title')
            try:
                return meta_keywords.get_text().replace('\n', '').strip()
            except AttributeError:
                return ''

        else:
            try:
                keywords_content = meta_keywords[0]['content']
                keywords_content = re.sub('(?<!:)[ ,;]+', ',', keywords_content)
                keywords_content = keywords_content.replace('\n', '').replace('\t', ' ').strip()
                return keywords_content
            except KeyError:
                return []
    

def extract_information_from_directory():
    extracted_data = {}
    for filename in os.listdir('html_files'):
        if not filename.endswith('.py'):
            filepath = os.path.join('html_files', filename)
            extracted_data[filename] = extract_information_from_html(filepath)
    return extracted_data

if __name__ == "__main__":
    extracted_data = extract_information_from_directory()
    
    # # save to file as json
    # with open('extracted_keywords.json', 'w', encoding='utf-8') as f:
    #     # f.write('{\n')
    #     for filename, keywords in extracted_data.items():
    #         f.write("{\n")
    #         f.write(f'"link": "{filename}",\n')
    #         if isinstance(keywords, list):
    #             f.write(f'"keywords": {keywords}\n')
    #         else:
    #             f.write(f'"keywords": "{keywords}"\n')
    #         f.write("},\n")
    #     # f.write('}\n')
        
    # save each entry as a separate json file
    if not os.path.exists('extracted_keywords'):
        os.mkdir('extracted_keywords')
    
    for filename, keywords in extracted_data.items():
        with open(f'extracted_keywords/{filename}.json', 'w', encoding='utf-8') as f:
            f.write('{\n')
            f.write(f'"link": "{filename}",\n')
            if isinstance(keywords, list):
                f.write(f'"keywords": {keywords}\n')
            else:
                f.write(f'"keywords": "{keywords}"\n')
            f.write('}\n')
            
    