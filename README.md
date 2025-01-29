# Advanced OCR GUI Application

A powerful and user-friendly Optical Character Recognition (OCR) application built with Python and Tkinter. This application supports multiple languages, can process both images and PDF files, and includes image preprocessing capabilities for improved accuracy.

## Features

- Support for multiple image formats (PNG, JPG, JPEG, TIFF, BMP)
- PDF document processing with multi-page support
- Multi-language OCR capabilities
- Automatic language detection
- Image preprocessing for better OCR results
- Real-time processing progress tracking
- Preview window for images
- Easy-to-use graphical interface
- Text export functionality

## Prerequisites

Before running the application, ensure you have the following installed:

1. Python 3.7 or higher
2. Tesseract OCR engine
3. Poppler (for PDF processing)

## Required Python Packages

```bash
pip install pytesseract
pip install Pillow
pip install pdf2image
pip install langdetect
```

## Installation Steps

1. Install Tesseract OCR:
   - Windows: Download and install from [GitHub Tesseract Release](https://github.com/UB-Mannheim/tesseract/wiki)
   - Linux: `sudo apt-get install tesseract-ocr`
   - macOS: `brew install tesseract`

2. Install Poppler:
   - Windows: Download from [Poppler Release](http://blog.alivate.com.au/poppler-windows/) and add to PATH
   - Linux: `sudo apt-get install poppler-utils`
   - macOS: `brew install poppler`

3. Clone this repository or download the source code.

4. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. Update the Poppler path in the code if necessary:
   ```python
   self.poppler_path = r"C:\Program Files\poppler-24.08.0\bin"  # Adjust as needed
   ```

2. Ensure Tesseract is properly installed and accessible from your system's PATH.

## Usage

1. Run the application:
   ```bash
   python ocr_gui.py
   ```

2. Using the application:
   - Select one or more languages from the language list
   - Click "Select Image" or "Select PDF" to choose a file
   - Click "Process" to start OCR
   - Use "Save Text" to export the extracted text

## Supported Languages

The application supports various languages including:
- English
- French
- German
- Spanish
- Chinese (Simplified and Traditional)
- Japanese
- Korean
- Arabic
- Russian
- Hindi
- And more...

## Image Preprocessing

The application automatically applies the following preprocessing steps to improve OCR accuracy:
- Conversion to grayscale
- Image sharpening
- Contrast enhancement

## Error Handling

The application includes comprehensive error handling for:
- File selection issues
- Processing errors
- Language detection problems
- File saving errors

All errors are logged and displayed to the user via message boxes.

## Performance Considerations

- Large PDF files may take longer to process
- Processing is done in a separate thread to keep the UI responsive
- Memory usage increases with PDF page count
- Image preprocessing may affect processing speed

## Troubleshooting

1. If OCR fails:
   - Ensure Tesseract is properly installed
   - Verify the selected languages are installed
   - Check if the image quality is sufficient

2. If PDF processing fails:
   - Verify Poppler is installed correctly
   - Check the Poppler path in the code
   - Ensure PDF is not corrupted or password-protected

3. If language detection issues occur:
   - Verify the image quality
   - Ensure text is clear and readable
   - Try selecting languages manually

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Tesseract OCR engine
- Python Pillow library
- pdf2image and poppler-utils
- langdetect library

## Future Improvements

Planned features and improvements:
1. Batch processing capabilities
2. Additional image preprocessing options
3. Custom language model support
4. OCR accuracy improvements
5. Advanced PDF handling options
6. Export to multiple formats
