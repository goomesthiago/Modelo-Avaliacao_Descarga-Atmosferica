# Função para pegar os dados das variáveis num arquivo .log e transformar em variável para o Python

def log_para_variaveis(nome_arquivo):
    listas_variaveis = []
    conjunto_atual = []

    try:
        with open(nome_arquivo, 'r') as arquivo:
            for linha in arquivo:
                # Verifica se a linha contém "Variables KNT="
                if "Variables KNT=" in linha:
                    # Se houver um conjunto anterior, adiciona à lista principal
                    if conjunto_atual:
                        listas_variaveis.append(conjunto_atual)
                    # Inicia um novo conjunto
                    conjunto_atual = []
                elif linha.strip():  # Ignora linhas em branco
                    # Extrai os valores de RAIO, RMEIO, TAXA, TFRENT e TFIM
                    variavel, valor = linha.strip().split('=')
                    #conjunto_atual.append(float(valor))
                    conjunto_atual.append(valor)

        # Adiciona o último conjunto à lista principal
        if conjunto_atual:
            listas_variaveis.append(conjunto_atual)

    except FileNotFoundError:
        print(f'Arquivo {nome_arquivo} não encontrado.')
    except Exception as e:
        print(f'Ocorreu um erro: {e}')

    return listas_variaveis
 
    
# Função para formatar os valores do jeito que o ATP aceita
def formatar_valores(valores):
    valores_formatados = []

    for valor in valores:

        # Verifica se a string tem notação científica
        if 'E' in valor.upper():
            #mantém a notação científica até o final
            valor_formatado = f'{valor[:7]}{valor[-3:]}'
        else:
            #se não tiver notação, mantem os 10 primeiros caracteres
            valor_formatado = valor[:10]

        valores_formatados.append(valor_formatado)

    return valores_formatados


# Função pra alterar o código do ATP

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

        #print(f'Linha substituída com sucesso em {working_dir}')

    except FileNotFoundError:
        print(f'Arquivo {working_dir} não encontrado.')
    except Exception as e:
        print(f'Ocorreu um erro: {e}')

# Função para rodar .atp

def rodar_atp(working_dir, knt):
    import subprocess
    subprocess.run([r"C:\ATP\tools\runATP.exe" ,r'"' + working_dir + '"'])
    #os.system(r'"C:\ATP\tools\runATP.exe C:\ATP\atpdraw\work\VAO_01_estocastico.atp s -r"') #video que Matheus mandou eh esse comadno
    return print(f'O caso [{knt}] foi executado com sucesso.')

# Função para pegar os resultados do .lis

def ler_lis(diretorio, knt):
    import os
    import numpy as np
    import pandas as pd
    
    #Exibe todos os arquivos para posteriormente fazer o filtro de só rodar os arquivos .lis
    arquivos = os.listdir(diretorio)  
    
    
    resultados = open(diretorio + '\\resultados.txt','w')

    # Vetor para armazenar nome das variáveis
    variaveis = []
    #max = []
    #min = []
    casos = []
    n_var = 0
    # Variável para identificar o número de linhas com resultados de saída
    linhas_var = 0
    # Variável para identificar o número de colunas da última linha
    colunas_var = 0
    # Maximo absoluto
    #maximo = []
    
    
    for arquivo in arquivos:

        if arquivo.endswith('.lis'):

            # Vetor para armazenar nome das variáveis
    #        variaveis = []
            max = []
            min = []
    #        casos = []
    #        n_var = 0
            # Variável para identificar o número de linhas com resultados de saída
    #        linhas_var = 0
            # Variável para identificar o número de colunas da última linha
    #        colunas_var = 0
            # Maximo absoluto
            maximo = []

            casos.append(arquivo)
            file_ = open(diretorio + '\\' + arquivo, 'r')
            texto = file_.readlines()
            for linha in texto:

                # Detecta as variáveis monitoradas

                if 'Column headings for the' in linha and len(casos) == 1:

                    n_var = int(texto[texto.index(linha)][23:29])
                    linhas_var = int(n_var / 10) + 1
                    colunas_var = n_var % 10


                    i = 1

                    while texto[texto.index(linha) + i][0:4] != ' ***':

                        if texto[texto.index(linha) + i][0:7] == '   Step':

                            flag = 1

                            while flag == 1:

                                for linhas in range(linhas_var):

                                    if linhas == linhas_var - 1:

                                        for j in range(colunas_var):

                                            variaveis.append(texto[texto.index(linha) + i][23 + j * 11:29 + j * 11] +
                                                             '-' + texto[texto.index(linha) + i + 1][23 + j * 11:29 + j * 11])

                                        flag = 0
                                        i = i + 2

                                    else:

                                        for j in range(10):

                                            variaveis.append(texto[texto.index(linha) + i][23 + j * 11:29 + j * 11] +
                                                             '-' + texto[texto.index(linha) + i + 1][23 + j * 11: 29 + j * 11])

                                        i = i + 3
                                        linhas = linhas + 1

                        else:

                            i = i + 1

                if 'Variable maxima :' in linha:

                    i = 0

                    for linhas in range(linhas_var):

                        if linhas == linhas_var - 1:

                            for j in range(colunas_var):

                                max.append(float(texto[texto.index(linha) + i][19 + j * 11:29 + j * 11]))

                        else:

                            for j in range(10):

                                max.append(float(texto[texto.index(linha) + i][19 + j * 11:29 + j * 11]))

                            i = i + 1

                elif 'Variable minima :' in linha:

                    i = 0

                    for linhas in range(linhas_var):

                        if linhas == linhas_var - 1:

                            for j in range(colunas_var):

                                min.append(float(texto[texto.index(linha) + i][19 + j * 11:29 + j * 11]))

                        else:

                            for j in range(10):

                                min.append(float(texto[texto.index(linha) + i][19 + j * 11:29 + j * 11]))

                            i = i + 1

            # Pega valor absoluto
            for i in range(len(max)):
                maximo.append(np.max([max[i], np.abs(min[i])]))

            # Criando DataFrames
            if knt == 1:
                # trazer o cabeçalho e tudo mais
                #resultados = {'variaveis': variaveis, knt: maximo}
                resultados = [variaveis,maximo]
                file_.close()
                return resultados
    #            return pd.DataFrame(resultados) nao retornar um DF agora mas sim o dicionário, para que eu crie o DF só no main lá no fim
    #            resultados = resultados.set_index('variaveis')
    #            resultados = resultados.T
    #            print(resultados)

            else:
                #trazer só a últiam coluna como resultado
    #            resultados_new = pd.Series(maximo)
    #            resultados_new = pd.DataFrame(resultados_new)
    #            resultados_new = resultados_new.set_index('variaveis')
                #THIAGOresultados.insert(len(casos), str(arquivo), maximo, allow_duplicates=False)
                file_.close()
                return maximo


    
    
    