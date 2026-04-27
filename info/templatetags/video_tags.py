import re
from django import template

register = template.Library()


@register.filter
def video_embed_url(url):
    """
    Convert a YouTube or Vimeo watch URL to its embed URL.

    YouTube:
      https://www.youtube.com/watch?v=ID  ->  https://www.youtube.com/embed/ID
      https://youtu.be/ID                 ->  https://www.youtube.com/embed/ID

    Vimeo:
      https://vimeo.com/ID                ->  https://player.vimeo.com/video/ID

    Returns None if the URL is not a recognised video URL.
    """
    if not url:
        return None

    # YouTube long form
    yt = re.match(
        r'https?://(?:www\.)?youtube\.com/watch\?(?:.*&)?v=([\w-]+)', url
    )
    if yt:
        return f'https://www.youtube.com/embed/{yt.group(1)}'

    # YouTube short form
    yt_short = re.match(r'https?://youtu\.be/([\w-]+)', url)
    if yt_short:
        return f'https://www.youtube.com/embed/{yt_short.group(1)}'

    # Vimeo
    vimeo = re.match(r'https?://(?:www\.)?vimeo\.com/(\d+)', url)
    if vimeo:
        return f'https://player.vimeo.com/video/{vimeo.group(1)}'

    return None
