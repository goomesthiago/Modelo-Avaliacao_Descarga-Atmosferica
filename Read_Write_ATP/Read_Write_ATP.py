# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 15:06:21 2024

@author: thiag
"""
import os
import subprocess


def alterar_linha_em_arquivo(working_dir, prefixo_linha, nova_linha):
    try:
        with open(working_dir, 'r') as arquivo:
            linhas = arquivo.readlines()

        for i, linha in enumerate(linhas):
            if linha.startswith(prefixo_linha):
                # Substitui a linha inteira
                linhas[i] = nova_linha + '\n'  # Adiciona uma quebra de linha no final

        with open(working_dir, 'w') as arquivo_modificado:
            arquivo_modificado.writelines(linhas)

        print(f'Linha substituída com sucesso em {working_dir}')

    except FileNotFoundError:
        print(f'Arquivo {working_dir} não encontrado.')
    except Exception as e:
        print(f'Ocorreu um erro: {e}')


def rodar_atp(working_dir):
    subprocess.run([r"C:\ATP\tools\runATP.exe" ,r'"' + working_dir + '"'])
    #os.system(r'"C:\ATP\tools\runATP.exe C:\ATP\atpdraw\work\VAO_01_estocastico.atp s -r"') #video que Matheus mandou eh esse comadno
    return print('O arquivo .atp foi executado com sucesso')





#parametros da fonte de corrente
amplitude = '123014.767' #valor da magnitude da fonte de corrente
T_frente = '1.78783E-5' #valor do tempo de frente da fonte de corrente
A1 = '61507.3837'    #valor da magnitude/2 da fonte de corrente
T1 = '6.88064422'   #valor do tempo em que atinge A1
TSTOP = '0.00013212'  #valor do tempo em que a magnitude da fonte de corrente vai a 0


working_dir = 'C:\\ATP\\atpdraw\\work\\VAO_01_estocastico.atp'
prefixo_a_procurar = '13RAIO__-1'
#nova_linha_completa = "13RAIO__-1123014.767          1.78783E-561507.38376.88064422          0.00013212"
nova_linha_completa = f"13RAIO__-1{amplitude}          {T_frente}{A1}{T1}          {TSTOP}"

alterar_linha_em_arquivo(working_dir, prefixo_a_procurar, nova_linha_completa)

#rodar_atp(working_dir)


    

