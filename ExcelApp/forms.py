from django import forms
from ExcelApp.models import Excel

class ExcelForm(forms.ModelForm):
  
  class Meta:  
    model = Excel
    fields = ['name', 'file'] 

  def __init__(self, *args, **kwargs):
    super(ExcelForm, self).__init__(*args, **kwargs)
    for visible in self.visible_fields():
      visible.field.widget.attrs.update({'class': 'form-control'})

    