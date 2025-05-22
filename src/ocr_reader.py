import easyocr

def load_reader(lang_list=None):
    """
    Initializes the EasyOCR reader with given language list.
    """
    if lang_list is None:
        lang_list = ['ru']
    return easyocr.Reader(lang_list)

def read_text(reader, image_path):
    """
    Performs OCR on the image using EasyOCR.
    """
    return reader.readtext(image_path)
