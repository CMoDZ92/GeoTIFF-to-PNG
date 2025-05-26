import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import numpy as np

def copy_to_clipboard(root, text):
    root.clipboard_clear()
    root.clipboard_append(text)
    messagebox.showinfo("Copied", f"Copied to clipboard:\n{text}")

def show_heightscale_info(min_val, max_val, ideal_val):
    info_win = tk.Toplevel()
    info_win.title("Heightscale Info")
    info_win.geometry("300x180")

    tk.Label(info_win, text=f"Min Heightscale: {min_val}", font=("Arial", 12)).pack(pady=5)
    tk.Label(info_win, text=f"Max Heightscale: {max_val}", font=("Arial", 12)).pack(pady=5)
    tk.Label(info_win, text=f"Ideal Heightscale: {ideal_val:.2f}", font=("Arial", 12, "bold")).pack(pady=10)

    copy_btn = tk.Button(
        info_win,
        text="Copy Ideal Heightscale",
        command=lambda: copy_to_clipboard(info_win, f"{ideal_val:.2f}")
    )
    copy_btn.pack(pady=10)

def convert_tiff_to_png():
    tiff_path = filedialog.askopenfilename(
        filetypes=[("TIFF files", "*.tif *.tiff")],
        title="Select a TIFF file"
    )
    if not tiff_path:
        return

    save_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG files", "*.png")],
        title="Save PNG file as"
    )
    if not save_path:
        return

    try:
        img = Image.open(tiff_path)

        arr = np.array(img)
        min_val = arr.min()
        max_val = arr.max()
        ideal = (min_val + max_val) / 2

        norm_arr = ((arr - min_val) / (max_val - min_val) * 65535).astype(np.uint16)
        img_16bit = Image.fromarray(norm_arr, mode='I;16')
        img_16bit.save(save_path, "PNG")

        # Show heightscale info window with copy button
        show_heightscale_info(min_val, max_val, ideal)

    except Exception as e:
        messagebox.showerror("Error", f"Failed to convert image:\n{e}")

# Setup GUI
root = tk.Tk()
root.title("TIFF to 16-bit PNG Converter")
root.geometry("350x150")

label = tk.Label(root, text="Convert .TIFF to 16-bit .PNG", font=("Arial", 14))
label.pack(pady=10)

convert_button = tk.Button(root, text="Select and Convert", command=convert_tiff_to_png)
convert_button.pack(pady=20, ipadx=10, ipady=5)

root.configure(bg="#f0f0f0")
label.configure(bg="#f0f0f0", fg="#333333")
convert_button.configure(bg="#4CAF50", fg="white", activebackground="#45a049")


root.mainloop()
