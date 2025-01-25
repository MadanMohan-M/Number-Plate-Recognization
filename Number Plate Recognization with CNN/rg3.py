import cv2
import numpy as np
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, messagebox

def preprocess_image(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 30, 150)
    return image, edged

def detect_number_plate(image, edged_image):
    contours, _ = cv2.findContours(edged_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        aspect_ratio = w / h
        
        if 2 < aspect_ratio < 6:
            plate_image = image[y:y+h, x:x+w]
            plate_image_path = "detected_number_plate.jpg"
            cv2.imwrite(plate_image_path, plate_image)
            return plate_image_path
    return None

def upload_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        image, edged_image = preprocess_image(file_path)
        plate_image_path = detect_number_plate(image, edged_image)
        
        if plate_image_path:
            result_label.config(text="Detected Number Plate Image:")
            
            # Load and display the plate image
            plate_image = Image.open(plate_image_path)
            plate_image = plate_image.resize((250, 100))
            plate_image_tk = ImageTk.PhotoImage(plate_image)
            image_label.config(image=plate_image_tk)
            image_label.image = plate_image_tk
            
            # Enable the save button
            save_button.config(state=tk.NORMAL)
        else:
            messagebox.showinfo("No Plate Detected", "No number plate detected in the image.")

def save_image():
    file_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg"), ("All files", "*.*")])
    if file_path:
        plate_image_path = "detected_number_plate.jpg"
        plate_image = Image.open(plate_image_path)
        plate_image.save(file_path)
        messagebox.showinfo("Image Saved", f"Image saved as {file_path}")

def create_gui():
    global result_label, image_label, save_button
    
    window = tk.Tk()
    window.title("Number Plate Recognition")
    
    upload_button = tk.Button(window, text="Upload Image", command=upload_image)
    upload_button.pack(pady=20)
    
    result_label = tk.Label(window, text="Detected Number Plate Image:")
    result_label.pack(pady=10)
    
    image_label = tk.Label(window)
    image_label.pack(pady=10)
    
    save_button = tk.Button(window, text="Save Image", command=save_image, state=tk.DISABLED)
    save_button.pack(pady=20)
    
    window.mainloop()

if __name__ == "__main__":
    create_gui()
