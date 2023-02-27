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
def url_or_default(img, key=settings.DEFAULT_IMAGE_KEY):
    try:
        url = img.url
    except:
        url = static(settings.DEFAULT_IMAGE[key])
    return url

@register.simple_tag
def settings_value(key):
    return getattr(settings, key, '')


@register.filter(name='is_gt_settings_val')
def is_gt_settings_val(val, settings_key):
    return val > getattr(settings, settings_key)


@register.filter(name='slice_page_range')
def slice_page_range(val, page_number, by_val=settings.NUMBER_PAGINATIONS):
    print(page_number)
    print(by_val)
    if len(val) < by_val:
        return val
    else:
        return val
        # list_pages = list(val)
        # first = list_pages[:by_val]
        # del list_pages[:by_val]
        # last = list_pages[-by_val:]
        # return [*first, None, *last]