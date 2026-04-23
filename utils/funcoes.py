import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns

# Função que personaliza o método describe() do pandas 
def df_summary_report(df):
    """
    Descreve valores estatísticos da dataframe.

    Parâmetros
    ----------
    df : pd.DataFrame
        DataFrame a ser analisado.
    Retorno
    -------
    pd.Series
        Valores estatísticos e quantitativos estilizados.
    """

    moda = df.mode().iloc[0]

    mem_consumo = df.memory_usage(deep=True, index=False)/1024**2
    total = sum(mem_consumo)

    freq = df.apply(
        lambda col: col.value_counts(dropna=True).iloc[0]
        if not col.dropna().empty else None
    )


    resumo = pd.DataFrame({
        'Coluna': df.columns,            #Lista os nomes das colunas do DataFrame.
        'Tipo': df.dtypes.values,        #Retorna o tipo de dado (dtype) de cada coluna.
        'Quantidade de Dados Não Vazios': df.notna().sum().values,  #Conta a quantidade de valores não nulos por coluna.
        'Quantidade de Dados Vazios': df.isna().sum().values,       #Conta a quantidade de valores nulos (NaN) por coluna.
        'Valores Únicos': df.nunique().values,       #Conta a quantidade de valores únicos de cada coluna
        'Valor mais Frequente': moda,    #Calcula a moda de cada coluna    
        'Frequência': freq,               #Mostra a frequência da moda
        'Porcentagem de Unicidade': ((df.nunique() / len(df)) * 100).round(2).values,    #Cardinalidade - baixa cardinalidade indica alta repetição; alta cardinalidade indica baixa repetição
        'Porcentagem de Valor Vazios (%)': (df.isna().mean() * 100).round(2).values,  #Calcula a porcentagem de valores nulos por coluna.
        f'Consumo de Memória - Total: {total:.2f} (MB)': mem_consumo    #Calcula a quantidade de memória usada pelo dataset
    }).reset_index(drop=True)

    #colormaps
    cmap_vazios = sns.light_palette("#BD2A2E", as_cmap=True)
    cmap_unicidade = sns.light_palette("#13678A", as_cmap=True)
    cmap_unique = sns.light_palette("#1f77b4", as_cmap=True)
    cmap_freq = sns.light_palette("#13678A", as_cmap=True)

    styled = (resumo.style
        .set_properties(**{
            'background-color': "#101719",
            'color': '#E0E0E0',  
            'border': '1px solid #2F3D40',
            'text-align': 'center'
        })
        .background_gradient(subset=['Porcentagem de Valor Vazios (%)'], cmap=cmap_vazios, vmin=0, vmax=100)
        .background_gradient(subset=['Porcentagem de Unicidade'], cmap=cmap_unicidade, vmin=0, vmax=100)
        .background_gradient(subset=["Valores Únicos"],cmap=cmap_unique)
        .background_gradient(subset=["Frequência"],cmap=cmap_freq)
        .background_gradient(subset=[f"Consumo de Memória - Total: {total:.2f} (MB)"], cmap=cmap_freq)
        .bar(subset=['Quantidade de Dados Vazios'], color="#BD2A2E")
        .format({'Porcentagem de Valor Vazios (%)': '{:.2f}', 'Porcentagem de Unicidade': '{:.2f}'})
        .set_table_styles([{
                'selector': 'th',
                'props': [
                    ('background-color', "#0c2845"),
                    ('color', 'white'),
                    ('text-align', 'center'),
                    ('font-size', '13px')
                ]
            }
        ])
        .set_properties(
            subset=pd.IndexSlice[:, resumo.columns[0]],**{
                'background-color': '#012030',
                'font-weight': 'bold',
                'color': '#FFFFFF'
            })
        
    )
    return styled
#-----------------------------------------------------------------------------------------------------
def df_describe_report(df):
    """
    Gera um relatório estatístico descritivo formatado para variáveis numéricas.

    A função calcula métricas como média, desvio padrão, mínimo,
    quartis e máximo, exibindo o resultado em formato transposto
    e com estilização visual utilizando pandas Styler.

    Parâmetros
    ----------
    df : pandas.DataFrame
        DataFrame contendo os dados a serem analisados.

    Retorno
        Tabela estilizada com estatísticas descritivas.
    """

    stats = pd.DataFrame({
        "Média": df.mean(numeric_only=True),
        "Desvio Padrão": df.std(numeric_only=True),
        "Valor Mínimo": df.min(numeric_only=True),
        "Primeiro Quartil - Q1": df.quantile(0.25, numeric_only=True),
        "Segundo Quartil - Q2/Mediana": df.quantile(0.50, numeric_only=True),
        "Terceiro Quartil - Q3": df.quantile(0.75, numeric_only=True),
        "Valor Máximo": df.max(numeric_only=True)
    }).T.reset_index().rename(columns={"index": "Estatística"})
    
    #colormaps
    cmap_cor = sns.light_palette("#13678A", as_cmap=True)

    styled = (stats.style 
            .set_properties(**{ 
            'background-color': "#101719", 
            'color': '#E0E0E0', 
            'border': '1px solid #2F3D40', 
            'text-align': 'center' 
            }) 
    
        #gradient para todas as colunas numéricas 
        .background_gradient(cmap=cmap_cor) 
        .format(precision=3) # formatação numérica 
        .set_table_styles([{ 
            'selector': 'th', 
            'props': [ 
                ('background-color', "#0c2845"), 
                ('color', 'white'), 
                ('text-align', 'center'), 
                ('font-size', '13px') 
                ]} 
            ])
        .set_properties(
            subset=pd.IndexSlice[:, stats.columns[0]],**{
                'background-color': '#012030',
                'font-weight': 'bold',
                'color': '#FFFFFF'
        })
            
        ) 
    
    return styled
#--------------------------------------------------------------------------------------------------------
def plot_vendas_mensais(df):
    """
    Plota vendas mensais agregadas ao longo do tempo.

    Parâmetros:
    - df: DataFrame original
    """

    # Criar cópia para evitar modificar o df original
    df_temp = df.copy()

    # Criar coluna ano_mes
    df_temp['ano_mes'] = df_temp["InvoiceDate"].dt.to_period('M')

    # Agrupar
    vendas_mes = df_temp.groupby('ano_mes')["Quantity"].sum()

    # Converter índice para datetime
    vendas_mes.index = vendas_mes.index.to_timestamp()

    # Garantir continuidade temporal
    idx_completo = pd.date_range(
        start=vendas_mes.index.min(),
        end=vendas_mes.index.max(),
        freq='MS'
    )

    vendas_mes = vendas_mes.reindex(idx_completo, fill_value=0)

    # Estilo
    sns.set_theme(style="whitegrid", context="talk")

    plt.figure(figsize=(15, 5))
    ax = sns.lineplot(
        x=vendas_mes.index,
        y=vendas_mes.values,
        marker="o"
    )

    # Formatação do eixo X
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

    plt.xticks(rotation=45)
    plt.title("Vendas Mensais ao Longo do Tempo", fontsize=18, weight="bold")
    plt.xlabel("Ano-Mês")
    plt.ylabel("Total")

    sns.despine()
    plt.tight_layout()
    plt.show()
#---------------------------------------------------------------------------
def plot_vendas_ano(df):
    """
    Plota a quantidade total vendida por mês.

    Parâmetros:
    - df: DataFrame original
    """
    vendas_por_mes = (
        df.groupby(df['InvoiceDate'].dt.month)['Quantity']
        .sum()
        .reindex(range(1, 13), fill_value=0)
    )

    sns.set_theme(style="whitegrid")

    plt.figure(figsize=(15, 5))
    sns.barplot(
        x=vendas_por_mes.index,
        y=vendas_por_mes.values
    )

    plt.title(f'Quantidade de Vendas por Mês do ano de 2011', fontsize=18, weight="bold")
    plt.xlabel('Mês')
    plt.ylabel('Quantidade Vendida')

    sns.despine()
    plt.show()
#---------------------------------------------------------------------
def plot_rfm_segmentos(df, palette=None):
    """
    Plota a distribuição de clientes por segmentos RFM.

    Parâmetros:
    - df: DataFrame contendo os segmentos
    - palettle: Paleta de cor customizada
    """

    # Contagem dos segmentos
    segment_counts = (
        df["Segmento RFM"]
        .value_counts()
        .rename_axis("RFM_Segment")
        .reset_index(name="Count")
    )

    # Definir ordem hierárquica dos segmentos
    ordem_segmentos = ["Bronze", "Prata", "Ouro", "Platinum"]
        
    segment_counts["RFM_Segment"] = pd.Categorical(
        segment_counts["RFM_Segment"],
        categories=ordem_segmentos,
        ordered=True
    )
    # Ordenar respeitando a hierarquia definida
    segment_counts = segment_counts.sort_values("RFM_Segment")

    plt.figure(figsize=(10,5))

    sns.barplot(
        data=segment_counts,
        x="RFM_Segment",
        y="Count",
        hue="RFM_Segment",
        dodge=False,
        palette=palette[:4],
        legend=False
    )

    plt.title("Distribuição de Clientes por Segmentos do RFM")
    plt.xlabel("Segmentos do RFM")
    plt.ylabel("Número de Clientes")

    plt.tight_layout()
    plt.show()
#----------------------------------------------------------------------------------
def plot_segmentos_rfm(df, palette=None):
    """
    Plota a distribuição dos segmentos RFM destacando um segmento específico.

    Parâmetros:
    - df: DataFrame com os segmentos
    - palettle: Paleta de cor customizada
    """

    # Contagem ordenada
    segment_counts = (
        df["Segmento Clientes"]
        .value_counts()
        .sort_index()
    )

    sns.set_theme(style="whitegrid")

    plt.figure(figsize=(12,5))

    ax = sns.barplot(
        x=segment_counts.index,
        y=segment_counts.values,
        hue=segment_counts.index,
        palette=palette
    )

    plt.title("Comparando os Segmentos do RFM", fontsize=16, weight="bold")
    plt.xlabel("Segmento RFM")
    plt.ylabel("Número de Clientes")


    sns.despine()
    plt.tight_layout()
    plt.show()
#----------------------------------------------------------------------------
def plot_heatmap_correlacao_rfm(df, palette=None):
    """
    Plota a matriz de correlação dos scores RFM para um segmento específico.

    Parâmetros:
    - df: DataFrame com dados RFM
    - palettle: Paleta de cor customizada
    """

    # Filtrar segmento
    df_segmento = df[df["Segmento Clientes"] == "VIP"]

    # Calcular correlação
    correlation_matrix = df_segmento[["Recency Score", "Frequency Score", "Monetary Score"]].corr()

    # Estilo
    custom_cmap = LinearSegmentedColormap.from_list("poseidon_cmap", palette)

    plt.figure(figsize=(10, 6))

    sns.heatmap(
        correlation_matrix,
        annot=True,
        fmt=".2f",
        #cmap="RdBu_r",
        cmap=custom_cmap,
        center=0,
        linewidths=0.5,
        cbar_kws={"label": "Correlação"}
    )

    plt.title(f"Matriz de Correlação RFM - VIP", 
              fontsize=14, weight="bold")

    plt.tight_layout()
    plt.show()