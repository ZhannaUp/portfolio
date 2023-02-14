#!/usr/bin/env python
# coding: utf-8

# <div class="alert alert-block alert-info">
# <font size="5">
# <center><b>АНАЛИЗ РЫНКА ЗАВЕДЕНИЙ ОБЩЕСТВЕННОГО ПИТАНИЯ МОСКВЫ</b></center>
# </font>
#     </div> 

# <span class="mark"> **Описание проекта**</span>
# 
# 
# Инвесторы из фонда «Shut Up and Take My Money» решили попробовать себя в новой области и открыть заведение общественного питания в Москве. Заказчики ещё не знают, что это будет за место: кафе, ресторан, пиццерия, паб или бар, — и какими будут расположение, меню и цены.
# Для начала они просят вас — аналитика — подготовить исследование рынка Москвы, найти интересные особенности и презентовать полученные результаты, которые в будущем помогут в выборе подходящего инвесторам места.
# 
# Доступен датасет с заведениями общественного питания Москвы, составленный на основе данных сервисов Яндекс Карты и Яндекс Бизнес на лето 2022 года. Информация, размещённая в сервисе Яндекс Бизнес, могла быть добавлена пользователями или найдена в общедоступных источниках. Она носит исключительно справочный характер.
# 
# <span class="mark">  **Цель проекта**</span>
# 1) Проанализировать рынок заведений общественного питания Москвы.\
# 2) Выявить закономерности и особенности рынка.\
# 3) Презентовать полученные результаты.
# 
# <span class="mark"> **Описание данных**</span>
# 
# Файл moscow_places.csv:
# 
# - `name` — название заведения;
# - `address` — адрес заведения;
# - `category` — категория заведения, например «кафе», «пиццерия» или «кофейня»;
# - `hours` — информация о днях и часах работы;
# - `lat` — широта географической точки, в которой находится заведение;
# - `lng` — долгота географической точки, в которой находится заведение;
# - `rating` — рейтинг заведения по оценкам пользователей в Яндекс Картах (высшая оценка — 5.0);
# - `price` — категория цен в заведении, например «средние», «ниже среднего», «выше среднего» и так далее;
# - `avg_bill` — строка, которая хранит среднюю стоимость заказа в виде диапазона, например:
# 
#    - «Средний счёт: 1000–1500 ₽»;
#    - «Цена чашки капучино: 130–220 ₽»;
#    - «Цена бокала пива: 400–600 ₽».
#    - и так далее;
#    
# - `middle_avg_bill` — число с оценкой среднего чека, которое указано только для значений из столбца avg_bill, начинающихся с подстроки «Средний счёт»:
#    - Если в строке указан ценовой диапазон из двух значений, в столбец войдёт медиана этих двух значений.
#    - Если в строке указано одно число — цена без диапазона, то в столбец войдёт это число.
#    - Если значения нет или оно не начинается с подстроки «Средний счёт», то в столбец ничего не войдёт.
# - `middle_coffee_cup` — число с оценкой одной чашки капучино, которое указано только для значений из столбца avg_bill, начинающихся с подстроки «Цена одной чашки капучино»:
#    - Если в строке указан ценовой диапазон из двух значений, в столбец войдёт медиана этих двух значений.
#    - Если в строке указано одно число — цена без диапазона, то в столбец войдёт это число.
#    - Если значения нет или оно не начинается с подстроки «Цена одной чашки капучино», то в столбец ничего не войдёт.
# - `chain` — число, выраженное 0 или 1, которое показывает, является ли заведение сетевым (для маленьких сетей могут встречаться ошибки);
# - `district` — административный район, в котором находится заведение, например Центральный административный округ;
# - `seats` — количество посадочных мест.

#  ## Оглавление
# 
# * [1. Изучение входных данных](#num1)
# 
# * [2. Предобработка данных](#num2)
#     * [2.1. Проверим дубликаты и пропуски](#num3)
#     * [2.2. Cоздадим столбец street с названиями улиц из столбца с адресом](#num4)
#     * [2.3. Создайте столбец is_24/7 с обозначением](#num5)   
# 
# * [3. Анализ данных](#num6)
#     * [3.1. Какие категории заведений представлены в данных](#num7)
#     * [3.2. Исследуйте количество посадочных мест в местах по категориям](#num8)
#     * [3.3. Соотношение сетевых и несетевых заведений](#num9)
#     * [3.4. Сгруппируйте данные по названиям заведений и найдите топ-15 популярных сетей в Москве](#num10)
#     * [3.5. Какие административные районы Москвы присутствуют в датасете](#num11)
#     * [3.6. Визуализируйте распределение средних рейтингов по категориям заведений](#num12)
#     * [3.7. Постройте фоновую картограмму (хороплет) со средним рейтингом заведений каждого района](#num13)
#     * [3.8. Отобразите все заведения датасета на карте с помощью кластеров](#num14)
#     * [3.9. Найдите топ-15 улиц по количеству заведений](#num15)
#     * [3.10. Найдите улицы, на которых находится только один объект общепита](#num16)
#     * [3.11. Значения средних чеков заведений](#num17)
#     * [3.12. Исследовать особенности заведений с плохими рейтингами, средние чеки в таких местах и распределение по категориям заведений.](#num19)
#     
# * [4. Детализация исследования: открытие кофейни](#num20)
#     * [4.1. Количество кофеен](#num21)
#     * [4.2. Терроториальное расположение](#num21)
#     * [4.3. Круглосуточные кофейни](#num22)
#     * [4.4. Рейтинги](#num23)
#     
# * [5. Презентация для инвесторов](#num24)
#     
# * [Общий вывод](#result)

# ## Выполнение проекта

# <a name="num1"></a>
# ### Изучение входных данных

# In[1]:


# Загружаем библиотеки
import pandas as pd
import numpy as np
import datetime as dt
from matplotlib.pyplot import figure
import warnings
warnings.filterwarnings('ignore')
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.pylab as pylab
import seaborn as sns
from matplotlib.ticker import FuncFormatter
import seaborn as sns
from plotly import graph_objects as go
import plotly.express as px
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import folium


# In[2]:


# Устанавливаю единый стиль палитры для всех графиков
sns.set_palette('pastel')        # Цветовая палитра пастельных тонов
sns.set_style('dark')            # Тёмный стиль графика


# In[3]:


moscow_places = pd.read_csv('https://code.s3.yandex.net/datasets/moscow_places.csv')

moscow_places.head(100)


# In[4]:


# Выведим основную информацию о датафрейме с помощью метода `info()`
moscow_places.info()


# In[5]:



moscow_places.shape


# In[6]:


# Преобразуем в строчку для визуализации
moscow_places['chain'] = moscow_places['chain'].astype('str')


# In[7]:


moscow_places.info()


# <a name="num2"></a>
# ### Предобработка данных

# <a name="num3"></a>
# #### Проверим дубликаты и пропуски

# In[8]:


# Проверим наличие пропусков в каждом столбце(%)
pd.DataFrame(round(moscow_places.isna().mean()*100,)).style.background_gradient('BuPu') 


# In[9]:


# пропущенные значения бары

def pass_value_barh(df):
    try:
        (
            (df.isna().mean()*100)
            .to_frame()
            .rename(columns = {0:'space'})
            .query('space > 0')
            .sort_values(by = 'space', ascending = True)
            .plot(kind= 'barh', figsize=(19,6), rot = -5, legend = False, fontsize = 16, color = '#d0e0e3')
            .set_title('Количество пропусков в разрезе данных' + "\n", fontsize = 22, color = '#444444')    
        );    
    except:
        print('пропусков не осталось :) ')


# In[10]:


pass_value_barh(moscow_places)


# In[11]:


# Проверим наличие дубликатов
moscow_places.duplicated().sum()


# <a name="num4"></a>
# #### Cоздадим столбец street с названиями улиц из столбца с адресом

# In[12]:


# Создаем функцию для разделения строки
def street_ext(value):
    ext_split=value.split(sep=', ')[1]
    return ext_split


# In[13]:


# Создаем столбец с помощью метода apply  
moscow_places['street'] = moscow_places['address'].apply(street_ext)


# In[14]:


moscow_places[['address','street']].head(10)


# In[15]:


# Топ 15 улиц по количеству заведений
temp = moscow_places.groupby('street').count().sort_values(by='category', ascending=False).head(15).reset_index()
top_15_streets = list(temp['street']) # более подробно про улицы в пп 1.2.2.12 
temp


# <a name="num5"></a>
# #### Cоздадим столбец is_24/7 с обозначением, что заведение работает ежедневно и круглосуточно (24/7):
#     - логическое значение True — если заведение работает ежедневно и круглосуточно;
#     - логическое значение False — в противоположном случае.

# In[16]:


# Создадим столбец moscow_places['is_24/7'] использовав метод contains
import re
moscow_places['is_24/7'] = moscow_places['hours'].str.contains('круглосуточно|ежедневно', regex=True)
                                                        


# In[17]:


moscow_places[['hours','is_24/7']].head(100)


# In[18]:


# Проверим количество
moscow_places['is_24/7'].value_counts().to_frame()


# **`ВЫВОД`**: 
# <div style="border:solid orange 2px; padding: 20px"> 
# 
# В исходном датасете  8406 строк и 14 столбцов.
#                      
# После того, как изучили датасеты, выявили следующие первичные отклонения:
#      
# 1) Добавили два новых столбца- с улицой и is_24/7.     
# 2) Пропуски не стала удалять, тк они не подлежат замене и имеют вес в данных.\
# 3) Дубликаты не выявлены.    
# </div>

# <a name="num6"></a>
# ### Анализ данных (EDA)

# <a name="num7"></a>
# #### Какие категории заведений представлены в данных? 
# - Исследуем количество объектов общественного питания по категориям: рестораны, кофейни, пиццерии, бары и так далее. 
# - Построим визуализацию. Ответьте на вопрос о распределении заведений по категориям.

# In[19]:


category_catering = moscow_places['category'].value_counts().to_frame()

sum_catering = len(moscow_places['category'])
print('Всего заведений:', sum_catering )

# Определим долю каждой категории
category_catering['share(%)'] = round((category_catering['category']/sum_catering)*100,2)
category_catering


# In[20]:


# Построим график

fig = px.bar(category_catering, y ='category', color = category_catering.index,             color_discrete_map = {'кафе':'#ff71ce', 'ресторан':'#01cdfe',                                 'кофейня':'#05ffa1', 'бар,паб':'#b967ff',                                 'пиццерия':'#fffb96','быстрое питание':'#cca01d',                                 'столовая':'#a1ab3e', 'булочная':'#376e83'})  
                                  
                                
# оформляем график
fig.update_layout(title='Распределение заведений по категориям',
                   xaxis_title='Категория заведения',
                   yaxis_title='Количество заведений',
                   width=800, # указываем размеры графика
                   height=500)
fig.show()


# <span class="mark">**Наблюдение:**</span> 
# Согласно графика, в топ-3 вошли такие категории, как:
# - кафе- 2378 (28,3%) 
# - ресторан- 2043 (24,3%) 
# - кофейня- 1413 (16,8%)

# <a name="num8"></a>
# #### Исследуем количество посадочных мест в местах по категориям: рестораны, кофейни, пиццерии, бары и так далее. Построим визуализацию. Проанализируем результаты и сделаем выводы.

# In[21]:


# Отсортируем события по среднему кол-ву посадочных мест. Использыем метод median, так как высокий разброс
category_seats = moscow_places.groupby('category').agg({'seats':'median'})                             .reset_index()                             .sort_values('seats', ascending=False)
category_seats.columns = ['Категория заведения', 'Среднее кол-во мест']

category_seats.style.bar(subset=['Среднее кол-во мест'], color='#ffe135')


# In[22]:


# Построим график

fig = px.bar(category_seats, y='Среднее кол-во мест', x= 'Категория заведения', color = 'Категория заведения',             color_discrete_map = {'кафе':'#ff71ce', 'ресторан':'#01cdfe',                                 'кофейня':'#05ffa1', 'бар,паб':'#b967ff',                                 'пиццерия':'#fffb96','быстрое питание':'#cca01d',                                 'столовая':'#a1ab3e', 'булочная':'#376e83'}) 
# оформляем график
fig.update_layout(title='Распределение среднего кол-ва посадочный мест в разрезе категорий заведений',
                   xaxis_title='Категория заведения',
                   yaxis_title='Среднее кол-во мест',
                   width=800, # указываем размеры графика
                   height=500)
fig.show()


# Посмотрим медианное значение посадочных мест по улицам

# In[23]:


top15_streets_list = temp['street'].to_list()
top15_streets_data = moscow_places.query('street in @top15_streets_list')


top15_streets_data['seats'].median()
moscow_places['seats'].median()
plt.figure(figsize=(15,9))
plt.xlim(0,700)
sns.boxplot(data=top15_streets_data, x='seats', y='street')
plt.title('Распределение количества посадочных мест для топ-15 улиц по кол-ву объектов')
plt.ylabel('')
plt.xlabel('Кол-во посадочных мест')
plt.show()

print('Среднее кол-во посадочных мест в заведениях на топ-15 улицах по количеству объектов: {}'.format(top15_streets_data['seats'].median()))
print('Среднее кол-во посадочных мест в заведениях НЕ на топ-15 улицах по количеству объектов: {}'.format(moscow_places.query('street not in @top15_streets_list')['seats'].median()))


# <span class="mark">**Наблюдение:**</span> 
# Согласно графика, в топ-3 категории по среднему кол-ву посадочных мест вошли:
# 
# - ресторан- 86 места
# - бар/паб- 82,5 мест
# - кофейня- 80 мест 
# 
# Не совсем уверена, что этот показатель эффективен, так как количество посадочных мест зависит от площади помещения и имеет определенные нормативы.

# <a name="num9"></a>
# #### Рассмотрим и изобразим соотношение сетевых и несетевых заведений в датасете. Каких заведений больше? Какие категории заведений чаще являются сетевыми? Исследуем данные и ответим на вопрос графиком.

# In[24]:


chain_catering_total = moscow_places['chain'].value_counts().to_frame()

# Определим долю 
chain_catering_total['share(%)'] = round((chain_catering_total['chain']/sum_catering)*100,2)

chain_catering_total.columns = ['Сетевое/Несетевое', 'Доля(%)']

chain_catering_total.style.bar(subset=['Доля(%)'], color='#ffe135')

chain_catering_total


# In[25]:


# группируем данные по категории заведений и типу и считаем кол-во
chain_catering = moscow_places.groupby(['category','chain'],                         as_index = False)[['name']].count()


# In[26]:


chain_catering


# In[27]:


fig = px.bar(chain_catering, x="category", y= 'name', color="chain", title="Соотношение сетевых и несетевых заведений",             #text_auto=True, 
             pattern_shape_sequence=["+"],\
             labels= {'name': 'Кол-во заведений', 'category': 'Категория заведения'},
             width=800, # указываем размеры графика
             height=500)

fig.show()


# <span class="mark">**Наблюдение:**</span> Проанализировав данные по соотношению сетевые/несетевые заведения выявили следующее:
# - 62% несетевые к 38% сетевые заведения;
# - лидерами сетевых заведений оказались - кафе, ректораны и кофейни;
# - стоит заметить, что пиццерии представляют чаще сетевые типы заведений.

# <a name="num10"></a>
# #### Сгруппируем данные по названиям заведений и найдите топ-15 популярных сетей в Москве. 
# 
# - Построим подходящую для такой информации визуализацию. Знакомы ли вам эти сети? 
# - Есть ли какой-то признак, который их объединяет? 
# - К какой категории заведений они относятся? 
# 

# In[28]:


# отфильтруем данные, сгруппируем по городам и посчитаем объявления
top_15_catering = moscow_places.loc[moscow_places['chain'] == '1'].groupby('name')[['name']].count()
# переименуем столбец
top_15_catering.columns = ['total_count']
# отсортируем и оставим пятьнадцать лидеров
top_15_catering = top_15_catering.reset_index().sort_values(by='total_count', ascending=False).head(15)
top_15_catering


# In[29]:


# Построим график
fig = px.bar(top_15_catering, x = 'name', y='total_count')
# оформляем график
fig.update_layout(title='Топ-15 популярных сетей в Москве',
                   xaxis_title='Категория заведения',
                   yaxis_title='Среднее кол-во мест',
                   width=800, # указываем размеры графика
                   height=500)
fig.show()


# <span class="mark">**Наблюдение:**</span> Лидерами сетевых заведений стали кофейни( "Шоколадница") и пиццерии("Домино'с Пицца" и "Додо Пицца"). Кофейня "Шоколадница" значитально опережает остальные сетевые заведения.

# <a name="num11"></a>
# #### Какие административные районы Москвы присутствуют в датасете? Отобразим общее количество заведений и количество заведений каждой категории по районам. Попробуем проиллюстрировать эту информацию одним графиком.

# In[30]:


# Найдем общее количество категорий заведений в каждом районе

regions = moscow_places.pivot_table(index='district', columns= 'category',               aggfunc={'category': 'count' })

regions


# In[31]:


# Построим heatmaps по районам Москвы, категории заведений и кол-ву заведений
fig, ax = plt.subplots(figsize=(12, 5))

sns.heatmap(regions, annot= True, fmt=" d", cmap="RdPu", linewidths= .3) 
  
# формируем заголовок графика и подписи осей средствами matplotlib
plt.title('Количество заведений по категориям и районам Москвы')
plt.xlabel('Категории заведений')
plt.ylabel('Районы Москвы')
plt.show()


# <span class="mark">**Наблюдение:**</span> В датасете присутствует 9 административных районов Москвы. Наиболее популярным по количеству заведения является ЦАО. 

# <a name="num12"></a>
# #### Визуализируем распределение средних рейтингов по категориям заведений. Сильно ли различаются усреднённые рейтинги в разных типах общепита?

# In[32]:


# Найдем средний рейтинг по всем заведениям
print('Медианный рейтинг по всем заведениям:', round(moscow_places['rating'].median(), 2))

# Найдем средний рейтинг в разрезе категорий заведений
rating = moscow_places.groupby('category')[['rating']].median().reset_index()
rating.columns = ['Категория заведения', 'Медианный рейтинг']
rating


# In[33]:


fig = px.bar(rating, y='Медианный рейтинг', x= 'Категория заведения', color = 'Категория заведения',             color_discrete_map = {'кафе':'#ff71ce', 'ресторан':'#01cdfe',                                 'кофейня':'#05ffa1', 'бар,паб':'#b967ff',                                 'пиццерия':'#fffb96','быстрое питание':'#cca01d',                                 'столовая':'#a1ab3e', 'булочная':'#376e83'}) 

# оформляем график
fig.update_layout(title='Медианный рейтинг по категориям заведений',
                   xaxis_title='Категория заведения',
                   yaxis_title='Медианный рейтинг',
                   width=800, # указываем размеры графика
                   height=500)
# добавляем ось X
fig.add_hline(y=4.23, line_dash="dash", line_color="grey")

fig.show()


# <span class="mark">**Наблюдение:**</span> Медианный рейтинг по всем заведениям 4.3. Практические все категории заведений в рамках среднего рейтинга, за исключением категорий "быстрое питание"(4.2) и "кафе"(4.2)

# <a name="num13"></a>
# #### Построим фоновую картограмму (хороплет) со средним рейтингом заведений каждого района. Границы районов Москвы, которые встречаются в датасете, хранятся в файле admin_level_geomap.geojson (скачать файл для локальной работы).

# In[34]:


# Выведим районы Москвы
moscow_places['district'].unique()


# В датасете представлено 9 округов.
# 
# Для каждого округа посчитаем медианный рейтинг заведений, которые находятся на его территории:

# In[35]:


rating_moscow_places = moscow_places.groupby('district', as_index=False)['rating'].agg('median')
rating_moscow_places = rating_moscow_places.sort_values(by='rating', ascending = False)
rating_moscow_places


# In[36]:


import urllib.request, json 
with urllib.request.urlopen("https://code.s3.yandex.net/data-analyst/admin_level_geomap.geojson") as url:
    geo_json = json.load(url)

print(json.dumps(geo_json, indent=2, ensure_ascii=False, sort_keys=True))


# In[37]:


# импортируем карту и хороплет
from folium import Map, Choropleth

# загружаем JSON-файл с границами округов Москвы
state_geo = 'https://code.s3.yandex.net/data-analyst/admin_level_geomap.geojson'
# moscow_lat - широта центра Москвы, moscow_lng - долгота центра Москвы
moscow_lat, moscow_lng = 55.751244, 37.618423

# создаём карту Москвы
m = Map(location=[moscow_lat, moscow_lng], zoom_start=10)

# создаём хороплет с помощью конструктора Choropleth и добавляем его на карту
Choropleth(
    geo_data=state_geo,
    data=rating_moscow_places,
    columns=['district', 'rating'],
    key_on='feature.name',
    fill_color='YlOrBr',
    fill_opacity=0.8,
    legend_name='Медианный рейтинг заведений по районам',
).add_to(m)

# выводим карту
m


# <span class="mark">**Наблюдение:**</span> Высокий рейтинг у ЦАО (4.4 балла), низкий рейтинг у СВАО и ЮВА по 4.2 баллов.

# <a name="num14"></a>
# #### Отобразим все заведения датасета на карте с помощью кластеров средствами библиотеки folium.

# In[38]:


# импортируем карту и маркер
from folium import Map, Marker
# импортируем кластер
from folium.plugins import MarkerCluster

# moscow_lat - широта центра Москвы, moscow_lng - долгота центра Москвы
moscow_lat, moscow_lng = 55.751244, 37.618423

# создаём карту Москвы
m = Map(location=[moscow_lat, moscow_lng], zoom_start=10)
# создаём пустой кластер, добавляем его на карту
marker_cluster = MarkerCluster().add_to(m)

# пишем функцию, которая принимает строку датафрейма,
# создаёт маркер в текущей точке и добавляет его в кластер marker_cluster
def create_clusters(row):
    Marker(
        [row['lat'], row['lng']],
        popup=f"{row['name']} {row['rating']}",
    ).add_to(marker_cluster)

# применяем функцию create_clusters() к каждой строке датафрейма
moscow_places.apply(create_clusters, axis=1)

# выводим карту
m


# <span class="mark">**Наблюдение:**</span> На карте видно, что основной объем заведений расположен в рамках третьего транспортного кольца. Меньше всего заведений на юге Москвы. 

# <a name="num15"></a>
# #### Найдем топ-15 улиц по количеству заведений. Построим график распределения количества заведений и их категорий по этим улицам. Попробуем проиллюстрировать эту информацию одним графиком.

# In[39]:


top15 = moscow_places['street'].value_counts().head(15).index
res = moscow_places.query('street in @top15')

map_street = res.groupby(['street', 'category'], as_index=False).count()
                

fig = px.bar(map_street, x = 'street', y='name', color= 'category', 
            labels= {'name': 'Кол-во заведений', 'street': 'Улица'}, title='Количество заведений по улицам Москвы в разрезе категории заведений',
            color_discrete_map = {'кафе':'#ff71ce', 'ресторан':'#01cdfe',\
                                 'кофейня':'#05ffa1', 'бар,паб':'#b967ff',\
                                 'пиццерия':'#fffb96','быстрое питание':'#cca01d',\
                                 'столовая':'#a1ab3e', 'булочная':'#376e83'}) 
fig.update_layout(xaxis={'categoryorder':'total descending'})
fig.show()


# In[40]:


# Посчитаем топ-15 улиц с общим кол-вом заведений 
top_streets = moscow_places.groupby('street', as_index=False).agg({'name':'count'})
top_streets.columns = ['улица', 'кол-во заведений']
top_streets = top_streets.sort_values(by='кол-во заведений', ascending = False)
top15_streets = top_streets.head(15)

top15_streets


# <span class="mark">**Наблюдение:**</span> Наибольшее количество объектов питания расположены на главных улицах города: проспект Мира, Профсоюзная улица и проспект Вернадского, с небольшим отрывом Ленинградский проспект.
# По категориям заведения большая часть расположилась на:
# - "кафе": проспект Мира;
# - "кофейня": проспект Мира;
# - "ресторан": проспект Мира;
# - "пиццерия": проспект Мира;
# - "бар/паб": Ленинградский проспект;
# - "столовая": Варшавское шоссе;
# - "булочная": Ленинградский проспект;
# - "быстрое питание": проспект Мира.

# <a name="num16"></a>
# #### Найдем улицы, на которых находится только один объект общепита. Что можно сказать об этих заведениях?

# In[41]:


# Выведим на экран все улицы с одним объектом общепита
one_in_street = moscow_places.pivot_table(index=['street'],
                                          values='name',
                                          aggfunc='count').reset_index().query('name == 1')
one_in_street= one_in_street.drop('name',1)
one_in_street


# Для того, чтобы узнать к каким районам принадлежат эти улицы, воспользуемся данными Мосгаза

# In[42]:


# Путь к внешней таблице
url = 'https://drive.google.com/file/d/1-ZkvuF415yLxJXnqqcxvHS7k8x9DGyNi/view?usp=share_link'
url='https://drive.google.com/uc?id=' + url.split('/')[-2]
df_moscow_streets = pd.read_csv(url)

df_moscow_streets.head()


# In[43]:


# Переименуем столбцы
df_moscow_streets = df_moscow_streets.rename(columns={'streetname':'улица'})


# In[44]:


# Посчитаем общее кол-во улиц с одним объектом
one_in_street = top_streets[top_streets['кол-во заведений']==1]
# Удалим дубликаты
#one_in_street= one_in_street.drop('кол-во заведений',1)

print('Всего улиц с 1 объектом общественного питания: {}, что составляет {:.1%} от всего кол-ва улиц с объектами общественного питания'      .format(len(one_in_street), (len(one_in_street)/len(top_streets))))

#  Объединим две таблицы с помощью метода merge для получения округов и районов
streets_with_1_object_merged = one_in_street.merge(df_moscow_streets[['улица', 'okrug', 'area']], left_on='улица', right_on='улица')

streets_with_1_object_merged.columns = ['улица', 'кол-во заведений', 'округ', 'район']
streets_with_1_object_merged


# In[45]:


#Найдем топ20 районов 
top20_regions_with_1_object = streets_with_1_object_merged.groupby('район').agg({'улица':'count'}).reset_index().                                             sort_values(by='улица', ascending = False)

top20_regions_with_1_object.head(20)


# In[46]:


# Найдем топ3 округов с одним объектом на улице
top5_okrug_with_1_object = streets_with_1_object_merged.groupby('округ').agg({'улица':'count'}).reset_index().                                             sort_values(by='улица', ascending = False)

top5_okrug_with_1_object.head(5)


# <span class="mark">**Наблюдение:**</span> Всего улиц с 1 объектом общественного питания: 458, что составляет 31.6% от всего кол-ва улиц с объектами общественного питания. Большая часть улиц расположена в ЦАО (возможно это связано с небольшими улицами) и ВАО.

# <a name="num17"></a>
# #### Значения средних чеков заведений хранятся в столбце middle_avg_bill. Эти числа показывают примерную стоимость заказа в рублях, которая чаще всего выражена диапазоном. 
# - Посчитаем медиану этого столбца для каждого района. Используем это значение в качестве ценового индикатора района. 
# - Построим фоновую картограмму (хороплет) с полученными значениями для каждого района. 
# - Проанализируем цены в центральном административном округе и других. Как удалённость от центра влияет на цены в заведениях?

# In[47]:


# Найдем средний чек по всем заведениям
print('Средний чек по всем заведениям:', round(moscow_places['middle_avg_bill'].median(), 2))

# Найдем средний чек для каждого района
middle_avg_bill_region = moscow_places.groupby('district')[['middle_avg_bill']].median().reset_index().                                             sort_values(by='middle_avg_bill', ascending = False)
middle_avg_bill_region.columns = ['Район', 'Средний чек(руб.)']
middle_avg_bill_region


# In[48]:


# Построим график
fig = px.bar(middle_avg_bill_region, y='Средний чек(руб.)', x= 'Район', color = 'Район') 
# оформляем график
fig.update_layout(title='Средний чек по всем округам',
                   xaxis_title='Район',
                   yaxis_title='Средний чек(руб.)',
                   width=800, # указываем размеры графика
                   height=500)
# добавляем ось X
fig.add_hline(y=750, line_dash="dash", line_color="grey")

fig.show()


# In[49]:


# создаём хороплет с помощью конструктора Choropleth и добавляем его на карту
Choropleth(
    geo_data=state_geo,
    data= middle_avg_bill_region,
    columns=['Район', 'Средний чек(руб.)'],
    key_on='feature.name',
    fill_color='YlOrBr',
    fill_opacity=0.8,
    legend_name='Средний чек по всем округам',
).add_to(m)

# выводим карту
m


# <span class="mark">**Наблюдение:**</span> 
# - средний чек по всем заведениям составил 750 р.;
# - высокий средний чек(1000руб.) оказался в таких округах, как ЦАО и ЗАО; 
# - экономный средний чек в округах ЮВАО (450р), ЮАО и СВАО(по 500р). 

# **Исследуем особенности заведений с плохими рейтингами, средние чеки в таких местах и распределение по категориям заведений.**

# In[51]:


# Сделаем срез заведений с рейтингом ниже 4 и будем считать их "плохими"
bad_rating = moscow_places.query('rating < 4')

# Посчитаем долю заведений с рейтингом ниже 4 балов
print('Всего заведений с рейтингом ниже 4 балов: {}, что составляет {:.1%} от всего количества заведений'      .format(len(bad_rating), (len(bad_rating)/sum_catering)))

# Найдем средний чек по "плохим" заведениям
print('Средний чек по "плохим" заведениям:', round(bad_rating['middle_avg_bill'].median(), 2))

# Распределим заведения по категориям
bad_rating_category =  bad_rating.groupby('category')[['rating', 'middle_avg_bill']].median().reset_index().                                  sort_values(by='middle_avg_bill', ascending = True)
bad_rating_category.columns = ['Категория заведения', 'Медианный рейтинг', 'Cредний чек(руб.)']

bad_rating_category


# In[52]:


# Посчитаем долю в каждой категории
bad_rating_category = bad_rating['category'].value_counts().to_frame()

# Определим долю каждой категории
bad_rating_category['share(%)'] = round((bad_rating_category['category']/len(bad_rating))*100,2)

bad_rating_category.style.bar(subset=['share(%)'], color='#d98095')


# <span class="mark">**Наблюдение:**</span>
# Проанализировав заведения с рейтингом ниже 4 балов, выявили следующее:
# - средний чек по "плохим" заведениям составил 400 р.;
# - всего "плохих" заведений 1169 или 13,% от всего количество;
# - минимальный средний чек в таких категориях, как столовая(275р.) и кофейня(300р.);
# - 46.5% доли составила категория "кафе".
# 

# <a name="result"></a>
# #### Соберите наблюдения по вопросам выше в один общий вывод

#    **`ВЫВОД`**: 
# <div style="border:solid orange 2px; padding: 20px"> 
#     
#     Изучив датасэт, в котором содержалось 8406 строк и 14 столбца,  нам позволило определить следующие особенности рынка 
#     заведений общепита в Москве:
#     
# <span class="mark">категориальный критерий</span>
# - в топ-3 вошли такие категории, как: кафе- 2378 (28,3%), ресторан- 2043 (24,3%) и кофейня- 1413 (16,8%);
# - в топ-3 категории по среднему кол-ву посадочных мест вошли: ресторан- 86 места, бар/паб- 82,5 мест, кофейня- 80 мест; 
# - по типу заведений 62% несетевых против 38% сетевые заведения;
#    - лидерами сетевых заведений оказались - кафе, ректораны и кофейни (пиццерии представляют чаще сетевые типы заведений);
#    - лидерами сетевых заведений стали кофейни( "Шоколадница") и пиццерии("Домино'с Пицца" и "Додо Пицца"). Кофейня "Шоколадница" значитально опережает остальные сетевые заведения;
#     
# <span class="mark">территориальный критерий</span>
# - в датасете присутствует 9 административных районов Москвы. Наиболее популярным по количеству заведения являемся ЦАО;
# - медианный рейтинг по всем заведениям 4.3. Практические все категории заведений в рамках среднего рейтинга, за исключением категорий "быстрое питание"(4.2) и "кафе"(4.2) Высокий рейтинг у ЦАО (4.4 балла), низкий рейтинг у СВАО и ЮВА по 4.2 баллов;
# - основной объем заведений расположен в рамках третьего транспортного кольца, меньше всего заведений на юге Москвы;
# - наибольшее количество объектов питания расположены на главных улицах города: проспект Мира, Профсоюзная улица и проспект Вернадского, с небольшим отрывом Ленинградский проспект.
#      По категориям заведения большая часть расположилась на:
#      - "кафе": проспект Мира;
#      - "кофейня": проспект Мира;
#      - "ресторан": проспект Мира;
#      - "пиццерия": проспект Мира;
#      - "бар/паб": Ленинградский проспект;
#      - "столовая": Варшавское шоссе;
#      - "булочная": Ленинградский проспект;
#      - "быстрое питание": проспект Мира.
# - всего улиц с 1 объектом общественного питания: 458, что составляет 31.6% от всего кол-ва улиц с объектами общественного питания (большая часть улиц расположена в ЦАО (возможно это связано с небольшими улицами) и ВАО).
#     
# <span class="mark">ценовой критерий</span>
# - средний чек по всем заведениям составил 750 р.;
# - высокий средний чек(1000руб.) оказался в таких округах, как ЦАО и ЗАО; 
# - экономный средний чек в округах ЮВАО (450р), ЮАО и СВАО(по 500р). 
# 
# Проанализировав заведения с рейтингом ниже 4 баллов, выявили следующее:
# - средний чек по "плохим" заведениям составил 400 р.;
# - всего "плохих" заведений 1169 или 13,% от всего количество;
# - минимальный средний чек в таких категориях, как столовая(275р.) и кофейня(300р.);
# - 46.5% доли составила категория "кафе".
# </div>

# <a name="num20"></a>
# ### Детализируем исследование: открытие кофейни

# Основателям фонда «Shut Up and Take My Money» не даёт покоя успех сериала «Друзья». Их мечта — открыть такую же крутую и доступную, как «Central Perk», кофейню в Москве. Будем считать, что заказчики не боятся конкуренции в этой сфере, ведь кофеен в больших городах уже достаточно. Попробуйте определить, осуществима ли мечта клиентов.

# <a name="num21"></a>
# #### Сколько всего кофеен в датасете? В каких районах их больше всего, каковы особенности их расположения?

# In[53]:


# Сделаем срез заведений с категорией "кофейня"

coffe_house_data = moscow_places[moscow_places['category'] == 'кофейня']

print('Всего кофеен в Москве:', len(coffe_house_data))

coffe_house_regions = coffe_house_data['district'].value_counts().to_frame()

coffe_house_regions


# Отобразим все кофейни на карте 

# In[54]:


# импортируем собственные иконки
from folium.features import CustomIcon
# moscow_lat - широта центра Москвы, moscow_lng - долгота центра Москвы
moscow_lat, moscow_lng = 55.751244, 37.618423

# moscow_lat - широта центра Москвы, moscow_lng - долгота центра Москвы
moscow_lat, moscow_lng = 55.751244, 37.618423

# создаём карту Москвы
m = Map(location=[moscow_lat, moscow_lng], zoom_start=10)
# создаём пустой кластер, добавляем его на карту
marker_cluster = MarkerCluster().add_to(m)

def create_clusters(row):
    # сохраняем URL-адрес изображения со значком coffe с icons8,
    # это путь к файлу на сервере icons8
    icon_url = 'https://img.icons8.com/external-flaticons-lineal-color-flat-icons/512/external-cofee-morning-flaticons-lineal-color-flat-icons.png'  
    # создаём объект с собственной иконкой размером 30x30
    icon = CustomIcon(icon_url, icon_size=(30, 30))
    
    # создаём маркер с иконкой icon и добавляем его в кластер
    Marker(
        [row['lat'], row['lng']],
        popup=f"{row['name']} {row['rating']}",
        icon=icon,
    ).add_to(marker_cluster)

# применяем функцию для создания кластеров к каждой строке датафрейма
coffe_house_data.apply(create_clusters, axis=1)

# выводим карту
m


# <a name="num21"></a>
# #### Есть ли круглосуточные кофейни?

# In[55]:


# добавим новый столбец и найдет только круглосуточные кофейни
coffe_house_data['24_hours'] = coffe_house_data['hours'].str.contains('круглосуточно', regex=True)
coffe_house_24_hours = coffe_house_data[coffe_house_data['24_hours'] == True]
coffe_house_24_7 = coffe_house_data[coffe_house_data['is_24/7'] == True]
print('Всего круглосуточных кофеен в Москве:', len(coffe_house_24_hours))
print('Всего круглосуточных и ежедневных кофеен в Москве:', len(coffe_house_24_7))


# **Отобразим на карте круглосуточные кофейни**

# In[56]:


# импортируем собственные иконки
from folium.features import CustomIcon
# moscow_lat - широта центра Москвы, moscow_lng - долгота центра Москвы
moscow_lat, moscow_lng = 55.751244, 37.618423

# moscow_lat - широта центра Москвы, moscow_lng - долгота центра Москвы
moscow_lat, moscow_lng = 55.751244, 37.618423

# создаём карту Москвы
m = Map(location=[moscow_lat, moscow_lng], zoom_start=10)
# создаём пустой кластер, добавляем его на карту
marker_cluster = MarkerCluster().add_to(m)

def create_clusters(row):
    # сохраняем URL-адрес изображения со значком coffe с icons8,
    # это путь к файлу на сервере icons8
    icon_url = 'https://img.icons8.com/external-flaticons-lineal-color-flat-icons/512/external-cofee-morning-flaticons-lineal-color-flat-icons.png'  
    # создаём объект с собственной иконкой размером 30x30
    icon = CustomIcon(icon_url, icon_size=(30, 30))
    
    # создаём маркер с иконкой icon и добавляем его в кластер
    Marker(
        [row['lat'], row['lng']],
        popup=f"{row['name']} {row['rating']}",
        icon=icon,
    ).add_to(marker_cluster)

# применяем функцию для создания кластеров к каждой строке датафрейма
coffe_house_24_hours.apply(create_clusters, axis=1)

# выводим карту
m


# <a name="num22"></a>
# #### Какие у кофеен рейтинги? Как они распределяются по районам?

# In[57]:


coffe_house_rating = coffe_house_data.groupby('district', as_index=False)['rating'].agg('mean')
coffe_house_rating = coffe_house_rating.sort_values(by='rating', ascending = False)
coffe_house_rating


# In[58]:


# Добавим "ящик с усами"
plt.figure(figsize=(10,5))

sns.boxplot(data=coffe_house_data, x='rating', y='district')
plt.title('Распределение рейтинга кофеин по районам')
plt.ylabel('')
plt.xlabel('Рейтинг')
plt.show()


# <span class="mark">**Наблюдение:**</span> Высокий рейтинг у ЦАО (4.3 балла), низкий рейтинг у ЗАО по 4.2 баллов.

# #### На какую стоимость чашки капучино стоит ориентироваться при открытии и почему?

# In[59]:


coffe_house_cost_cup = round(coffe_house_data['middle_coffee_cup'].mean(),2)
print('Средняя стоимость чашки капучино стоит:', coffe_house_cost_cup)


# #### Построим визуализации. Попробуем дать рекомендацию для открытия нового заведения. 
# 
# Это творческое задание: здесь нет правильного или неправильного ответа, но ваше решение должно быть чем-то обосновано. Объяснить свою рекомендацию можно текстом с описанием или маркерами на географической карте.

# ![](https://ic.pics.livejournal.com/newyorkrealty/58363224/39677/39677_original.jpg)
# 
# В связи с тем, что предположительно целевой аудиторией кофейни будут фанаты сериала "Друзья", а это в основном студенты от 18 до 25 лет, то выбирать стоит по следующим критериям:
# 
# <span class="mark">расположение:</span>
# - в рамках ТТК (возможно Пятницкая улица, Арбатская улица и пр.);
# - пешая доступность от метро;
# - с большим количеством конкурентов (да,да, данная ЦА любит передвигаться из одного места в другое, должно быть людно)
# 
# <span class="mark">график работы</span>
# - стоит рассмотреть возможность круглосуточной работы, тк всего в Москвке таких кофеен 76, а в пределах ТТК не более 20 (можно еще детально проанализировать каждую из этих кофеен, возможно там только придорожные)
# 
# <span class="mark">ценообразование</span>
# - стоимость чашки кофе не более 170 р.
# 
# 

# <a name="num23"></a>
# ### Подготовка презентации

# Подготовим презентацию исследования для инвесторов. Отвечая на вопросы о московском общепите, вы уже построили много диаграмм, и помещать каждую из них в презентацию не нужно. Выберите важные тезисы и наблюдения, которые могут заинтересовать заказчиков.
# Для создания презентации используйте любой удобный инструмент, но отправить презентацию нужно обязательно в формате PDF. Приложите ссылку на презентацию в markdown-ячейке в формате:
# 
# Презентация: [ссылка на облачное хранилище с презентацией](https://drive.google.com/file/d/1TFD03w3-u__eTNR_ju5lqNfZwP9N18KS/view?usp=share_link)
# 
# 