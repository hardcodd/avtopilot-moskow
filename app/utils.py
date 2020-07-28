from datetime import datetime
import yturl
from django.utils.text import slugify
from idna import unicode

from app import settings


def declension(num, *args):
    keys = [2, 0, 1, 1, 1, 2]
    mod = int(num) % 100
    index = 2 if 7 < mod < 20 else keys[min(mod % 10, 5)]
    try:
        return args[index]
    except IndexError:
        return ''


def build_url(uri):
    site_url = settings.SITE_URL
    if site_url[-1] == '/':
        site_url = site_url[:-1]
    if uri[0] == '/':
        uri = uri[1:]
    return '%s/%s' % (site_url, uri)


def views_today(request, instance):
    day = datetime.date(datetime.now())
    if not instance.current_day:
        instance.current_day = day
        instance.views = 0
        instance.save()
    elif not instance.current_day == day:
        instance.current_day = day
        instance.views = 0
        instance.save()
    else:
        set_views(request, instance)


def set_views(request, instance):
    if not request.user.is_superuser and not request.user.is_staff:
        instance.views += 1
        instance.save()


def video_url(link):
    return'https://www.youtube.com/embed/%s' % (yturl.video_id_from_url(link),)


def video_image(link):
    return'https://i.ytimg.com/vi/%s/hqdefault.jpg' % (yturl.video_id_from_url(link),)


def get_session_key(request):
    if request.user.is_authenticated:
        session_key = '%s_%s' % (request.user.id, request.user.email)
    else:
        session_key = request.session.session_key
    return session_key


def fn(instance, filename):
    ext = filename.split('.')[-1]

    if instance.pk:
        name = slugify(str(instance), allow_unicode=True)
    else:
        name = filename.split('.')[-2]

    file = '{}.{}'.format(name, ext)

    return file


def lost_time(timestamp):
    if not timestamp:
        return
    frm = '%Y-%m-%d %H:%M:%S'
    date1 = datetime.strftime(datetime.now(), frm)
    date2 = datetime.strftime(timestamp, frm)
    date1 = datetime.strptime(date1, frm)
    date2 = datetime.strptime(date2, frm)
    if date1 >= date2:
        return None
    sec = int(abs(date2 - date1).total_seconds())

    day = sec // (24 * 3600)
    sec = sec % (24 * 3600)
    hour = sec // 3600
    sec %= 3600
    minutes = sec // 60
    sec %= 60
    # seconds = sec

    output = ''
    if day:
        output += '%sд, ' % day
        output += '%sч' % hour
    else:
        output += '%sч, ' % hour
        output += '%sм' % minutes

    return output


def normalize_phone(mobile_tel):
    res_tel = ""
    for t in mobile_tel:
        if t in [unicode(n) for n in range(10)] or (t == "+"):
            res_tel += t
    return res_tel
