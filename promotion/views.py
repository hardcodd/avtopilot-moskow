from datetime import datetime

from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

from comment.forms import ReviewForm
from comment.models import Review
from . import models
from .utils import pagination, check_page


def promotion_detail(request, slug):
    instance = get_object_or_404(models.Promotion, slug=slug)
    categories = models.Category.objects.all().order_by('order')

    for cat in categories:
        cat.items = models.Promotion.objects.filter(
            ~Q(id=instance.id),
            published=True, category=cat, time_end__gte=datetime.now()).order_by('?')[:2]

    initial_data = {
        'content_type': instance.get_content_type,
        'obj_id': instance.id,
        'rating': 4
    }
    review_form = ReviewForm(request.POST or None, initial=initial_data)
    if review_form.is_valid():
        c_type = review_form.cleaned_data.get('content_type')
        content_type = ContentType.objects.get(model=c_type)
        obj_id = review_form.cleaned_data.get('obj_id')
        rating = review_form.cleaned_data.get('rating')
        content_data = review_form.cleaned_data.get('content')
        new_review, created = Review.objects.get_or_create(
            user=request.user,
            content_type=content_type,
            object_id=obj_id,
            rating=rating,
            content=content_data
        )
        if created:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    context = {
        'instance': instance,
        'review_form': review_form,
        'categories': categories
    }
    return render(request, 'promotion/promotion_detail.html', context)


def promotion_category(request, slug):
    instance = get_object_or_404(models.Category, slug=slug)

    categories = models.Category.objects.all().order_by('order')

    promotions = models.Promotion.objects.filter(published=True, category=instance).order_by('-time_end')

    promotions = pagination(request, promotions)

    to = check_page(request, promotions)
    if to:
        return redirect(to)

    context = {
        'instance': instance,
        'promotions': promotions,
        'categories': categories
    }
    return render(request, 'promotion/category.html', context)


def promotion_page(request):
    instance = get_object_or_404(models.PromotionPage, slug='promotion')

    categories = models.Category.objects.all().order_by('order')

    promotions = models.Promotion.objects.filter(published=True).order_by('-time_end')

    promotions = pagination(request, promotions)

    to = check_page(request, promotions)
    if to:
        return redirect(to)

    context = {
        'instance': instance,
        'promotions': promotions,
        'categories': categories
    }
    return render(request, 'promotion/promotion.html', context)
