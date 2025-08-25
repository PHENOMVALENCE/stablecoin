from django import forms
from .models import Post, FAQ, Event
from ckeditor.widgets import CKEditorWidget

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'video', 'post_type', 'language']



class FAQForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = ['question', 'answer', 'language']




class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'date', 'flyer', 'design', 'show']
        widgets = {
            'design': CKEditorWidget(),
        }
