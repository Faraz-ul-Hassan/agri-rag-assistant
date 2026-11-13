"""
One-off inspection script: extract text from every PDF in data/raw/ and report basic stats so we can judje extraction quality before building the real ingestion pipeline.
"""

from pathlib import Path
from pypdf import PdfReader

RAW_DIR = Path("data/raw")
OUT_DIR = Path("data/processed")
OUT_DIR.mkdir(parents=True, exist_ok=True)

def extract_pdf(pdf_path: Path) -> dict:
    reader = PdfReader(str(pdf_path))
    pages = []
    for page in reader.pages:
        pages.append(page.extract_text() or "")

    full_text = "\n\n".join(pages)

    return {
        "file":pdf_path.name,
        "num_pages": len(reader.pages),
        "num_chars": len(full_text),
        "first_500_chars": full_text[:500],
        "full_text": full_text,
    }

def main():
    pdfs = sorted(RAW_DIR.glob("*.pdf"))
    if not pdfs:
        print(f"No PDFs found in {RAW_DIR.resolve()}")
        return

    print(f"Found {len(pdfs)} PDF(s)\n")
    print(f"{'File':<50} {'Pages':>6} {'Chars':>10} {'Chars/Page':>12}")
    print("-" * 82)

    for pdf_path in pdfs:
        try:
            info = extract_pdf(pdf_path)
        except Exception as e:
            print(f"{pdf_path.name:<50} ERROR: {e}")
            continue

        chars_per_page = info["num_chars"] // max(info["num_pages"], 1)
        print(
            f"{info['file']:<50} {info['num_pages']:>6} "
            f"{info["num_chars"]:>10} {chars_per_page:>12}"
        )

        # Save full text for eyeballing
        out_file = OUT_DIR / (pdf_path.stem + ".txt")
        out_file.write_text(info["full_text"], encoding="utf=8")

    print(f"\nExtracted .txt files saved to {OUT_DIR.resolve()}/")


if __name__ == "__main__":
    main()
