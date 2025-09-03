import requests
from bs4 import BeautifulSoup

async def get_stats(url, update) -> None:

    # Realizamos la petición a la web
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})

    # print(url)

    # Comprobamos que la petición nos ha devuelto un código de estado 200 (OK)
    if response.status_code == 200:
        # Guardamos el contenido de la web en una variable
        html = response.content

        soup = BeautifulSoup(html, 'html.parser')

        stats = soup.find_all('div', class_='px-2')
        texto = "STATS DESEADAS:\n"
        for stat in stats:
            texto += stat.find('span').get_text()
            print(texto)
            await update.message.reply_text(texto + "\n")

    else:
        await update.message.reply_text(f"Error al conectar. Código: {response.status_code}")
