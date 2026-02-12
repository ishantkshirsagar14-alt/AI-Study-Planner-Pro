from datetime import date

def calculate_days_remaining(exam_date):
    return max((exam_date - date.today()).days, 1)

def get_weakest_subject(subjects, weights):
    return subjects[weights.index(max(weights))]
