import json
import requests
import os

def refine_with_llama(raw_text):
    url = "http://localhost:11434/api/generate"
    
    # Este es el "Prompt de Limpieza"
    prompt = f"""
    Eres un experto en extracción de datos. Tu tarea es limpiar y estructurar la información de un catálogo de fotografía.
    
    TEXTO CRUDO DEL PDF:
    {raw_text}
    
    INSTRUCCIONES:
    1. Extrae los nombres de los paquetes/servicios.
    2. Extrae los precios exactos.
    3. Resume los beneficios de cada paquete en bullets cortos.
    4. Identifica políticas de cancelación o reserva.
    5. Formatea TODO en Markdown elegante y fácil de leer para un humano.
    6. No inventes datos. Si no está en el texto, no lo pongas.
    
    RESPUESTA EN ESPAÑOL:
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
        return f"Error conectando con Ollama: {e}"

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(base_dir, "../src/data/tangerine-knowledge.json")
    output_file = os.path.join(base_dir, "tangerine-readable-check.md")

    if not os.path.exists(input_file):
        print(f"❌ No se encontró el archivo crudo: {input_file}")
        return

    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    refined_content = "# REVISIÓN DE CONOCIMIENTO: TANGERINE PHOTOGRAPHY\n\n"

    for key, text in data.items():
        print(f"🧠 Refinando contenido de: {key}...")
        summary = refine_with_llama(text)
        refined_content += f"## FUENTE: {key.upper()}\n\n{summary}\n\n"
        refined_content += "---\n\n"

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(refined_content)

    print(f"✨ ¡Refinamiento completado! Revisa el archivo: {output_file}")

if __name__ == "__main__":
    main()