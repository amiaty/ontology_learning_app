import os

def load_text_file(filename):
    """Load text content from a file"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        return f"Error loading file: {str(e)}"

def save_ontology(ontology_content, filename):
    """Save ontology content to a file"""
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(ontology_content)
        return True
    except Exception as e:
        return f"Error saving file: {str(e)}"