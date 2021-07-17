from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = '__all__'


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    form = PostAdminForm
    save_as = True
    save_on_top = True
    readonly_fields = [
        'views',
        'created_at',
        'updated_at',
        'get_photo',
    ]

    list_display = [
        'id',
        'title',
        'slug',
        'category',
        'created_at',
        'updated_at',
        'get_photo',
    ]
    list_display_links = [
        'id',
        'title',
    ]
    search_fields = [
        'title',
    ]
    list_filter = [
        'category',
        'tags'
    ]

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="50">')
        else:
            return '-'
    get_photo.short_description = 'Миниатюра (прикрепленное фото)'


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = [
        'title',
        'slug',
    ]


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = [
        'title',
        'slug',
    ]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)

admin.site.site_title = 'Управление публикациями'
admin.site.site_header = 'Управление публикациями'
