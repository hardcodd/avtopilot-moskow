from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, get_object_or_404, redirect

from itertools import chain

from app.forms import HomeInstallOrderForm
from app.utils import views_today, video_url, get_session_key
from catalog.forms import OrderForm
from catalog.models import UniversalProduct
from order.models import ProductInCart
from page.models import Home, Work, PortfolioCategory
from settings.models import General
from . import models
from comment.models import Review, MainReview
from comment.forms import ReviewForm


def home(request):
    context = {
        'reviews': MainReview.objects.filter(published=True).order_by('-timestamp')[:10],
        'instance': Home.objects.filter(slug='home').first(),
        'portfolio': Work.objects.all(),
        'portfolio_categories': PortfolioCategory.objects.all().order_by('order'),
        'install_order_form': HomeInstallOrderForm
    }
    return render(request, 'catalog/home.html', context)


def catalog_page(request, slug):
    instance = get_object_or_404(models.CatalogPage, slug=slug)
    context = {}

    if instance.video:
        instance.video = video_url(instance.video)

    if instance.model == 'MAKE':
        context['instance'] = instance
        context['objects'] = models.Make.objects.all().order_by('title')
        return render(request, 'catalog/makes.html', context)

    def get_context(obj, products_type):
        context['instance'] = obj
        context['objects'] = models.UniversalProduct.objects.filter(status='PUBLIC', product_type=products_type)[:16]
        context['categories'] = models.UniversalCategory.objects.filter(products_type=products_type).order_by('order')
        return context

    if instance.model == 'ACCESSORIES':
        context = get_context(instance, 'ACCESSORY')

    elif instance.model == 'MATES':
        context = get_context(instance, 'MATE')

    elif instance.model == 'CAPES':
        context = get_context(instance, 'CAPE')

    elif instance.model == 'BRAIDS':
        context = get_context(instance, 'BRAID')

    return render(request, 'catalog/universal_products.html', context)


def products_category(request, slug):
    instance = get_object_or_404(models.UniversalCategory, slug=slug)
    parent_slug = 'accessories'
    if instance.products_type == 'MATE':
        parent_slug = 'mates'
    elif instance.products_type == 'CAPE':
        parent_slug = 'capes'
    elif instance.products_type == 'BRAID':
        parent_slug = 'braids'
    parent = get_object_or_404(models.CatalogPage, slug=parent_slug)
    context = {
        'parent': parent
    }

    def get_context(obj, products_type):
        context['instance'] = obj
        context['products'] = models.UniversalProduct.objects.filter(status='PUBLIC', product_type=products_type,
                                                                     category=obj)
        context['categories'] = models.UniversalCategory.objects.filter(products_type=products_type).order_by('order')
        return context

    if instance.products_type == 'ACCESSORY':
        context = get_context(instance, 'ACCESSORY')

    elif instance.products_type == 'MATE':
        context = get_context(instance, 'MATE')

    elif instance.products_type == 'CAPE':
        context = get_context(instance, 'CAPE')

    elif instance.products_type == 'BRAID':
        context = get_context(instance, 'BRAID')

    return render(request, 'catalog/universal_category.html', context)


def catalog_page_filter(request):
    if request.method == 'POST':
        instance = get_object_or_404(models.CatalogPage, slug=request.POST.get('slug'))
        context = {}

        def get_context(products_type):
            objects = models.UniversalProduct.objects.filter(
                status='PUBLIC', product_type=products_type, category_id=request.POST.get('category_id')
            )
            items = list()
            for obj in objects:
                item = dict()
                item['slug'] = obj.slug
                item['title'] = obj.title
                item['url'] = obj.get_absolute_url()
                item['reviews'] = obj.reviews.count()
                item['price'] = obj.sizes.first().price
                if obj.image:
                    item['image'] = obj.image.url
                else:
                    item['image'] = 'static/386x386.jpg'
                items.append(item)
            context['objects'] = items
            return context

        if instance.model == 'ACCESSORIES':
            context = get_context('ACCESSORY')

        elif instance.model == 'MATES':
            context = get_context('MATE')

        elif instance.model == 'CAPES':
            context = get_context('CAPE')

        elif instance.model == 'BRAIDS':
            context = get_context('BRAID')

        return JsonResponse(context)
    return HttpResponseNotFound()


def catalog_page_load_more(request):
    if request.method == 'POST':
        instance = get_object_or_404(models.CatalogPage, slug=request.POST.get('slug'))
        context = {}

        def get_context(products_type):
            objects = models.UniversalProduct.objects.filter(
                status='PUBLIC', product_type=products_type
            )[int(request.POST.get('offset')):][:16]
            if objects:
                context['more'] = True
            items = list()
            for obj in objects:
                item = dict()
                item['slug'] = obj.slug
                item['title'] = obj.title
                item['url'] = obj.get_absolute_url()
                item['reviews'] = obj.reviews.count()
                item['price'] = obj.sizes.first().price
                if obj.image:
                    item['image'] = obj.image.url
                else:
                    item['image'] = 'static/386x386.jpg'
                items.append(item)
            context['objects'] = items
            return context

        if instance.model == 'ACCESSORIES':
            context = get_context('ACCESSORY')

        elif instance.model == 'MATES':
            context = get_context('MATE')

        elif instance.model == 'CAPES':
            context = get_context('CAPE')

        elif instance.model == 'BRAIDS':
            context = get_context('BRAID')

        return JsonResponse(context)
    return HttpResponseNotFound()


def make(request, slug):
    instance = get_object_or_404(models.Make, slug=slug)

    if instance.video:
        instance.video = video_url(instance.video)

    context = {
        'instance': instance,
        'objects': models.Case.objects.filter(model__make=instance, status='PUBLIC').order_by('order'),
        'models': models.Model.objects.filter(make=instance).order_by('order')
    }
    return render(request, 'catalog/make.html', context)


def review_detail(request, slug):
    instance = get_object_or_404(models.Reviews, slug=slug)
    print(instance.case_set.all())

    context = {
        'instance': instance
    }
    return render(request, 'catalog/review_detail.html', context)


def case_detail(request, slug):
    instance = get_object_or_404(models.Case, slug=slug, status='PUBLIC')
    accessories = instance.accessories.all()
    title = '%s %s' % (instance.model.make.title, instance.model.title)

    if accessories:
        ids = [a.id for a in accessories]
        products = UniversalProduct.objects.filter(
            ~Q(id__in=ids),
            status='PUBLIC',
            title__icontains=title).order_by('?')[:20]
    else:
        products = UniversalProduct.objects.filter(
            status='PUBLIC',
            title__icontains=title).order_by('?')[:20]
    if not products:
        try:
            settings = General.objects.get(id=1)
            products = settings.accessories.filter(status='PUBLIC').order_by('?')
        except ObjectDoesNotExist:
            pass
    elif len(products) < 3:
        try:
            settings = General.objects.get(id=1)
            _products = settings.accessories.filter(status='PUBLIC').order_by('?')[:3 - len(products)]
            products = list(chain(products, _products))
        except ObjectDoesNotExist:
            pass

    reviews = instance.tab_reviews.all().order_by('order')
    qna = instance.qna.all().order_by('order')
    views_today(request, instance)

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
        'products': products,
        'accessories': accessories,
        'qna': qna,
        'reviews': reviews,
        'review_form': review_form
    }
    return render(request, 'catalog/case_detail.html', context)


def guarantee(request, slug):
    pass


def product_detail(request, slug):
    instance = get_object_or_404(models.UniversalProduct, slug=slug, status='PUBLIC')

    accessories = instance.accessories.all()
    if accessories:
        ids = [a.id for a in accessories]
        products = UniversalProduct.objects.filter(
            ~Q(id__in=ids),
            status='PUBLIC',
            category=instance.category).order_by('?')[:20]
    else:
        products = UniversalProduct.objects.filter(~Q(id=instance.pk),
                                                   status='PUBLIC', category=instance.category).order_by('?')[:20]
    if not products:
        products = UniversalProduct.objects.filter(~Q(id=instance.pk), status='PUBLIC').order_by('?')[:3]
    elif len(products) < 3:
        products = list(chain(
            products, UniversalProduct.objects.filter(~Q(id=instance.pk),
                                                      status='PUBLIC').order_by('?')[:3 - len(products)]))

    reviews = instance.tab_reviews.all().order_by('order')
    qna = instance.qna.all().order_by('order')
    views_today(request, instance)

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
        'products': products,
        'reviews': reviews,
        'accessories': accessories,
        'qna': qna,
        'review_form': review_form
    }
    return render(request, 'catalog/product_detail.html', context)


def cart_detail(request):
    session_key = get_session_key(request)
    context = {
        'products': ProductInCart.objects.filter(session_key=session_key)
    }
    return render(request, 'catalog/cart.html', context)


def order(request):
    session_key = get_session_key(request)
    products = ProductInCart.objects.filter(session_key=session_key)
    instance = {
        'total': 0
    }

    if not products:
        return redirect('home')

    for product in products:
        product.price_per_item = product.price
        product.price_total = product.price * product.count
        if product.install:
            product.price_total += product.install_price * product.count
        instance['total'] += product.price_total

    if request.user.is_authenticated:
        user = request.user
        initial = {
            'name': user.first_name,
            'last_name': user.last_name,
            'middle_name': user.middle_name,
            'phone': user.phone,
            'email': user.email,
            'country': user.country,
            'city': user.city,
            'street': user.street,
            'house_num': user.house_num,
            'housing_num': user.housing_num,
            'flat_num': user.flat_num,
        }
        form = OrderForm(initial=initial)
    else:
        form = OrderForm()

    context = {
        'products': products,
        'instance': instance,
        'form': form
    }
    return render(request, 'catalog/order.html', context)


def check_promo_code(request):
    if request.method == 'POST':
        code = request.POST.get('promo_code')
        if code:
            try:
                promo = models.PromoCode.objects.get(code__iexact=code)
                return JsonResponse({'percent': promo.percent})
            except ObjectDoesNotExist:
                return JsonResponse({'percent': False})
    return HttpResponseNotFound()


def cases_turbo(request):
    from math import ceil
    count = models.Case.objects.count()
    per_page = 50
    pages = ceil(count / per_page)
    try:
        page = int(request.GET.get('page'))
        offset = per_page * page - per_page
    except:
        raise Http404()

    if request.method == 'GET' and page <= pages:
        _makes = models.Make.objects.all().order_by('order')
        _models = models.Model.objects.all().order_by('order')
        _cases = models.Case.objects.filter(status='PUBLIC').order_by('-created')[offset:][:per_page]
        context = {
            'makes': _makes,
            'models': _models,
            'cases': _cases
        }
        return render(request=request, template_name='xml/base.xml', context=context, content_type='text/xml')
    else:
        raise Http404()
