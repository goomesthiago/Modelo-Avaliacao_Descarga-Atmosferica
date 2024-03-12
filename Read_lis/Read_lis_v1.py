# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 14:21:27 2023
@author: thiag
"""
import os
import math

##Entradas
search_string = 'Solution at nodes with known voltage.' #string procurada
k = 4 #Número de linhas que pega acima da string procurada

folder_path = os.getcwd() #Pasta onde os arquivos .lis se encontram

extensao_arquivo = ".lis" #Dizer para o programa qual a extensão de arquivos que estamos procurando
lista = [["Nome Arquivo", "Barra", "Tipo", "Valor Absoluto", "Valor Eficaz (rms)"]]  #Inicializando lista que vai conter os arquivos


tipo = ''  #Inicializando a variável que vai dizer se é mono ou trifásico
barra =""  #Inicializando a variável que vai trazer o código da barra
#Início do código

file_names = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) if f.endswith(extensao_arquivo)]

for file_name in file_names:
    
    if file_name[-6:-6+2] == "1f" :
        tipo = "Monofásico"
    elif file_name[-6:-6+2] == "3f":
        tipo = "Trifásico"
        
    barra = file_name[-12:-12+5].upper()
    
    with open(file_name, 'r') as file:
        lines = file.readlines()
        joined_lines = ''.join(lines)
        index = joined_lines.find(search_string)
  
        if index == -1:
            print("A string não foi encontrada! Tente outra vez")
        
        prior_text = joined_lines[:index]
        prior_lines = prior_text.split('\n')[-(k+1):-1]  # Pegar as k linhas acima da string procurada
    resultado = str.split('\n'.join(prior_lines))

    
    lista.append([file_name, barra, tipo, resultado[3], float(resultado[3]) / math.sqrt(2)])

with open("curto_circuito.txt", 'w', encoding='utf-8') as arquivo_txt:
    # Escrever os dados no arquivo de texto
    for linha in lista:
        arquivo_txt.write('\t'.join(map(str, linha)) + '\n')

print("Dados exportados para o arquivo txt com sucesso.")