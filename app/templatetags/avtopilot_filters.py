import re
import uuid
from html import unescape

from django import template
from django.utils.html import strip_tags, mark_safe
from django.middleware.csrf import get_token

register = template.Library()


@register.filter
def multiply(value, arg):
    return value * arg


@register.filter
def _slugify(value):
    char_map = {
        'а': 'a', 'б': 'b', 'в': 'v',
        'г': 'g', 'д': 'd', 'е': 'e',
        'ё': 'e', 'ж': 'zh', 'з': 'z',
        'и': 'i', 'й': 'y', 'к': 'k',
        'л': 'l', 'м': 'm', 'н': 'n',
        'о': 'o', 'п': 'p', 'р': 'r',
        'с': 's', 'т': 't', 'у': 'u',
        'ф': 'f', 'х': 'h', 'ц': 'c',
        'ч': 'ch', 'ш': 'sh', 'щ': 'sh',
        'ъ': '', 'ы': 'y', 'ь': '',
        'э': 'e', 'ю': 'yu', 'я': 'ya',
    }
    value = value.lower()
    value = re.sub('([^a-zа-я0-9])', '_', value)
    spl = re.sub('([\'])', '', value)
    value = ''
    for l in spl:
        if char_map.get(l):
            value += char_map.get(l)
        else:
            value += l
    return value


@register.filter
def video_responsive(content):
    regex = '((?:<iframe[^>]*)(?:(?:\/>)|(?:>.*?<\/iframe>)))'
    content = re.sub(regex, r'<div class="video-responsive">\1</div>', content)
    return content


@register.filter
def short(content, arg=250):
    content = '<p>%s</p>' % strip_tags(content)[:arg]
    return mark_safe(content)


@register.filter
def sc(content, request):

    # Inline Forms
    open_form = '(?:\[form\]){1}'
    close_form = '(?:\[\/form\]){1}'
    regexps = [
        '(\[(input){1}[\sёa-zA-Zа-яА-Я0-9\;\:\=\,\.\'\"\-\!\_]*\])',  # input
        '(\[(textarea){1}[\sёa-zA-Zа-яА-Я0-9\;\:\=\,\.\'\"\-\!\_]*\])',  # textarea
        '(\[(select){1}[\sёa-zA-Zа-яА-Я0-9\;\:\=\,\.\'\"\-\!\_]*\])',  # select
        '(\[(button){1}[\sёa-zA-Zа-яА-Я0-9\;\:\=\,\.\'\"\-\!\_]*\])',  # button
    ]

    token = '<input type="hidden" name="csrfmiddlewaretoken" value="%s">' % get_token(request)

    content = re.sub(open_form, '<form method="post" action="/forms_handler" data-form-bx24'
                                ' enctype="multipart/form-data">%s'
                     % token, content)
    content = re.sub(close_form, '</form>', content)

    for rex in regexps:
        content = re.sub(rex, re_callback, content)
    # End Inline Forms

    # Code Execute
    regex = r'(\[execute\]{1})((\n|.)*)(\[\/execute\]{1})'
    matches = re.finditer(regex, content, re.MULTILINE)
    for matchNum, match in enumerate(matches, start=1):
        code = re.sub('<br />', '', unescape(match.group(2)))
        code = re.sub('<br/>', '', code)
        code = re.sub('<br>', '', code)
        code = re.sub('<p>', '', code)
        code = re.sub('</p>', '', code)
        content = re.sub(regex, code, content)
    # End Code Execute

    return mark_safe(content)


def re_callback(match):
    if match:
        match = re.sub('\[', '', match.group())
        match = re.sub('\]', '', match).split(';')
        markup = ''
        match_len = len(match)

        if match[0] == 'input':
            for i in range(match_len):
                if i == 0:
                    _id = uuid.uuid4()
                    label = [j for j in match if j.strip().startswith('data-label')] or ''
                    if label:
                        label = '<label for="%s">%s</label>' % (_id, label[0].split('=')[1].strip())
                    markup = markup + '<div>%s<%s id="%s"' % (label, match[i], _id)
                else:
                    props = match[i].split('=')
                    markup = markup + '%s' % props[0]
                    if len(props) == 2:
                        markup = markup + '="%s"' % props[1]
                    if match_len == i+1:
                        markup = markup + '></div>'

        if match[0] == 'button' or match[0] == 'textarea':
            for i in range(match_len):
                if i == 0:
                    _id = uuid.uuid4()
                    label = [j for j in match if j.strip().startswith('data-label')] or ''
                    if label:
                        label = '<label for="%s">%s</label>' % (_id, label[0].split('=')[1].strip())
                    markup = markup + '<div>%s<%s id="%s"' % (label, match[i], _id)
                else:
                    props = match[i].split('=')
                    if not props[0].strip() == 'value':
                        markup = markup + '%s' % props[0]
                        if len(props) == 2:
                            markup = markup + '="%s"' % props[1]
                    if match_len == i+1:
                        value = [j for j in match if j.strip().startswith('value')] or ''
                        if value:
                            value = value[0].split('=')[1].strip()
                        markup = markup + '>%s</%s></div>' % (value, match[0])

        if match[0] == 'select':
            for i in range(match_len):
                if i == 0:
                    _id = uuid.uuid4()
                    label = [j for j in match if j.strip().startswith('data-label')] or ''
                    if label:
                        label = '<label for="%s">%s</label>' % (_id, label[0].split('=')[1].strip())
                    markup = markup + '<div>%s<%s id="%s"' % (label, match[i], _id)
                else:
                    props = match[i].split('=')
                    if not props[0].strip() == 'values':
                        markup = markup + '%s' % props[0]
                        if len(props) == 2:
                            markup = markup + '="%s"' % props[1]
                    if match_len == i+1:
                        values = [j for j in match if j.strip().startswith('values')] or ''
                        if values:
                            values = values[0].split('=')[1].strip().split(',')
                            if len(values):
                                options = ''
                                for option in values:
                                    option = option.strip()
                                    if option.startswith('!'):
                                        options = options + '<option value="">%s</option>' % option[1:]
                                    else:
                                        options = options + '<option value="%s">%s</option>' % (option, option)
                                markup = markup + '>%s</%s></div>' % (options, match[0])

        return markup
