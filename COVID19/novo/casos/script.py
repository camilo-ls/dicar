from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.request
from datetime import date, datetime
import shutil
import time
import os
import csv
import glob


# var. do programa:
current_path = os.path.dirname(os.path.abspath(__file__))
dir_tmp = current_path + '\\tmp'
dir_br_tmp = dir_tmp + '\\br'
dir_final = current_path + '/bases'
dir_copia = 'M:\GERENCIA DE ESTATISTICA\Covid19\Casos Covid19 (Auto)'
lista_estados = (['AC', 'AM', 'AP', 'PA', 'RO', 'RR', 'TO', 'AL', 'BA', 'CE', 'MA', 'PB', 'PE', 'PI', 'RN', 'SE', 'ES', 'MG', 'RJ', 'SP', 'DF', 'GO', 'MS', 'MT', 'PR', 'SC', 'RS'],
                ['Acre', 'Amazonas', 'Amapá', 'Pará', 'Rondônia', 'Roraima', 'Tocantins', 'Alagoas', 'Bahia', 'Ceará', 'Maranhão', 'Paraíba', 'Pernambuco', 'Piauí', 'Rio Grande do Norte', 'Sergipe', 'Espírito Santo', 'Minas Gerais', 'Rio de Janeiro', 'São Paulo', 'Distrito Federal', 'Goiás', 'Mato Grosso do Sul', 'Mato Grosso', 'Paraná', 'Santa Catarina', 'Rio Grande do Sul'])

# scraping dos dados mundiais:
print('> Recuperando base mundial...')
urllib.request.urlretrieve('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv', str(dir_tmp) + '/tmp.csv')


# criação das bases locais:
tmp = open(str(dir_tmp) + '/tmp.csv', 'r')
world = open(str(dir_tmp) + '/world.csv', 'w')

# transformação da informação em memória em lista
info = list(csv.reader(tmp))

# tratamento de dados:
# > split da primeira linha:
info = info[1:]
# > remover os valores '0'
# (todo) otimização: fazer esse tratamento com complexidade O(n2)
for row in info:
    new_row = []
    for cell in row:
        if row.index(cell) == 2 or row.index(cell) == 3:
            continue
        if cell != '0':
            new_row.append(cell)
    for cell in new_row:
        world.write(cell + ';')
    world.write('\n')

# fechar os arquivos (salva parcialmente):
tmp.close()
world.close()
os.remove(str(dir_tmp) + '/tmp.csv')

# pegar nº total de dias:
n_dias = len(info[0]) - 4

# # scraping dos dados brasileiros:
print('> Recuperando base nacional...')
driver_opt = webdriver.ChromeOptions()
#driver_opt.add_argument('--headless')
driver_opt.add_experimental_option('prefs', {'download.default_directory': dir_br_tmp})
#driver = webdriver.Chrome(options=driver_opt)
driver = webdriver.Chrome('C:/Users/camilo.sidou/Google Drive/DICAR/PATH/chromedriver.exe', options=driver_opt)
driver.get('https://covid.saude.gov.br/')
btn_baixar = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//ion-content[@class='ion-padding md hydrated']/div[@class='content-bottom']/div[@class='ok']")))
driver.execute_script('arguments[0].click()', btn_baixar)
time.sleep(10)
driver.close()

# achar o arquivo baixado e renomeá-lo para br_tmp.csv:
for file in glob.glob(dir_br_tmp + '/*.csv'):
    os.rename(file, str(dir_br_tmp) + '/br_tmp.csv')
    break

# abrir os arquivos para formalizar a base br:
tmp = open(str(dir_br_tmp) + '/br_tmp.csv', 'r')
br = open(str(dir_tmp) + '/br.csv', 'w')

# tratamento de dados
# > organizar os dados na memória de forma mais compreensível:
dic_br = {}

for row in tmp:
    row_sep = row.split(';')
    if row_sep[1] not in dic_br:
        dic_br.update({row_sep[1]: []})
    else:
        if int(row_sep[4]) > 0:
            dic_br[row_sep[1]].append(row_sep[4])

dic_br.pop('estado', None) # faz o pop da key 'estados'

# escreve no arquivo final br:
for key in dic_br:
    br.write(lista_estados[1][lista_estados[0].index(key)]) # escreve o nome do estado por extenso
    br.write(';Brazil') # adiciona a coluna com o nome do país
    for valor in dic_br[key]: # termina de adicionar os valores
        br.write(';' + valor)
    br.write('\n')

# salvamento parcial:
tmp.close()
br.close()

# remove os arquivos desnecessários:
os.remove(dir_br_tmp + '/br_tmp.csv')

# criação da base final:
print('> Criação da base local...')
world = open(str(dir_tmp) + '/world.csv', 'r')
br = open(str(dir_tmp) + '/br.csv', 'r')
manaus = open(str(dir_tmp) + '/manaus.csv', 'r')
base = open(str(dir_final) + '/casos ' + str(date.today()) + '.csv', 'w')

# inserção do cabeçalho:
base.write('ESTADO/PROVÍNCIA;PAÍS/REGIÃO;PAÍS/ESTADO')
for i in range(1,n_dias+1):
    base.write(';' + str(i) + ' º DIA')
base.write('\n')

# inserção dos dados mundiais na base final:
for row in world:
    row_sep = row.split(';')
    if row_sep[0] == '': # condicional para criar a terceira coluna
        row_sep.insert(2, row_sep[1]) # repete o nome do país se não tiver
    else:
        row_sep.insert(2, row_sep[1] + ' - ' + row_sep[0]) # se tiver, acrescenta
    for cell in row_sep: # escreve com as modificações
        if row_sep.index(cell) == 0: # se for a primeira coluna
            base.write(cell)
        else:
            base.write(';' + cell) # se for o resto
    #base.write('\n')
world.close()

# inserção dos dados nacionais na base final:
for row in br:
    row_sep = row.split(';')
    if row_sep[0] == '': # condicional para criar a terceira coluna
        row_sep.insert(2, row_sep[1]) # repete o nome do país se não tiver
    else:
        row_sep.insert(2, row_sep[1] + ' - ' + row_sep[0]) # se tiver, acrescenta
    for cell in row_sep: # escreve com as modificações
        if row_sep.index(cell) == 0: # se for a primeira coluna
            base.write(cell)
        else:
            base.write(';' + cell) # se for o resto
    #base.write('\n')
br.close()

# inserção dos dados de Manaus:
for row in manaus:
    row_sep = row.split(';')
    if row_sep[0] == '': # condicional para criar a terceira coluna
        row_sep.insert(2, row_sep[1]) # repete o nome do país se não tiver
    else:
        row_sep.insert(2, row_sep[1] + ' - ' + row_sep[0]) # se tiver, acrescenta
    for cell in row_sep: # escreve com as modificações
        if row_sep.index(cell) == 0: # se for a primeira coluna
            base.write(cell)
        else:
            base.write(';' + cell) # se for o resto
    #base.write('\n')
manaus.close()

# finalização da base:
base.close()
print('> Copiando a base para o local:', dir_copia)
arq_local = dir_final + '\\casos ' + str(date.today()) + '.csv'
arq_copia = dir_copia + '\\casos.csv'
shutil.copyfile(arq_local, arq_copia)
print('> Finalizado.')