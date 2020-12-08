from django import forms  
from VehiculosApp.models import Vehicle
class VehicleForm(forms.ModelForm):  
    class Meta:  
        model = Vehicle
        fields = "__all__"  

    def __init__(self, *args, **kwargs):
        super(VehicleForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs.update({'class': 'form-control'})