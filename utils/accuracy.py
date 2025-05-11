import Levenshtein

def calculate_accuracy(transcript, expected_text):
    distance = Levenshtein.distance(transcript.lower(), expected_text.lower())
    accuracy = 1 - distance / max(len(transcript), len(expected_text))
    return round(accuracy * 100, 2)
