import requests
from bs4 import BeautifulSoup

# Função para coletar o link da proxima pagina
def next_page(soup):
    # Ir na ultima pagina com o botao proximo desabilitado
    if not soup.find( 'li', {'class' : 'next disabled'} ):
        next = soup.find('link', {'rel': 'next'})
        return next['href'].replace('?', '/computadores/monitores?')
    else:
        return None
    
# URL do site que será feito o scraping (Página inicial)
url = 'https://www.kabum.com.br/computadores/monitores?page_number=42'

# Essa linha é necessária para que o site não bloqueie a requisição por ser um bot
headers = {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"}

# Faz a requisição do site e armazena o conteúdo na variável site
site = requests.get(url, headers = headers)

# Transforma o conteúdo do site (html) em um objeto BeautifulSoup
soup = BeautifulSoup(site.content, 'html.parser')

print(next_page(soup))
