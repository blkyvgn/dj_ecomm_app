from django import template
from django.conf import settings
from django.templatetags.static import static
from django.utils.translation import get_language

register = template.Library()

@register.filter(name='in_lang_or_default')
def in_lang_or_default(val, lang_key=get_language()):
    try:
        res = val.get(lang_key, val.get(settings.LANGUAGE_CODE))
    except:
        res = None
    return res

@register.filter(name='url_or_default')
def url_or_default(img, key=settings.DEFAULT_IMAGE['PLACEHOLDER']):
    try:
        url = img.url
    except:
        url = static(key)
    return url