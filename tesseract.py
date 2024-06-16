from PIL import Image
import pytesseract

def parse():
    # Load the image with PIL
    img = Image.open('table.png')

    # Convert the image to grayscale
    img = img.convert('L')

    # Save the grayscale image
    img.save('table_gray.png')

    # Perform OCR on the image
    text = pytesseract.image_to_string(Image.open('table_gray.png'))
    
    # Print the extracted text
    print(text)