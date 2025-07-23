import json
from ocr_reader import load_reader, read_text
from utils import plot_easyocr_boxes, easyocr_to_json

IMAGE_PATH = 'images/BLD.jpg'
OUTPUT_JSON = 'output/ocr_result.json'

def main():
    # Load OCR reader for Russian language
    reader = load_reader(['ru'])

    # Run OCR
    result = read_text(reader, IMAGE_PATH)

    # Show result with bounding boxes
    plot_easyocr_boxes(IMAGE_PATH, result)

    # Convert to JSON-serializable format
    json_data = easyocr_to_json(result)

    # Save to JSON file
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)

    print(f"OCR results saved to {OUTPUT_JSON}")

if __name__ == '__main__':
    main()
