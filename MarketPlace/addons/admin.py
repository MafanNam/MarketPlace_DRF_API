from django.contrib import admin

from addons.models import News, Main, Licence, About


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at',)
    list_filter = ('created_at',)
    ordering = ('-created_at',)
    search_fields = ('title', 'created_at',)


admin.site.register(Main)
admin.site.register(Licence)
admin.site.register(About)
