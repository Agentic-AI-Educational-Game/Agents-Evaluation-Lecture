def detect_fluency(segments):
    pauses = 0
    for i in range(1, len(segments)):
        pause = segments[i]['start'] - segments[i-1]['end']
        if pause > 1.5:
            pauses += 1
    if pauses == 0:
        return "excellent"
    elif pauses <= 2:
        return "good"
    else:
        return "needs improvement"