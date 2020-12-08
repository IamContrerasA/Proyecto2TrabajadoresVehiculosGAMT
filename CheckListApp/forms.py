from django import forms  
from CheckListApp.models import CheckList
class CheckListForm(forms.ModelForm):  
    class Meta:  
        model = CheckList
        fields = "__all__"  

    def __init__(self, *args, **kwargs):
        super(CheckListForm, self).__init__(*args, **kwargs)        
        for visible in self.visible_fields():
            visible.field.widget.attrs.update({'class': 'form-control'})