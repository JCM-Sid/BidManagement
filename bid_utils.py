import textwrap
import json
import pandas as pd

def print_text_wrapped(text, max_chars_per_line=90):
    """
    Prints a given text string, wrapping it to a maximum number of characters per line.
    Handles existing line breaks and very long lines by breaking words if necessary.

    Args:
        text (str): The input string.
        max_chars_per_line (int): The maximum number of characters allowed per line.
    """

    # Replace existing line breaks with a space to allow textwrap to re-wrap properly,
    # then split the text into "paragraphs" by double line breaks (or more).
    # This helps preserve intentional paragraph breaks.
    paragraphs = text.replace('\r\n', '\n').split('\n\n')

    for para in paragraphs:
        # For each paragraph, further split by single line breaks and re-wrap
        # to ensure even lines within a paragraph are handled.
        sub_lines = para.split('\n')
        for sub_line in sub_lines:
            # Use textwrap.fill to handle the actual wrapping.
            # break_long_words=True ensures that if a single word is longer
            # than max_chars_per_line, it will be broken.
            wrapped_line = textwrap.fill(sub_line,
                                         width=max_chars_per_line,
                                         break_long_words=True,
                                         replace_whitespace=True)
            print(wrapped_line)
        # Add an extra line break between original paragraphs
        if para != paragraphs[-1]: # Don't add an extra line break after the last paragraph
            print()

def print_json_info_cctp(text_json):
    
    # Délimiteurs du bloc JSON
    start_delimiter = "```json"
    end_delimiter = "```"
    pure_json_str= ""

    # Trouver la position du début du JSON
    start_index = text_json.find(start_delimiter)
    if start_index == -1:
        print("Erreur : Le délimiteur de début JSON n'a pas été trouvé.")
        return # Exit the function if the start delimiter is not found
    else:
    # Ajuster l'index pour commencer juste après le délimiteur
        json_start = start_index + len(start_delimiter)

    # Trouver la position de la fin du JSON
    end_index = text_json.find(end_delimiter, json_start)
    if end_index == -1:
        print("Erreur : Le délimiteur de fin JSON n'a pas été trouvé.")
        return
    else:
        # Extraire la sous-chaîne qui contient uniquement le JSON
        pure_json_str = text_json[json_start:end_index].strip()

        try:
            # Charger la chaîne JSON dans un dictionnaire Python
            chantier_info = json.loads(pure_json_str)

            print("JSON extrait et chargé dans un dictionnaire Python :")
            print(chantier_info)
            print(f"\nType de l'objet : {type(chantier_info)}")

            # Vous pouvez maintenant accéder aux données comme un dictionnaire normal
            keys_to_display = [
            'Nom Chantier',
            'Lieu du Chantier',
            'Maitre ouvrage',
            'Maitre oeuvre' , 
            'Type de Travaux',
            'Phase de la mission',
            'Durée Prévisionnelle des Travaux (en mois)',
            'Prix des travaux (en euros HT)',
            'Categorie operation SPS'
            ]

            not_present = "*** pas dispo ***"
            print("\nAccès aux données du dictionnaire :")
            for key in keys_to_display:
                if key in chantier_info:
                    print(f"{key}: {chantier_info[key]}")
                else:
                    print(f"{key}: Information non disponible")

        except json.JSONDecodeError as e:
            print(f"Erreur lors du décodage JSON : {e}")
            print(f"JSON brut qui a causé l'erreur :\n{pure_json_str}")
        except KeyError as e:
            print(f"Erreur : La clé '{e}' est manquante dans le dictionnaire.")

    return pure_json_str

