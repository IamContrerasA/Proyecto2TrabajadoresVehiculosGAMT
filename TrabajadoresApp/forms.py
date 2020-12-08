from django import forms  
from TrabajadoresApp.models import Worker


class WorkerForm(forms.ModelForm):  
    class Meta:  
        model = Worker  
        fields = "__all__"  

    def __init__(self, *args, **kwargs):
        super(WorkerForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs.update({'class': 'form-control'})

