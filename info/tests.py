from django.test import TestCase, override_settings
from django.urls import reverse

from info.models import Info, Category
from info.templatetags.video_tags import video_embed_url

_TEST_OVERRIDES = dict(
    STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage',
    SECURE_SSL_REDIRECT=False,
)


class VideoEmbedUrlFilterTests(TestCase):
    """Unit tests for the video_embed_url template filter."""

    def test_youtube_long_url(self):
        result = video_embed_url('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
        self.assertEqual(result, 'https://www.youtube.com/embed/dQw4w9WgXcQ')

    def test_youtube_long_url_with_extra_params(self):
        result = video_embed_url('https://www.youtube.com/watch?t=30&v=dQw4w9WgXcQ&feature=share')
        self.assertEqual(result, 'https://www.youtube.com/embed/dQw4w9WgXcQ')

    def test_youtube_short_url(self):
        result = video_embed_url('https://youtu.be/dQw4w9WgXcQ')
        self.assertEqual(result, 'https://www.youtube.com/embed/dQw4w9WgXcQ')

    def test_vimeo_url(self):
        result = video_embed_url('https://vimeo.com/123456789')
        self.assertEqual(result, 'https://player.vimeo.com/video/123456789')

    def test_unrecognised_url_returns_none(self):
        result = video_embed_url('https://example.com/video')
        self.assertIsNone(result)

    def test_none_input_returns_none(self):
        result = video_embed_url(None)
        self.assertIsNone(result)

    def test_empty_string_returns_none(self):
        result = video_embed_url('')
        self.assertIsNone(result)


@override_settings(**_TEST_OVERRIDES)
class NewsVideoRenderTests(TestCase):
    """Integration tests: news page renders video embed when video_url is set."""

    def setUp(self):
        self.category = Category.objects.create(name='news', friendly_name='News')

    def test_news_page_loads(self):
        response = self.client.get(reverse('news'))
        self.assertEqual(response.status_code, 200)

    def test_video_embed_rendered_for_youtube(self):
        Info.objects.create(
            category=self.category,
            title='Video Item',
            date='2024-01-01',
            description='A news item with a video.',
            video_url='https://www.youtube.com/watch?v=dQw4w9WgXcQ',
        )
        response = self.client.get(reverse('news'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'https://www.youtube.com/embed/dQw4w9WgXcQ')
        self.assertContains(response, '<iframe')

    def test_video_embed_rendered_for_vimeo(self):
        Info.objects.create(
            category=self.category,
            title='Vimeo Item',
            date='2024-01-01',
            description='A news item with a vimeo video.',
            video_url='https://vimeo.com/123456789',
        )
        response = self.client.get(reverse('news'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'https://player.vimeo.com/video/123456789')

    def test_image_rendered_when_no_video_url(self):
        """Existing image behaviour must be unaffected when video_url is absent."""
        Info.objects.create(
            category=self.category,
            title='Image Item',
            date='2024-01-01',
            description='A news item without a video.',
            video_url=None,
        )
        response = self.client.get(reverse('news'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, '<iframe')

    def test_video_url_field_on_model(self):
        """Info model must have a video_url field."""
        item = Info.objects.create(
            category=self.category,
            title='Field Test',
            date='2024-01-01',
            description='test',
            video_url='https://www.youtube.com/watch?v=abc123',
        )
        item.refresh_from_db()
        self.assertEqual(item.video_url, 'https://www.youtube.com/watch?v=abc123')
