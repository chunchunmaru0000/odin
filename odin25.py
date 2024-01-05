import matplotlib.pyplot as plt
import seaborn as sns


iris = sns.load_dataset('iris')
print('Загрузите набор данных iris с помощью Seaborn.Выведите первые несколько строк данных для осмотра.')
print(iris.head())

# Создайте гистограмму для визуализации распределения длины лепестков (petal_length).
species = list(set(iris['species']))

fig, axes = plt.subplots(1, 3, figsize=(15, 5))
for i in range(3):
    sns.histplot(x="petal_length", data=iris[iris['species'] == species[i]], ax=axes[i],
                 color=f'#{"00"*i}ff{"00"*(3-i)}'[:7])
    axes[i].set_xlabel('Длина лепестка')
    axes[i].set_ylabel('Колличество образцев')
    axes[i].set_title(f'Вид цветка: {species[i]}')

plt.show()

# Используйте ящиковую диаграмму (boxplot), чтобы сравнить распределение длины лепестков (petal_length)
# для разных видов ириса.
sns.boxplot(y='species', x='petal_length', data=iris)
plt.show()

# Постройте диаграмму рассеяния (scatterplot), чтобы исследовать взаимосвязь между длиной (petal_length)
# и шириной (petal_width) лепестков.
for i in range(3):
    sns.scatterplot(x="petal_length", y='petal_width', data=iris[iris['species'] == species[i]],
                    color=f'#{"00"*i}ff{"00"*(3-i)}'[:7], label=species[i])
plt.grid(True)
plt.show()
