from django.contrib import admin
from recepts.models import Dimensions, Ingredients, ResipesIngredients, Resipes, Steps, Marinades, Sauces


class ResipesIngredientsInline(admin.TabularInline):
    # readonly_fields = ['']
    model = ResipesIngredients
    extra = 1


class StepsInline(admin.TabularInline):
    readonly_fields = ['img_preview',]
    model = Steps
    extra = 1


class MarinadesIngredientsInline(admin.TabularInline):
    # readonly_fields = ['']
    model = Marinades
    extra = 1


class ResipesSaucesInline(admin.TabularInline):
    # readonly_fields = ['']
    model = Sauces
    extra = 1


class ResipesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'img_preview')
    search_fields = ['name',]
    readonly_fields = ['img_preview',]
    inlines = (ResipesIngredientsInline, MarinadesIngredientsInline, ResipesSaucesInline, StepsInline)
admin.site.register(Resipes, ResipesAdmin)


class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ['name',]
admin.site.register(Ingredients, IngredientsAdmin)


class DimensionsAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'number']
    list_editable = ['number',]
    search_fields = ['name', 'number']
admin.site.register(Dimensions, DimensionsAdmin)