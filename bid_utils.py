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

"""
def loadpdf_as_text(file_path):
    text_extract = ""
    if os.path.exists(file_path):
        try:
            doc = fitz.open(file_path)
            for page_num in range(doc.page_count):
                page = doc.load_page(page_num)
                text_extract += page.get_text()
            doc.close()
            return text_extract
        except Exception as e:
            print(f"Error processing PDF file: {e}")
            return text_extract
    else:
        print(f"Error: File not found at {file_path}")
        return text_extract
"""

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

