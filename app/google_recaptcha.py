import requests
from django.http import HttpResponseNotFound, JsonResponse

from app.settings import GOOGLE_RECAPTCHA_SECRET_KEY


def check(request):
    if request.method == 'POST':
        post = request.POST
        success = False

        if 'google-recaptcha' not in post:
            return JsonResponse({'success': success})
        else:
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data={
                'secret': GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': post['google-recaptcha']
            })
            r = r.json()
            success = r['success'] and r['score'] > 0.5

            if success:
                return JsonResponse({'success': success})
            return JsonResponse({'success': success})
    return HttpResponseNotFound()
