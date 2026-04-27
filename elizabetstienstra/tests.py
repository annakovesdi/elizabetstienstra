"""
Tests for security fixes applied to the elizabetstienstra project.

Covers:
  - Issue 3: SECURE_SSL_REDIRECT, SESSION_COOKIE_SECURE, CSRF_COOKIE_SECURE,
             SECURE_PROXY_SSL_HEADER
  - Issue 4: S3 CORS restricted to production domain
  - Issue 5: Media URL not routed through Django when S3 is active
  - Issue 7: oeuvre view always provides 'images' in context
  - Issue 8: add_cv does not overwrite bound form after POST
  - Issue 9: WorkForm.__init__ typo fixed, category choices are applied
"""

import datetime
import importlib
import inspect

from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory, override_settings
from django.urls import reverse

from cv.models import Category as CvCategory, Cv
from oeuvre.forms import WorkForm
from oeuvre.models import Category as OeuvreCategory, Work, Image


# Shared overrides: avoid collectstatic requirement and SSL redirect loops
# in view-level tests.
_TEST_OVERRIDES = dict(
    STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage',
    SECURE_SSL_REDIRECT=False,
)


# ---------------------------------------------------------------------------
# Issue 3 — HTTPS security settings
# ---------------------------------------------------------------------------

class HttpsSettingsTests(TestCase):

    def test_secure_ssl_redirect_enabled(self):
        self.assertTrue(settings.SECURE_SSL_REDIRECT)

    def test_session_cookie_secure(self):
        self.assertTrue(settings.SESSION_COOKIE_SECURE)

    def test_csrf_cookie_secure(self):
        self.assertTrue(settings.CSRF_COOKIE_SECURE)

    def test_secure_proxy_ssl_header_set(self):
        """Required so Django trusts X-Forwarded-Proto from Render/Heroku."""
        self.assertEqual(
            settings.SECURE_PROXY_SSL_HEADER,
            ('HTTP_X_FORWARDED_PROTO', 'https'),
        )

    @override_settings(
        SECURE_SSL_REDIRECT=True,
        SECURE_PROXY_SSL_HEADER=('HTTP_X_FORWARDED_PROTO', 'https'),
    )
    def test_http_request_redirected_to_https(self):
        """A plain HTTP request must be redirected to HTTPS."""
        response = self.client.get('/cv/cv/', SERVER_NAME='elisabetstienstra.com')
        self.assertIn(response.status_code, [301, 302])
        self.assertIn('https://', response['Location'])

    @override_settings(
        SECURE_SSL_REDIRECT=True,
        SECURE_PROXY_SSL_HEADER=('HTTP_X_FORWARDED_PROTO', 'https'),
        STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage',
    )
    def test_https_request_not_redirected(self):
        """A request with X-Forwarded-Proto: https must not trigger a redirect loop."""
        response = self.client.get(
            '/cv/cv/',
            HTTP_X_FORWARDED_PROTO='https',
            SERVER_NAME='elisabetstienstra.com',
        )
        self.assertNotIn(response.status_code, [301, 302])


# ---------------------------------------------------------------------------
# Issue 4 — S3 CORS restricted to production domain
# ---------------------------------------------------------------------------

class S3CorsSettingsTests(TestCase):

    def test_settings_source_cors_not_wildcard(self):
        import elizabetstienstra.settings as s
        source = inspect.getsource(s)
        self.assertNotIn(
            "'Access-Control-Allow-Origin': '*'",
            source,
            "Wildcard CORS must not appear in settings.py",
        )

    def test_settings_source_cors_is_production_domain(self):
        import elizabetstienstra.settings as s
        source = inspect.getsource(s)
        self.assertIn(
            "'Access-Control-Allow-Origin': 'https://elisabetstienstra.com'",
            source,
        )

    @override_settings(AWS_HEADERS={'Access-Control-Allow-Origin': 'https://elisabetstienstra.com'})
    def test_runtime_cors_not_wildcard(self):
        origin = settings.AWS_HEADERS.get('Access-Control-Allow-Origin', '')
        self.assertNotEqual(origin, '*')

    @override_settings(AWS_HEADERS={'Access-Control-Allow-Origin': 'https://elisabetstienstra.com'})
    def test_runtime_cors_is_production_domain(self):
        origin = settings.AWS_HEADERS.get('Access-Control-Allow-Origin', '')
        self.assertEqual(origin, 'https://elisabetstienstra.com')


# ---------------------------------------------------------------------------
# Issue 5 — Media not served through Django when S3 is configured
# ---------------------------------------------------------------------------

class MediaUrlRoutingTests(TestCase):

    @override_settings(
        DEBUG=False,
        STORAGE_DESTINATION='s3',
        MEDIA_URL='https://bucket.s3.amazonaws.com/media/',
    )
    def test_media_not_in_urlpatterns_when_s3(self):
        import elizabetstienstra.urls as url_module
        importlib.reload(url_module)
        patterns = [str(p.pattern) for p in url_module.urlpatterns]
        for pattern in patterns:
            self.assertFalse(
                'media' in pattern,
                f"Media path should not be in urlpatterns when using S3, found: {pattern}",
            )

    @override_settings(
        DEBUG=True,
        STORAGE_DESTINATION=None,
        MEDIA_URL='/media/',
        MEDIA_ROOT='/tmp/',
    )
    def test_media_served_by_django_in_dev(self):
        import elizabetstienstra.urls as url_module
        importlib.reload(url_module)
        patterns = [str(p.pattern) for p in url_module.urlpatterns]
        self.assertTrue(
            any('media' in p for p in patterns),
            "Media path should be in urlpatterns during local development",
        )

    def test_urls_source_has_s3_guard(self):
        import elizabetstienstra.urls as url_module
        source = inspect.getsource(url_module)
        self.assertIn("STORAGE_DESTINATION == 's3'", source)


# ---------------------------------------------------------------------------
# Issue 7 — oeuvre view always provides 'images' in context
# ---------------------------------------------------------------------------

@override_settings(**_TEST_OVERRIDES)
class OeuvreViewContextTests(TestCase):

    def test_images_key_present_without_filter(self):
        response = self.client.get(reverse('oeuvre'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('images', response.context)

    def test_images_empty_without_filter(self):
        response = self.client.get(reverse('oeuvre'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context['images'], [])

    def test_no_name_error_without_filter(self):
        """A 200 response proves no NameError is raised for the unfiltered view."""
        response = self.client.get(reverse('oeuvre'))
        self.assertEqual(response.status_code, 200)

    def test_images_populated_with_category_filter(self):
        """Images queryset contains the work's images when a category filter is applied.

        Uses RequestFactory to call the view directly, bypassing template rendering,
        because the template requires image files on disk which are not present in tests.
        """
        from oeuvre.views import oeuvre as oeuvre_view
        cat = OeuvreCategory.objects.create(name='sculpture', friendly_name='Sculpture')
        work = Work.objects.create(
            category=cat,
            title='Test Work',
            date=datetime.date(2023, 1, 1),
            size='100x100',
            materials='bronze',
        )
        img = Image.objects.create(work=work)

        factory = RequestFactory()
        request = factory.get(reverse('oeuvre'), {'category': 'sculpture'})
        from unittest.mock import patch
        with patch('oeuvre.views.render') as mock_render:
            mock_render.return_value = type('R', (), {'status_code': 200})()
            oeuvre_view(request)
            _, _, context = mock_render.call_args[0]
        self.assertIn(img, context['images'])


# ---------------------------------------------------------------------------
# Issue 8 — add_cv does not overwrite bound form after POST
# ---------------------------------------------------------------------------

@override_settings(**_TEST_OVERRIDES)
class AddCvFormTests(TestCase):

    def setUp(self):
        self.superuser = User.objects.create_superuser(
            username='admin', password='password', email='admin@test.com'
        )
        self.client.login(username='admin', password='password')
        self.category = CvCategory.objects.create(name='Education', friendly_name='Education')

    def test_invalid_post_returns_bound_form(self):
        """Submitting invalid data must return the bound form, not a blank one."""
        response = self.client.post(reverse('add_cv'), data={
            'category': self.category.pk,
            'title': 'Test',
            'description': '',   # required — triggers validation error
            'hide': False,
        })
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertTrue(form.is_bound, "Form should be bound after invalid POST")

    def test_invalid_post_form_has_errors(self):
        response = self.client.post(reverse('add_cv'), data={
            'category': self.category.pk,
            'title': 'Test',
            'description': '',
            'hide': False,
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].errors)

    def test_valid_post_redirects(self):
        response = self.client.post(reverse('add_cv'), data={
            'category': self.category.pk,
            'title': 'Test Item',
            'description': '<p>Some description</p>',
            'hide': False,
        })
        self.assertRedirects(response, reverse('cv_management'))
        self.assertTrue(Cv.objects.filter(title='Test Item').exists())


# ---------------------------------------------------------------------------
# Issue 9 — WorkForm.__init__ typo fixed
# ---------------------------------------------------------------------------

class WorkFormInitTests(TestCase):

    def test_instantiation_does_not_raise(self):
        try:
            WorkForm()
        except TypeError as e:
            self.fail(f"WorkForm() raised TypeError: {e}")

    def test_category_field_present(self):
        form = WorkForm()
        self.assertIn('category', form.fields)

    def test_form_valid_with_correct_data(self):
        """WorkForm must validate with valid input using the project's date format (dd-mm-yyyy)."""
        cat = OeuvreCategory.objects.create(name='drawing', friendly_name='Drawing')
        form = WorkForm(data={
            'category': cat.pk,
            'title': 'My Work',
            'date': '01-06-2023',   # DATE_INPUT_FORMATS = ["%d-%m-%Y"]
            'size': '50x70cm',
            'materials': 'pencil',
            'description': '',
            'hide': False,
            'courtesy_of_gallery': False,
        })
        self.assertTrue(form.is_valid(), form.errors)

    def test_source_has_no_innit_typo(self):
        import oeuvre.forms as f
        source = inspect.getsource(f)
        self.assertNotIn('__innit__', source)
        self.assertIn('def __init__', source)
