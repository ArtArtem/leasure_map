import os
import json
import requests

API_KEY = 'e18673a2a0374788b0c52b8d8af47588'
ENDPOINT = 'https://westcentralus.api.cognitive.microsoft.com/vision/v2.0/ocr'
DIR = 'imgs'

#можно сделать перем с инпутом расширения картинки
#пока пусть будет без
rashir=".jpg"
lang="ru"
def handler():
    text = ''
    for filename in sorted(os.listdir(DIR)):
        if filename.endswith(rashir): 
            pathToImage = '{0}/{1}'.format(DIR, filename)
            results = get_text(pathToImage)
            text += parse_text(results)
    

    #open('output.txt', 'w').write(text)
    #создает или презаписывает файл с результатом анализа изображения
    #пока что закомментировал


    print(text)

def parse_text(results):
    text = ''
    for region in results['regions']:
        for line in region['lines']:
            for word in line['words']:
                text += word['text'] + ' '
            text += '\n'
    return text  

def get_text(pathToImage):
    print('Processing: ' + pathToImage)
    headers  = {
        'Ocp-Apim-Subscription-Key': API_KEY,
        'Content-Type': 'application/octet-stream'
    }
    params   = {
        'language': lang,
        'detectOrientation ': 'true'
    }
    payload = open(pathToImage, 'rb').read()
    response = requests.post(ENDPOINT, headers=headers, params=params, data=payload)
    results = json.loads(response.content)
    return results

if __name__ == '__main__':
    handler()
