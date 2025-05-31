from openai import OpenAI
from api_key import KEY

req = '''Кластер 0:
profession: Manager; income: 10172.36; activity_score: 0.66;
profession: Lawyer; income: 53224.08; activity_score: 0.897;
profession: Engineer; income: 35854.15; activity_score: 0.633;
profession: Manager; income: 33912.02; activity_score: 0.897;

Кластер 1:
profession: Teacher; income: 24897.43; activity_score: 0.726;
profession: Lawyer; income: 35111.21; activity_score: 0.887;
profession: Artist; income: 43510.86; activity_score: 0.642;
profession: Doctor; income: 49889.3; activity_score: 0.005;

Кластер 2:
profession: Engineer; income: 44067.25; activity_score: 0.555;
profession: Doctor; income: 56794.04; activity_score: 0.242;
profession: Lawyer; income: 40112.27; activity_score: 0.084;
profession: Lawyer; income: 32753.11; activity_score: 0.549;

Кластер 3:
profession: Artist; income: 55182.77; activity_score: 0.817;
profession: Doctor; income: 45662.95; activity_score: 0.53;
profession: Teacher; income: 47509.09; activity_score: 0.093;
profession: Artist; income: 19665.28; activity_score: 0.9;'''


def request_to_deepseek(df_as_text):
  '''Функция получает на вход датафрейм в виде текста. Отправляет его в дипсик. Затем возвращает ответ по заданному шаблону'''
  client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key= KEY,
  )

  completion = client.chat.completions.create(

    extra_body={},
    model="deepseek/deepseek-r1:free",
  messages = [
      {
          "role": "system",
          "content": "Ты маркетинговый аналитик. Ты получаешь данные по каждому кластеру и пишешь сегмент и образ человека для каждого кластера строго по такому шаблону, основываясь на присланных данных. Шаблон: Сегмент <n>; Краткое описание представителя сегмента: <описание>. Не нужно давать рекомендаций. Действуй строго по шаблону."
      },
      {
          "role": "user",
          "content": df_as_text
      }
  ])
  return completion.choices[0].message.content