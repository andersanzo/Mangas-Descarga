import os
import time
import io
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from PIL import Image

def scroll_to_bottom(driver, pause_time=2):
    """Realiza scroll hasta el final de la página para activar el lazy load."""
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(pause_time)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def extract_chapter_urls(driver, manga_list_url, manga_name):
    """
    Carga la página de listado de capítulos, realiza scroll y extrae todos los enlaces
    que tengan la estructura: https://inmanga.com/ver/manga/{manga_name}/{capítulo}/{uuid}
    Devuelve una lista de tuplas (número_de_capítulo, url) ordenadas de menor a mayor.
    """
    driver.get(manga_list_url)
    time.sleep(5)  # Espera para que cargue la página
    scroll_to_bottom(driver, pause_time=2)
    
    # Extraemos todos los links que contengan la parte del manga
    link_elements = driver.find_elements(By.XPATH, f"//a[contains(@href, '/ver/manga/{manga_name}/')]")
    chapters = {}
    for link in link_elements:
        href = link.get_attribute("href")
        if not href:
            continue
        # Se espera que la URL tenga la forma:
        # https://inmanga.com/ver/manga/Berserk/104/88406410-4D9D-439C-8704-3297B27D7158
        parts = href.split('/')
        if len(parts) >= 7 and parts[5].lower() == manga_name.lower():
            chapter_part = parts[6]
            if chapter_part.isdigit():
                chapter_num = int(chapter_part)
                chapters[chapter_num] = href
    # Ordenamos los capítulos por número (de menor a mayor)
    sorted_chapters = sorted(chapters.items(), key=lambda x: x[0])
    return sorted_chapters

def process_chapter(chapter_url, chapter_folder, driver):
    """
    Procesa la página de un capítulo:
      - Abre la página, realiza scroll y espera a que las imágenes se carguen (reemplazando el "loading gear").
      - Extrae la lista de URLs de las imágenes.
      - Descarga cada imagen, la convierte a JPG y la guarda con nombres autoincrementales (1.jpg, 2.jpg, ...).
    """
    driver.get(chapter_url)
    time.sleep(5)  # Espera para la carga inicial
    scroll_to_bottom(driver, pause_time=2)
    
    image_elements = driver.find_elements(By.CSS_SELECTOR, "img.ImageContainer")
    loading_gear = "https://inmanga.com/content/img/loading-gear.gif"
    
    # Esperamos a que cada imagen tenga una URL distinta al "loading gear"
    timeout = 30  # segundos
    start_time = time.time()
    while time.time() - start_time < timeout:
        all_loaded = True
        for element in image_elements:
            src = element.get_attribute("src")
            if src == loading_gear:
                all_loaded = False
                driver.execute_script("arguments[0].scrollIntoView(true);", element)
        if all_loaded:
            break
        time.sleep(1)
    
    # Extraemos las URLs reales de las imágenes
    urls = [elem.get_attribute("src") for elem in image_elements]
    
    if not os.path.exists(chapter_folder):
        os.makedirs(chapter_folder)
    
    # Descargamos y convertimos cada imagen a JPG
    for index, img_url in enumerate(urls, start=1):
        try:
            response = requests.get(img_url, stream=True)
            response.raise_for_status()
            image_data = response.content
            image = Image.open(io.BytesIO(image_data))
            image = image.convert("RGB")  # Aseguramos el modo RGB para JPEG
            output_filename = f"{index}.jpg"
            output_path = os.path.join(chapter_folder, output_filename)
            image.save(output_path, "JPEG")
            print(f"Descargado y convertido: {output_path}")
        except Exception as e:
            print("Error al procesar", img_url, e)

def main():
    # Pide la URL de la lista de capítulos desde la terminal
    manga_list_url = input("Introduce la URL de la lista de capítulos del manga: ").strip()
    # Ejemplo de entrada: https://inmanga.com/ver/manga/Berserk/5cc13fca-2e10-41e7-bbca-d70353d6a55a
    
    # Extrae el nombre del manga de la URL (asumiendo estructura fija)
    parts = manga_list_url.split('/')
    if len(parts) < 6:
        print("URL no válida.")
        return
    manga_name = parts[5]
    
    # Crea la carpeta principal con el nombre del manga (en minúsculas)
    main_folder = manga_name.lower()
    if not os.path.exists(main_folder):
        os.makedirs(main_folder)
    
    # Configuración de Selenium en modo headless
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=chrome_options)
    
    # Extrae los capítulos ordenados (lista de tuplas: (número, url))
    sorted_chapters = extract_chapter_urls(driver, manga_list_url, manga_name)
    print("Capítulos encontrados (ordenados):")
    for chap_num, url in sorted_chapters:
        print(chap_num, url)

    # Nueva funcionalidad añadida: preguntar si quiere comenzar desde un capítulo específico
    start_chapter = 0
    respuesta = input("¿Quieres empezar desde un capítulo específico? (s/n): ").strip().lower()
    if respuesta == 's':
        try:
            start_chapter = int(input("Introduce el número de capítulo desde el que quieres empezar: ").strip())
        except ValueError:
            print("Número no válido, empezando desde el principio.")
            start_chapter = 0

    # Filtra los capítulos si se especificó un número de inicio
    filtered_chapters = [(num, url) for num, url in sorted_chapters if num >= start_chapter]

    # Recorre cada capítulo filtrado y procesa las imágenes
    for idx, (chap_num, url) in enumerate(filtered_chapters, start=1):
        # Cada capítulo se guarda en una carpeta con nombre incremental: 1, 2, 3, etc.
        chapter_folder = os.path.join(main_folder, str(idx))
        print(f"Procesando capítulo {chap_num} en carpeta {chapter_folder} ...")
        process_chapter(url, chapter_folder, driver)
    
    driver.quit()
    print("Proceso completado.")

if __name__ == "__main__":
    main()
