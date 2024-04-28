from django import forms
from django.core.exceptions import ValidationError

from .models import Post

class PostForm(forms.ModelForm):
   class Meta:
       model = Post
       fields = [
           'author',
           'categoryType',
           'category',
           'title',
           'text',

       ]

   def clean(self):
       cleaned_data = super().clean()
       title = cleaned_data.get("title")
       text = cleaned_data.get("text")
       if title is not None and len(title) < 3 or text is not None and len(text) < 3:
           raise ValidationError({
               "title": "Заголовок не может быть менее 3 символов.",
               "text": "Текст не может быть менее 3 символов."
           })

       if text == title:
           raise ValidationError(
               "Текст не должен быть идентичным заголовоку."
           )

       return cleaned_data


# class SearchForm(forms.ModelForm):
#     class Meta:
#         model = Post
#         fields = [
#             'title',
#             'category',
#             #'dateCreation',
#         ]

class EditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['category', 'title', 'text']
