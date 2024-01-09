from django.contrib import admin

from .models import MenuConfig, Menu, RecipeMenu, ShopList

class MenuConfigAdmin(admin.ModelAdmin):
    list_display = ["user", "meal_count", "portions_count"]
    search_fields = ["user__email", ]
admin.site.register(MenuConfig, MenuConfigAdmin)


class RecipeMenuAdmin(admin.TabularInline):
    readonly_fields = ["week_day", "date"]
    model = RecipeMenu
    extra = 1
    
class ShopListAdmin(admin.TabularInline):
    readonly_fields = ["id", "ingredient", "description", "is_check"]
    model = ShopList
    extra = 1

class MenuAdmin(admin.ModelAdmin):
    list_display = ["user", "start_date", "end_date", "is_history"]
    list_filter = ["user", "is_history"]
    search_fields = ["user__email", ]
    inlines = [RecipeMenuAdmin, ShopListAdmin]
admin.site.register(Menu, MenuAdmin)


# class RecipeMenuAdmin(admin.ModelAdmin):
#     list_display = ["menu", "week_day", "recipe"]
# admin.site.register(RecipeMenu, RecipeMenuAdmin)

# class ShopListAdmin(admin.ModelAdmin):
#     list_display = ["menu", "ingredient", "is_check"]
# admin.site.register(ShopList, ShopListAdmin)
