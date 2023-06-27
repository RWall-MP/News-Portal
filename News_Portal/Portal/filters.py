from django_filters import FilterSet, ModelMultipleChoiceFilter, DateTimeFilter
from django.forms import DateTimeInput
from .models import Post, Category


class ProductFilter(FilterSet):
    category = ModelMultipleChoiceFilter(
        field_name='category__category_name',
        queryset=Category.objects.all(),
        label='Категории публикации',
    )
    added_after = DateTimeFilter(
        label='Дата публикации после',
        field_name='time_in',
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%d-%m-%Y',
            attrs={'type': 'datetime-local'},
        ),
    )

    class Meta:
        model = Post
        fields = {
            'title': ['iexact'],
            'category': ['exact'],
        }
