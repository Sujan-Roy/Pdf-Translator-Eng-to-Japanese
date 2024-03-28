import gradio as gr
from pdf2docx import parse
import argostranslate.package, argostranslate.translate
import argostranslatefiles
from argostranslatefiles import argostranslatefiles
import os

# Select languages (modify as needed)
from_code = "en"
to_code = "ja"

# Download and install Argos Translate package (run once initially)
# argostranslate.package.update_package_index()
# available_packages = argostranslate.package.get_available_packages()
# package_to_install = next(
#     filter(
#         lambda x: x.from_code == from_code and x.to_code == to_code, available_packages
#     )
# )
# argostranslate.package.install_from_path(package_to_install.download())

# Load installed languages (assuming package is already installed)
installed_languages = argostranslate.translate.get_installed_languages()
from_lang = list(filter(
    lambda x: x.code == from_code,
    installed_languages))[0]
to_lang = list(filter(
    lambda x: x.code == to_code,
    installed_languages))[0]
underlying_translation = from_lang.get_translation(to_lang)


def translate_pdf(pdf_file):
    # Get the file name without the extension
    file_name = os.path.splitext(pdf_file)[0]

    # Get the file extension
    file_extension = os.path.splitext(pdf_file)[1]

    # Check if the file is a PDF file
    if file_extension == ".pdf":
        # Create a path to the temporary docx file
        docx_file_path = f"{file_name}.docx"  # Temporary file for translation

        # Convert the PDF file to a temporary docx file
        parse(pdf_file, docx_file_path, start=0, end=None)

        # Translate the temporary docx file
        translated_text = argostranslatefiles.translate_file(underlying_translation, docx_file_path)

        # Remove the temporary docx file
        os.remove(docx_file_path)

        return translated_text
    else:
        return None


def translate_ui(uploaded_pdf):
    if uploaded_pdf is not None:
        translated_text = translate_pdf(uploaded_pdf)
        return translated_text
    else:
        return "Please upload a PDF file for translation."


# Gradio Interface creation
interface = gr.Interface(
    fn=translate_ui,
    inputs=gr.File(label="Upload PDF"),
    outputs="textbox",
    title="PDF Translate and Convert",
    description="Upload a PDF file to translate and get the translated text.",
)

# Launch the Gradio interface
interface.launch()