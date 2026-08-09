# Объявление переменной
def format_text(text, width=70):
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        # Проверка, поместится ли слово в текущую строку
        if len(current_line) + len(word) + (1 if current_line else 0) <= width:
            if current_line:
                current_line += " " + word
            else:
                current_line = word
        else:
            # Начать новую строку
            lines.append(current_line)
            current_line = word

    # Добавить последнюю строку
    if current_line:
        lines.append(current_line)

    return "\n".join(lines)

# Пример текста
text = ( "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua." 
        "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat." 
        "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur."
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua." 
        "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat." 
        "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur." )

result = format_text(text)
print(result)
