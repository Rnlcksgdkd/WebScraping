from django.contrib import admin
from polls.models import Accomodation
from .models import Question


class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['subject']


admin.site.register(Question, QuestionAdmin)
# Register your models here.

admin.site.register(Accomodation)
