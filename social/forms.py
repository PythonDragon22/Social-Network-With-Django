from django import forms
from social.models import Post, Comment, MessageModel


class AddPostForm(forms.ModelForm):
    body = forms.CharField(
        label='',
        widget=forms.Textarea(
            attrs={
                'class': 'post-input',
                'placeholder': 'Say Something ...'
            }
        )
    )

    # post_image = forms.ImageField(required=False, label='')
    post_image = forms.ImageField(
        required=False,
        label='',
        widget=forms.ClearableFileInput(
            attrs={
                'class': 'upload-post-file',
                'multiple': True,
            }
        )
    )   # not to raise an error while submitting the post form that has no image

    class Meta:
        model = Post
        fields = ['body', 'post_image']


class AddCommentForm(forms.ModelForm):
    comment = forms.CharField(
        label='',
        widget=forms.Textarea(
            attrs={
                'rows': 3,
                'placeholder': 'Write a Comment ...'
            }
        )
    )

    class Meta:
        model = Comment
        fields = ['comment']


class ThreadForm(forms.Form):
    username = forms.CharField(label='', max_length=100)


class MessageForm(forms.ModelForm):
    body = forms.CharField(label='', max_length=220)
    img = forms.ImageField(required=False, label='')

    class Meta:
        model = MessageModel
        fields = ['body', 'img']


