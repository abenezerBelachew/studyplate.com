from django import forms



# For file size checker
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
from django.conf import settings



from .models import Syllabus

class SyllabusFileForm(forms.ModelForm):
    class Meta:
        model = Syllabus
        fields = ('professor', 'term', 'year', 'file', 'anonymous')
    

    # def clean_file(self):
    #     # Check the size of the uploaded file
    #     file = self.cleaned_data['file']
    #     if file._size > int(settings.MAX_UPLOAD_SIZE):
    #         raise forms.ValidationError(_(f"Please keep filesize \
    #         under {filesizeformat(settings.MAX_UPLOAD_SIZE)}. Current filesize: {filesizeformat(file._size)}"))

    #     return file

    # def clean_file(self):
    #     # Check images form to see better way of implementing it
    #     file = self.cleaned_data['file']
    #     if file.endswith('.pdf'):
    #         return file
    #     else:
    #         raise forms.ValidationError('Please upload a pdf file')
    
class SyllabusLinkForm(forms.ModelForm):
    class Meta:
        model = Syllabus
        fields = ('professor', 'term', 'year', 'link', 'anonymous')