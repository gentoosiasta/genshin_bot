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

        div_tag = soup.find('div', class_='px-2')

        if div_tag:
            for span_tag in div_tag.find_all('br'):
                # print(span_tag.get_text())
                span_tag.replace_with('\n')

            texto = "ESTADÍSTICAS DESEADAS:\n"
            texto += div_tag.get_text()
            # print(texto)
            await update.message.reply_text(texto)
            await update.message.reply_text("Para información más detallada, consulta el enlace:\n" + url)
        else:
            await update.message.reply_text("No se encontraron estadísticas desde el enlace:\n" + url)

    else:
        await update.message.reply_text(f"Error al conectar. Código: {response.status_code}")
