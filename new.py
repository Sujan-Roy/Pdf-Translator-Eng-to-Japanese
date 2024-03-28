import os
from pdf2docx import parse
import argostranslate.package, argostranslate.translate
import argostranslatefiles
from argostranslatefiles import argostranslatefiles


def download_and_install_argos_package(from_code, to_code):
    """Downloads and installs the Argos Translate package for the specified languages."""

    argostranslate.package.update_package_index()
    available_packages = argostranslate.package.get_available_packages()
    package_to_install = next(
        filter(
            lambda x: x.from_code == from_code and x.to_code == to_code,
            available_packages,
        )
    )
    argostranslate.package.install_from_path(package_to_install.download())


def load_languages(from_code, to_code):
    """Loads the specified languages for translation."""

    installed_languages = argostranslate.translate.get_installed_languages()
    from_lang = list(filter(lambda x: x.code == from_code, installed_languages))[0]
    to_lang = list(filter(lambda x: x.code == to_code, installed_languages))[0]
    underlying_translation = from_lang.get_translation(to_lang)
    return underlying_translation


def convert_to_docx(file_path):
    """Converts a PDF file to a DOCX file.

    Args:
        file_path (str): The path to the PDF file.

    Returns:
        str: The path to the converted DOCX file, or None if the file is not a PDF.
    """

    file_name, file_extension = os.path.splitext(file_path)
    if file_extension == ".pdf":
        docx_file_path = os.path.join(search_directory, f"{file_name}.docx")
        parse(file_path, docx_file_path, start=0, end=None)
        print(f"Successfully converted '{file_path}' to '{docx_file_path}'.")
        return docx_file_path
    else:
        return None


def translate_docx(docx_file_path, underlying_translation):
    """Translates a DOCX file using the provided translation object.

    Args:
        docx_file_path (str): The path to the DOCX file.
        underlying_translation: The Argos Translate translation object.
    """

    argostranslatefiles.translate_file(underlying_translation, os.path.abspath(docx_file_path))


def process_pdf_files(from_code, to_code, search_directory):
    """Processes all PDF files in the specified directory, translating them to the target language.

    Args:
        from_code (str): The source language code.
        to_code (str): The target language code.
        search_directory (str): The directory containing the PDF files.
    """

    # Download and install Argos Translate package if needed
    try:
        underlying_translation = load_languages(from_code, to_code)
    except RuntimeError:  # Likely caused by missing package
        download_and_install_argos_package(from_code, to_code)
        underlying_translation = load_languages(from_code, to_code)

    # Check if directory exists
    if not os.path.exists(search_directory) or not os.path.isdir(search_directory):
        os.mkdir(search_directory)
        print(f"The '{search_directory}' directory does not exist. Now, it has been created.")

    # Process all PDF files
    for file in os.listdir(search_directory):
        pdf_file_path = os.path.join(search_directory, file)
        docx_path = convert_to_docx(pdf_file_path)
        if docx_path:
            translate_docx(docx_path, underlying_translation)


# Define constants
from_code = "en"
to_code = "ja"
search_directory = "Translated_PDFs"


def main():
    """The main function that starts the PDF processing."""

    process_pdf_files(from_code, to_code, search_directory)


if __name__ == "__main__":
    main()