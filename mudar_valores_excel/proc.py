# Script para modificar valores em planilhas do Excel
# -> O script roda em todas as planilhas num diretório
# USE COM CUIDADO - de preferência não nos arquivos originais (use cópias)

import os
import openpyxl
import csv

# Parâmetros:
# path: diretório dos arquivos (UNICODE: use / para separar os dirs)
# lista_ext: formatos que serão abertos
# lin_proc_v: valor que identifica a linha procurada
# col_proc_v: valor(es) que serão substituídos
#novo_valor: valor que irá substituir
#base_ref: base de referência
path = 'C:/Users/camilo.sidou/Desktop/PMPS2' 
lista_ext = ['.xlsx']

lista_path = []

for root, dir, file in os.walk(path):
    for i in file:
        for ext in lista_ext:
            if ext in i:
                arq_path = [i, os.path.join(root, i)]
                lista_path.append(arq_path)


saida = open(path + '/saida.csv', 'w')

for item in lista_path:
    arq = openpyxl.load_workbook(filename=item[1])
    plan = arq.active
    print(item[0], "aberto")
    for row in plan.iter_rows(min_row = 13, max_row = 100, min_col = 0, max_col = 2):
        cod = str(row[0].value)
        desc = str(row[1].value).replace('\n', '')
        if cod != None and cod != 'None':
            saida.write(cod + ';' + desc + '\n')

saida.close()