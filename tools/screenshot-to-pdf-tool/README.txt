# 📸 Automated Course Slide Capture & PDF Converter

This tool automates the process of capturing educational course slides, turning pages automatically, and compiling them into a single **Searchable PDF**.

It includes "Smart Detection" to handle stuck pages, duplicate slides, and inactive "Next" buttons.

## ✨ Features
* **Auto-Navigation:** Automatically clicks the "Next" button to advance slides.
* **Smart Validation:** Checks if the page actually turned before capturing.
* **Stuck Page Handling:** Prompts the user if the script gets stuck or if the button is disabled.
* **Searchable PDF:** Uses Tesseract OCR to convert images into text-selectable PDFs (great for NotebookLM).
* **High-Quality Capture:** Forces DPI awareness to ensure sharp text on high-resolution monitors.

## 🛠️ Prerequisites

1.  **Python 3.x** installed.
2.  **Tesseract OCR** (Required for text-searchable PDFs).
    * [Download for Windows](https://github.com/UB-Mannheim/tesseract/wiki)
    * *Note the installation path (usually `C:\Program Files\Tesseract-OCR`)*.

## 📦 Installation

1.  Clone this repository or download the files.
2.  Install the required Python libraries:
    ```bash
    pip install -r requirements.txt
    ```

## 🚀 How to Use

### Step 1: Calibration (One-Time Setup)
Since every screen is different, you must tell the script where to look.

1.  Open your course in a browser.
2.  **Zoom In (`Ctrl` + `+`)** until the content fills the screen (this improves PDF clarity).
3.  Run the calibration tool (if included) or manually determine the coordinates for:
    * **Region:** The Top-Left `(x, y)` and `Width/Height` of the content box.
    * **Buttons:** The `(x, y)` coordinates of the "Next" button.
    * **Color:** The RGB color of the active "Next" button.

### Step 2: Update Configuration
Open `screenshot_tool.py` and update the **CONFIGURATION** section at the top:

```python
# Example Configuration
REGION_LEFT = 557
REGION_TOP = 81
REGION_WIDTH = 802
REGION_HEIGHT = 941

NEXT_BUTTONS = [
    (1304, 988),   # Primary Button Location
    (1295, 1021)   # Backup Button Location
]

CORRECT_COLOR = (131, 23, 26) # RGB Color of the active button
SEARCHABLE_PDF = True         # Set to False for faster, image-only PDF


### Basic CLI Usage (Defaults)
Run the tool without any arguments to use the default settings (OCR enabled, saving to `XCEL_Course_Material.pdf`).
```bash
python screenshot_tool.py

Option	    Short	Description	                                Default Value
--filename	-f	    Sets the name of the output PDF file.	    screenshot_output.pdf
--no-ocr	N/A	    Disables OCR/Text recognition (saves as 
                    standard images). If this flag is NOT 
                    used, OCR is enabled by default.    
                    OCR Enabled
--tesseract	-t	    Custom path to the tesseract.exe file 
                    if installed in a non-standard location.    C:\Program Files\Tesseract-OCR\tesseract.exe