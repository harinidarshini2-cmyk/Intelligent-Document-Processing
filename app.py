from pypdf import PdfReader
import os
import re
from collections import Counter

DOCUMENTS_FOLDER = "documents"

STOP_WORDS = {
    "the", "and", "for", "with", "that", "this", "from",
    "have", "will", "your", "their", "into", "been",
    "also", "about", "which", "are", "was", "were",
    "has", "had", "you", "they", "them", "its"
}


def extract_pdf_data(pdf_path):
    reader = PdfReader(pdf_path)

    full_text = ""

    for page in reader.pages:
        text = page.extract_text()

        if text:
            full_text += text + "\n"

    pages = len(reader.pages)

    return full_text, pages


def detect_title(text):
    lines = text.split("\n")

    for line in lines:
        line = line.strip()

        if len(line) > 5:
            return line[:100]

    return "Title Not Found"


def extract_keywords(text, top_n=10):
    words = re.findall(r"\b[a-zA-Z]{4,}\b", text.lower())

    filtered_words = [
        word for word in words
        if word not in STOP_WORDS
    ]

    word_freq = Counter(filtered_words)

    return [word for word, count in word_freq.most_common(top_n)]


def generate_summary(text, max_sentences=3):
    sentences = re.split(r'[.!?]', text)

    clean_sentences = []

    for sentence in sentences:
        sentence = sentence.strip()

        if len(sentence) > 40:
            clean_sentences.append(sentence)

    summary = clean_sentences[:max_sentences]

    return ". ".join(summary)


def classify_document(keywords):
    topics = {
        "Artificial Intelligence": [
            "ai", "machine", "learning", "neural",
            "deep", "model", "data"
        ],

        "Python Programming": [
            "python", "function", "class",
            "program", "code"
        ],

        "Electrical Engineering": [
            "voltage", "current", "circuit",
            "electrical", "power"
        ],

        "Mathematics": [
            "equation", "matrix",
            "probability", "calculus"
        ]
    }

    for topic, words in topics.items():
        for keyword in keywords:
            if keyword in words:
                return topic

    return "General Document"


def generate_report():
    report = []

    pdf_files = [
        file for file in os.listdir(DOCUMENTS_FOLDER)
        if file.endswith(".pdf")
    ]

    report.append("=" * 60)
    report.append("INTELLIGENT DOCUMENT PROCESSING REPORT")
    report.append("=" * 60)
    report.append(f"Total PDFs Processed: {len(pdf_files)}")
    report.append("")

    for pdf in pdf_files:

        pdf_path = os.path.join(DOCUMENTS_FOLDER, pdf)

        text, pages = extract_pdf_data(pdf_path)

        title = detect_title(text)

        keywords = extract_keywords(text)

        summary = generate_summary(text)

        category = classify_document(keywords)

        report.append(f"Document File : {pdf}")
        report.append(f"Title : {title}")
        report.append(f"Category : {category}")
        report.append(f"Pages : {pages}")
        report.append(f"Characters : {len(text)}")

        report.append("\nTop Keywords:")

        for keyword in keywords:
            report.append(f" - {keyword}")

        report.append("\nSummary:")
        report.append(summary)

        report.append("\n" + "-" * 60 + "\n")

    return "\n".join(report)


final_report = generate_report()

print(final_report)

with open("output.txt", "w", encoding="utf-8") as file:
    file.write(final_report)

print("\nReport saved as output.txt")