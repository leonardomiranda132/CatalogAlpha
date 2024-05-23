import pandas as pd
from jinja2 import Environment, FileSystemLoader
import os

# Leitura da planilha catalogo.xlsx
df_catalogo = pd.read_excel('catalogo.xlsx')

# Inicializar a coluna 'LOCAL_IMGS' com uma lista vazia
df_catalogo['LOCAL_IMGS'] = df_catalogo.apply(lambda row: [row['foto1'], row['foto2'], row['foto3'], row['foto4'], row['foto5']], axis=1)

# Preencher NaNs com strings vazias
df_catalogo['LOCAL_IMGS'] = df_catalogo['LOCAL_IMGS'].apply(lambda imgs: [img for img in imgs if pd.notnull(img)])

# Agrupar as referências por contêiner (um contêiner para cada referência)
containers = []
for ref, group in df_catalogo.groupby('REF'):
    container = {
        'REF': ref,
        'Grupo': group['GRUPO'].iloc[0],
        'Categoria Similar': group['Categoria Similar'].iloc[0],
        'Preço Cheio': group['PREÇO CHEIO'].iloc[0],
        'Preço Venda': group['PREÇO VENDA'].iloc[0],
        'NomeProduto': group['NomeProduto'].iloc[0],
        'Descrição': group['descrição'].iloc[0],
        'Grade': {},  # Dicionário para armazenar a grade de disponibilidade dos tamanhos
        'LOCAL_IMGS': group['LOCAL_IMGS'].iloc[0]  # Caminhos das imagens para este contêiner
    }
    for index, row in group.iterrows():
        tamanho = row['TAM']
        cor = row['COR']
        qtd = row['QTD']
        if tamanho not in container['Grade']:
            container['Grade'][tamanho] = {}
        if cor not in container['Grade'][tamanho]:
            container['Grade'][tamanho][cor] = qtd
    containers.append(container)

# Obter os valores únicos de grupos e categorias
grupos = df_catalogo['GRUPO'].unique().tolist()
categorias = df_catalogo['Categoria Similar'].unique().tolist()

# Configurar o ambiente Jinja2
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('template.html')

# Renderizar o template com os dados agrupados
html_content = template.render(containers=containers, grupos=grupos, categorias=categorias)

# Escrever o conteúdo HTML em um arquivo
with open('catalogo.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print('Arquivo HTML gerado com sucesso: catalogo.html')
