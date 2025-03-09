import matplotlib.pyplot as plt
input_values = [1, 2, 3, 4, 5 ]
squares = [1, 4, 9, 16, 25 ]

x_values = [1, 2, 3, 4, 5 ]
y_values = [1, 4, 9, 16, 25 ]

# Style
plt.style.use('fivethirtyeight')

fig, random_name = plt.subplots()
random_name.plot(input_values, squares, linewidth=4)
# Scatter

random_name.scatter(3, 9, s = 200)
random_name.scatter(x_values, y_values, s = 200)
# s == size

# Назначение заголовка диаграммы и метос осей.
random_name.set_title('Square Numbers', fontsize=20)
random_name.set_xlabel('Value', fontsize=14)
random_name.set_ylabel('Square of Value', fontsize=14)

# Назначение размера шрифта делений на осях
random_name.tick_params(axis = "both", which = 'major', labelsize=14)

plt.show()