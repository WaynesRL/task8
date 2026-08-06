# Импорт pandas
import pandas as pd

# Объявить d1 и d2
d1 = {'a': [1, 2, 3], 'b': [None, 5, 6], 'c': [7, None, 9]}
d2 = {'b': [4, 89, 87], 'c': [54, 8, 35], 'd': [10, 11, 12]}

# Объявить dataframe
df1 = pd.DataFrame(d1)
df2 = pd.DataFrame(d2)

# Можно вывести dataframe, но по заданию необязательно
# print(df1)
# print(df2)

# Объявить dataframe 3, заполнить df1 значениями из df2, перевести в int
df3 = df1.fillna(df2).astype(int)

# Вывести df3
print(df3)
