from ocr_reader import load_reader, read_text
from utils import get_plot


def get_output(image_path):
    reader = load_reader(['ru'])
    result = read_text(reader, image_path)
    plot = get_plot(image_path, result)
    return result, plot