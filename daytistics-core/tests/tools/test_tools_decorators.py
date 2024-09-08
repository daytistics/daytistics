import pytest
from django.conf import settings
from django.http import HttpRequest
from django.test import override_settings
from django.shortcuts import render

from app.tools.decorators import internal_only


class TestInternalOnly:
	@pytest.fixture
	def mock_view(self):
		def view(request):
			return 'view_response'

		return view

	@pytest.fixture
	def decorated_view(self, mock_view):
		return internal_only(mock_view)

	def test_internal_only_allowed_ip(self, rf, decorated_view):
		with override_settings(ALLOWED_HOSTS=['127.0.0.1']):
			request = rf.get('/')
			request.META['REMOTE_ADDR'] = '127.0.0.1'
			response = decorated_view(request)
			assert response == 'view_response'

	def test_internal_only_disallowed_ip(self, rf, decorated_view):
		with override_settings(ALLOWED_HOSTS=['127.0.0.1']):
			request = rf.get('/')
			request.META['REMOTE_ADDR'] = '192.168.1.1'
			response = decorated_view(request)
			assert response.status_code == 403
			assert 'Access to this page is only allowed internally' in str(response.content)

	def test_internal_only_wildcard_allowed_hosts(self, rf, decorated_view):
		with override_settings(ALLOWED_HOSTS=['*']):
			request = rf.get('/')
			request.META['REMOTE_ADDR'] = '192.168.1.1'
			response = decorated_view(request)
			assert response == 'view_response'

	def test_internal_only_no_remote_addr(self, rf, decorated_view):
		with override_settings(ALLOWED_HOSTS=['127.0.0.1']):
			request = rf.get('/')
			# Ensure REMOTE_ADDR is not in request.META
			if 'REMOTE_ADDR' in request.META:
				del request.META['REMOTE_ADDR']
			response = decorated_view(request)
			assert response.status_code == 403
			assert b'Access to this page is only allowed internally' in response.content

	@pytest.mark.parametrize(
		'allowed_hosts, remote_addr, expected_result',
		[
			(['127.0.0.1'], '127.0.0.1', 'view_response'),
			(['127.0.0.1'], '192.168.1.1', 403),
			(['*'], '192.168.1.1', 'view_response'),
			(['127.0.0.1', '192.168.1.1'], '192.168.1.1', 'view_response'),
		],
	)
	def test_internal_only_parametrized(
		self, rf, mock_view, allowed_hosts, remote_addr, expected_result
	):
		decorated_view = internal_only(mock_view)
		with override_settings(ALLOWED_HOSTS=allowed_hosts):
			request = rf.get('/')
			request.META['REMOTE_ADDR'] = remote_addr
			response = decorated_view(request)
			if expected_result == 403:
				assert response.status_code == 403
				assert 'Access to this page is only allowed internally' in str(response.content)
			else:
				assert response == expected_result
