import matplotlib.pyplot as plt

x_values = list(range(1, 1001))
y_values = [x**2 for x in x_values]

# Style
plt.style.use('seaborn')
fig, my_plot = plt.subplots()

my_plot.scatter(x_values, y_values, c = 'green', s = 10)

my_plot.set_title('Square Numbers', fontsize=20)
my_plot.set_xlabel('Value', fontsize=14)
my_plot.set_ylabel('Square of Value', fontsize=14)


my_plot.axis([0, 1100, 0, 1100000])

my_plot.ticklabel_format(style='plain', axis='y')

plt.show()