from django.db import models


class Experiment(models.Model):
    code = models.CharField(
        unique=True,
        max_length=5,
        verbose_name="Code de l'expérience",
        help_text="Exemple : A1417"
    )
    group = models.CharField(
        max_length=50,
        verbose_name="Groupe d'expérience"
    )
    # JSON field ?
    labels = models.CharField(
        max_length=500,
        verbose_name="labels de l'expérience",
        help_text="sous format json ?"
    )

    recipe_log = models.FileField(
        verbose_name='Fichier Growth .log qui contient le récapitulatif des étapes',
        upload_to='recipe_log'
    )
    shutter_csv = models.FileField(
        verbose_name='Fichier Growth .csv qui contient les données des shutters',
        upload_to='shutter_csv'
    )

    recipe_layer_number_tdms = models.FileField(
        verbose_name=(
            "Fichier 'Recipe Layer Number.tdms' faisant le "
            "lien entre les étapes et le temps des capteurs"
        ),
        upload_to='recipe_layer_number_tdms'
    )
    curvature_tdms = models.FileField(
        verbose_name="Fichier 'Curvature.tdms' des données de courbure",
        upload_to='curvature_tdms'
    )
    roughness_tdms = models.FileField(
        verbose_name="Fichier 'Roughness.tdms' des données de ruguouosité",
        upload_to='roughness_tdms'
    )
    wafer_temperature_tdms = models.FileField(
        verbose_name="Fichier 'Wafer Temperature.tdms' des données de température du wafer",
        upload_to='wafer_temperature_tdms'
    )
    reflectivity_tdms = models.FileField(
        verbose_name="Fichier 'Reflectivity.tdms' des données de réflectivité",
        upload_to='reflectivity_tdms'
    )

    def __str__(self):
        return self.code
