def calculate_result(s1, s2):
    if s1 <= 4 and s2 <= 4:
        return 1  # Низкая вероятность"
    if s1 >= 8 and s2 >= 8:
        return 2  # Смешанный
    if s1 >= 8:
        return 3  # Гиперактивный
    if s2 >= 8:
        return 4  # Невнимательный
    if 5 <= s1 <= 7 or 5 <= s2 <= 7:
        return 5  # Умеренное
    return 6  # Все хорошо
