"""
    Manejador de peticiones
"""

from django.shortcuts import render
from .services import get_definition

def search_word (request) :
    """
    Vista principal del buscador. Recibe los parámetros de la URL,
    consulta el servicio y devuelve el contexto a la plantilla HTML.
    """

    # Diccionario 'context'
    # Se almacena la info que se mostrara en pantalla
    context = {
        # Solo se declara si la busqueda esta activa debido a que los otros datos serian vacios ya que se obtienen despues
        'active_search' : False
    }

    # Recibir palabra
    word = request.GET.get('word')

    # Obetner idioma
    # Si no se recibe, se asume que es ingles
    lang = request.GET.get('lang', 'en')

    if word :
        # 1. Se llama a la funcion que obtiene las definiciones de la palabra
        response = get_definition(word, lang)

        # 2. Se almacenan los resultados en el diccionario contexto
        context['active_search'] = True
        context['response'] = response
        context['searched_word'] = word
        context['selected_lang'] = lang

        # 3. Se renderiza el archivo HTML donde se presentan las definiciones
        return render(request, 'searcher/index.html', context) # [PLACEHOLDER (Aun no se crean los templates)]