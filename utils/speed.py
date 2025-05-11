def calculate_wpm(word_count, duration_seconds):
    minutes = duration_seconds / 60
    return round(word_count / minutes, 2)