from django.contrib import admin
from schedule.models import *


class School_classAdmin(admin.ModelAdmin):
    list_display = ['class_name', 'class_max_load']


class TeacherAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'middle_name', 'class_management', 'teacher_cabinet', 'staff_type']


class CommonRelAdmin(admin.ModelAdmin):
    list_display = ['sclass', 'subject', 'cabinet', 'teacher', 'subject_max_load', 'difficulty_level']


class SubjectTeacherRelAdmin(admin.ModelAdmin):
    list_display = ['subject', 'teacher', 'teacher_max_load']


admin.site.register(Cabinet)
admin.site.register(Staff_type)
admin.site.register(School_class, School_classAdmin)
admin.site.register(Subject)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(SubjectTeacherRel, SubjectTeacherRelAdmin)
admin.site.register(CommonRel, CommonRelAdmin)



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
