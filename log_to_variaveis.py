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

# Exemplo de uso:
nome_do_arquivo = 'exemplo.log'
listas_variaveis = log_para_variaveis(nome_do_arquivo)

# # Imprimir as listas extraídas
# for i, conjunto in enumerate(listas_variaveis):
#     print(f'Conjunto {i + 1}: {conjunto}')
    

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


valores_formatados = formatar_valores(listas_variaveis[1])

print("Valores formatados:", valores_formatados)