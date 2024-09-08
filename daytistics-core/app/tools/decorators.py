from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponseForbidden


def internal_only(view_func):
	def _wrapped_view(request, *args, **kwargs):
		allowed_ips = settings.ALLOWED_HOSTS
		remote_addr = request.META.get('REMOTE_ADDR')
		if not remote_addr or (remote_addr not in allowed_ips and '*' not in allowed_ips):
			return HttpResponseForbidden(
				render(
					request,
					'error.html',
					{
						'error_message': 'Access to this page is only allowed internally',
						'error_help': 'docs.daytistics.com',
					},
				).content
			)
		return view_func(request, *args, **kwargs)

	return _wrapped_view
