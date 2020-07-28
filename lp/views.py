from django.shortcuts import HttpResponse, get_object_or_404
from itertools import chain
from django.utils.safestring import mark_safe

from lp import models
import json
from django.template.loader import render_to_string
from django.http import Http404, JsonResponse
import requests


def lp(request, slug):
	instance = get_object_or_404(models.LandingPage, slug=slug)

	context = {
		'instance': instance
	}

	header = instance.headers.first()
	sections = instance.sections.all().order_by('order')
	footer = instance.footers.first()

	# HEADER
	if header:
		try:
			props = json.loads(s=header.json, encoding='utf8')
			header_id = props.get('header', None)
		except:
			props = {}
		if header_id:
			context['header'] = render_to_string('lp/headers/header_%s.html' % header_id, props, request)
			for k in props.keys():
				key = '%{k}%'.format(k=k)
				if key in context['header']:
					context['header'] = mark_safe(context['header'].replace(key, props[k]))

	# SECTIONS
	if len(sections):
		for section in sections:
			try:
				props = json.loads(s=section.json, encoding='utf8')
				section_id = props.get('section', None)
			except:
				props = {}
			if section_id:
				if 'sections' in context:
					context['sections'] = context['sections'] + render_to_string('lp/sections/section_%s.html' % section_id, props, request)
				else:
					context['sections'] = render_to_string('lp/sections/section_%s.html' % section_id, props, request)

	# FOOTER
	if footer:
		try:
			props = json.loads(s=footer.json, encoding='utf8')
			footer_id = props.get('footer', None)
		except:
			props = {}
		if footer_id:
			context['footer'] = render_to_string('lp/footers/footer_%s.html' % footer_id, props, request)

	html = render_to_string('lp/base.html', context, request)

	return HttpResponse(content=html)


def bx24(request):
	if request.method == 'POST':
		data = request.POST
		data = {k: data[k] for k in data}
		r = requests.post(data.get('action'), data)
		return JsonResponse({'data': json.loads(r.text)})

	raise Http404()
