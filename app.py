# ---------------------------------------- BIBLIOTECAS ---------------------------------------

from selenium import webdriver                  # Simula o uso do navegador
from selenium.webdriver.common.by import By     # Permite encontrar informações dentro de sites
import openpyxl                 # Permite criar e manipular planilhas do excel
import pandas as pd             # Abrir e manipular arquivos em excel
import plotly.express as px     # Gerar gráficos interativos
import plotly                   # Usado para baixar o gráfico

# ------------------------------------------ FUNÇÕES -----------------------------------------

# Função para coletar o link da proxima pagina
def next_page(driver):
    # Verifica se existe o elemento que indica o fim das páginas
    if not driver.find_elements(By.XPATH,"//li[@class='next disabled']"):
        # Retorna o conteudo do elemento que indica o link da próxima página
        return driver.find_element(By.XPATH,"//link[@rel='next']").get_attribute('href')
    else:
        return None

# --------------------------------------- CRIANDO PLANILHA --------------------------------------

# Cria uma planilha do excel para armazenar os dados (database.xlsx)
planilha = openpyxl.Workbook()

# Cria uma página na planilha (monitores)
planilha.create_sheet('monitores')

# Seleciona a página criada e insere os títulos das colunas
sheet_monitores = planilha['monitores']
sheet_monitores['A1'].value = 'Nome do Monitor'
sheet_monitores['B1'].value = 'Preço'

# -------------------------------------- INICIANDO A RASPAGEM -------------------------------------

# URL do site que será feito o scraping
url = 'https://www.kabum.com.br/computadores/monitores/monitor-gamer'

# inicializando o webdriver (navegador que será usado) - Chrome
driver = webdriver.Chrome()

# Loop para coletar os dados de todas as páginas
while True:
    
    # Abre a página da url atual no navegador
    driver.get(url)

    # Coletando os dados utilizando o xpath
    titles = driver.find_elements(By.XPATH,"//span[@class='sc-d79c9c3f-0 nlmfp sc-93fa31de-16 bBOYrL nameCard']")
    promotional_prices = driver.find_elements(By.XPATH,"//span[@class='sc-6889e656-2 bYcXfg priceCard']")

    # Inserindo os dados na planilha (somente tuplas de nome, preço com valors diferentes de null para manter consistência)
    for title, price in zip(titles, promotional_prices):
        sheet_monitores.append([title.text, price.text])

    # Recebe o link da proxima pagina
    url = next_page(driver)

    if url == None:
        break

# Fechando o navegador (webdriver) - Não será mais usado a partir daqui
driver.quit()

# ------------------------------------------- FORMATANDO OS DADOS (PREÇO) ---------------------------------------

# Excluindo excesso de informação nos preços
for cell in sheet_monitores['B']:
    cell.value = cell.value.replace('R$ ', '')  # Excluindo o 'R$ ' pois atrapalha a conversão para float
    cell.value = cell.value.replace('.', '')    # Excluindo o '.' pois também atrapalha a conversão para float
    cell.value = cell.value.replace(',', '.')   # Trocando a vírgula por ponto para evitar problemas com string e float

# Convertendo os preços para float (com exceção do cabeçalho)
for cell in sheet_monitores['B'][1:]:
  cell.value = float(cell.value)

# Salvando a planilha
planilha.save('database.xlsx')

# ---------------------------------------- ORDENANDO OS DADOS PARA O GRÁFICO ---------------------------------------- #

# Criando uma lista para armazenar os produtos (nome, preço)
produtos = []

# Inserindo os produtos na lista (OBS.: zip() é uma função que permite iterar sobre duas listas ao mesmo tempo)
for title, price in zip(sheet_monitores['A'][1:], sheet_monitores['B'][1:]):
  produtos.append([title.value, price.value])

# Ordenando a lista de produtos pelo preço (crescente)
produtos.sort(key=lambda produto: produto[1]) # key = lambda é um parâmetro que permite ordenar a lista por um valor específico, nesse caso o preço
 
# -------------------------------------------------- GERANDO O GRÁFICO -------------------------------------------------- #

# Criando um dataframe com os dados da lista de produtos
df = pd.DataFrame(produtos, columns=['Produto', 'Preço Promocional'])

# Gerando o gráfico de linhas
fig = px.line(
    df, 
    x = df.index,
    y = 'Preço Promocional',
    labels={'x': 'PRODUTO', 'Preço Promocional': 'PREÇO'},
    hover_data=['Produto'],
    markers=True,
    #color = 'Produto',
    title = 'BENCHMARK COMPLETO DE PREÇOS DE MONITORES GAMER - KABUM',
)

fig.show()

# Baixando o gráfico
plotly.offline.plot(fig)