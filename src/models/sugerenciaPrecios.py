import requests
from bs4 import BeautifulSoup
import re

def analizador(query):
    url = f"https://www.google.com/search?q={query}+restaurante"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        textos = soup.find_all(text=True)
        textos_encontrados = []
        for texto in textos:
            textos_encontrados.append(texto)
        

        precios = []
        patron_precio = r'(€\s*\d+[,.]?\d{0,2})|(\d+[,.]?\d{0,2}\s*€)'
        for texto in textos_encontrados:
            matches = re.findall(patron_precio, texto)
            for match in matches:
                precio = ''.join(match).strip()
                precios.append(precio)

        vector_precios=[]
        vector_precios.append(precios)
        print(vector_precios)
        suma_precios = 0
        for precio in precios:
            precio = precio.replace('€', '').replace(',', '.').strip()
            suma_precios += float(precio)
        precio_medio = suma_precios / len(precios)
        precio_medio = "{:.2f}".format(precio_medio)
        return precio_medio
    else:
        print(f"Error al realizar la solicitud: {response.status_code}")


