# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 14:21:27 2023
@author: thiag
"""
import os
import math

##Entradas
search_string = 'C < n 1><>< Ampl.  >< Freq.  ><Phase/T0><   A1   ><   T1   >< TSTART >< TSTOP  >' #string procurada
k = 4 #Número de linhas que pega acima da string procurada

folder_path = os.getcwd() #Pasta onde os arquivos .lis se encontram

extensao_arquivo = ".atp" #Dizer para o programa qual a extensão de arquivos que estamos procurando
#lista = [["Nome Arquivo", "Barra", "Tipo", "Valor Absoluto", "Valor Eficaz (rms)"]]  #Inicializando lista que vai conter os arquivos


#parametros da fonte de corrente
amplitude = 1 #valor da magnitude da fonte de corrente
fase = 2.0E-6 #valor do tempo de frente da fonte de corrente
A1 = 2.4E4    #valor da magnitude/2 da fonte de corrente
T1 = 7.5E-5   #valor do tempo em que atinge A1
TSTOP = T1/2  #valor do tempo em que a magnitude da fonte de corrente vai a 0


fonte_achar = '13RAIO__-1     4.8E4               2.E-6     2.4E4    7.5E-5             .000148'

#parametros que vamos inputar
fonte_corrente = '13RAIO__-1   4.853E4             1.22E-6     2.4E4    7.5E-5             .000148'


#Início do código

file_names = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) if f.endswith(extensao_arquivo)]

for file_name in file_names:
    print('testado')

    with open(file_name, 'r') as file:
        lines = file.readlines()
        joined_lines = ''.join(lines)
        index = joined_lines.find(search_string)
  
        if index == -1:
            print("A string não foi encontrada! Tente outra vez")



        
#         prior_text = joined_lines[:index]
#         prior_lines = prior_text.split('\n')[-(k+1):-1]  # Pegar as k linhas acima da string procurada
#     resultado = str.split('\n'.join(prior_lines))

    
#     lista.append([file_name, barra, tipo, resultado[3], float(resultado[3]) / math.sqrt(2)])

# with open("curto_circuito.txt", 'w', encoding='utf-8') as arquivo_txt:
#     # Escrever os dados no arquivo de texto
#     for linha in lista:
#         arquivo_txt.write('\t'.join(map(str, linha)) + '\n')

# print("Dados exportados para o arquivo txt com sucesso.")