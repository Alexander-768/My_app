#Работает последовательно как и надо
import streamlit as st
import pandas as pd
from sklearn.cluster import KMeans
from picture_generation import FusionBrainAPI
from df_to_text import df_to_text_about_segmentation
from deepseek_market_analyst import request_to_deepseek
from proccess_of_GPT_answer import extract_segment_descriptions
import base64
import plotly.express as px

st.set_page_config(page_title="Сегментация клиентов", layout="wide")
st.title("🎯 Система сегментации клиентов с визуализацией")

# Компонент для загрузки CSV-файла; Показывает кнопку выбора файла
uploaded_file = st.file_uploader("Загрузите CSV файл с данными", type=['csv'])

if uploaded_file is not None:
    # Читаем csv
    df = pd.read_csv(uploaded_file)
    
    # Предпросмотр данных
    st.subheader("Предпросмотр данных")
    st.dataframe(df.head())
    
    # Выбор признаков
    st.subheader("Выберите переменные для сегментации")
    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
    selected_features = st.multiselect(
        "Выберите переменные для кластеризации:",
        options=numeric_columns.tolist()
    )
    
    # Только после выбора переменных показываем остальной интерфейс
    if selected_features:
        # Кол-во кластеров
        n_clusters = st.slider("Количество сегментов:", min_value=2, max_value=4, value=3)
        
        if st.button("Провести сегментацию"):
            with st.spinner("Выполняется сегментация. Это займет до 3 минут..."):
                # Кластеризация
                X = df[selected_features]
                kmeans = KMeans(n_clusters=n_clusters, random_state=42)
                kmeans.fit(X)
                
                
                clustered_df = X.copy()
                clustered_df['cluster'] = kmeans.labels_
                
                # Текстовое описание
                text_description = df_to_text_about_segmentation(clustered_df)
                
                # Описание от дипсика
                with st.spinner("Генерируются описания сегментов. Это займет до 3 минут..."):
                    deepseek_response = request_to_deepseek(text_description)
                    segment_descriptions = extract_segment_descriptions(deepseek_response)
                
                
                st.subheader("Результаты сегментации")
                
                
                api = FusionBrainAPI()
                pipeline_id = api.get_pipeline()
                
                
                cols = st.columns(n_clusters)
                
                for idx, (description, col) in enumerate(zip(segment_descriptions, cols)):
                    with col:
                        st.write(f"**Сегмент {idx+1}**")
                        st.write(description)
                        
                        
                        with st.spinner(f"Генерируется изображение для сегмента {idx+1}..."):
                            try:
                                uuid = api.generate(description, pipeline_id)
                                files = api.check_generation(uuid)
                                if files:
                                    image_data = base64.b64decode(files[0])
                                    st.image(image_data, caption=f"Визуализация сегмента {idx+1}")
                            except Exception as e:
                                st.error(f"Ошибка при генерации изображения: {str(e)}")
                

            # Статистики каждого сегмента
            st.subheader("Статистика по сегментам")
            for cluster in range(n_clusters):
                with st.expander(f"Статистика сегмента {cluster+1}"):
                    cluster_data = clustered_df[clustered_df['cluster'] == cluster]
                    st.write(cluster_data[selected_features].describe())
            

 
            st.subheader("Распределение клиентов по сегментам")

            
            segment_sizes = clustered_df['cluster'].value_counts().sort_index()

            # Создаём метки "Сегмент 1", "Сегмент 2", ...
            segment_labels = [f"Сегмент {i+1}" for i in segment_sizes.index]

            #  pie chart 
            fig = px.pie(
                values=segment_sizes.values,
                names=segment_labels,  # Используем метки вместо чисел
                title='Распределение клиентов по сегментам',
                labels={'names': 'Сегмент', 'values': 'Количество клиентов'}
            )

     
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(
                showlegend=True,
                width=800,
                height=600
            )

            
            st.plotly_chart(fig)

    
    elif not selected_features and st.button("Провести сегментацию"):
        st.warning("Пожалуйста, выберите переменные для сегментации")

else:
    st.info("👆 Загрузите CSV файл для начала анализа")