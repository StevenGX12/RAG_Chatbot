import os
import pandas as pd
from pptx import Presentation
from docx import Document
import PyPDF2
from pathlib import Path

# For image/video/audio analysis (later)
# from transformers import pipeline  # e.g., for BLIP
# import cv2
# import moviepy.editor as mp

# Constants
CORPUS_DIR = "./corpus"
OUTPUT_FILE = "./processed_corpus/processed_chunks.jsonl"

# Whisper model (for audio/video transcription)
# whisper_model = whisper.load_model("base")


def extract_text_from_pdf(file_path):
    text_chunks = []
    with open(file_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                text_chunks.append(
                    {
                        "content": text.strip(),
                        "type": "text",
                        "metadata": {"source": file_path, "page_slide": f"Page {i+1}"},
                    }
                )
    return text_chunks


def extract_text_from_docx(file_path):
    doc = Document(file_path)
    text = "\n".join(p.text for p in doc.paragraphs if p.text.strip())
    return [
        {"content": text.strip(), "type": "text", "metadata": {"source": file_path}}
    ]


def extract_text_from_pptx(file_path):
    prs = Presentation(file_path)
    slides = []
    for i, slide in enumerate(prs.slides):
        slide_text = []
        for shape in slide.shapes:
            if hasattr(shape, "text"):
                slide_text.append(shape.text)
        if slide_text:
            slides.append(
                {
                    "content": "\n".join(slide_text).strip(),
                    "type": "text",
                    "metadata": {"source": file_path, "page_slide": f"Slide {i+1}"},
                }
            )
    return slides


def extract_text_from_csv(file_path):
    df = pd.read_csv(file_path)
    markdown = df.to_markdown(index=False)
    return [{"content": markdown, "type": "table", "metadata": {"source": file_path}}]


# def extract_text_from_audio(file_path):
#     result = whisper_model.transcribe(file_path)
#     return [
#         {
#             "content": result["text"].strip(),
#             "type": "audio_transcript",
#             "metadata": {"source": file_path},
#         }
#     ]


def process_corpus(corpus_path):
    all_chunks = []

    for root, _, files in os.walk(corpus_path):
        for file in files:
            file_path = os.path.join(root, file)
            ext = Path(file).suffix.lower()

            try:
                if ext == ".pdf":
                    all_chunks.extend(extract_text_from_pdf(file_path))
                elif ext == ".docx":
                    all_chunks.extend(extract_text_from_docx(file_path))
                elif ext == ".pptx":
                    all_chunks.extend(extract_text_from_pptx(file_path))
                elif ext == ".csv":
                    all_chunks.extend(extract_text_from_csv(file_path))
                # elif ext in [".mp3", ".wav"]:
                #     all_chunks.extend(extract_text_from_audio(file_path))
                # elif ext in [".jpg", ".png", ".mp4"]:
                #     all_chunks.extend(extract_image_or_video_description(file_path))
                else:
                    print(f"Unsupported file format: {file}")
            except Exception as e:
                print(f"Error processing {file_path}: {e}")

    return all_chunks


def save_chunks_as_jsonl(chunks, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        for chunk in chunks:
            f.write(f"{chunk}\n")


if __name__ == "__main__":
    chunks = process_corpus(CORPUS_DIR)
    save_chunks_as_jsonl(chunks, OUTPUT_FILE)
    print(f"✅ Extracted {len(chunks)} chunks to {OUTPUT_FILE}")
