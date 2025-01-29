# Advanced OCR (Optical Character Recognition) GUI Application
# A desktop application for extracting text from images and PDFs using Tesseract OCR
# Features include image preprocessing, PDF support, and a user-friendly interface

import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox  # GUI components
import pytesseract  # OCR engine
from PIL import Image, ImageTk, ImageEnhance, ImageFilter  # Image processing
import os
import logging
import threading
from pdf2image import convert_from_path  # PDF to image conversion

class OCRGUI:
    """
    Main GUI class for the OCR application.
    Handles the user interface, file processing, and OCR operations.
    """
    def __init__(self, root):
        # Initialize main window properties
        self.root = root
        self.root.title("Advanced OCR")
        self.root.geometry("1200x800")  # Set window size
        
        # Configure logging for debugging and error tracking
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        
        # Initialize instance variables
        self.current_image_path = None  # Path to selected file
        self.preview_image = None  # Holds the preview image reference
        self.poppler_path = r"C:\Program Files\poppler-24.08.0\bin"  # Required for PDF processing
        self.ocr_language = "eng"  # Default OCR language
        
        # Configure GUI styles
        self.style = ttk.Style()
        self.style.configure('Title.TLabel', font=('Helvetica', 14, 'bold'))
        self.style.configure('Header.TLabel', font=('Helvetica', 12, 'bold'))
        
        # Configure grid weights for responsive layout
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        self.create_gui()
        
    def create_gui(self):
        """Create and configure all GUI elements using grid layout"""
        # Title section
        title_label = ttk.Label(self.root, text="Optical Character Recognition for Documents", style='Title.TLabel')
        title_label.grid(row=0, column=0, pady=10, padx=10, sticky='w')
        
        # Main container frame
        main_frame = ttk.Frame(self.root)
        main_frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=(0, 10))
        
        # Configure main frame grid weights
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)
        
        # Left panel setup (preview and controls)
        left_panel = ttk.Frame(main_frame)
        left_panel.grid(row=0, column=0, padx=(0, 5), sticky='nsew')
        
        # Preview section
        ttk.Label(left_panel, text="Image Preview", style='Header.TLabel').grid(row=0, column=0, pady=(0, 5))
        
        preview_frame = ttk.Frame(left_panel, borderwidth=2, relief='solid')
        preview_frame.grid(row=1, column=0, sticky='nsew')
        
        # Canvas for image preview
        self.preview_canvas = tk.Canvas(preview_frame, width=400, height=400, bg='white')
        self.preview_canvas.grid(row=0, column=0, padx=2, pady=2)
        
        # Control buttons
        button_frame = ttk.Frame(left_panel)
        button_frame.grid(row=2, column=0, pady=10)
        
        ttk.Button(button_frame, text="Select Image", command=self.select_image).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Select PDF", command=self.select_pdf).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Process", command=self.process_file).grid(row=0, column=2, padx=5)
        ttk.Button(button_frame, text="Save Text", command=self.save_text).grid(row=0, column=3, padx=5)
        
        # OCR options section
        ocr_options_frame = ttk.Frame(left_panel)
        ocr_options_frame.grid(row=3, column=0, pady=10)
        
        ttk.Label(ocr_options_frame, text="OCR Language:", style='Header.TLabel').grid(row=0, column=0, padx=5)
        self.language_entry = ttk.Entry(ocr_options_frame)
        self.language_entry.insert(0, self.ocr_language)
        self.language_entry.grid(row=0, column=1, padx=5)
        
        # Right panel setup (text output)
        right_panel = ttk.Frame(main_frame)
        right_panel.grid(row=0, column=1, padx=(5, 0), sticky='nsew')
        right_panel.grid_columnconfigure(0, weight=1)
        right_panel.grid_rowconfigure(1, weight=1)
        
        ttk.Label(right_panel, text="Extracted Text", style='Header.TLabel').grid(row=0, column=0, pady=(0, 5))
        
        # Text output area
        output_frame = ttk.Frame(right_panel, borderwidth=2, relief='solid')
        output_frame.grid(row=1, column=0, sticky='nsew')
        
        output_frame.grid_columnconfigure(0, weight=1)
        output_frame.grid_rowconfigure(0, weight=1)
        
        self.text_output = scrolledtext.ScrolledText(
            output_frame,
            font=('Courier', 10),
            wrap=tk.WORD,
            width=50,
            height=30)
        self.text_output.grid(row=0, column=0, sticky='nsew', padx=2, pady=2)
        
        # Progress bar section
        progress_frame = ttk.Frame(self.root)
        progress_frame.grid(row=2, column=0, sticky='ew', padx=10, pady=(0, 5))
        
        progress_frame.grid_columnconfigure(1, weight=1)
        
        ttk.Label(progress_frame, text="Progress:").grid(row=0, column=0, padx=(0, 5))
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.grid(row=0, column=1, sticky='ew')
        
        # Status label
        self.status_label = ttk.Label(self.root, text="Ready", font=('Helvetica', 9, 'italic'))
        self.status_label.grid(row=3, column=0, pady=(0, 5))

    def preprocess_image(self, image):
        """
        Enhance image quality for better OCR results
        Args:
            image: PIL Image object
        Returns:
            Processed PIL Image object
        """
        image = image.convert('L')  # Convert to grayscale
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.5)  # Increase contrast
        image = image.filter(ImageFilter.SHARPEN)  # Sharpen image
        return image

    def select_image(self):
        """Handle image file selection dialog and display preview"""
        file_types = [('Image files', '*.png *.jpg *.jpeg *.tiff *.bmp'), ('All files', '*.*')]
        filename = filedialog.askopenfilename(filetypes=file_types)
        if filename:
            self.current_image_path = filename
            self.display_preview(filename)
            self.status_label.config(text=f"Selected: {os.path.basename(filename)}")
            
    def select_pdf(self):
        """Handle PDF file selection dialog"""
        file_types = [('PDF files', '*.pdf'), ('All files', '*.*')]
        filename = filedialog.askopenfilename(filetypes=file_types)
        if filename:
            self.current_image_path = filename
            self.status_label.config(text=f"Selected PDF: {os.path.basename(filename)}")
            self.preview_canvas.delete("all")
            self.preview_canvas.create_text(200, 200, text="PDF Document\n(Preview not available)", fill="gray")
            
    def display_preview(self, image_path):
        """
        Display scaled preview of selected image on canvas
        Args:
            image_path: Path to image file
        """
        try:
            image = Image.open(image_path)
            # Calculate scaling factor to maintain aspect ratio
            width_scale = 400 / image.width
            height_scale = 400 / image.height
            scale = min(width_scale, height_scale)
            
            new_width = int(image.width * scale)
            new_height = int(image.height * scale)
            
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            self.preview_image = ImageTk.PhotoImage(image)
            
            self.preview_canvas.delete("all")
            # Center the image on canvas
            x = (400 - new_width) // 2
            y = (400 - new_height) // 2
            self.preview_canvas.create_image(x, y, image=self.preview_image, anchor=tk.NW)
        except Exception as e:
            self.logger.error(f"Error displaying preview: {str(e)}")
            messagebox.showerror("Error", "Failed to display image preview")
            
    def process_file(self):
        """Validate inputs and start OCR processing in separate thread"""
        if not self.current_image_path:
            messagebox.showwarning("Warning", "Please select a file first")
            return
            
        self.ocr_language = self.language_entry.get()
        
        # Start processing in separate thread to keep UI responsive
        thread = threading.Thread(target=self._process_file_thread)
        thread.daemon = True
        thread.start()
        
    def _process_file_thread(self):
        """
        Main OCR processing function running in separate thread
        Handles both PDF and image files
        Updates progress bar and status during processing
        """
        try:
            self.root.after(0, lambda: self.status_label.config(text="Processing..."))
            self.progress_var.set(0)
            
            file_extension = os.path.splitext(self.current_image_path)[1].lower()
            ocr_config = f'--oem 3 --psm 3'  # OCR Engine Mode = 3 (Default), Page Segmentation Mode = 3 (Auto)
            
            # Handle PDF files
            if file_extension == '.pdf':
                images = convert_from_path(self.current_image_path, poppler_path=self.poppler_path)
                text_results = []
                for i, image in enumerate(images):
                    image = self.preprocess_image(image)
                    text = pytesseract.image_to_string(image, lang=self.ocr_language, config=ocr_config)
                    text_results.append(f"--- Page {i+1} ---\n{text}")
                    self.progress_var.set((i + 1) / len(images) * 100)
                final_text = '\n\n'.join(text_results)
            # Handle image files
            else:
                image = Image.open(self.current_image_path)
                image = self.preprocess_image(image)
                final_text = pytesseract.image_to_string(image, lang=self.ocr_language, config=ocr_config)
                self.progress_var.set(100)
            
            # Update UI with results
            self.root.after(0, self._update_text_output, final_text)
            self.root.after(0, lambda: self.status_label.config(text="Processing complete"))
            
        except Exception as e:
            self.logger.error(f"Error processing file: {str(e)}")
            self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to process file: {str(e)}"))
            self.root.after(0, lambda: self.status_label.config(text="Error processing file"))
            
    def _update_text_output(self, text):
        """Update text output widget with OCR results"""
        self.text_output.delete(1.0, tk.END)
        self.text_output.insert(tk.END, text)
        
    def save_text(self):
        """Save extracted text to a file"""
        if not self.text_output.get(1.0, tk.END).strip():
            messagebox.showwarning("Warning", "No text to save")
            return
            
        file_types = [('Text files', '*.txt'), ('All files', '*.*')]
        filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=file_types)
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(self.text_output.get(1.0, tk.END))
                self.status_label.config(text=f"Saved to: {os.path.basename(filename)}")
            except Exception as e:
                self.logger.error(f"Error saving file: {str(e)}")
                messagebox.showerror("Error", f"Failed to save file: {str(e)}")

def main():
    """Application entry point"""
    root = tk.Tk()
    app = OCRGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()