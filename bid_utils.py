import textwrap
import json
import pandas as pd
import fitz
import os
from IPython.display import display, HTML
from PIL import Image
import pytesseract
import io


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
    start_delimiter1 = "```json"
    start_delimiter2 = "```"
    start_delimiter3 = "{"
    end_delimiter = "```"
    pure_json_str= ""

    # Trouver la position du début du JSON
    start_index1 = text_json.find(start_delimiter1)
    start_index2 = text_json.find(start_delimiter2)
    start_index3 = text_json.find(start_delimiter3)
    if start_index1 != -1:
        start_index = start_index1
        start_delimiter = start_delimiter1
    elif start_index2 != -1:
        start_index = start_index2
        start_delimiter = start_delimiter2
    elif start_index3 != -1:    
        start_index = start_index3
        start_delimiter = start_delimiter3
        end_delimiter = "}"
        
    # Trouver la position de la fin du JSON
    json_start = start_index + len(start_delimiter)
    end_index = text_json.find(end_delimiter, json_start)
    if end_index == -1:
        print("Erreur : Le délimiteur de fin JSON n'a pas été trouvé.")
        return
    else:
        # Extraire la sous-chaîne qui contient uniquement le JSON
        pure_json_str = text_json[json_start:end_index].strip()
        #print(pure_json_str)
        try:
            # Charger la chaîne JSON dans un dictionnaire Python
            chantier_info = json.loads(pure_json_str)

            #print("JSON extrait et chargé dans un dictionnaire Python :")
            #print(chantier_info)
            #print(f"\nType de l'objet : {type(chantier_info)}")

            # Vous pouvez maintenant accéder aux données comme un dictionnaire normal
            keys_to_display = [
            'Nom Chantier',
            'Lieu du Chantier',
            'Maitre ouvrage',
            'Maitre oeuvre' , 
            'Type de Travaux',
            'Planning previsionnel',
            'Durée Prévisionnelle des Travaux (en mois)',
            'Prix des travaux (en euros)',
            'Categorie operation SPS'
            ]

            print("\nAccès aux données extraites :")
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

def loadpdf_as_text(file_path, ocr_threshold=20):
    """
    Extract text from a PDF file. If a page contains little or no text,
    perform OCR to extract text from images (for scanned PDFs).
    :param file_path: Path to the PDF file.
    :param ocr_threshold: Minimum number of characters to consider a page as 'textual'.
    :return: Extracted text as a string.
    """
    text_extract = ""
    if os.path.exists(file_path):
        try:
            doc = fitz.open(file_path)
            for page_num in range(doc.page_count):
                page = doc.load_page(page_num)
                text = page.get_text()
                # If not enough text, try OCR
                if len(text.strip()) < ocr_threshold:
                    # Render page as image
                    pix = page.get_pixmap(dpi=300)
                    img = Image.open(io.BytesIO(pix.tobytes("png")))
                    text = pytesseract.image_to_string(img, lang='fra')  # or 'fra' for French
                text_extract += text + "\n"
            doc.close()
            return text_extract
        except Exception as e:
            print(f"Error processing PDF file: {e}")
            return text_extract
    else:
        print(f"Error: File not found at {file_path}")
        return text_extract


def path_to_link(file_path, option=None):
    full_path = file_path.strip()
    nb_segment = file_path.split("\\")
    file_name = nb_segment[-1].strip()
    if os.path.exists(full_path.strip()):
        nb_segment = file_path.split("\\")
        file_name = nb_segment[-1].strip()
        file_url = 'file:///' + full_path.replace('\\', '/')
        if option == None:
            display(HTML(f'<a href="{file_url}">{file_path}</a>'))
        elif option == "link":
            display(HTML(f'<a href="{file_url}">Link</a>'))
        elif option == "name":
            display(HTML(f'<a href="{file_url}">{file_name}</a>'))
        else:
            print("warning: Option not valid")
            display(HTML(f'<a href="{file_url}">{file_path}</a>'))
    else:
        print("warning: Fichier non accessible")


def update_df_with_json_cctp(json_string, ebp_id, df_update):
    try:
        parsed_json = json.loads(json_string)
        
        # Extrait chaque clef
        nom_value = parsed_json.get("Nom Chantier")
        lieu_value = parsed_json.get("Lieu du Chantier")
        type_travaux_value = parsed_json.get("Type de Travaux")
        planning_concept_value = parsed_json.get("Planning phase conception")
        planning_real_value = parsed_json.get("Planning phase realistion")
        duree_travaux_value = parsed_json.get("Duree des travaux")
        prix_travaux_value = parsed_json.get("Prix des travaux")
        cat_sps_value = parsed_json.get("Categorie operation SPS")
        moa_value = parsed_json.get("Maitre ouvrage")
        moe_value = parsed_json.get("Maitre oeuvre")

        # Mise à jour du df_consult_elevated
        mask = df_update['ID EBP'] == ebp_id
        if nom_value is not None:
            df_update.loc[mask, 'nom_chantier'] = nom_value
        if lieu_value is not None and not isinstance(lieu_value, list):
            df_update.loc[mask, 'lieu'] = lieu_value
        if type_travaux_value is not None and not isinstance(type_travaux_value, list):
            df_update.loc[mask, 'type travaux'] = type_travaux_value
        if duree_travaux_value is not None and not isinstance(duree_travaux_value, list):
            df_update.loc[mask, 'duree travaux'] = duree_travaux_value
        if planning_concept_value is not None and not isinstance(planning_concept_value, list):
            df_update.loc[mask, 'planning conception'] = planning_concept_value
        if planning_real_value is not None and not isinstance(planning_real_value, list):
            df_update.loc[mask, 'planning realisation '] = planning_real_value
        if prix_travaux_value is not None and not isinstance(prix_travaux_value, list):
            df_update.loc[mask, 'prix travaux'] = prix_travaux_value
        if moa_value is not None and not isinstance(moa_value, list):
            df_update.loc[mask, 'maitre ouvrage'] = moa_value
        if moe_value is not None and not isinstance(moe_value, list):
            df_update.loc[mask, 'maitre oeuvre'] = moe_value
        if cat_sps_value is not None and not isinstance(cat_sps_value, list):
            df_update.loc[mask, 'Categorie operation SPS'] = cat_sps_value
    
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON string: {e}")
    except TypeError:
        print("Input is not a string.") 
    
format_json_regl = {
    "Critere Prix": 0,
    "Critere Technique": {
        "Moyen Humain et Experience" : 0,
        "Methodologie" : 0,
        "Cohérence du temps" : 0
    }
} 

def update_df_with_json_regl(json_string, ebp_id, df_update):
    parsed_json = json.loads(json_string)
    prix = parsed_json.get("Critere Prix")
    technique = parsed_json.get("Critere Technique")
    """
    parsed_tech = json.loads(technique)
    moyen_humain = parsed_tech.get("Moyen Humain et Experience")
    methodologie = technique["Methodologie"]
    coherence_temps = technique["Cohérence du temps"]
    """
    # Mise à jour du df_consult_elevated
    mask = df_update['ID EBP'] == ebp_id
    if prix is not None:
        df_update.loc[mask, 'Critere Prix'] = prix
    if technique is not None:
        df_update.loc[mask, 'Critere Tech'] = technique

    """
    if moyen_humain is not None:
        df_update.loc[mask, 'Critere Tech-Humain'] = moyen_humain
    if methodologie is not None:
        df_update.loc[mask, 'Critere Tech-Method'] = methodologie
    if coherence_temps is not None:
        df_update.loc[mask, 'Critere Tech-Temps'] = coherence_temps
    """

def update_df_with_json_aapc(json_string, ebp_id, df_update):
    
    parsed_json = json.loads(json_string)

    Mission = parsed_json.get("Mission")
    lieu = parsed_json.get("Lieu du Chantier")
    m_ouvrage = parsed_json.get("Maitre ouvrage")
    Lot = parsed_json.get("Lot")
    Tranche = parsed_json.get("Tranche")
    prix_travaux = parsed_json.get("Prix des travaux")
    Duree_travaux = parsed_json.get("Duree des travaux")
    cpv = parsed_json.get("Classification CPV")

    # Mise à jour du df_consult_elevated
    mask = df_update['ID EBP'] == ebp_id
    if Mission is not None:
        df_update.loc[mask, 'Mission aapc'] = Mission
    if lieu is not None:
        df_update.loc[mask, 'lieu aapc'] = lieu
    if m_ouvrage is not None:
        df_update.loc[mask, 'm_ouvrage aapc'] = m_ouvrage
    if Lot is not None:
        df_update.loc[mask, 'Lot aapc'] = Lot
    if Tranche is not None:
        df_update.loc[mask, 'Tranche aapc'] = Tranche
    if prix_travaux is not None:
        df_update.loc[mask, 'prix_travaux aapc'] = prix_travaux
    if Duree_travaux is not None:
        df_update.loc[mask, 'Duree_travaux aapc'] = Duree_travaux
    if cpv is not None:
        df_update.loc[mask, 'cpv'] = cpv

def update_df_with_json_ccap(json_string, ebp_id, df_update):
    
    parsed_json = json.loads(json_string)

    objet = parsed_json.get("Objet du marché")  
    lieu = parsed_json.get("Lieu du Chantier")
    m_ouvrage = parsed_json.get("Maitre ouvrage")
    m_oeuvre = parsed_json.get("Maitre oeuvre")
    Lot = parsed_json.get("Lot")
    Tranche = parsed_json.get("Tranche")

    # Mise à jour du df_consult_elevated
    mask = df_update['ID EBP'] == ebp_id
    if objet is not None:
        df_update.loc[mask, 'objet ccap'] = objet
    if lieu is not None:
        df_update.loc[mask, 'lieu ccap'] = lieu
    if m_ouvrage is not None:
        df_update.loc[mask, 'm_ouvrage ccap'] = m_ouvrage
    if m_oeuvre is not None:
        df_update.loc[mask, 'm_oeuvre ccap'] = m_oeuvre
    if Lot is not None:
        df_update.loc[mask, 'Lot ccap'] = Lot
    if Tranche is not None:
        df_update.loc[mask, 'Tranche ccap'] = Tranche
    