#!/usr/bin/env python
# coding: utf-8

# <font size="5">
# <center><b>Оценка результатов A/B-теста, связанных с внедрением улучшенной рекомендательной системы в интернет-магазине</b></center>
# </font>

# # Описание данных и задачи
# 
# <span class="mark">**Постановка задачи**</span>
# 
# Ваша задача — провести оценку результатов A/B-теста. В вашем распоряжении есть датасет с действиями пользователей, техническое задание и несколько вспомогательных датасетов.
# 
# - Оцените корректность проведения теста
# - Проанализируйте результаты теста
# 
# Чтобы оценить корректность проведения теста, проверьте:
# 
# - пересечение тестовой аудитории с конкурирующим тестом,
# - совпадение теста и маркетинговых событий, другие проблемы временных границ теста.
# 
# <span class="mark">**Техническое задание**</span>
# 
# - Название теста: `recommender_system_test`;
# - группы: А — контрольная, B — новая платёжная воронка;
# - дата запуска: 2020-12-07;
# - дата остановки набора новых пользователей: 2020-12-21;
# - дата остановки: 2021-01-04;
# - аудитория: 15% новых пользователей из региона EU;
# - назначение теста: тестирование изменений, связанных с внедрением улучшенной рекомендательной системы;
# - ожидаемое количество участников теста: 6000.
# - ожидаемый эффект: за 14 дней с момента регистрации пользователи покажут улучшение каждой метрики не менее, чем на 10%:
#     - конверсии в просмотр карточек товаров — событие `product_page`,
#     - просмотры корзины — `product_cart`,
#     - покупки — `purchase`.
#     
# 
# <span class="mark">**Данные**</span>
# 
# [final_ab_events.csv](https://disk.yandex.ru/d/pgKgZ9lRp0Enwg)
# 
# [ab_project_marketing_events.csv](https://disk.yandex.ru/d/ZVC7GUYYckKnGQ)
# 
# [final_ab_new_users.csv](https://disk.yandex.ru/d/Qrto8Gerpu424g)
# 
# [final_ab_participants.csv](https://disk.yandex.ru/d/nhGUR3ZkNIG4VA)
# 
# <span class="mark">**Описание данных**</span>
# 
# `ab_project_marketing_events.csv` — календарь маркетинговых событий на 2020 год.
# 
# Структура файла:
# 
# - `name` — название маркетингового события;
# - `regions` — регионы, в которых будет проводиться рекламная кампания;
# - `start_dt` — дата начала кампании;
# - `finish_dt` — дата завершения кампании.
# 
# `final_ab_new_users.csv` — пользователи, зарегистрировавшиеся с 7 по 21 декабря 2020 года.
# 
# Структура файла:
# 
# - `user_id` — идентификатор пользователя;
# - `first_date` — дата регистрации;
# - `region` — регион пользователя;
# - `device` — устройство, с которого происходила регистрация.
# 
# `final_ab_events.csv` — действия новых пользователей в период с 7 декабря 2020 по 4 января 2021 года.
# 
# Структура файла:
# 
# - `user_id` — идентификатор пользователя;
# - `event_dt` — дата и время покупки;
# - `event_name` — тип события;
# - `details` — дополнительные данные о событии. Например, для покупок, `purchase,` в этом поле хранится стоимость покупки в долларах.
# 
# `final_ab_participants.csv` — таблица участников тестов.
# 
# Структура файла:
# 
# - `user_id` — идентификатор пользователя;
# - `ab_test` — название теста;
# - `group` — группа пользователя.
# 
# 
# 
# <span class="mark">**Оглавление**</span>
# 
# * [1. Изучение входных данных](#num1)
# * [2. Предобработка данных](#num2)
#     * [2.1. Проверка типов данных](#num4)
#     * [2.2. Проверим дубликаты и пропуски](#num5)     
# * [3. Анализ данных (EDA)](#num6)
#     * [3.1. Оценка корректности проведения теста](#num3)
#     * [3.2. Распределение количества событий на пользователя в выборках](#num7)
#     * [3.3. Распределение количество событий по дням](#num8)
#     * [3.4. Изменение конверсии воронки в выборках на разных эатапах ](#num9)
#     * [3.5. Особенности данных перед А/В-тестирование](#num10)    
# * [4. Оценка результатов А/В-тестирования](#num11)
#     * [4.1. Результаты А/В-тестирования](#num12)
#     * [4.2. Проверка статистической разницы долей z-критериев](#num13)
#         
# * [5. Общий вывод по этапу исследовательского анализа данных и по проведённой оценке результатов A/B-тестирования. Заключение о корректности проведения теста](#result) 
# 
# Примечание:
# - Оцените корректность проведения теста. Обратите внимание на:
#     - Соответствие данных требованиям технического задания. Проверьте корректность всех пунктов технического задания.
#     - Время проведения теста. Убедитесь, что оно не совпадает с маркетинговыми и другими активностями.
#     - Аудиторию теста. Удостоверьтесь, что нет пересечений с конкурирующим тестом и нет пользователей, участвующих в двух группах теста одновременно. Проверьте равномерность распределения по тестовым группам и правильность их формирования.
# 

# # Выполнение проекта

# <a name="num1"></a>
# ## Изучение входных данных

# In[1]:


# Загружаем библиотеки
import pandas as pd
from urllib.parse import urlencode
import requests
import numpy as np
import seaborn as sns
import datetime as dt
from scipy import stats as st
import math as mth
from datetime import date, datetime, timedelta
from matplotlib import pyplot as plt
from plotly import graph_objects as go
import plotly.express as px
import warnings
warnings.filterwarnings('ignore')


# ## Откроем файлы

# In[2]:


#Напишем функцию

def datasets (base_url, public_key):
    final_url = base_url + urlencode(dict(public_key=public_key))
    response = requests.get(final_url)
    download_url = response.json()['href']
    dataset = pd.read_csv(download_url)
    return dataset


# In[3]:


#Выведим данные таблицы final_ab_participants
base_url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?'
public_key = 'https://disk.yandex.ru/d/nhGUR3ZkNIG4VA' 

final_ab_participants  = datasets (base_url, public_key)
final_ab_participants


# In[4]:


#Выведим данные таблицы final_ab_events
base_url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?'
public_key = 'https://disk.yandex.ru/d/pgKgZ9lRp0Enwg'

final_ab_events  = datasets (base_url, public_key)
final_ab_events


# In[5]:


#Выведим данные таблицы ab_project_marketing_events
base_url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?'
public_key = 'https://disk.yandex.ru/d/ZVC7GUYYckKnGQ'

ab_project_marketing_events  = datasets (base_url, public_key)
ab_project_marketing_events


# In[6]:


#Выведим данные таблицы final_ab_new_users
base_url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?'
public_key = 'https://disk.yandex.ru/d/Qrto8Gerpu424g'

final_ab_new_users  = datasets (base_url, public_key)
final_ab_new_users


# In[7]:


# Выведим основную информацию о датафреймах с помощью метода `info()`,`head()`,`describe()`,`shape`
# с помощью цикла
for data in [final_ab_events, 
             ab_project_marketing_events, 
             final_ab_new_users, 
             final_ab_participants]:
    display(data.head(), 
            data.info(), 
            data.describe().T, 
            data.shape)
    display('****************************************************')


# <a name="num2"></a>
# ## Предобработка данных

# <a name="num4"></a>
# ### Проверка типов данных

# Изменим типы данных с датами на тип `datetime`

# In[8]:


final_ab_events['event_dt']= pd.to_datetime(final_ab_events['event_dt'], format = '%Y-%m-%d')
ab_project_marketing_events ['start_dt']= pd.to_datetime(ab_project_marketing_events ['start_dt'], format = '%Y-%m-%d')
ab_project_marketing_events ['finish_dt']= pd.to_datetime(ab_project_marketing_events ['finish_dt'], format = '%Y-%m-%d')
final_ab_new_users['first_date']= pd.to_datetime(final_ab_new_users['first_date'], format = '%Y-%m-%d')


# Проверим изменения

# In[9]:


for data in [final_ab_events, 
             ab_project_marketing_events, 
             final_ab_new_users]:
    display(data.info())
    display('****************************************************')


# <a name="num5"></a>
# ### Проверим дубликаты и пропуски

# In[10]:


for data in [final_ab_events, 
             ab_project_marketing_events, 
             final_ab_new_users,
            final_ab_participants]:
    display(data.duplicated().sum(), data.isna().sum())
    display('****************************************************')


# Проверим датафрейм `final_ab_events`, где обаружены пропуски

# In[11]:


display(final_ab_events['details'].value_counts())
display(final_ab_events['event_name'].value_counts())


# <span class="mark">**Наблюдение:**</span> Столбец `delails`содержит 377 577 пропусков, заполним их пропусками, тк это доп данные по событию `purchase`.

# In[12]:


final_ab_events['details'] = final_ab_events['details'].fillna(0)


# In[13]:


# Проверим
final_ab_events.isna().sum()


# <a name="num6"></a>
# ## Анализ данных (EDA)
# 

# <span class="mark">**Техническое задание**</span>
# 
# - Название теста: `recommender_system_test`;
# - группы: А — контрольная, B — новая платёжная воронка;
# - дата запуска: 2020-12-07;
# - дата остановки набора новых пользователей: 2020-12-21;
# - дата остановки: 2021-01-04;
# - аудитория: 15% новых пользователей из региона EU;
# - назначение теста: тестирование изменений, связанных с внедрением улучшенной рекомендательной системы;
# - ожидаемое количество участников теста: 6000.
# - ожидаемый эффект: за 14 дней с момента регистрации пользователи покажут улучшение каждой метрики не менее, чем на 10%:
#     - конверсии в просмотр карточек товаров — событие `product_page`,
#     - просмотры корзины — `product_cart`,
#     - покупки — `purchase`.
#     
# `Во времея проведения EDA нам нужно ответить на следующие вопросы:`
# * Одинаково ли распределено количество событий на каждого пользователя в выборке?
# * Как распределено количество событий по дням?
# * Встречаются ли в разных выборках одни и теже пользователи?
# * Как меняется корверсия в воронке на разных этапах?
# * Что нужно учесть перед началом А/В- тестирования?

# <a name="num3"></a>
# ### Оценка корректности проведения теста

# **Проверим, что время проведения теста не совпадает с маркетинговыми и другими активностями из таблицы `ab_project_marketing_events`**

# In[14]:


ab_project_marketing_events[np.logical_and(ab_project_marketing_events['start_dt'] > '2020-12-07',                                            ab_project_marketing_events['finish_dt'] < '2021-04-01')]


# <span class="mark">**Наблюдение:**</span>  В период проведения теста проводились маркетинговые активности Christmas&New Year Promo и CIS New Year Gift Lottery .

# In[15]:


#Посмотрим распределение пользователей по тестам и по группам
final_ab_participants.groupby(['ab_test', 'group']).agg({'user_id': 'nunique'}).reset_index()


# В тесте recommender_system_test имееется две группы. В группу А попали 3824 пользователя, а в группу В 2877.

# In[16]:


#проверим соответствие дат регистрации техническому заданию
print('Минимальная дата:',  final_ab_new_users['first_date'].min())
print('Максимальная дата:', final_ab_new_users['first_date'].max())


# В ТЗ указано, что дата остановки набора новых пользователей: 2020-12-21. А в наших данных, как мы видим, есть регистрации и 23.12.2020. Удалим лишние записи.

# In[17]:


# Создадим датафрэйм только у теми пользователеми, которые были зарегистрованы на тест в это промежуток

final_ab_new_users = final_ab_new_users.query ('first_date <="2020-12-21"')
final_ab_new_users['first_date'].max()


# **Дата остановки теста: 2021-01-04, согласно ТЗ. Проверим на корректность даты в таблице с событиями**

# In[18]:


print('Минимальная дата:',  final_ab_events['event_dt'].min())
print('Максимальная дата:',  final_ab_events['event_dt'].max())


# Последняя дата событий в данных 30 декабря. Хотя тест должен был продолжаться до 4 января. Возможно тест завершили раньше.

# Пользователи, зарегистрировавшиеся после 16 декабря не "прошли" весь лайфтайм в 14 дней, и не в полной мере показали как внесенные изменения повлияли на их активность. Это может сильно исказить результаты тестирования.

# In[19]:


print('Количество новых пользователей', final_ab_new_users['first_date'].count())
print('Количество пользователей, участвующих в тесте', final_ab_participants['user_id'].nunique())


# **Посмотрим количество аудитории: 15% новых пользователей из региона EU по датафрейму, где только с период с 07 по 21.12.2020**

# In[20]:


# Объеденим таблицы методом merge по user_id
users = final_ab_participants.merge(final_ab_new_users, on = 'user_id', how = 'left').dropna()
users.shape


# In[21]:


print('Пользователи из Европы, принявшие участие в тесте',      len(users.query('ab_test == "recommender_system_test" and region == "EU"')))
print('Всего зарегистрировалось пользователей из Европы',len(final_ab_new_users.query('region == "EU"')))
print('Процент пользователей из Европы, принявших участие в тесте', len(users.query('ab_test == "recommender_system_test" and region == "EU"'))      /len(final_ab_new_users.query('region == "EU"'))*100)


# Данные соответствуют ТЗ, тк доля пользователей из Европы 15%

# **Проверим правильность распределения участников теста**

# Согласно таблице `final_ab_participants` параллельно проводилось два теста, наша задача исключить задвоение участников, которые были в двух тестах.

# In[22]:


# Сгруппируем данные по пользователю и группе

dupl_user = users.groupby('user_id', as_index=False).agg({'ab_test': 'nunique'})
#dupl_user.columns = ['user_id', 'group', 'count']
# Сделаем сред по количеству 
dupl_user = dupl_user.query('ab_test > 1').sort_values(by='user_id')
print('Количество пользователей, которые участвовали в двух тестах {} или {:.1%}'
      .format(dupl_user['user_id'].count(), dupl_user['user_id'].count()/final_ab_participants['user_id'].count()))


# In[23]:


dupl_user.head(3)


# In[24]:


# Перепроверим любого пользователя на участие в друх выборках
display(final_ab_participants.query('user_id == "001064FEAAB631A1"'))
display(final_ab_participants.query('user_id == "003B6786B4FF5B03"'))


# Пользователей, принявших участие в двух тестах одновременно 1602 или 8,8%. Для чистоты эксперемента необходимо удалить этих пользователей, так как при дальнейшем анализе они могут исказить конечный результат. Ведь мы точно не можем сказать, какой из экспериментов повлиял на принятие того или иного решения пользователя.

# In[25]:


print('Всего пользователей БЫЛО', users['user_id'].nunique())

print(users.groupby('ab_test').agg({'user_id': 'nunique'}))


# In[26]:


#удаляем дубликаты
list = dupl_user['user_id']
users = users.query('user_id not in @list')


# In[27]:


print('Всего пользователей СТАЛО', users['user_id'].nunique())

print(users.groupby('ab_test').agg({'user_id': 'nunique'}))


# В итоге после удаления у нас осталось всего 14062 уникальных пользователя, из которых 5099 попали в recommender_system_test. Для дальнейшей работы выделим данные по тесту recommender_system_test в отдельный датафрейм и проверим на пересечение пользователей в группах.

# In[28]:


#оставляем данные о тесте recommender_system_test
recommender_system_test = users.query('ab_test == "recommender_system_test"')
recommender_system_test['ab_test'].unique()
recommender_system_test.sample(5)


# In[29]:


#смотрим распределение по группам
recommender_system_test.groupby('group').agg({'user_id': 'nunique'}).reset_index()


# In[30]:


# Сгруппируем данные по пользователю и группе

dupl_group = recommender_system_test.groupby('user_id', as_index=False).agg({'ab_test': 'nunique'}).reset_index()
dupl_group.columns = ['user_id', 'group', 'count']
# Сделаем сред по количеству 
dupl_group = dupl_group.query('count > 1').sort_values(by='user_id')
print('Количество пользователей, которые участвовали в двух группах {} или {:.1%}'
      .format(dupl_group['user_id'].count(), dupl_group['user_id'].count()/final_ab_participants['user_id'].count()))


# Пересечений пользователей по группам нет.

# **Посмотрим равномерное распределение по группам**

# In[31]:


recommender_system_test['group'].value_counts()


# Группы распределены не одинаково. В группе А присутствует 2903 пользователей (57%), а в группе В - 2196 пользователей (43%)

# **Посмотрим на горизонт проведения теста в 14 дней и удалим не нужное**

# Согласно нашему ТЗ наш тест происходил в промежуток с **2020-12-07 по 2020-12-21**, присоеденим данные о событиях пользователей к имеющемуся тесту

# In[32]:


#присоединяем события
user_event = recommender_system_test.merge(final_ab_events, on = 'user_id', how = 'left')
display(user_event.head(), user_event.info())


# In[33]:


#удалим пользователей без событий, они нам без надобности
df_AB_testing = user_event.dropna(subset = ['event_name'])
len(user_event)


# In[34]:


# удаляем события, совершенные после лайфтайма
df_AB_testing = (df_AB_testing.drop(df_AB_testing[df_AB_testing['event_dt'] >= (df_AB_testing['first_date'] + pd.Timedelta(14, 'D'))].index))
df_AB_testing.shape


# После того,  как мы нашли участников тестирования и зарегистрированных участников в нужный промежуток времени, мы объединили таблицы, удалили пользователей без событий и удалили события, которые не вошли в указанный промежуток.
# 
# Можно приступить к основному анализу данных.

# <a name="num7"></a>
# ### Распределение количества событий на пользователя в выборках

# Посмотрим, сколько уникальных пользователей входит в каждую группу.

# In[35]:


AB_testing_unique_users = df_AB_testing.groupby('group')['user_id'].agg(['count']).reset_index()
AB_testing_unique_users['%'] = ((AB_testing_unique_users['count']/AB_testing_unique_users['count'].sum())*100).round(1)
AB_testing_unique_users.sort_values(by='%', ascending=False)
AB_testing_unique_users.style.bar(subset=['%'], color='#ffe135')


# Посмотрим на гистограмме распределение количества событий на одного пользователя в каждой группе

# In[36]:


# Сгруппируем данные
events_users_count = df_AB_testing.groupby(['user_id', 'group'], as_index=False).agg({'event_name' : 'count'})
events_users_count.columns = ['user_id', 'group', 'events']


# In[37]:


events_users_count.query('group == ["A","B"] & events > 0')                                .groupby('group')['events']                                .plot(kind='hist', bins=len(events_users_count['events'].unique()), alpha=0.5,                                      figsize=(15,8))
plt.legend(['"группа "А"','"группа "B"'])
plt.xlabel('Количество событий')
plt.ylabel('Количество пользователей')
plt.title('Гистограмма распределения количества событий на одного пользователя')
plt.show()


# Посмотрим, как происходило распределение событий на одного пользователя в выборках

# In[38]:


print('В среднем на пользователя приходится %d событий' % (df_AB_testing['user_id'].value_counts().mean()))
print('По медиане на пользователя приходится %d событий' % (df_AB_testing['user_id'].value_counts().median()))
print('По моде на пользователя приходится %d событий' % (df_AB_testing['user_id'].value_counts().mode()))


# В группе В на одного пользователя чаще всего приходится от 1 до 6 событий. В группе А чаще совершают событий от 2 до 12.

# In[39]:


#смотрим описательную статистику распределения событий в группе А
df_AB_testing.query('group == "A"').groupby('user_id')['event_name'].count().describe()


# In[40]:


#смотрим описательную статистику распределения событий в группе B
df_AB_testing.query('group == "B"').groupby('user_id')['event_name'].count().describe()


# In[41]:


#распределение количества участников по группам
df_AB_testing.groupby('group')['user_id'].nunique()


# **`ВЫВОД`**: 
# <div style="border:solid orange 2px; padding: 20px"> 
# 
# После изучения данных, предобработки данных, соединение полученных таблиц в единую таблицу `df_AB_testing` мы видим следующее:
#     
# В группе А на одного пользователя в среднем приходится 7 событий. В группе В пользователь совершает в среднем 5 событий.
# 
# **<font color="maroon">Разница в среднем количестве событий между группами может быть обусловленна:
# <br>- неравномерным распределением количества пользователей по группам
# <br>- на активность пользователей из группы В могли повлиять внесенные изменения в рамках теста
# </font>**
# </div>

# <a name="num8"></a>
# ### Распределение количество событий по дням

# Посчитаем, как число событий распределено по дням. Сгруппируем таблицу `df_AB_testing` по дню события и группе A/B-теста, посчитаем количество пользователей. Сохраним результат в переменную `df_AB_testing_daily`.

# In[42]:


# Добавим в датафрэйм столбец с датой
df_AB_testing['event_day'] = df_AB_testing['event_dt'].dt.date
df_AB_testing.sample(5)


# In[43]:


# Посчитаем кол-во событий по дням
df_AB_testing['event_day'].value_counts()


# In[44]:


df_AB_testing_daily = df_AB_testing.groupby(['event_day', 'group'])                                   .agg({'event_name':'count'})                                   .reset_index()
df_AB_testing_daily.head(30)


# In[45]:


# Построим график

fig = px.bar(df_AB_testing_daily, x="event_day", y= 'event_name', color="group", title="Распределение событий по группам в разрезе дней",             #text_auto=True, 
             pattern_shape_sequence=["+"],\
             labels= {'event_day': 'Дата', 'event_name': 'Количество событий'},
             width=1000, # указываем размеры графика
             height=500)

fig.show()


# <span class="mark">**Наблюдение:**</span> Основная активность двух групп в разрезе событий пришлась на **21 декабря 2020 года**. В этот день обе группы имеют максимальные значения. 

# Посмотрим отдельно распределение каждого события в каждой группе по дням

# In[46]:


# Сделаем срез по группам

group_A = df_AB_testing.query('group == "A"')
group_B = df_AB_testing.query('group == "B"')


# In[47]:


# Сгруппируем события группы "А" по дням 
group_A.pivot_table(index='event_day', values='user_id',columns='event_name',aggfunc='count')       .plot.bar(stacked=True,figsize=(12,6))
plt.title("Группа A")
plt.show()


# In[48]:


# Сгруппируем события группы "B" по дням
group_B.pivot_table(index='event_day', values='user_id',columns='event_name',aggfunc='count')       .plot.bar(stacked=True,figsize=(12,6))
plt.title("Группа B")
plt.show()


# **`ВЫВОД`**: 
# <div style="border:solid orange 2px; padding: 20px"> 
# 
# В группе А рост активности начинается с 14 декабря. Пик активности приходится на 21 декабря, в этот день было совершено около 1400 событий. Затем активность идёт на спад. В группе В таких резких всплесков не наблюдается, там события распределны более равномерно. Самое большое число событий в этой группе так же пришлось на 21 декабря и достигало 300 событий.
# 
# **<font color="brown"> Резкое увеличение событий в группе А 14.12.20 вызвано большим количеством новых регистрации в это день. На графике количества регистраций по дням, мы видели пик наплыва новых пользователей в этот день - почти 300 человек.
# </font>**
# </div>

# <a name="num9"></a>
# ### Изменение конверсии воронки в выборках на разных этапах

# **Этапы воронки продаж**
# 
# `1. Login` - пользователь входит на сайт;\
# `2. Product_page` - предложение о товаре (экран с товаром);\
# `3. Product_card` - переход в корзину;\
# `4. Purshase` - экран успешной оплаты заказа.\
# Этапы `Product_card` и `Purshase` имеют разное количество заходов пользователей, причем покупок больще чем переходов в корзину. Следовательно покупки совершаются по одному товару миную корзину. Надо расставить события в нужный порядок.

# Посчитаем общее количество событий по всем этапам

# In[49]:


# Сгруппируем данные по событиям
steps = df_AB_testing.groupby('event_name').agg({'event_name': ['count'], 'user_id': ['nunique'] }).reset_index()
steps.columns = ('event_name', "count", 'users')

# добавим столбец с конверсией
start= steps.loc[0,'users']
steps['Конверсия'] = round(steps['users']/start*100, 1)
# Посчитаем конверсию от этапа к этапу
steps['Конверсия в шаг %'] = round(steps['users']/steps['users'].shift()*100, 1)
#добавим вручную первое значение stage_conversion
steps.loc[0, 'Конверсия в шаг %'] = round(steps.loc[0,'users']/start*100, 1)
steps = steps.sort_values(by='count', ascending=False)
steps


# In[50]:


#построим воронку с процентом перехода на каждый этап относительно начального 
fig = go.Figure(go.Funnel(
    x = steps['count'], 
    y = steps['event_name'],
    textinfo = "value+percent previous+percent initial"))
fig.update_layout(title='Этапы воронки продаж', title_x = 0.55)
fig.show();


# <span class="mark">**Наблюдение:**</span>
# 
# По итогам анализа воронки продаж было выявлено следующее:
# 
# - Конверсия (расчет с первого шага):
# 
#      - зарегистрованных пользователей мы взяли за **100%**
#         - предложение о товара **63%** пользователей
#             - перешли в корзину **29,6%**
#               - оплата заказа **30,5%** 
#                               
# 
# * При переходе с первого этапа на второй теряется 37.3% пользователей. Переходит 62.7% пользователей.
# * При переходе со второго этапа на третий теряется 53.1% пользователей. Переходит 46.9% пользователей.
# * При переходе с третьего на четвертый этап увеличивается количество на 4.5% пользователей. Дошло до оплаты 51.4% пользователей.

# Создадим сводную таблицу `conver_group`, сгруппируем данные по группам A/B-теста, в качестве столбцов — названия события, посчитаем количество пользователей и выведем на экран.

# In[51]:


conver_group = df_AB_testing.pivot_table(index='event_name', columns='group', values='user_id', aggfunc='nunique').reset_index()
conver_group= conver_group.replace({'event_name':{'login':'1_регистрация', 'product_page':'2_просмотр карточек товара',                                                     'product_cart':'3_просмотр корзины','purchase':'4_покупка'}})
conver_group = conver_group.sort_values(by='event_name')
conver_group


# Посмотрим изменение воронки продаж по каждой группе

# In[52]:


funnel_A = (group_A.groupby('event_name')['user_id'].nunique().sort_values(ascending=False).to_frame().reset_index()
              .rename(columns={'user_id': 'total_users'}))
funnel_A['step'] = pd.Series([0, 1, 3, 2])
funnel_A = funnel_A.sort_values(by='step', ascending=True)


funnel_B = (group_B.groupby('event_name')['user_id'].nunique().sort_values(ascending=False).to_frame().reset_index()
              .rename(columns={'user_id': 'total_users'}))
funnel_B['step'] = pd.Series([0, 1, 3, 2])
funnel_B = funnel_B.sort_values(by='step', ascending=True)
funnel_B


# In[53]:


#Построим Stacked Funnel Plot with go.Funnel

fig = go.Figure()
fig.add_trace(go.Funnel(
    name = 'group_A',
    y = funnel_A['event_name'],
    x = funnel_A['total_users'],
    textinfo = "value+percent initial"))
fig.update_layout(title='Воронка продаж группы "А" и группы "В"', title_x = 0.55)

fig.add_trace(go.Funnel(
    name = 'group_B',
    orientation = "h",
    y = funnel_B['event_name'],
    x = funnel_B['total_users'],
    textposition = "inside",
    textinfo = "value+percent initial"))

fig.show()


# <span class="mark">**Наблюдение:**</span>  
# 
# По графику видно, что в группе А конверсия по этапам чуть лучше, чем в группе В. После авторизации в группе А лишь 31% доходит до покупок, в группе В - 28%. Больше всего пользователей отваливается на этапе просмотра карточек товара, к следующему этапу  переходит не более 50%. Показатель прехода от 3 этапа к 4 очень позитивный - после просмотра корзины все пользователи переходят к покупкам. Можно заметить,что на 4 этапе в обеих группах процент пользователей больше, чем на предыдущем этапе. Это может говорить о том, что на платформе нестрогая воронка продаж и можно приобрести продукт минуя некоторые этапы.  
# Согласно ТЗ, Ожидаемый эффект: за 14 дней с момента регистрации в системе пользователи покажут улучшение каждой метрики не менее, чем на 10%. Что же мы имеем по факту:  
# - Процент перехода от первого этапа ко второму в контрольной группе составил 65%, в эксперементальной - 56%. Разница в 18% с отрицательных покаазателем.
# - Процент перехода от второго этапа к третьему в контрольной группе 46%, в эксперементальной 49%. Тут динамика положительна, увеличение на 3%
# - Процент перехода с третьего этапа к покупке составил 103% в контрольной и 101% в эксперементальной группах.  
# 
# Как мы видим, ожидаемый эффект не оправдался.

# <a name="num10"></a>
# ### Особенности данных перед А/В-тестирование

# Перед А/В тестом проводят A/A-тест. Если трафик и инструмент проведения A/A-теста не подвели, различий в показателях не будет и поможет определить длительность теста и методику анализа данных.
# Критерии успешного A/A-теста:
# 
# - если деление трафика, не более чем на 1% отличается
# 
# *Итого: Контрольная группа почти в 3 раза превышает эксперементальную.*
# 
# - достаточное количество участников в выборке
# 
# *Итого: Согласно ТЗ, предполагалась, что аудитория теста будет сотоять из 15% новых пользователей региона EU. По факту же, в эксперимент попали пользователи из других регионов, пусть и в незначительном количестве, но это тоже может исказить результат эксперимента.*
# 
# - различие ключевых метрик по группам не превышает 1% и не имеет статистической значимости;
# - выброны корректные промежутки времени проведения теста без параллельного вмешательства других активностей в период проведения теста.
# 
# *Итого: Изначально предполагалось, что дата окончания эксперимента 2021-01-04. Но по событиям пользователей мы видим, что фактически эксперемент заканчивается 29 декабря- последняя дата наблюдаемой активности пользователей. Время проведения эксперимента выбрано неудачно, так как это новогодние праздники и предновогодняя суета могла повлиять на активность пользователей в этот период.
# На время проведения теста накладывается маркетинговая кампания, проводимая с 25 декабря*
# 
# Перед тем как начать A/B-тест, нужно убедиться, что:
# 
# - на результаты не влияют аномалии и выбросы в генеральной совокупности;
# - что в тесте неслишком большое количество групп, что чаще приводит к ложнопозитивному результату;
# - измеритель качества «деления» трафика подтвердил однородность трафика и работает корректно.

# <a name="num11"></a>
# ## Оценка результатов А/В-тестирования

# <a name="num12"></a>
# ### Результаты А/В-тестирования

# Перед началом проведения А/В теста вероятно всего не проводился А/А тест для оценки корректного времени и необходимого количества данных. К сожалению, в данном примере мы столкнулись с проблемой некорректного деления трафика теста, те пользователи были распределены меджу группами неравномерно, что привело к искажению результатов.

# <a name="num13"></a>
# ### Проверка статистической разницы долей z-критериев

# **1. Проверим по группам**

# Проверим гипотезу о равенстве долей при помощи Z-критерия. Для этого напишем функцию.
# 
# Посчитаем статистическую значимость различия между группами.

# <span class="girk">Формулировка гипотез:</span>
# 
# * `Нулевая гипотеза(H_0)`: группа "А" = группа "В" - **одинаковые**
# * `Альтернативная гипотеза (H_a)`: группа "А" = группа "В" -" **разные**
# 
# alpha = 0.05 - выберим данный уровень значимости (вероятный порог "необычности")

# In[54]:


user_event = df_AB_testing.pivot_table(index = 'group', columns = 'event_name', values = 'user_id',
                                       aggfunc = 'nunique').reset_index()
user_events = user_event.set_index(user_event.columns[0])
user_events 


# In[55]:


# Напишем функцию

def st_test(pA_ev, pB_ev, pA_us, pB_us): 
    # пропорция успехов в первой группе:
    pA = pA_ev / pA_us
    # пропорция успехов во второй группе:
    pB = pB_ev / pB_us 
    # пропорция успехов в комбинированном датасете:
    p_combined = (pA_ev + pB_ev) / (pA_us + pB_us)
    # разница пропорций в датасетах
    difference = pA - pB
    z_value = difference / mth.sqrt(p_combined * (1 - p_combined) * (1 / pA_us + 1 / pB_us))
    # задаем стандартное нормальное распределение (среднее 0, ст.отклонение 1)
    distr = st.norm(0, 1)
    p_value = (1 - distr.cdf(abs(z_value))) * 2

    return p_value


# In[56]:


# Укажем значения по группам А и В в p-value
p_value = st_test(2082, 705, user_events.loc['A'].sum(), user_events.loc['B'].sum())
print('p-значение: ',"{0:.3f}".format(p_value))

alpha = .05 
if (p_value < alpha):
    print("Отвергаем нулевую гипотезу: между долями есть значимая разница")
else:
    print("Не получилось отвергнуть нулевую гипотезу, нет оснований считать доли разными")


# <span class="mark">**Наблюдение:**</span>

# Получив крайне маленькое значение p-value, мы отвергли Нулевую гипотезу. Таким образом, у нас практически нет вероятности получить одинаковые доли групп "А" и "В".

# **2. Проверим по каждому событию**

# In[57]:


total_users = df_AB_testing.groupby('group')['user_id'].nunique()
total_users


# Событие login совершили все пользователи каждой группы, поэтому проводить сравнение на данном этапе бессмыслено. Удалим эту строку из таблицы.

# In[58]:


conver_group = conver_group.drop(0, 0).reset_index(drop=True)
conver_group


# При написании функции применим поправку Бонферрони, чтобы смягчить увеличение вероятности совершения ошибки 1-го рода при многократной проверке

# In[59]:


#напишем функцию для проведения А/В теста. В качестве аргумента функции будем передовать названия сравниваемых групп
def stat_test(group1, group2):
    for i in conver_group.index:
        alpha = .05/len(conver_group) # критический уровень статистической значимости c поправкой Бонферрони


        successes = np.array([conver_group[group1][i],conver_group[group2][i]])
        trials = np.array([total_users[group1], total_users[group2]])

# пропорция успехов в первой группе:
        p1 = successes[0]/trials[0]

# пропорция успехов во второй группе:
        p2 = successes[1]/trials[1]

# пропорция успехов в комбинированном датасете:
        p_combined = (successes[0] + successes[1]) / (trials[0] + trials[1])

# разница пропорций в датасетах
        difference = p1 - p2 

# считаем статистику в ст.отклонениях стандартного нормального распределения
        z_value = difference / mth.sqrt(p_combined * (1 - p_combined) * (1/trials[0] + 1/trials[1]))

# задаем стандартное нормальное распределение (среднее 0, ст.отклонение 1)
        distr = st.norm(0, 1)  

        p_value = (1 - distr.cdf(abs(z_value))) * 2
        print('Событие: ', conver_group['event_name'][i])
        print('p-значение: ', p_value)

        if p_value < alpha:
            print('Отвергаем нулевую гипотезу: между долями есть значимая разница')
            print()
        else:
            print('Не получилось отвергнуть нулевую гипотезу, нет оснований считать доли разными')
            print()


# In[60]:


stat_test('A', 'B')


# <span class="mark">**Наблюдение:**</span>
# 
# По результатам А/В теста значимая разница между группами прослеживается только на этапе просмотра карточек товара. А вот что касается перехода в корзину и покупки товара, то тут значимой разницы не наблюдается. Нет оснований считать, что есть разница в конверсии между контрольной и экспериментальной группой после внедрения новшеств на сайте.

# <a name="result"></a>
# ## Общий вывод по этапу исследовательского анализа данных и по проведённой оценке результатов A/B-тестирования. Заключение о корректности проведения теста

# **`ВЫВОД`**: 
# <div style="border:solid orange 2px; padding: 20px"> 
#           
#  После того, как изучили датасеты, выявили следующее:
#  
#  <span class="girk">на этапе изучения данных</span>   
#     
# * Типы данных в датах были изменены.
# * Дубликатов не было.
# * Пустые значения в столбце `details` были заменены на нули.
# * После проведения среза по виду теста и периоду проведения было обнаружено 1602 человека или 8,8%, которые учавствовали в двух выборках.
# * Количесво строк таблицы: 24698, данные после обработки уменьшилось на 5.61%
# Количество уникальных участников тестирования: 3675, данные после обработки уменьшилось на 61.25% 
# * Внутри исследуемого теста пересечений пользоветеле между группами не выявлено    * На одного пользователя приходилось в среднем 6 событий и распределение событий в каждой группе на каждого пользователя одинаковое (группа А-7 событий, группа В- 5 событий).
# * Активность пользователей на сайте прекращается после 30.12, хотя тест продолжался до 4 января.
# * В группе А рост активности начинается с 14 декабря. Пик активности приходится на 21 декабря, далее идут спад. В группе В таких резких всплесков не наблюдается, там события распределны равномерно с начала эксперимента до 21 декабря. Далее тоже наблюдается спад активности.
# 
# <span class="girk">на этапе изучения воронки</span>    
# 
# * События распределились следующим образом:
# 1.login - авторизация на сайте магазина
# 2.product_page - просмотр карточек товаров
# 3.product_cart - переход в корзину
# 4.purchase - покупка товара
# * Процент перехода от первого этапа ко второму в контрольной группе составил 65%, в эксперементальной - 56%. Разница в 18% с отрицательных покаазателем.
# * Процент перехода от второго этапа к третьему в контрольной группе 46%, в эксперементальной 49%. Тут динамика положительна, увеличение на 3%
# * Процент перехода с третьего этапа к покупке составил 103% в контрольной и 101% в эксперементальной группах.
# * По результатам заметно, что некоторые пользователи делают заказ, минуя шаг "просмотр корзины". Вероятнее всего, на сайте можно купить товар сразу, не добавляя его в корзину.
# 
# <span class="girk">в ходе проведения А/В тестирования </span> 
# * Выявлено значительное расхождение между двумы группами
# * Разницы в поведении между контрольными и эксперементальной группой на этапе перехода в корзину и покупки товара не выявлено. Внедренные изменения никак не повляли на поведение пользователей.
# * Cтоит обратить внимание на особенности в данных, которые могли негативно повлиять на результат проводимого теста:
# 1. Контрольная группа почти в 3 раза превышает эксперементальную.
# 2. В эксперимент попали пользователи из других регионов, участие которых не предполагалось в данном тестировании
# 3. Фактически, эксперимент закончился раньше, чем предпологалось изначально
# 4. Во время проведения эксперимента проводилась маркетинговая кампания, которая могла повлиять на активность пользователей.
#     
# <span class="pirk">Рекомендация:</span> Стоит не принимать результаты А/В тестирования, тк они искажены.Предлагаю провести тест повторно в период, не захватывающий праздники, и не влиящий на поведение пользователей.
# 
# 
#     
# </div>