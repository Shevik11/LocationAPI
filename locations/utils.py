from feedbacks.models import Feedback


def calculate_average_rating(location_id):
    feedbacks = Feedback.objects.filter(location_id=location_id)
    total_stars = sum(feedback.stars for feedback in feedbacks)
    count = feedbacks.count()
    if count > 0:
        average_rating = total_stars / count
    else:
        average_rating = 0
    return average_rating
