from django import forms  
from AreasApp.models import Area
class AreaForm(forms.ModelForm):  
    class Meta:  
        model = Area
        fields = "__all__"  

    def __init__(self, *args, **kwargs):
        super(AreaForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs.update({'class': 'form-control'})