import cv2
import matplotlib.pyplot as plt
import numpy as np
import json

def plot_easyocr_boxes(image_path, ocr_result):
    """
    Plots bounding boxes and recognized text from EasyOCR results on the image.
    """
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    for detection in ocr_result:
        box, text, score = detection
        box = np.array(box).astype(int)
        cv2.polylines(image, [box], isClosed=True, color=(0, 255, 0), thickness=2)

    plt.figure(figsize=(12, 8))
    plt.imshow(image)
    plt.axis('off')
    plt.title("Detected Text with Bounding Boxes")
    plt.show()

def get_plot(image_path, ocr_result):
    """
    Plots bounding boxes and recognized text from EasyOCR results on the image.
    """
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    for detection in ocr_result:
        box, text, score = detection
        box = np.array(box).astype(int)
        cv2.polylines(image, [box], isClosed=True, color=(0, 255, 0), thickness=2)

    return image


def easyocr_to_json(ocr_result):
    """
    Converts EasyOCR output to a JSON-serializable structure.

    Args:
        ocr_result (list): Output from easyocr.Reader().readtext()

    Returns:
        list: List of dicts with 'text' and 'bbox' keys.
    """
    output = []
    for detection in ocr_result:
        box, text, score = detection
        bbox = [[int(point[0]), int(point[1])] for point in box]  # convert np.int32 to int
        output.append({
            "text": text,
            "bbox": bbox,
            "confidence": float(score)
        })
    return output

def easyocr_to_text(ocr_result):
    """
    Converts EasyOCR output to a plain text string without bbox or confidence info.

    Args:
        ocr_result (list): Output from easyocr.Reader().readtext()

    Returns:
        str: Concatenated text from OCR results.
    """
    lines = []
    for detection in ocr_result:
        _, text, _ = detection
        if text.strip():  # Optional: skip empty strings
            lines.append(text.strip())
    return "\n".join(lines)

def easyocr_to_structured_text(ocr_result, line_threshold=15, space_scale=10):
    """
    Converts EasyOCR output to structured text with layout preserved.

    Args:
        ocr_result (list): EasyOCR output [(bbox, text, confidence), ...]
        line_threshold (int): Max vertical distance between words on the same line
        space_scale (int): Number of pixels per space character

    Returns:
        str: Visually structured plain text
    """
    import numpy as np

    # Prepare list of entries with avg y and x positions
    entries = []
    for bbox, text, _ in ocr_result:
        x_coords = [p[0] for p in bbox]
        y_coords = [p[1] for p in bbox]
        avg_y = sum(y_coords) / len(y_coords)
        avg_x = min(x_coords)
        entries.append({'text': text, 'y': avg_y, 'x': avg_x})

    # Sort entries top to bottom
    entries.sort(key=lambda x: x['y'])

    # Group by lines
    lines = []
    current_line = []
    last_y = None

    for entry in entries:
        if last_y is None or abs(entry['y'] - last_y) <= line_threshold:
            current_line.append(entry)
        else:
            lines.append(current_line)
            current_line = [entry]
        last_y = entry['y']
    if current_line:
        lines.append(current_line)

    # Sort each line left to right, and format with indentation
    output_lines = []
    for line in lines:
        line.sort(key=lambda x: x['x'])
        line_text = ''
        last_x = 0
        for word in line:
            spaces = int((word['x'] - last_x) / space_scale)
            line_text += ' ' * max(spaces, 1) + word['text']
            last_x = word['x'] + len(word['text']) * space_scale // 2  # Estimate next start
        output_lines.append(line_text.strip())

    return '\n'.join(output_lines)



from PIL import Image, ImageDraw, ImageFont

def plot_easyocr_boxes(image_path, ocr_result):
    """
    Plots bounding boxes and recognized Russian text from EasyOCR results on the image.
    """
    # Load image with OpenCV and convert to RGB
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Convert to PIL for text rendering
    pil_img = Image.fromarray(image)
    draw = ImageDraw.Draw(pil_img)

    # Try to load a font that supports Cyrillic (adjust path if needed)
    try:
        font = ImageFont.truetype("arial.ttf", size=16)  # Windows
    except:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size=16)  # Linux

    for detection in ocr_result:
        box, text, score = detection
        box = np.array(box).astype(int)

        # Draw bounding box (polygon)
        draw.polygon(box.flatten().tolist(), outline=(0, 255, 0))

        # Draw text near top-left corner of the box
        top_left = tuple(box[0])
        draw.text((top_left[0], top_left[1] - 20), text, fill=(255, 0, 0), font=font)

    # Convert back to NumPy for display with matplotlib
    image_with_text = np.array(pil_img)

    # Plot
    plt.figure(figsize=(12, 8))
    plt.imshow(image_with_text)
    plt.axis('off')
    plt.title("Detected Text with Bounding Boxes (Russian)")
    plt.show()
