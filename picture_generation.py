from api_key import PICTURE_KEY
import requests
import time
import json
import base64



class FusionBrainAPI:
    def __init__(self, url='https://api-key.fusionbrain.ai/', api_key='81680EFB6B571EBF721F60C4EE2BFA46', secret_key=PICTURE_KEY):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    def get_pipeline(self):
        response = requests.get(self.URL + 'key/api/v1/pipelines', headers=self.AUTH_HEADERS)
        response.raise_for_status()  # 💡 Это поможет выявить ошибки, если они есть
        data = response.json()
        return data[0]['id']
    
    def generate(self, prompt, pipeline, images=1, width=1024, height=1024): # Если надо поменять размеры изображения то, это сюда
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {
                "query": f'{prompt}'
            }
        }

        data = {
            'pipeline_id': (None, pipeline),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post(self.URL + 'key/api/v1/pipeline/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        return data['uuid']
    

    def check_generation(self, request_id, attempts=10, delay=10):
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/pipeline/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                return data['result']['files']

            attempts -= 1
            time.sleep(delay)

def generate_picture(prompt):
    if __name__ == '__main__':
        api = FusionBrainAPI()
        pipeline_id = api.get_pipeline()
        uuid = api.generate(f"Сегмент: {prompt}. На картинке один человек-представитель сегмента. Не надо цифр, грфиков и надписей.", pipeline_id)
        files = api.check_generation(uuid)
        with open('image.jpg', 'wb') as f:
           f.write(base64.b64decode(files[0]))
        ##print(files[0]) тут возвращается base-64 строка
        ###img_data = base64.b64decode(files[0])
        ####return files[0]



#generate_picture('Люди в возрасте от 25 до 56 лет с умеренным доходом (от $26 тыс. до $47 тыс. в год). Сегмент включает как молодых специалистов на старте карьеры, так и лиц среднего возраста с невысоким или стабильным заработком')
#print(generate_picture('Мужчина в очках'))
#print('Все')