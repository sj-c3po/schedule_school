from django.contrib import admin
from schedule.models import *



admin.site.register(Cabinet)
admin.site.register(School_class)
admin.site.register(Subject)
admin.site.register(Teacher)
admin.site.register(SubjectTeacherRel)
admin.site.register(CommonRel)



#
# class CategoryAdmin(admin.ModelAdmin):
#     list_filter = ['products']
#     filter_horizontal = ['products']
#
# class ProductAdmin(admin.ModelAdmin):
#     list_filter = ['categories']
#     filter_horizontal = ['categories']
#
# admin.site.register(Product, ProductAdmin)
# admin.site.register(Category, CategoryAdmin)
