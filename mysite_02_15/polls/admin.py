from django.contrib import admin
from polls.models import Accomodation
from polls.models import Room_detail
from polls.models import Question
from polls.models import Answer

# Register your models here.

admin.site.register(Accomodation)
admin.site.register(Question)
admin.site.register(Room_detail)
admin.site.register(Answer)
