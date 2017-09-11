from django import forms


class EssayForm(forms.Form):
    question_body = forms.CharField(widget=forms.Textarea(attrs={'style': 'width:100%'}))
    answer = forms.CharField(widget=forms.Textarea(attrs={'style': 'width:100%'}))