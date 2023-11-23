#import PyPDF2

from pypdf import PdfReader

def extract_paragraphs(pdf_path):
    paragraphs = []

    # Open the PDF file
    with open(pdf_path, 'rb') as file:
        reader = PdfReader(file)

        # Iterate through each page and extract text
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text = page.extract_text()

            # Split text into paragraphs (assuming paragraphs are separated by '\n')
            paragraphs.extend([para for para in text.split('\n') if para.strip()])
            if page_num == 5:
                break

    return paragraphs

# Replace 'your_pdf_file.pdf' with the path to your PDF file
pdf_path = 'C:/Users/Jikhan Jung/Downloads/gibson-et-al-2023-reconstructing-the-feeding-ecology-of-cambrian-sponge-reefs-the-case-for-active-suspension-feeding-in.pdf'
paragraphs = extract_paragraphs(pdf_path)

# Print the extracted paragraphs
for i, para in enumerate(paragraphs):
    print(i, "["+para[0:50]+"]")
