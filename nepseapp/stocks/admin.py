from django.contrib import admin
from .models import StockData, BlogPost, User

# Register your models here.
class StockDataAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'company_name', 'open', 'close', 'volume')
    list_filter = ('conf', 'range_percent')
    search_fields = ('symbol', 'company_name')

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_date')
    list_filter = ('author', 'created_date')
    search_fields = ('title', 'content')

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email',)
    list_filter = ('username', 'email',)
    search_fields = ('username', 'email',)
    ordering = ('username',)

admin.site.register(User, UserAdmin)
admin.site.register(StockData, StockDataAdmin)
admin.site.register(BlogPost, BlogPostAdmin)