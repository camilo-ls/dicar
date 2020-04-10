# Script para modificar valores em planilhas do Excel
# -> O script roda em todas as planilhas num diretório
# USE COM CUIDADO - de preferência não nos arquivos originais (use cópias)

import os
import openpyxl
import csv
import re


# Parâmetros:
# path: diretório dos arquivos (UNICODE: use / para separar os dirs)
# lista_ext: formatos que serão abertos
# lin_proc_v: valor que identifica a linha procurada
# col_proc_v: valor(es) que serão substituídos
#novo_valor: valor que irá substituir
#base_ref: base de referência
path = 'M:/GERENCIA DE ESTATISTICA/Projetos/DICAR 010 - Nobre/NOBRE/FEVEREIROO'
cnes = 'M:/GERENCIA DE ESTATISTICA/Projetos/DICAR 010 - Nobre/NOBRE/loginsenha.csv'
lista_ext = ['.csv']


lista_path = []

for root, dir, file in os.walk(path):
    for i in file:
        for ext in lista_ext:
            if ext in i:
                arq_path = [i, os.path.join(root, i)]
                lista_path.append(arq_path)

cnes_arq = open(cnes, 'r')
lista_cnes = list(csv.reader(cnes_arq))

lista_cnes_comp = []
lista_arq_comp = []
lista_final = []

for n in lista_cnes:
    elemento = n[0].split(';')[4]
    lista_cnes_comp.append(elemento)
       
for arq in lista_path:
    elemento = arq[0].replace('.csv', '').split('-')[1]
    lista_arq_comp.append(elemento)
   
for n in lista_cnes_comp:
    if n not in lista_arq_comp:
        lista_final.append(n)

lista_final.sort()

arq_final = open(path + '/lista_cnes_omissos.csv', 'w')

for n in lista_final:
    arq_final.write(n)
    arq_final.write('\n')
    print(n)