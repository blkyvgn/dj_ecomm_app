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
def slice_page_range(val, page_number, by_number=settings.NUMBER_PAGINATIONS):
    if len(val.page_range) < by_number:
        return val.page_range
    else:
        falf_number = int(by_number/2 if by_number%2==0 else (by_number-1)/2)
        full_number = int(falf_number*2)
        first = int(page_number - falf_number)
        last = int(page_number + falf_number)
        if first < 0:
            first = 0
            last = full_number
        if last > val.num_pages:
            last = val.num_pages
            first = last - full_number
        res = list(val.page_range)[first:last] 
        return res