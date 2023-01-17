import requests

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages

from .models import Experiment

from .forms import ExperimentForm

# Create your views here.

def index(request: HttpRequest):
    return render(request, 'epitaxy_web_interface/index.html', {})


def upload_files(request: HttpRequest):

    context = {
        'form': ExperimentForm(
            request.POST or None,
            request.FILES or None
        )
    }

    if request.method == "POST":

        if context['form'].is_valid():
            instance: Experiment = context['form'].save(commit=False)

            # Only save if the response is not 503.
            r = requests.get(url='http://172.20.0.3:8001/start', params={'code': instance.code})
            if r.status_code == 200:
                messages.success(request, "Changements sauvegardés")
                instance.save()
                return redirect('/')
            else:
                if r.status_code == 503:
                    messages.error(
                        request,
                        f"Le serveur est occupé avec la requête précédente. Veuillez réessayer plus tard."
                    )
                else:
                    messages.error(request, f"Une erreur inattendue s'est produite ({r.status_code}).")

    return render(request, 'epitaxy_web_interface/form.html', context)


def predict(request: HttpRequest):
    return HttpResponse("Prédiction du résultat final")


def end(request: HttpRequest, code: int):
    # TODO: this is useless, have an actual interface with the CT status
    if code == 201:
        messages.success(request, "Les données ont été sauvegardées.")
    else:
        messages.error(request, f"Le processus de sauvegarde a échoué (erreur {code})")

    return HttpResponse(status=200)
