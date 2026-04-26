import requests
import os

def traducir_conocimiento(texto_md):
    url = "http://localhost:11434/api/generate"
    
    prompt = f"""
    Eres un traductor profesional de marketing para estudios de fotografía de lujo.
    Traduce el siguiente contenido de Markdown del ESPAÑOL al INGLÉS.
    
    REGLAS:
    1. Mantén el formato Markdown intacto.
    2. Usa un lenguaje sofisticado y profesional (ej. en lugar de 'Pictures', usa 'Imagery' o 'Photography').
    3. No traduzcas nombres propios como 'Tangerine'.
    
    CONTENIDO A TRADUCIR:
    {texto_md}
    """

    payload = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(url, json=payload)
        return response.json().get('response', '')
    except Exception as e:
        return f"Error: {e}"

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(base_dir, "tangerine-readable-check.md")
    output_path = os.path.join(base_dir, "tangerine-knowledge-en.md")

    if not os.path.exists(input_path):
        print("❌ Primero debes correr el refiner.")
        return

    with open(input_path, 'r', encoding='utf-8') as f:
        contenido_es = f.read()

    print("🌎 Traduciendo base de conocimientos al inglés...")
    contenido_en = traducir_conocimiento(contenido_es)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(contenido_en)

    print(f"✨ ¡Traducción lista! Archivo: {output_path}")

if __name__ == "__main__":
    main()