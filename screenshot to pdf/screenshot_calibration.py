import pyautogui
import time
import ctypes

# --- FORCE HIGH QUALITY ---
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    ctypes.windll.user32.SetProcessDPIAware()

print("--- SETUP TOOL: CAPTURE ACTIVE COLOR ---")
print("Switch to your browser window NOW.")

# --- STEP 1: TOP-LEFT ---
print("\n[STEP 1/5] Hover over TOP-LEFT of blue box.")
print("Recording in 5 seconds...", end="", flush=True)
for i in range(5, 0, -1):
    print(f" {i}...", end="", flush=True)
    time.sleep(1)
x1, y1 = pyautogui.position()
print(f"\n✅ Top-Left: ({x1}, {y1})")

# --- STEP 2: BOTTOM-RIGHT ---
print("\n[STEP 2/5] Hover over BOTTOM-RIGHT of blue box.")
print("Recording in 5 seconds...", end="", flush=True)
for i in range(5, 0, -1):
    print(f" {i}...", end="", flush=True)
    time.sleep(1)
x2, y2 = pyautogui.position()
print(f"\n✅ Bottom-Right: ({x2}, {y2})")

# --- STEP 3: BUTTON #1 ---
print("\n[STEP 3/5] Hover over PRIMARY 'Next' button.")
print("Recording in 5 seconds...", end="", flush=True)
for i in range(5, 0, -1):
    print(f" {i}...", end="", flush=True)
    time.sleep(1)
btn1_x, btn1_y = pyautogui.position()
print(f"\n✅ Button #1: ({btn1_x}, {btn1_y})")

# --- STEP 4: BUTTON #2 ---
print("\n[STEP 4/5] Hover over SECONDARY 'Next' button (or same spot).")
print("Recording in 5 seconds...", end="", flush=True)
for i in range(5, 0, -1):
    print(f" {i}...", end="", flush=True)
    time.sleep(1)
btn2_x, btn2_y = pyautogui.position()
print(f"\n✅ Button #2: ({btn2_x}, {btn2_y})")

# --- STEP 5: CORRECT (ACTIVE) COLOR ---
print("\n[STEP 5/5] Hover over the RED/ACTIVE 'Next' button.")
print("Recording in 5 seconds...", end="", flush=True)
for i in range(5, 0, -1):
    print(f" {i}...", end="", flush=True)
    time.sleep(1)
color_x, color_y = pyautogui.position()
pixel_color = pyautogui.screenshot().getpixel((color_x, color_y))
print(f"\n✅ Captured Active Color: {pixel_color}")

# --- OUTPUT ---
width = x2 - x1
height = y2 - y1

print("\n" + "="*50)
print(f"REGION_LEFT = {x1}")
print(f"REGION_TOP = {y1}")
print(f"REGION_WIDTH = {width}")
print(f"REGION_HEIGHT = {height}")
print("")
print("NEXT_BUTTONS = [")
print(f"    ({btn1_x}, {btn1_y}),")
print(f"    ({btn2_x}, {btn2_y})")
print("]")
print("")
print(f"CORRECT_COLOR = {pixel_color}")
print("="*50)