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

lista_path = []

for root, dir, file in os.walk(path):
    for i in file:
        for ext in lista_ext:
            if ext in i:
                arq_path = [i, os.path.join(root, i)]
                lista_path.append(arq_path)

idx = 0
for i in lista_path:
    try:
        arq = openpyxl.load_workbook(filename=i[1])
        plan = arq.active
        print(lista_path[idx][0], "aberto")
        for row in plan:
            for cell in row:
                if cell.value == '50 fixo':
                    cell.value = 50
                    print('50 fixo')
                elif cell.value == '20 fixo':
                    cell.value = 20
                    print('20 fixo')
                elif cell.value == 'se CD = 0, TSB = 216':
                    cell.value = None
                    print('se CD = 0, TSB = 216')
                elif cell.value == 'se CD = 0, ASB = 216':
                    cell.value = None
                    print('se CD = 0, ASB = 216')
                elif cell.value == 'se CD = 0, TSB = 260':
                    cell.value = None
                    print('se CD = 0, TSB = 260')
                elif cell.value == 'se CD = 0, ASB = 260':
                    cell.value = None                
                elif cell.value == ' 1, se CD = 0, TSB = 13':
                    cell.value = 1
                    print(' 1, se CD = 0, TSB = 13')
                elif cell.value == ' 1, se CD = 0, ASB = 13':
                    cell.value = 1
                    print(' 1, se CD = 0, ASB = 13')
                elif cell.value == ' 1, se CD = 0, ASB = 4':
                    cell.value = 1
                    print(' 1, se CD = 0, ASB = 4')
                elif cell.value == ' 1, se CD = 0, ASB = 4':
                    cell.value = 1
                    print(' 1, se CD = 0, ASB = 4')
                elif cell.value == '20 lembrar que o produto não pode ser superior a 200':
                    cell.value = 20
                    print('20 lembrar que o produto não pode ser superior a 200')
                elif cell.value == '1 fixo por CBO':
                    cell.value = 1
                    print('1 fixo por CBO')
                elif cell.value == 'se CD = 0, TSB = 63':
                    cell.value = None
                    print('se CD = 0, TSB = 63')
                elif cell.value == 'se CD = 0, ASB = 63':
                    print('se CD = 0, ASB = 63')
                    cell.value = None
                elif cell.value == 'se CD = 0, TSB = 80':
                    print('se CD = 0, TSB = 80')
                    cell.value = None
    except:
        print('>> ERRO: (não aberto):', i[1])
        continue

    idx += 1
    arq.save(i[1])