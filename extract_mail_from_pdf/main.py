import re
import fitz


class MailFinder:
    """
    Simple class to find email in PDF files
    """
    def __init__(self):
        self.regex_mail = r"\w{1,}" \
                          r"(?=[.-_]\w{1,})" \
                          "@" \
                          r"[a-zA-Z]{1,}[-a-zA-Z]{0,}" \
                          r"\." \
                          "[a-zA-Z]{2,}"

    @staticmethod
    def text_from_pdf(pdf_path):
        """Get text from PDF given its path"""
        with fitz.open(pdf_path) as doc:
            text = ""
            for page in doc:
                text += page.get_text()
        return text

    def find_mail_in_pdf(self, pdf_path):
        """Find emails in PDF given its path"""
        text = self.text_from_pdf(pdf_path)
        mails = re.findall(self.regex_mail, text)
        return mails


if __name__ == "__main__":
    pdf_path = "./path_to_file.pdf"
    finder = MailFinder()
    mails = finder.find_mail_in_pdf(pdf_path)

    if len(mails) == 0:
        print(f"No email found for file {pdf_path}")
    else:
        print(f"Found {len(mails)} emails for file {pdf_path}: ")
        for mail in mails:
            print(f"- {mail}")
