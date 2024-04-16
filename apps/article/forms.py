
from django import forms

from .models import Post, Tag

DEMO_CHOICES =( 
    ("1", "Naveen"), 
    ("2", "Pranav"), 
    ("3", "Isha"), 
    ("4", "Saloni"), 
) 

class PostForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(  # детальна конфігурація поля "теги", замість виділення, обираються чекбокси
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Post
        fields = ('title', 'content', 'image', 'tags')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["content"].required = False
        self.fields["tags"].required = False


class CommentForm(forms.Form):
    content = forms.CharField(min_length=4,max_length=200)
