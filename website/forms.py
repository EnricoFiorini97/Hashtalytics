from crispy_forms.layout import Submit
from crispy_forms.helper import FormHelper
from django import forms

from django import forms

class MainForm(forms.Form):
    hasher = forms.CharField(max_length=100,label="", widget=forms.TextInput(attrs={'placeholder': '@user #hashtag $luogo'}))

    @property
    def helper(self):
        helper = FormHelper()
        helper.form_id='Submit_research'
        helper.form_class='submit'
        helper.add_input(Submit('submit','Cerca'))
        helper.disable_csrf = True

        return helper

class LocForm(forms.Form):
    lat = forms.FloatField(min_value=-90, max_value=90)
    lon = forms.FloatField(min_value=-180, max_value=180)
