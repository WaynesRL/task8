# Импорт библиотеки json
import json

# Переменная inData
inData = '{"one": ["http", "yandex.ru"], "two": ["https", "google.com"]}'

# Парсинг JSON, возвращает объект Python (словарь)
outData = json.loads(inData)

print (f"one: {outData['one']}")
print (f"two: {outData['two']}")