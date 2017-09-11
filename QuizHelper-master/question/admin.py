from django.contrib import admin
from .models import EssayQuestion
from .models import MultipleChoiceQuestion
from .models import MultipleChoiceAnswer

# Register your models here.
admin.site.register(EssayQuestion)
admin.site.register(MultipleChoiceQuestion)
admin.site.register(MultipleChoiceAnswer)