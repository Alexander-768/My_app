
import pandas as pd
import numpy as np
# Просто создал датафрейм для теста

def df_to_text_about_segmentation(df):
    '''Функция принимает на вход датафрейм с нужными переменными (важно чтобы поле cluster было последним ),
    а возвращает его содержимое, сгруппированное по кластерам, в текстовом формате.
    Важно, что для каждого кластера получаем максимум 5 строк, чтобы не тарить много токенов'''
    clustered_text = ""

    for cluster_id, group in df.groupby("cluster"):
        clustered_text += f"\nКластер {cluster_id}:\n"
        for num,  (_, row) in enumerate(group.iterrows()):  # индекс строки (_ — мы его не используем, поэтому подставлен прочерк);объект строки — row, который ведёт себя как словарь (row['name'], row['age'] и т.п.).
            if num<4:
                for i in df.columns[:-1]:
                    clustered_text += f"{i}: {row[i]}; "
                clustered_text += "\n"

    return clustered_text


#print(df_to_text_about_segmentation(df))
