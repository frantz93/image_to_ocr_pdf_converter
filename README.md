# Image to OCR PDF Converter

Small Python script to convert a folder of images into a searchable (OCR) PDF by placing each image as a page and writing invisible OCR text on top.

The script in this repository: `image_to_ocr-pdf_converter.py` uses:
- `pytesseract` (Tesseract OCR Python wrapper)
- `Pillow` (PIL) for image handling
- `reportlab` to generate the PDF

Key points
- The script currently sets `pytesseract.pytesseract.tesseract_cmd` to a Windows path. Update this if your Tesseract executable is installed elsewhere.
- It adds each image as a background and overlays invisible OCR text so the PDF becomes searchable.

Requirements
- Python 3.8+
- Tesseract OCR (external program) — install separately (see below)

Installation

1. (Optional) Create and activate a virtual environment in PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install Python dependencies:

```powershell
pip install -r requirements.txt
```

3. Install Tesseract OCR
- Windows: Download and install from https://github.com/tesseract-ocr/tesseract
- After installation, note the path of `tesseract.exe` (example: `C:\Program Files\Tesseract-OCR\tesseract.exe`).
- If needed, update the `pytesseract.pytesseract.tesseract_cmd` value at the top of `image_to_ocr-pdf_converter.py`.

Usage

- Edit the values at the bottom of `image_to_ocr-pdf_converter.py` (the `dossier` and `sortie` variables) to point to your input images folder and desired output PDF path.
- Supported image extensions: `.png`, `.jpg`, `.jpeg`, `.tif` (case-insensitive)
- Run the script:

```powershell
python image_to_ocr-pdf_converter.py
```

Notes and tips
- The script filters OCR data by confidence (`conf > 60`). You can adjust this threshold in the function `image_to_pdf_ocr`.
- The script sets page size equal to the image pixel dimensions; very large images may produce very large PDF pages. Resize images if necessary before conversion.
- If your images are scanned upside-down or rotated, consider running preprocessing (rotation/deskew) prior to OCR to improve accuracy.

License
- No license specified. Add a license file if you plan to publish.

Contact / Improvements
- If you'd like, I can add CLI options (input folder, output path, confidence threshold) or an argument parser to avoid editing the script directly.
# image_to_ocr_pdf_converter
Convert image to searchable pdf
