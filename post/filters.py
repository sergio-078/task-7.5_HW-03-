from django_filters import FilterSet, DateTimeFilter #DateFilter
#from django import forms
from django.forms import DateTimeInput

from .models import Post



# Создаем свой набор фильтров для модели Post.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.
class PostFilter(FilterSet):
    # data = DateFilter(
    #     field_name='dateCreation',
    #     widget=forms.DateInput(attrs={'type': 'date'}),
    #     lookup_expr='date__gte',
    # )

    added_after = DateTimeFilter(
        field_name='dateCreation',
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
        ),
    )

    class Meta:
       # В Meta классе мы должны указать Django модель,
       # в которой будем фильтровать записи.
       model = Post
       # В fields мы описываем по каким полям модели
       # будет производиться фильтрация.
       fields = {
           # поиск по названию
           'title': ['icontains'],
           'categoryType': ['exact'],
           'category': ['exact'],

       }
