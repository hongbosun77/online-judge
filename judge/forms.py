from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django_ace import AceWidget
from judge.comments import valid_comment_page
from .models import Profile, Submission, Comment

try:
    from pagedown.widgets import PagedownWidget
except ImportError:
    PagedownWidget = None


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'about', 'timezone', 'language', 'ace_theme']


class ProblemSubmitForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProblemSubmitForm, self).__init__(*args, **kwargs)
        self.fields['problem'].empty_label = None
        self.fields['language'].empty_label = None

    class Meta:
        model = Submission
        fields = ['problem', 'source', 'language']
        widgets = {
            'source': AceWidget(theme='twilight'),
        }


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['title', 'body', 'parent']
        widgets = {
            'parent': forms.HiddenInput(),
        }
        if PagedownWidget is not None:
            widgets['body'] = PagedownWidget()

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'style': 'min-width:100%'})
        self.fields['body'].widget.attrs.update({'style': 'min-width:100%'})

    def clean_page(self):
        page = self.cleaned_data['page']
        if not valid_comment_page(page):
            raise ValidationError('Invalid page id: %(id)s', params={'id': page})
