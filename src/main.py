from ocr_reader import load_reader, read_text
from utils import plot_easyocr_boxes

IMAGE_PATH = 'images/6.png'

def main():
    reader = load_reader(['ru'])
    result = read_text(reader, IMAGE_PATH)
    plot_easyocr_boxes(IMAGE_PATH, result)

if __name__ == '__main__':
    main()
