import os
from PIL import Image
import pytesseract
from pytesseract import Output
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

# Chemin vers tesseract.exe sur ton système
# Note: This might need to be configurable or checked
if os.path.exists(r"C:\Program Files\Tesseract-OCR\tesseract.exe"):
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def image_to_pdf_ocr(image_path, pdf_canvas):
    """Ajoute une image + texte OCR à un PDF existant (canvas)."""
    img = Image.open(image_path)
    width, height = img.size

    # OCR avec positions
    try:
        data = pytesseract.image_to_data(img, output_type=Output.DICT)
    except pytesseract.TesseractNotFoundError:
        print("Tesseract not found. Please install Tesseract-OCR and set the path.")
        return

    # Ajouter l’image en fond
    pdf_canvas.setPageSize((width, height))
    pdf_canvas.drawInlineImage(image_path, 0, 0, width=width, height=height)

    # Ajouter texte OCR invisible
    pdf_canvas.setFont("Helvetica", 8)
    pdf_canvas.setFillColorRGB(1, 1, 1, alpha=0)  # texte transparent
    if "text" in data:
        for i in range(len(data["text"])):
            if "conf" in data and int(data["conf"][i]) > 60:  # ignorer texte peu fiable
                x, y, w, h = data["left"][i], data["top"][i], data["width"][i], data["height"][i]
                pdf_canvas.drawString(x, height - y - h, data["text"][i])

    pdf_canvas.showPage()


def images_to_pdf_ocr(input_folder, output_filepath):
    """Convertit toutes les images d’un dossier en un PDF OCR."""
    c = canvas.Canvas(output_filepath)

    # Trier les fichiers pour garder l’ordre
    images = sorted(
        [f for f in os.listdir(input_folder) if f.lower().endswith((".png", ".jpg", ".jpeg", ".tif"))]
    )

    if not images:
        print(f"Aucune image trouvée dans {input_folder}")
        return

    for img_file in images:
        print(f"Traitement : {img_file}")
        image_path = os.path.join(input_folder, img_file)
        image_to_pdf_ocr(image_path, c)

    c.save()
    print(f"✅ PDF OCR généré : {output_filepath}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Convert images to OCR PDF")
    parser.add_argument("input_dir", help="Input directory containing images")
    parser.add_argument("output_file", help="Output PDF file path")
    
    args = parser.parse_args()
    
    images_to_pdf_ocr(args.input_dir, args.output_file)


if __name__ == "__main__":
    main()