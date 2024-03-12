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

def ler_lis(diretorio, knt, nome_arquivo):
    import os
    import numpy as np
    
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

        #if arquivo.endswith('.lis'):
        if arquivo == diretorio + nome_arquivo + '.lis':

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
                resultados = {'variaveis': variaveis, knt: maximo}
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
    
    
    









# Função para ler o .log, o .xlsx e plotar os .log

def le_resultados(log, excel, pasta_destino ):
    import matplotlib.pyplot as plt
    import pandas as pd
    import os

    diretorio = 0

    variaveis = {'KNT': [], 'RAIO': [], 'TFRENT': []}
    #variaveis = {'KNT': [], 'RAIO': []}

    # while diretorio == 0:
    #     try:
    #         leitura = input('Digite o diretório do arquivo .log contendo os valores dos parâmetros adotados em cada'
    #                         'simulação, com seu nome e sua extensão \n'
    #                         'por exemplo: C:/Users/Matheus/Desktop/meuarquivo.log: \n')
    #         arquivo = open(leitura, 'r', encoding='utf8')
    #     except:
    #         print('Há algo errado com o diretorio ou arquivo informados, verifique.')
    #     else:
    #         arquivo.close
    #         diretorio = 1

    with open(log, 'r', encoding='ISO-8859-2') as arquivo:
        texto = arquivo.readlines()

        for linha in texto:

            if 'KNT' in linha:
                variaveis['KNT'].append(float(linha.replace('Variables KNT=', '').replace(':', '')))

            elif 'RAIO' in linha:
                variaveis['RAIO'].append(float(linha.replace('RAIO=', '')))

            elif 'TFRENT' in linha:
                variaveis['TFRENT'].append(float(linha.replace('TFRENT=', '')))
                
                


    # Dividir todos os elementos de 'RAIO' por 1000 para ter os valores em kA

    divisao_ka = 1000

    variaveis = {chave: [valor / divisao_ka if chave == 'RAIO' else valor for valor in valores] for chave, valores in variaveis.items()}

    
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(20,7))
    
    
    # Histograma primeiro subplot
    ax1.hist(variaveis['RAIO'], rwidth=0.9)
    ax1.set_title('Amplitudes', fontsize=16)
    ax1.set_xlabel('Corrente (A)', fontsize=14)
    ax1.set_ylabel('Frequência', fontsize=14)
    
    # Histograma no segundo plot
    ax2.hist(variaveis['TFRENT'])
    ax2.set_title('Tempos de frente', fontsize=16)
    ax2.set_xlabel('Tempo de frente (s)', fontsize=14)
    ax2.set_ylabel('Frequência', fontsize=14)
    
    # Histograma no terceiro plot
    ax3.scatter(variaveis['TFRENT'], variaveis['RAIO'])
    ax3.set_title('Correntes versus tempo de frente', fontsize=16)
    ax3.set_xlabel('Tempo de frente (s)', fontsize=14)
    ax3.set_ylabel('Amplitude (kA)', fontsize=14)

    
    
    
    

    # plt.subplot(1,3,1, figsize=(12,4))
    # plt.title('Amplitudes')
    # plt.xlabel('Corrente (A)')
    # plt.ylabel('Frequência')
    # plt.hist(variaveis['RAIO'], rwidth=0.9)
    # plt.subplot(1,3,2, figsize=(12,4))
    # plt.title('Tempos de frente')
    # plt.xlabel('Tempo de frente (s)')
    # plt.ylabel('Frequência')
    # plt.hist(variaveis['TFRENT'], rwidth=0.9)
    # plt.subplot(1,3,3, figsize=(12,4))
    # plt.title('Correntes versus tempo de frente')
    # plt.xlabel('Tempo de frente (s)')
    # plt.ylabel('Amplitude (A)')
    # plt.scatter(variaveis['TFRENT'], variaveis['RAIO'])
    
    nome_fig = 'descarga_atmosferica.png'
    caminho_fig = os.path.join(pasta_destino, nome_fig)
    
    
    plt.savefig(caminho_fig)
    plt.close()
# Até aqui é a figura, com 3 gráficos, que vai falar sobre as fontes de correntes que usamos para modelar as descargas


    # Leitura das saídas do ATP, coladas em uma planilha excel
    # diretorio = 0

    # while diretorio == 0:
    #     try:
    #         leitura = input(
    #              'Digite o diretório do arquivo excel contendo as saídas do ATP com seu nome e sua extensão \n'
    #              'por exemplo: C:/Users/Matheus/Desktop/meuarquivo.xlsx: \n')
    #         resultados = pd.read_excel(leitura, engine='openpyxl')

    #     except:
    #         print('Há algo errado com o diretorio ou arquivo informados, verifique.')
    #     else:
    #         diretorio = 1

    resultados = pd.read_excel(excel, engine='openpyxl')
    var = pd.DataFrame(variaveis)

    analises = pd.concat([var, resultados], axis=1)

    return analises


# Função para criar e salvar os gráficos de histograma e CDF da sobretensão

def plota_individual(analise, pasta_destino):
    import matplotlib.pyplot as plt
    import numpy as np
    import os

    for i in range(4,len(analise.columns)):
    #for i in range(4,len(analise.columns)):
        nome_coluna = analise.columns[i]
        valor_coluna = analise[nome_coluna] / 1000
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20,7))
        
        
        #Histograma primeiro subplot
        ax1.hist(valor_coluna, rwidth = 0.9, bins = 20)
        ax1.set_title(f'Histograma ({nome_coluna.replace(" ", "")})', fontsize=16)
        ax1.set_xlabel('Amplitudes (kV)', fontsize=14)
        ax1.set_ylabel('Frequência', fontsize=14)
        
        #CDF no segundo subplot
        count, bins_count = np.histogram(valor_coluna, bins=1000)
        pdf = count / sum(count)
        cdf = np.cumsum(pdf)
        ax2.plot(bins_count[1:], 100 * (1 - cdf), label='CDF: ' + nome_coluna.replace(" ", ""))
        ax2.set_ylabel('Prob. (%)', fontsize=14)
        ax2.set_yticks([0, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
        ax2.set_xlabel('V (kV)', fontsize=14)
        ax2.grid(True)
        ax2.set_title(f"Probabilidade de determinada tensão ser excedida ({len(analise['KNT'])} simulações)", fontsize=16)
        ax2.legend()
            
        
        # Salvar a fig
        nome_fig = f'CDF_{nome_coluna.replace(" ", "")}.png'
        caminho_figura = os.path.join(pasta_destino, nome_fig)
        plt.savefig(caminho_figura)
        plt.close() # Fechando a figura

    
    
    
    
    
    
    
