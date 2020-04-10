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
path = 'C:/Users/camilo.sidou/Desktop/PMPS' 
lista_ext = ['.xlsx']
path_ref = open('C:/Users/camilo.sidou/Desktop/bases_camilo/bases/base_sigtap.csv', 'r')
ref = list(csv.reader(path_ref))
val_proc_v = re.compile(r'0+\d\d\d\d\d\d\d\d\d')
#lin_proc_v = '0301000001'
#col_proc_v = [20]
#novo_valor = '14'


lista_path = []

for root, dir, file in os.walk(path):
    for i in file:
        for ext in lista_ext:
            if ext in i:
                arq_path = [i, os.path.join(root, i)]
                lista_path.append(arq_path)

idx = 0
for item in lista_path:
    arq = openpyxl.load_workbook(filename=item[1])
    plan = arq.active
    print(lista_path[idx][0], "aberto")
    max_lin = plan.max_row
    for i in range(1, max_lin):
        corresp = val_proc_v.findall(str(plan[i][0].value))
        if len(corresp) > 0:
            achou = None
            for cod in ref:
                cod_queb = cod[0].split(';')
                achou = cod[0].split(';')[0]
                if len(cod_queb) > 2:
                    nome = cod_queb[2]
                else:
                    nome = cod_queb[1]
                if achou == corresp[0]:
                    print(str(plan[i][1].value) + ' -> ' + str(nome))
                    plan[i][1].value = nome
    idx += 1
    arq.save(lista_path[idx][1])
