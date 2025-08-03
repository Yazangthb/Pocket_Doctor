import json
from ocr_reader import load_reader, read_text
from utils import plot_easyocr_boxes, easyocr_to_json, easyocr_to_text, easyocr_to_structured_text

IMAGE_PATH = 'images/1.jpg'
OUTPUT_JSON = 'output/ocr_result1.json'
OUTPUT_TEXT = 'output/ocr_text1.txt'

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

    # Convert to plain text
    plain_text = easyocr_to_structured_text(result)

    # Save to text file
    with open(OUTPUT_TEXT, 'w', encoding='utf-8') as f:
        f.write(plain_text)
    print(f"OCR text saved to {OUTPUT_TEXT}")

if __name__ == '__main__':
    main()
