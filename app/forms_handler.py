from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse, Http404


def forms_handler(request):
    """Sends email to managers"""

    if request.method != 'POST':
        raise Http404()

    try:
        message = _build_html_email_message(request)
        send_mail(subject=f'Новая заявка с сайта AVTOPILOT '
                          f'«{request.build_absolute_uri(location="/")}»',
                  message=message,
                  html_message=message,
                  from_email=settings.DEFAULT_FROM_EMAIL,
                  recipient_list=settings.RECIPIENT_LIST)
        return JsonResponse({'success': True})

    except Exception as error:
        return JsonResponse({'success': False, 'error': error})


def _build_html_email_message(request, exclude_fields: list = None) -> str:
    """Returns html email message that created by using fields taken from request.POST."""

    message = ''
    even = False
    post_query = request.POST

    exclude_fields = [
        'csrfmiddlewaretoken',
        'google-recaptcha'
    ] + _check_exclude_fields_format(exclude_fields)

    for field in post_query:
        value = post_query.get(field) or None
        if field not in exclude_fields and value is not None:
            even = not even
            message += '<tr>' if even else '<tr style="background-color:#f8f8f8">'
            message += f'<td style="padding:10px;border:#e9e9e9 1px solid"><b>{field}</b></td>' \
                       f'<td style="padding:10px;border:#e9e9e9 1px solid">{value}</td></tr>'

    return f'<table style="width:100%">{message}</table>'


def _check_exclude_fields_format(exclude_fields: list = None) -> list:
    """Returns exclude_fields if is list else empty list."""
    return exclude_fields if isinstance(exclude_fields, list) else list()
