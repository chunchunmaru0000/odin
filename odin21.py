import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import datetime


df = pd.read_csv("Продажи.csv", encoding='windows-1251')

print('#Отображение первых нескольких строк данных для ознакомления')
print(df.head(), '\n\n')

# Проверку наличия пропущенных значений и их обработку, если необходимо
df.dropna(inplace=True)

print('#Описательную статистику для числовых переменных (сумма, среднее, минимум, максимум)')
print(f"---Количество статистика---\nсумма: {np.sum(df['Количество'])}\nсреднее: {np.mean(df['Количество'])}"
      f"\nминимальное: {np.min(df['Количество'])}\nмаксимальное: {np.max(df['Количество'])}")
print(f"---Цена статистика---\nсумма: {np.sum(df['Цена'])}\nсреднее: {np.mean(df['Цена'])}"
      f"\nминимальное: {np.min(df['Цена'])}\nмаксимальное: {np.max(df['Цена'])}")

# Преобразуйте столбец с датой в формат datetime
df['Дата'] = list(map(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'), df['Дата']))

# Создайте график временного ряда, отображающий изменение продаж в течение времени
plots = [plt.subplot2grid((5, 2), (0, 0), rowspan=2, colspan=2),
         plt.subplot2grid((5, 2), (3, 0), rowspan=2, colspan=2)]

plots[0].bar(df['Дата'], df['Количество'], color='r', label='Количество', linestyle="-")
plots[0].legend()
plots[0].set_title("изменение количества продаж в течение времени")
plots[0].grid(True)

plots[1].bar(df['Дата'], df['Цена'], color='g', label='Цена', linestyle="-")
plots[1].legend()
plots[1].set_title("изменение цен товара на штуку в течение времени")
plots[1].grid(True)

plt.show()

print('#Рассчитайте общую выручку')
print(sum(list(map(lambda x, y: x * y, df['Цена'], df['Количество']))))

print('#Определите самый популярный продукт или категорию продуктов')
products_and_prices = {}
for i in range(len(df['Продукт'])):
    if df['Продукт'][i] in products_and_prices.keys():
        products_and_prices[df['Продукт'][i]] += df['Количество'][i]
    else:
        products_and_prices[df['Продукт'][i]] = df['Количество'][i]
# print(products_and_prices)
popular = max(products_and_prices, key=products_and_prices.get)
print(popular)
print('#Рассчитайте средний чек')
print(sum(list(map(lambda x, y: x * y, df['Цена'], df['Количество']))) / len(df['Продукт']))

# Постройте графики для общей выручки
plots = [plt.subplot2grid((8, 2), (0, 0), rowspan=2, colspan=2),
         plt.subplot2grid((8, 2), (3, 0), rowspan=2, colspan=2),
         plt.subplot2grid((8, 2), (6, 0), rowspan=2, colspan=2)]

plots[0].bar(df['Дата'], list(map(lambda x, y: x * y, df['Цена'], df['Количество'])),
             color='r', label='общая выручка', linestyle="-")
plots[0].legend()
plots[0].set_title("Постройте графики для общей выручки")
plots[0].grid(True)


plots[1].bar(df[df['Продукт'] == popular]['Дата'], df[df['Продукт'] == popular]['Количество'],
             color='g', label='количество продаж', linestyle="-")
plots[1].legend()
plots[1].set_title("самого популярного продукта ")
plots[1].grid(True)

plots[2].bar(df['Дата'], list(map(lambda current_length:
                                  sum(list(map(lambda x, y: x * y,
                                               df.head(current_length)['Цена'], df.head(current_length)['Количество'])))
                                  / (current_length + 1), range(len(df['Дата'])))), color='b', linestyle="-")
# plots[2].bar(df['Дата'], list(map(lambda current_length: sum(list(map(lambda x, y: x * y, df.head(current_length)['Цена'], df.head(current_length)['Количество']))) / (current_length + 1), range(len(df['Дата'])))), color='b', linestyle="-")
plots[2].set_title("и среднего чека")
plots[2].grid(True)

plt.show()

# все графики получились столбцами, потому что все они распереляются по дням, а в одном дне по 5 продаж и из-за этого
# там по несколько точек в каждом столбце получается, так как продаж 25, а дней 5
# что бы это исправить пришлось бы это переделать в другие массивы длиной по 5 со средними значениями в день
# и я так изначально и делал используя это
'''
last_time = df['Дата'][0]
ammounts = [0]
prices = [0]
total_revenue = [0]
times = [df['Дата'][0]]
for i in range(len(df['Дата'])):
    if df['Дата'][i] == last_time:
        ammounts[-1] += df['Количество'][i]
        prices[-1] += df['Цена'][i]
        total_revenue[-1] += df['Количество'][i] * df['Цена'][i]
    else:
        last_time = df['Дата'][i]
        ammounts.append(df['Количество'][i])
        prices.append(df['Цена'][i])
        total_revenue.append(df['Количество'][i] * df['Цена'][i])
        times.append(df['Дата'][i])
'''
# получалось тоже самое но график был просто линиями, а так как задание по пандасу и плотлибу я оставил вариант,
# где графики построены на одном пандасе без лишних массивов
