import os
from PIL import Image
import pytesseract
from pytesseract import Output
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe" # Chemin vers tesseract.exe sur ton système

def image_to_pdf_ocr(image_path, pdf_canvas):
    """Ajoute une image + texte OCR à un PDF existant (canvas)."""
    img = Image.open(image_path)
    width, height = img.size

    # OCR avec positions
    data = pytesseract.image_to_data(img, output_type=Output.DICT)

    # Ajouter l’image en fond
    pdf_canvas.setPageSize((width, height))
    pdf_canvas.drawInlineImage(image_path, 0, 0, width=width, height=height)

    # Ajouter texte OCR invisible
    pdf_canvas.setFont("Helvetica", 8)
    pdf_canvas.setFillColorRGB(1, 1, 1, alpha=0)  # texte transparent
    for i in range(len(data["text"])):
        if int(data["conf"][i]) > 60:  # ignorer texte peu fiable
            x, y, w, h = data["left"][i], data["top"][i], data["width"][i], data["height"][i]
            pdf_canvas.drawString(x, height - y - h, data["text"][i])

    pdf_canvas.showPage()


def images_to_pdf_ocr(input_folder, output_filepath):
    """Convertit toutes les images d’un dossier en un PDF OCR."""
    pdf_canvas = canvas.Canvas(output_filepath)

    # Trier les fichiers pour garder l’ordre
    images = sorted(
        [f for f in os.listdir(input_folder) if f.lower().endswith((".png", ".jpg", ".jpeg", ".tif"))]
    )

    for img_file in images:
        print(f"Traitement : {img_file}")
        image_path = os.path.join(input_folder, img_file)
        image_to_pdf_ocr(image_path, pdf_canvas)

    pdf_canvas.save()
    print(f"✅ PDF OCR généré : {output_filepath}")


# Exemple d’utilisation
if __name__ == "__main__":
    dossier = r"C:\Users\user\Desktop\github\web_image_downloader\images\data_standardization"      # dossier contenant tes images
    sortie = r"C:\Users\user\Desktop\github\web_image_downloader\images\data_standardization\data_standardization.pdf"      # chemin de sortie du PDF OCR
    images_to_pdf_ocr(dossier, sortie)