from django.contrib import admin
from .models import Test, Question, Attempt, Answer

# Register your models here.

admin.site.register(Test)
admin.site.register(Question)
admin.site.register(Attempt)
admin.site.register(Answer)