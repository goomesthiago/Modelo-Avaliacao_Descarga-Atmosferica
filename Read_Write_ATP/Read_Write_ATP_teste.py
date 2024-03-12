# -*- coding: utf-8 -*-
"""
Created on Tue Jan  9 21:22:07 2024

@author: thiag
"""

with open(nome_arquivo, 'r') as arquivo:
            conteudo = arquivo.read()
            
        conteudo_modificado = conteudo.replace(trecho_antigo, trecho_novo)
        
        with open(nome_arquivo, 'w') as arquivo_modificado:
            arquivo_modificado.write(conteudo_modificado)
            
        print(f'Trecho alterado com sucesso em {nome_arquivo}')
        
    except FileNotFoundError:
        print(f'Arquivo {nome_arquivo} não encontrado.')
    except Exception as e:
        print(f'Ocorreu um erro: {e}')

# Exemplo de uso:
nome_do_arquivo = 'VAO_01_estocastico.atp'
trecho_antigo = 'Texto antigo a ser substituido'
trecho_novo = 'Novo texto para substituir o antigo'

alterar_trecho_arquivo(nome_do_arquivo, trecho_antigo, trecho_novo)