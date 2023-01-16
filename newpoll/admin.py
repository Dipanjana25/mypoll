from django.contrib import admin

from .models import Question, Choice, Notification


class ChoiceInline(admin.TabularInline):
    model = Choice


class QuestionAdmin(admin.ModelAdmin):
    inlines=[ChoiceInline]

admin.site.register(Question,QuestionAdmin)
admin.site.register(Notification)