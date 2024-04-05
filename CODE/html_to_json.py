import json
import os
import re
from bs4 import BeautifulSoup

def extract_information_from_html(html_file):
    with open(html_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
        
        # Replace this with your specific logic to extract information from the HTML file
        # For example, let's say you want to extract all the text within <p> tags:
        # paragraphs = soup.find_all('p')
        # extracted_text = '\n'.join([p.get_text() for p in paragraphs])

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
                keywords_content = keywords_content.replace('\n', '').strip()
                # keywords_content = keywords_content.split(',')
                # keywords_content = json.dumps(keywords_content)
                # print(keywords_content)
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
    
    # save to file as json
    with open('extracted_keywords.json', 'w', encoding='utf-8') as f:
        f.write('{\n')
        for filename, keywords in extracted_data.items():
            if isinstance(keywords, list):
                f.write(f'"{filename}": {keywords},\n')
            else:
                f.write(f'"{filename}": "{keywords}",\n')

        f.write('}\n')
        
        
    

# import os
# from bs4 import BeautifulSoup

# def extract_information_from_html(html_file):
#     with open(html_file, 'r', encoding='utf-8') as f:
#         soup = BeautifulSoup(f, 'html.parser')
        
#         # Replace this with your specific logic to extract information from the HTML file
#         # For example, let's say you want to extract all the text within <p> tags:
#         # paragraphs = soup.find_all('p')
#         # extracted_text = '\n'.join([p.get_text() for p in paragraphs])

#         meta_keywords = soup.find_all('meta', attrs={'name': 'keywords'})
#         # print(meta_keywords)
        
#         # Extract content attribute from each meta tag
#         try:
#             keywords_content = [meta['content'] for meta in meta_keywords]
#         except KeyError:
#             return []
#         # print(keywords_content)
        
#         return keywords_content
        
#         # return extracted_text

# def extract_information_from_directory():
#     extracted_data = {}
#     for filename in os.listdir('html_files'):
#         if not filename.endswith('.py'):
#             filepath = os.path.join('html_files', filename)
#             extracted_data[filename] = extract_information_from_html(filepath)
#     return extracted_data

# if __name__ == "__main__":
#     extracted_data = extract_information_from_directory()
    
#     # save to file
#     with open('extracted_keywords.txt', 'w', encoding='utf-8') as f:
#         for filename, data in extracted_data.items():
#             f.write(f'{filename}\n')
#             f.write(f'{data}\n\n')
    