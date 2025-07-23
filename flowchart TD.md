```mermaid
flowchart TD
    A[User Uploads Document] --> B[Doc Type & Format Handler]
    B --> C[Preprocessing OpenCV]
    C --> D[OCR TrOCR for scans, Tesseract for clean text]
    D --> E[Field Extraction]
    E --> F[Format Validation]
    F --> G[Output: Validated JSON Fields]
    G --> H[Pass to Form Autofill Module]
```
# ML Component Implementation Plan

## Objective

Implement a machine learning-based pipeline for extracting payment-related details from documents (PDF, DOCX, XLSX) using OCR and NLP.

## Scope

* Handle 3 document types or 1 type in 3 formats
* OCR preprocessing and text extraction
* Field extraction: TIN, BIC, amount, payment purpose
* Format validation
* Output structured JSON for downstream modules

## Architecture

* **Preprocessing**: OpenCV for deskewing, denoising
* **OCR**: Tesseract (CPU) or TrOCR (GPU) for layout-aware recognition
* **NLP**: Regex + spaCy or Transformers for field detection
* **Validation**: Basic checks on TIN, BIC, amount formats
* **Output**: JSON object with extracted values

## ML Pipeline Diagram

```mermaid
flowchart TD
    A[Input: PDF / DOCX / XLSX] --> B["Preprocessing (OpenCV)"]
    B --> C["OCR (Tesseract / TrOCR)"]
    C --> D[Text Segmentation]
    D --> E["Field Extraction (TIN, BIC, Amount)"]
    E --> F[Format Validation Rules]
    F --> G[Output JSON with structured fields]
```

## Time Estimate

| Task                        | Duration |
| --------------------------- | -------- |
| Document structure analysis | 3 days   |
| Preprocessing pipeline      | 3 days   |
| OCR setup                   | 2 days   |
| Field extraction (NLP)      | 6 days   |
| Format validation           | 2 days   |
| Multi-format handling       | 4 days   |
| Testing & annotation        | 5 days   |
| Refactor & generalization   | 3 days   |
| Integration prep & buffer   | 2 days   |

**Total: 30 calendar days (\~22 working days)**
    
## Gantt Chart

```mermaid
gantt
    title ML Pipeline Implementation Plan (1 Month Target)
    dateFormat  YYYY-MM-DD
    section Setup & Preprocessing
    Sample analysis            :a1, 2025-06-10, 3d
    Preprocessing pipeline     :a2, after a1, 3d
    OCR integration            :a3, after a2, 2d
    section Core Extraction
    Field extraction           :b1, after a3, 6d
    Format validation rules    :b2, after b1, 2d
    Multi-format support       :b3, after b2, 4d
    section Testing & Finalization
    Annotation + evaluation    :c1, after b3, 5d
    Generalization/refactor    :c2, after c1, 3d
    Final polish & integration prep :c3, after c2, 2d
```

## Deliverables

* OCR and preprocessing module
* Field extractor for 3 doc types or 3 formats
* Output schema (JSON)
* Evaluation report on extraction accuracy

## Cost Comparison for T4 GPU Deployment

| Provider                   | GPU Type       | Estimated Cost (USD/hr) | Notes |
|---------------------------|----------------|--------------------------|-------|
| **Google Cloud Platform** | T4 (on-demand) | $0.35 GPU + ~$0.38 VM = **~$0.73/hr** | VM + GPU billed separately |
| **Yandex Cloud**          | T4-equivalent  | **~$0.60–0.70/hr**       | Includes GPU + typical VM usage |
| **GPUDC.ru**              | 1xRTX 3090 24GB (T4 not available)   | ₽30–40/hr → **~$0.33–0.44/hr** | Physical workstation access |
