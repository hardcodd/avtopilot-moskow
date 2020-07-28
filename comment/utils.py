from comment import models


def get_reviews(instance):
    qs = models.Review.objects.filter_by_instance(instance).order_by('-timestamp')
    for rev in qs:
        rev.stars = range(0, rev.rating)
    return qs


def total_rating(instance):
    qs = models.Review.objects.filter_by_instance(instance)
    total = 0
    for review in qs:
        total += review.rating
    if total == 0:
        return 0
    computed = (100 * (total / qs.count()) / 5)
    return int(computed)
