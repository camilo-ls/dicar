# Converte arquivos .xlsx dentro de uma pasta para .csv

import openpyxl as pl
import csv
import os


# path: endereço onde estão os arquivos .xls(x):
path = 'C:/Users/camilo.sidou/Desktop/PMPS EM CSV' 
lista_ext = ['.xlsx']

lista_path = []

for root, dir, file in os.walk(path):
    for i in file:
        for ext in lista_ext:
            if ext in i:
                arq_path = [i, os.path.join(root, i)]
                lista_path.append(arq_path)

idx = 1

for i in lista_path:
    arq = pl.load_workbook(i[1])
    plan = arq.active
    nome_out = i[1].replace('.xlsx', '.csv')
    arq_csv = open(nome_out, 'w')

    data = plan.rows

    for row in data:
        l = list(row)
        for j in range(len(l)):
            if j == len(l) - 1:
                arq_csv.write(str(l[j].value))
            else:
                arq_csv.write((str(l[j].value) + ';'))
        arq_csv.write(' \n')
    arq_csv.close()
    print('[' + str(idx) + '/' + str(len(lista_path)) + ']', i[0], 'convertido')
    idx += 1