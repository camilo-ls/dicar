# Script para modificar valores em planilhas do Excel
# -> O script roda em todas as planilhas num diretório
# USE COM CUIDADO - de preferência não nos arquivos originais (use cópias)

import os
import openpyxl
import re


# Parâmetros:
# path: diretório dos arquivos (UNICODE: use / para separar os dirs)
# lista_ext: formatos que serão abertos
# lin_proc_v: valor que identifica a linha procurada
# col_proc_v: valor(es) que serão substituídos
#novo_valor: valor que irá substituir
#base_ref: base de referência
path = 'C:/Users/camilo.sidou/Desktop/PMPS2' 
lista_ext = ['.xlsx']
lin_proc_v = '600000009'


lista_path = []

for root, dir, file in os.walk(path):
    for i in file:
        for ext in lista_ext:
            if ext in i:
                arq_path = [i, os.path.join(root, i)]
                lista_path.append(arq_path)

idx = 0
for i in lista_path:
    arq = openpyxl.load_workbook(filename=i[1])
    plan = arq.active
    print(i[0], "aberto")
    for row in plan:
        if lin_proc_v in str(row[0].value):
           print('ACHOU!!')                            
    idx += 1