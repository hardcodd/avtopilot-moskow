from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from app.utils import video_url
from comment.forms import ReviewForm
from comment.models import Review, MainReviewSection
from page.forms import ContactForm, PartnerForm, StaffMemberForm, BecomePartnerForm, ConsultationForm, InlineForm
from . import models


def contacts(request):
    instance = get_object_or_404(models.Contact, slug='contacts')
    context = {
        'instance': instance,
        'partners': models.Partner.objects.filter(parent=instance, section='PARTNERS').order_by('order'),
        'other_partners': models.Partner.objects.filter(parent=instance, section='OTHER_PARTNERS').order_by('order'),
        'installs': models.Partner.objects.filter(parent=instance, section='INSTALL').order_by('order'),
        'form': ContactForm,
        'partner_form': PartnerForm
    }
    return render(request, 'page/contacts.html', context)


def help_page(request, slug):
    instance = get_object_or_404(models.Help, slug=slug, published=True)
    pages = models.Help.objects.filter(published=True).order_by('order')
    context = {
        'instance': instance,
        'pages': pages
    }
    return render(request, 'page/help.html', context)


def info_page(request, slug):
    instance = get_object_or_404(models.Info, slug=slug, published=True)
    context = {
        'instance': instance,
    }
    return render(request, 'page/info.html', context)


def staff_page(request, slug):
    instance = get_object_or_404(models.StaffMember, slug=slug, published=True)

    initial_data = {
        'to': 'Сообщение для: %s' % instance.title,
    }
    contact_form = StaffMemberForm(request.POST or None, initial=initial_data)

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

    if instance.video:
        instance.video = video_url(instance.video)

    context = {
        'instance': instance,
        'review_form': review_form,
        'contact_form': contact_form
    }
    return render(request, 'page/staff.html', context)


def portfolio_page(request, slug):
    instance = get_object_or_404(models.Portfolio, slug=slug, published=True)

    context = {
        'instance': instance,
    }
    return render(request, 'page/portfolio.html', context)


def about_page(request, slug):
    instance = get_object_or_404(models.About, slug=slug, published=True)
    staff = models.StaffMember.objects.filter(published=True).order_by('order')
    context = {
        'instance': instance,
        'partner_form': BecomePartnerForm,
        'consultation_form': ConsultationForm,
        'staff': staff
    }
    return render(request, 'page/about.html', context)


def team(request):
    instance = get_object_or_404(models.Contact, slug='team')
    staff = models.Depd.objects.all().order_by('order')
    context = {
        'instance': instance,
        'inline_form': InlineForm,
        'staff': staff
    }
    return render(request, 'page/team.html', context)


def reviews(request):
    instance = get_object_or_404(models.Contact, slug='reviews')
    sections = MainReviewSection.objects.all().order_by('order')
    context = {
        'instance': instance,
        'sections': sections
    }
    return render(request, 'page/reviews.html', context)

