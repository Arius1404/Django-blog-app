from django import forms
from django.forms import TextInput
from blog.models import Post, Category, Tag

DATA = Category.objects.only('id', 'title')
TAGS = Tag.objects.only('id', 'title')
CHOICES_CATEGORY = []
CHOICES_TAGS = []
for row in DATA:
    CHOICES_CATEGORY.append((row.id, row.title))
for row in TAGS:
    CHOICES_TAGS.append((row.id, row.title))


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'photo',
            'category',
            'tags',
        ]

    def __init__(self, *args, **kwargs):
        super(CreatePostForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget = TextInput(attrs={
            'id': 'title',
            'class': 'form-control',
            'name': 'title',
            'placeholder': 'Название поста'})
        self.fields['category'].widget = forms.Select(choices=CHOICES_CATEGORY, attrs={
            'class': 'js-example-basic-single', 'id': 'cat-select'
        })
        self.fields['photo'].widget = forms.FileInput(attrs={
            'class': 'field field__file', 'id': 'field__file-2', 'accept': '.jpg, .jpeg, .png',
            'onchange': "showPreview(event);"
        })
        self.fields['tags'].widget = forms.SelectMultiple(choices=CHOICES_TAGS, attrs={
            'id': 'tag-select-field',
        })


class UpdatePostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'photo',
            'category',
            'tags',
        ]

    def __init__(self, *args, **kwargs):
        super(UpdatePostForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget = TextInput(attrs={
            'id': 'title',
            'class': 'form-control',
            'name': 'title',
            'placeholder': 'Название поста',
            'value': "{{form.initial.title}}",
        })
        self.fields['category'].widget = forms.Select(choices=CHOICES_CATEGORY, attrs={
            'class': 'js-example-basic-single',
            'id': 'cat-select',
            'value': "{{form.initial.category}}",
        })
        self.fields['photo'].widget = forms.FileInput(attrs={
            'class': 'field field__file',
            'id': 'field__file-2',
            'accept': '.jpg, .jpeg, .png',
            'onchange': "showPreview(event);",

        })
        self.fields['tags'].widget = forms.SelectMultiple(choices=CHOICES_TAGS, attrs={
            'id': 'tag-select-field',
            'value': '{{form.initial.tags}}'
        })

    def save(self, commit=True):
        blog_post = self.instance
        blog_post.title = self.cleaned_data['title']
        blog_post.content = self.cleaned_data['content']
        blog_post.category = self.cleaned_data['category']

        if self.cleaned_data['photo']:
            blog_post.image = self.cleaned_data['photo']

        if commit:
            blog_post.save()
        return blog_post
