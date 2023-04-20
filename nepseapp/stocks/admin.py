from django.contrib import admin
from .models import StockData, BlogPost, User, Favorite

# Register your models here.
class StockDataAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'company_name', 'open', 'close', 'volume')
    list_filter = ('conf', 'range_percent')
    search_fields = ('symbol', 'company_name')

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_date')
    list_filter = ('author', 'created_date')
    search_fields = ('title', 'content')

class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'stock')
    list_filter = ('user', 'stock')
    search_fields = ('user__username', 'stock__company_name')

admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(StockData, StockDataAdmin)
admin.site.register(BlogPost, BlogPostAdmin)