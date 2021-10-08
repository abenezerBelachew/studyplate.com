from django.core.exceptions import ValidationError

def validate_file_extension(value):
    """
    Validates the file extension
    """
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.pdf', '.doc', '.docx']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Please upload pdf, doc or docx files.')



def file_size(value): 
    """
    Sets the limit of the file size to be uploaded
    """
    limit = 2 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 2 MiB.')
