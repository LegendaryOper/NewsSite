from django.contrib import admin
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import News,Category,NewsComment
from django import forms
from django.utils.safestring import mark_safe

# Register your models here.

class NewsAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = News
        fields = '__all__'

class NewsAdmin(admin.ModelAdmin):
    form = NewsAdminForm
    list_display = ('id','title','created_at','updated_at','is_publishied','category')
    list_display_links = ('id','title',)
    search_fields = ('title','content','category')
    list_editable = ('is_publishied',)
    list_filter = ('is_publishied','category')

    def get_photo(self,obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="75">')
        else:
            return '-'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'id')
    list_display_links = ('id', 'title')
    search_fields = ('title',)

class NewsCommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'id','mail')
    list_display_links = ('id', 'author',)
    search_fields = ('author','mail')




admin.site.register(News, NewsAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(NewsComment,NewsCommentAdmin)