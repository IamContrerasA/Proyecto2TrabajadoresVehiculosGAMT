from django import forms  
from FatigasApp.models import Fatigue
class FatigueForm(forms.ModelForm):  
    class Meta:  
        model = Fatigue
        fields = "__all__"  

    def __init__(self, *args, **kwargs):
        super(FatigueForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs.update({'class': 'form-control'})