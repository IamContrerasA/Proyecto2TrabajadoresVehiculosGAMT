from django import forms  
from EmpresasApp.models import Company
class CompanyForm(forms.ModelForm):  
    class Meta:  
        model = Company
        fields = "__all__"  

    def __init__(self, *args, **kwargs):
        super(CompanyForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs.update({'class': 'form-control'})