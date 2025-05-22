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

