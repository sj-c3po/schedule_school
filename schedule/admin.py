from django.contrib import admin
from schedule.models import *


class School_classAdmin(admin.ModelAdmin):
    list_display = ['id', 'parallel_letter', 'class_max_load']


class SubjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'subject_name']


class TeacherAdmin(admin.ModelAdmin):
    list_display = ['id', 'last_name', 'first_name', 'middle_name', 'class_management', 'teacher_cabinet', 'staff_type', 'ban_hours'] # 'scope',


class CommonRelAdmin(admin.ModelAdmin):
    list_display = ['sclass', 'subject', 'subject_max_load', 'teacher', 'cabinet', 'difficulty_level', 'division_class'] #'id',


class SubjectTeacherRelAdmin(admin.ModelAdmin):
    list_display = ['id', 'subject', 'teacher', 'teacher_max_load']


admin.site.register(Cabinet)
admin.site.register(Schedule)
admin.site.register(Schedule_items)
admin.site.register(Division)
admin.site.register(Class_profiles)
admin.site.register(School_class, School_classAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Teacher, TeacherAdmin)
# admin.site.register(SubjectTeacherRel, SubjectTeacherRelAdmin)
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
