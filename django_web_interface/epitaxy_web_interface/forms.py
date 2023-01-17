import os

from django import forms

from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Column, Row, Submit

from .models import Experiment


class ExperimentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.layout = Layout(
            Row(
                Column('code', css_class='form-group col col-md-2'),
                Column('group', css_class='form-group col col-md-2'),
                Column('labels', css_class='form-group col col-md-4'),
                css_class='row'
            ),
            Row(
                Column('recipe_layer_number_tdms', css_class='form-group col col-md-4'),
                css_class='row'
            ),
            Row(
                Column('recipe_log', css_class='form-group col col-md-4'),
                Column('shutter_csv', css_class='form-group col col-md-4'),
                css_class='row'
            ),
            
            Row(
                Column('curvature_tdms', css_class='form-group col col-md-4'),
                Column('roughness_tdms', css_class='form-group col col-md-4'),
                css_class='row'
            ),
            Row(
                Column('wafer_temperature_tdms', css_class='form-group col col-md-4'),
                Column('reflectivity_tdms', css_class='form-group col col-md-4'),
                css_class='row'
            ),

            Submit(
                'submit', 'Valider',
                css_class='btn btn-secondary my-5'
            )
        )
    

    def clean(self):
        cleaned_data = super(ExperimentForm, self).clean()

        tdms_files = {
            'reflectivity_tdms': cleaned_data.get('reflectivity_tdms').name[-5:],
            'curvature_tdms': cleaned_data.get('curvature_tdms').name[-5:],
            'recipe_layer_number_tdms': cleaned_data.get('recipe_layer_number_tdms').name[-5:],
            'roughness_tdms': cleaned_data.get('roughness_tdms').name[-5:],
            'wafer_temperature_tdms': cleaned_data.get('wafer_temperature_tdms').name[-5:],
        }

        for file in tdms_files.items():
            if file[1] != '.tdms':
                self._errors[file[0]] = self.error_class([
                "Le ficher doit être un fichier .tdms"])
        
        if cleaned_data.get('recipe_log').name[-4:] != ".log":
            self._errors['recipe_log'] = self.error_class([
                "Le ficher doit être un fichier .log"])
        
        if cleaned_data.get('shutter_csv').name[-4:] != ".csv":
            self._errors['shutter_csv'] = self.error_class([
                "Le ficher doit être un fichier .csv"])
        

        return cleaned_data
    

    def save(self, commit=True):
        instance: Experiment = super(ExperimentForm, self).save(commit=False)
        
        instance.curvature_tdms.name = f"{instance.code}_curvature.tdms"
        instance.roughness_tdms.name = f"{instance.code}_roughness.tdms"
        instance.recipe_layer_number_tdms.name = f"{instance.code}_recipe_layer_number.tdms"
        instance.reflectivity_tdms.name = f"{instance.code}_reflectivity.tdms"
        instance.wafer_temperature_tdms.name = f"{instance.code}_wafer_temperature.tdms"
        instance.recipe_log.name = f"{instance.code}_recipe.log"
        instance.shutter_csv.name = f"{instance.code}_shutter.csv"

        if commit:
            instance.save()
        return instance


    class Meta:
        model = Experiment
        fields = '__all__'
