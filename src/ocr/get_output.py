from Pocket_Doctor.src.ocr.ocr_reader import load_reader, read_text
from Pocket_Doctor.src.ocr.utils import get_plot, easyocr_to_json


def get_output(image_path):
    reader = load_reader(['ru'])
    result = read_text(reader, image_path)
    plot = get_plot(image_path, result)
    return easyocr_to_json(result), plot