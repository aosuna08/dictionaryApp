import requests
from typing import Dict, Any

def get_definition (word : str, lang : str) -> Dict[str, Any] :
    """
    Conexion a la API de diccionario en tiempo real. Maneja errores de red
    y códigos de estado HTTP de manera segura.
    """

    # Formatear palabra que se ingresa al buscador
    cleanWord = word.strip()
    url = f"https://api.dictionaryapi.dev/api/v2/entries/{lang}/{cleanWord}"

    try :
        response = requests.get(url, timeout=5)

        if response.status_code == 200 :
            data = response.json()
            return parse_dictionary_response(data)
        
        # Código 404: La API funciona pero la palabra no existe en su base de datos
        elif response.status_code == 404:
            return {
                "error": True,
                "description": f"La palabra '{word}' no se encuentra en el diccionario ({lang.upper()})."
            }
        
        else:
            return {
                "error": True,
                "description": f"El servicio externo de diccionario reportó un problema (Código HTTP {response.status_code})."
            }
    
    except requests.exceptions.Timeout:
        return {
            "error": True,
            "description": "El servidor del diccionario tardó demasiado en responder. Inténtalo más tarde."
        }

    except requests.exceptions.RequestException:
        return {
            "error": True,
            "description": "Error de conexión. Asegúrate de tener acceso a internet."
        }

def parse_dictionary_response(data : list) -> Dict[str, Any] :
    """
    Toma la estructura la API externa,
    y la limpia para que la vista de Django reciba un diccionario.
    """
    try:
        # La API devuelve una lista de estructuras. Tomamos el primer bloque que coincida.
        first_block = data[0]
        found_word = first_block.get("word", "").capitalize()
        
        # Una palabra puede tener varios significados según su categoría gramatical (verbo, sustantivo, etc.)
        clean_definitions = []
        
        for definition in first_block.get("meanings", []):
            category = definition.get("partOfSpeech", "General")
            definitions = definition.get("definitions", [])
            
            # Se toma la primera definición disponible de cada categoría para no saturar la pantalla
            if definitions:
                first_definition = definitions[0].get("definition", "Sin definición disponible.")
                example = definitions[0].get("example", None)
                
                clean_definitions.append({
                    "category": category,
                    "definition": first_definition,
                    "example": example
                })
                
        return {
            "error": False,
            "word": found_word,
            "definition": clean_definitions
        }
        
    except (IndexError, KeyError, TypeError):
        return {
            "error": True,
            "description ": "El formato de los datos recibidos del diccionario no es el esperado."
        }