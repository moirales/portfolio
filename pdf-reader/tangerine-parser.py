import fitz  # PyMuPDF
import json
import os

def parse_tangerine_docs(pdf_folder):
    knowledge_base = {}
    
    # Validar que la carpeta de PDFs existe
    if not os.path.exists(pdf_folder):
        print(f"❌ Error: No se encuentra la carpeta de PDFs en: {pdf_folder}")
        return

    # Obtener lista de PDFs
    files = [f for f in os.listdir(pdf_folder) if f.endswith('.pdf')]
    
    if not files:
        print("⚠️ No se encontraron archivos PDF para procesar.")
        return

    print(f"🚀 Iniciando extracción de {len(files)} documentos...")

    for file_name in files:
        file_path = os.path.join(pdf_folder, file_name)
        try:
            doc = fitz.open(file_path)
            full_text = ""
            
            for page_num, page in enumerate(doc):
                # Extraemos el texto de la página
                page_text = page.get_text()
                full_text += f"\n[SECTION: {file_name} - PAGE {page_num + 1}]\n"
                full_text += page_text
            
            # Usamos un nombre de clave limpio para el JSON
            key_name = file_name.replace('.pdf', '').lower().replace(' ', '_')
            knowledge_base[key_name] = full_text.strip()
            print(f"✅ Procesado: {file_name}")
            
        except Exception as e:
            print(f"❌ Error procesando {file_name}: {e}")

    # Definir ruta de salida (hacia src/data/ de tu proyecto Astro)
    # Buscamos la carpeta 'src/data' subiendo un nivel desde 'pdf-reader'
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(base_dir, "../src/data")
    
    # Crear la carpeta src/data si no existe
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"📁 Carpeta creada: {output_dir}")

    output_file = os.path.join(output_dir, "tangerine-knowledge.json")

    # Guardar el JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(knowledge_base, f, ensure_ascii=False, indent=4)

    print("\n" + "="*40)
    print(f"✨ PROCESO COMPLETADO ✨")
    print(f"📂 Datos guardados en: {output_file}")
    print("="*40)

if __name__ == "__main__":
    # La ruta absoluta a tus PDFs
    target_path = "/home/moirales/mi-portafolio/public/images/tangerine-pdf/"
    parse_tangerine_docs(target_path)