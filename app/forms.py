from django.forms import ModelForm, Textarea, CharField, CheckboxInput, TextInput, Select, RadioSelect
from django.utils.translation import gettext_lazy as _
from app.models import Post, Answer, Comment, Upvote, PsuedoUser
from taggit.forms import TagField
import bleach

POST_TYPE_CHOICES = (
    ('Q', 'Question'),
    ('E', 'Experience')
)

class PostForm(ModelForm):
    title = CharField()
    tags = TagField()
    is_anonymous = CheckboxInput()
    description = CharField()

    title.widget.attrs.update({'class': 'input title-input', 'placeholder' : 'Enter a title'})
    tags.widget.attrs.update({'class': 'input', 'placeholder': 'Tag your post'})
    description.widget.attrs.update({'class': 'textarea', 'rows': 3, 'placeholder': 'Start typing...'})

    class Meta:
        model = Post
        fields = ('title', 'tags', 'description', 'is_anonymous')
        labels = {
            'is_anonymous': _('Post with psuedo name'),
        }

class PostFormQuestion(ModelForm):
    title = CharField()
    tags = TagField()
    is_anonymous = CheckboxInput()

    title.widget.attrs.update({'class': 'input title-input', 'placeholder' : 'Enter a title'})
    tags.widget.attrs.update({'class': 'input', 'placeholder': 'Tag your post'})

    class Meta:
        model = Post
        fields = ('title', 'tags', 'is_anonymous')
        labels = {
            'is_anonymous': _('Post with psuedo name'),
        }

class PostFormExperience(ModelForm):
    title = CharField()
    tags = TagField()
    description = CharField(widget=Textarea)
    is_anonymous = CheckboxInput()

    title.widget.attrs.update({'class': 'input title-input', 'placeholder' : 'Enter a title'})
    tags.widget.attrs.update({'class': 'input', 'placeholder': 'Tag your post'})
    description.widget.attrs.update({'class': 'textarea', 'rows': 3, 'placeholder': 'Start typing...'})

    class Meta:
        model = Post
        fields = ('title', 'tags', 'description', 'is_anonymous')
        labels = {
            'is_anonymous': _('Post with psuedo name'),
        }

class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = ('answer', 'is_anonymous')
        widgets = {
            'answer' : Textarea(attrs={'class': 'textarea', 'rows': 3})
        }
        labels = {
            'is_anonymous': _('Answer with my psuedo name'),
            'answer': _('')
        }

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('comment', 'is_anonymous',)
        widgets = {
            'comment': Textarea(attrs={'class': 'textarea is-auto-resize', 'rows': 1, 'placeholder': 'Share a comment...'})
        }
        labels = {
            'comment': _('')
        }

class PsuedoUserForm(ModelForm):
    class Meta:
        model = PsuedoUser
        fields = ('first_name', 'last_name')
        widgets = {
            'first_name': TextInput(attrs={'class':'input', 'placeholder':'First name'}),
            'last_name': TextInput(attrs={'class':'input', 'placeholder':'Last name'}),
        }

class FlagPostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('flagged_reason',)
        widgets = {
            'flagged_reason': RadioSelect()
        }
