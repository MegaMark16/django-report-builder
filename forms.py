from django import forms
from django.utils.datastructures import SortedDict

def get_report_form(report):
    parameters = report.reportparameter_set.all()
    
    fields = SortedDict()
    for parameter in parameters:
        if parameter.parameter_type == 'TEXT':
            fields[parameter.label] = forms.CharField(initial = parameter.default_value, label=parameter.label)
        elif parameter.parameter_type == 'DATETIME':
            fields[parameter.label] = forms.DateTimeField(initial = parameter.default_value, label=parameter.label)
        elif parameter.is_dropdown_list():
            fields[parameter.label] = forms.ChoiceField(initial = parameter.default_value, label=parameter.label, choices=parameter.get_list_items())
        fields[parameter.label].required = False
    return type('ReportForm', (forms.BaseForm,), { 'base_fields': fields })
    """
    class ReportForm(forms.Form):
        def __init__(self, *args, **kwargs):
            super(ReportForm, self).__init__(*args, **kwargs)
            for parameter in parameters:
                if parameter.parameter_type == 'TEXT':
                    self.fields[parameter.label] = forms.CharField(initial = parameter.default_value, label=parameter.label)
                elif parameter.parameter_type == 'DATETIME':
                    self.fields[parameter.label] = forms.DateTimeField(initial = parameter.default_value, label=parameter.label)
                elif parameter.parameter_type == 'DROPDOWNLIST':
                    self.fields[parameter.label] = forms.ChoiceField(initial = parameter.default_value, label=parameter.label, choices=[(item, item) for item in parameter.get_list_items()])
                self.fields[parameter.label].required = False
    return ReportForm
    """
    
    
