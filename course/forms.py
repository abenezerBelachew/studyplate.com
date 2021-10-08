from django import forms



class CourseSearchForm(forms.Form):
    query = forms.CharField(label='Search')