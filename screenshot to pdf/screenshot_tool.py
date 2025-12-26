import pyautogui
import time
import os
import io
import ctypes
import pytesseract
from PIL import Image, ImageChops

# Try to import pypdf for the OCR feature
try:
    from pypdf import PdfWriter, PdfReader
    HAS_PYPDF = True
except ImportError:
    HAS_PYPDF = False

# --- FORCE HIGH QUALITY (SHARPNESS) ---
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    ctypes.windll.user32.SetProcessDPIAware()

# ================= CONFIGURATION =================
# 1. COORDINATES
REGION_LEFT = 557
REGION_TOP = 81
REGION_WIDTH = 802
REGION_HEIGHT = 941

# 2. BUTTON LOCATIONS
NEXT_BUTTONS = [
    (1304, 988),   # Priority 1
    (1295, 1021)   # Priority 2
]

# 3. COLOR CHECK
CORRECT_COLOR = (131, 23, 26)

# 4. OCR SETTINGS (INTEGRATED)
SEARCHABLE_PDF = True  # Set to True for text-selectable PDF
TESSERACT_PATH = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# 5. GENERAL SETTINGS
PAGE_LOAD_DELAY = 2 
FILE_NAME = "XCEL_Course_Material.pdf"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FULL_OUTPUT_PATH = os.path.join(SCRIPT_DIR, FILE_NAME)

# Setup Tesseract
if SEARCHABLE_PDF:
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH
# =================================================

def images_are_identical(img1, img2):
    if img1 is None or img2 is None:
        return False
    diff = ImageChops.difference(img1, img2)
    return diff.getbbox() is None

def create_searchable_pdf(image_list, output_path):
    """
    Function to convert a list of images into a single searchable PDF.
    """
    if not HAS_PYPDF:
        print("❌ Error: 'pypdf' library not found. Run 'pip install pypdf'.")
        return False

    if not os.path.exists(TESSERACT_PATH):
        print(f"❌ Error: Tesseract not found at {TESSERACT_PATH}")
        return False

    print(f"🚀 Processing OCR for {len(image_list)} pages...")
    
    try:
        pdf_writer = PdfWriter()
        
        for i, img in enumerate(image_list):
            print(f"   > Converting Page {i+1} to text...")
            
            # 1. Get a single page PDF bytes from Tesseract
            page_pdf_bytes = pytesseract.image_to_pdf_or_hocr(img, extension='pdf')
            
            # 2. Read it into a PdfReader object
            # (We use io.BytesIO to treat the bytes like a file in memory)
            pdf_reader = PdfReader(io.BytesIO(page_pdf_bytes))
            
            # 3. Add the page to our writer
            pdf_writer.add_page(pdf_reader.pages[0])

        # 4. Write the final big file
        with open(output_path, "wb") as f:
            pdf_writer.write(f)
            
        print(f"✅ SUCCESS! Searchable PDF saved to: {output_path}")
        return True

    except Exception as e:
        print(f"❌ OCR Conversion Failed: {e}")
        return False

def main():
    captured_images = []
    page_counter = 1

    print(f"Starting in 5 seconds...")
    mode_name = "Searchable OCR" if (SEARCHABLE_PDF and HAS_PYPDF) else "Standard Image"
    print(f"Mode: {mode_name}")
    print(f"Saving to: {FULL_OUTPUT_PATH}")
    print("Switch to your browser window NOW.")
    time.sleep(5)

    try:
        while True:
            print(f"Processing Page {page_counter}...")

            # --- 1. CAPTURE PAGE IMMEDIATELY ---
            current_screenshot = pyautogui.screenshot(region=(REGION_LEFT, REGION_TOP, REGION_WIDTH, REGION_HEIGHT))
            current_screenshot = current_screenshot.convert("RGB")

            # --- 2. CHECK BUTTONS COLOR ---
            active_button = None
            for index, (btn_x, btn_y) in enumerate(NEXT_BUTTONS):
                pyautogui.moveTo(btn_x, btn_y)
                time.sleep(0.2) 

                if pyautogui.pixelMatchesColor(btn_x, btn_y, CORRECT_COLOR, tolerance=25):
                    print(f"  > Button #{index + 1} is ACTIVE.")
                    active_button = (btn_x, btn_y)
                    break 
                else:
                    print(f"  > Button #{index + 1} is inactive...")

            # --- 3. IF BUTTON ERROR (NO BUTTON FOUND) ---
            if active_button is None:
                print(f">> PAUSE: No active buttons found.")
                
                choice = pyautogui.confirm(
                    text='All "Next" buttons have the wrong color.\n\nChoose an action:', 
                    title='Button Error', 
                    buttons=['I Fixed It', 'End (Add Page)', 'End (Discard)']
                )

                last_pdf_page = captured_images[-1] if captured_images else None

                if choice == 'I Fixed It':
                    if not images_are_identical(current_screenshot, last_pdf_page):
                        print("   > Page is NEW. Adding to PDF.")
                        captured_images.append(current_screenshot)
                        continue 
                    else:
                        print("   > Page is DUPLICATE. Prompting again.")
                        sub_choice = pyautogui.confirm(
                            text='Captured page matches the previous page.\n\nWhat would you like to do?', 
                            title='Duplicate Page', 
                            buttons=['Try Again (Recapture)', 'End (Add Page)', 'End (Discard)']
                        )

                        if sub_choice == 'Try Again (Recapture)':
                            time.sleep(0.5)
                            recaptured_shot = pyautogui.screenshot(region=(REGION_LEFT, REGION_TOP, REGION_WIDTH, REGION_HEIGHT))
                            recaptured_shot = recaptured_shot.convert("RGB")
                            
                            if not images_are_identical(recaptured_shot, last_pdf_page):
                                print("   > New capture is valid. Adding.")
                                captured_images.append(recaptured_shot)
                            else:
                                print("   > New capture is still duplicate. Ignoring.")
                            continue

                        elif sub_choice == 'End (Add Page)':
                            captured_images.append(current_screenshot)
                            break
                        elif sub_choice == 'End (Discard)':
                            break

                elif choice == 'End (Add Page)':
                    captured_images.append(current_screenshot)
                    break 

                elif choice == 'End (Discard)':
                    break

            # --- 4. HAPPY PATH ---
            captured_images.append(current_screenshot)

            click_x, click_y = active_button
            pyautogui.click(click_x, click_y)
            time.sleep(PAGE_LOAD_DELAY)
            
            # --- 5. VERIFY PAGE TURN ---
            new_state = pyautogui.screenshot(region=(REGION_LEFT, REGION_TOP, REGION_WIDTH, REGION_HEIGHT))
            new_state = new_state.convert("RGB")
            
            if images_are_identical(current_screenshot, new_state):
                print("\n🛑 STUCK! Page did not turn.")
                choice = pyautogui.confirm(
                    text="Screen didn't change after clicking.\n\nChoose an action:", 
                    title="Script Stuck", 
                    buttons=['I Fixed It (Resume)', 'End (Add Page)', 'End (Discard)']
                )
                
                if choice == 'End (Add Page)':
                    break
                elif choice == 'End (Discard)':
                    if captured_images:
                        captured_images.pop()
                    break
                
                time.sleep(2)
            else:
                 print("    ✅ Page changed successfully.")

            page_counter += 1

    except KeyboardInterrupt:
        print("\nStopping capture...")
    
    # --- SAVE LOGIC ---
    if not captured_images:
        print("No images captured. Exiting.")
        return

    print(f"\nSaving {len(captured_images)} pages...")
    
    # 1. Attempt Searchable PDF
    success = False
    if SEARCHABLE_PDF:
        success = create_searchable_pdf(captured_images, FULL_OUTPUT_PATH)
    
    # 2. Fallback to Standard PDF if OCR failed or was disabled
    if not success:
        if SEARCHABLE_PDF:
            print("⚠️ Falling back to Standard Image PDF...")
        
        try:
            captured_images[0].save(
                FULL_OUTPUT_PATH, 
                "PDF", 
                resolution=100.0, 
                save_all=True, 
                append_images=captured_images[1:],
                quality=100, 
                subsampling=0
            )
            print(f"✅ SUCCESS! Standard PDF saved to: {FULL_OUTPUT_PATH}")
        except Exception as e:
            print(f"❌ Error saving PDF: {e}")

if __name__ == "__main__":
    main()