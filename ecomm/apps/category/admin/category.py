from django.contrib import admin
from django.conf import settings
from mptt.admin import MPTTModelAdmin
from mptt.admin import DraggableMPTTAdmin
from ecomm.vendors.base.model import AdminBaseModel
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from ecomm.apps.category.models import (
	Category,
)

class CategoryMPTTModelAdmin(DraggableMPTTAdmin):
	mptt_level_indent = 20
	mptt_indent_field = "some_node_field"

@admin.register(Category)
class CategoryAdmin(AdminBaseModel, CategoryMPTTModelAdmin):
	model = Category
	list_display = (
		'tree_actions',
		'get_thumb',
		'slug', 
		'get_name',
		'is_valid', 
	)
	list_display_links = ('slug',)
	list_filter = (
		'is_valid', 
	)
	fieldsets = (
		(None, {
			'fields': (
				('is_valid',), 
				'slug',
				'name',
				'thumb',
				'svg',
				'thumb_as',
				'parent',
				'company', 
			)
		}),
	)
	search_fields = ('slug',)
	prepopulated_fields = {'slug': ('name',)}
	raw_id_fields = ['parent',]

	@admin.display(description='Name')
	def get_name(self, obj):
		return obj.name_in_lang_or_default

	@admin.display(description='Thumb')
	def get_thumb(self, obj):
		if obj.thumb_as == Category.ThumbAs.HIDDEN:
			return format_html(settings.HIDDEN_SVG)
		if obj.thumb_as == Category.ThumbAs.IMG:
			return format_html(
				'<img width="60" height="60" src="{}" />'.format(
					obj.img_url_or_default('thumb', settings.DEFAULT_IMAGE['PLACEHOLDER'])
				)
			)
		if obj.thumb_as == Category.ThumbAs.SVG:
			return format_html(obj.svg)

	def save_model(self, request, obj, form, change):
		super().save_model(request, obj, form, change)

	def delete_model(self, request, obj, form, change):
		super().delete_model(request, obj, form, change)
