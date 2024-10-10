from django import forms
from .models import Post
from django import forms
from .models import Comment


class PostForm(forms.ModelForm):
    hashtags = forms.CharField(required=False, help_text="Add hashtags separated by commas.")
    categories = forms.MultipleChoiceField(
        choices=[
            ("Group 1", "Group 1: Studies in Language and Literature"),
            ("Group 2", "Group 2: Language Acquisition"),
            ("Group 3", "Group 3: Individuals and Societies"),
            ("Group 4", "Group 4: Sciences"),
            ("Group 5", "Group 5: Mathematics"),
            ("Group 6", "Group 6: The Arts"),
            ("Others", "Others: Non IB Related")
        ],
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'hashtags', 'categories']
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']