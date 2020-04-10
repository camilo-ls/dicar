#!/usr/bin/python3
from selenium import webdriver
import urllib.request
import shutil
from datetime import date, datetime
import time
import os
import csv
import re

# var. do programa:
current_path = os.path.dirname(os.path.abspath(__file__))
final_path = 'M:\GERENCIA DE ESTATISTICA\Covid19\Casos Covid19 (Auto)'
lista_estados = (['AC', 'AM', 'AP', 'PA', 'RO', 'RR', 'TO', 'AL', 'BA', 'CE', 'MA', 'PB', 'PE', 'PI', 'RN', 'SE', 'ES', 'MG', 'RJ', 'SP', 'DF', 'GO', 'MS', 'MT', 'PR', 'SC', 'RS'],
                ['Acre', 'Amazonas', 'Amapá', 'Pará', 'Rondônia', 'Roraima', 'Tocantins', 'Alagoas', 'Bahia', 'Ceará', 'Maranhão', 'Paraíba', 'Pernambuco', 'Piauí', 'Rio Grande do Norte', 'Sergipe', 'Espírito Santo', 'Minas Gerais', 'Rio de Janeiro', 'São Paulo', 'Distrito Federal', 'Goiás', 'Mato Grosso do Sul', 'Mato Grosso', 'Paraná', 'Santa Catarina', 'Rio Grande do Sul'])

# scraping dos dados mundiais:
print('> Recuperando base mundial...')
urllib.request.urlretrieve('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv', str(current_path) + '/tmp.csv')


# criação das bases locais:
tmp = open(str(current_path) + '/tmp.csv', 'r', encoding='utf-8-sig')
world = open(str(current_path) + '/world.csv', 'w', encoding='utf-8-sig')

# transformação da informação em memória em lista
info = list(csv.reader(tmp))

# tratamento de dados:
# > split da primeira linha:
info = info[1:]
# > remover os valores '0'
# otimização: fazer esse tratamento com complexidade O(n2)
for row in info:
    new_row = []
    for cell in row:
        if cell != '0':
            new_row.append(cell)
    for cell in new_row:
        world.write(cell + ';')
    world.write('\n')

# fechar os arquivos (salva parcialmente):
tmp.close()
world.close()
os.remove(str(current_path) + '/tmp.csv')

# pegar nº total de dias:
n_dias = len(info[0]) - 4

# # scraping dos dados brasileiros:
print('> Recuperando base nacional...')
driver_opt = webdriver.ChromeOptions()
driver_opt.add_argument('--headless')
#driver = webdriver.Chrome() # linux
driver = webdriver.Chrome('C:/Users/camilo.sidou/Google Drive/DICAR/PATH/chromedriver.exe', options=driver_opt) # windows
driver.get('https://www.saude.gov.br/noticias/agencia-saude')

try:
    driver.find_element_by_partial_link_text('Brasil registra').click()
except:
    try:
        driver.find_element_by_partial_link_text('casos confirmados').click()
    except:
        try:
            driver.find_element_by_partial_link_text('Coronavírus: ').click()
        except:
            print('Erro')


time.sleep(1)

# abrindo e escrevendo no .csv:
br_tmp = open(str(current_path) + '/br_tmp.csv', 'w', encoding='utf-8-sig')
br_wr = csv.writer(br_tmp)
for row in table.find_elements_by_tag_name('tr'):
    br_wr.writerow([d.text for d in row.find_elements_by_tag_name('td')])
br_tmp.close()
driver.close()

# tratamento dos dados:
br_tmp = open(str(current_path) + '/br_tmp.csv', 'r', encoding='utf-8-sig')
br = open(str(current_path) + '/br.csv', 'w', encoding='utf-8-sig')
info = csv.reader(br_tmp)
br.write(str(date.today()) + '\n')
for row in info:
    try:
        idx = lista_estados[0].index(row[1])
    except:
        continue
    else:
        br.write(lista_estados[1][idx] + ';' + row[2] + ';' + row[3])
        br.write('\n')

br_tmp.close()
os.remove(str(current_path) + '/br_tmp.csv')
br.close()

# atualizar os dados na base histórica do Brasil:
# > abrindo os arquivos:
br_hist = open(str(current_path) + '/br_hist.csv', 'r', encoding='utf-8-sig')
br = open(str(current_path) + '/br.csv', 'r', encoding='utf-8-sig')
br_hist_f = open(str(current_path) + '/br_hist_f.csv', 'w', encoding='utf-8-sig')
# > transformando os dados em listas:
info_br_hist = list(csv.reader(br_hist))
info_br = list(csv.reader(br))

# > pegando o dia que foi realizada a atualização:
dia_novo = info_br[0][0]
dia_novo = datetime.strptime(dia_novo, '%Y-%m-%d').date()
dia_velho = info_br_hist[0][0]
dia_velho = datetime.strptime(dia_velho, '%Y-%m-%d').date()

br_hist_f.write(str(dia_novo))
br_hist_f.write('\n')

info_br = info_br[1:]
info_br_hist = info_br_hist[1:]

# > incluindo as informações no br_hist_f:
for row in info_br_hist:
    nova_row = row[0].split(';')
    for nova_info in info_br:
        nova_info_list = nova_info[0].split(';')
        if nova_row[0] == nova_info_list[0]:
            if dia_novo <= dia_velho:
                nova_row.pop()
                nova_row.append(nova_info_list[1])
            else:
                nova_row.append(nova_info_list[1])
    n_col = len(nova_row)
    for j in range(n_col):
        if (j > 0):
            br_hist_f.write(';' + nova_row[j])
        else:
            br_hist_f.write(nova_row[j])
    br_hist_f.write('\n')

# > finalizando os arquivos (salvamento parcial):
br_hist.close()
br_hist_f.close()
br.close()

# > deletando os arquivos desnecessários:
os.rename(str(current_path) + '/br_hist.csv', str(current_path) + '/br_hist_ex.csv')
os.rename(str(current_path) + '/br_hist_f.csv', str(current_path) + '/br_hist.csv')
br.close()
os.remove(str(current_path) + '/br.csv')
os.remove(str(current_path) + '/br_hist_ex.csv')

# criar a planilha final:
# > abrir os arquivos locais:
print('> Construindo base local...')
world = open(str(current_path) + '/world.csv', 'r', encoding='utf-8-sig')
br = open(str(current_path) + '/br_hist.csv', 'r', encoding='utf-8-sig')
final = open(str(current_path) + '/hist/base ' + str(dia_novo) + '.csv', 'w', encoding='utf-8-sig')

# > colocar o cabeçalho:
final.write('ESTADO/PROVÍNCIA;PAÍS/REGIÃO;PAIS/ESTADO;LAT;LON')
for i in range(1,n_dias+1):
    final.write(';' + str(i) + ' º DIA')
final.write('\n')

# > colocar as informações mundiais:
info = list(csv.reader(world))

for row in info:
    new_row = row[0].split(';')
    n_col = len(new_row)
    if new_row[0] == '':
        new_row.insert(2, new_row[1])
    else:
        new_row.insert(2, str(new_row[1]) + ' - ' + str(new_row[0]))
    for cell in new_row:
        final.write(str(cell) + ';')
    final.write('\n')
world.close()

# > colocar as informações nacionais:
info = list(csv.reader(br))
info = info[1:]

for row in info:
    new_row = row[0].split(';')
    new_row = new_row
    new_row.insert(2, '')
    new_row.insert(2, '')
    n_col = len(new_row)
    if new_row[0] == '':
        new_row.insert(2, new_row[1])
    else:
        new_row.insert(2, str(new_row[1]) + ' - ' + str(new_row[0]))
    for cell in new_row:
        final.write(str(cell) + ';')
    final.write('\n')
br.close()
final.close()

file_out = str(current_path) + '/hist/base ' + str(dia_novo) + '.csv'
path_out = final_path + '/base_f ' + str(dia_novo) + '.csv'
shutil.copyfile(file_out, path_out)

print('> Finalizado.')

# # # scraping dos dados do Amazonas:
# # driver = webdriver.Chrome('C:/Users/camilo.sidou/Google Drive/DICAR/PATH/chromedriver.exe', options=driver_opt)
# # driver.get('http://www.fvs.am.gov.br/noticias')
# # info = driver.find_elements_by_class_name('link-normal')
# # info_filt = []

# # n_casos = 0

# # for row in info:
# #     if ('corona' in row.text or 'ovid-19' in row.text) and ('Caso' in row.text or 'caso' in row.text):
# #         n_aux = re.findall(r'\d+', row.text)
# #         if n_aux:
# #             elemento = (n_aux[0], row.text)
# #             info_filt.append(elemento)

# # for row in info_filt:
# #     print(row)
# #     if int(row[0]) > n_casos:
# #         n_casos = int(row[0])

# # am = open(str(current_path) + '/am.csv', 'w')
# # info = csv.reader(am)

# # # fecha tudo:
# # am.close()
# # tmp.close()
# # driver.close()