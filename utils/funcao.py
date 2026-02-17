import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns

# Função que personaliza o método describe() do pandas 
# É necessário instalar o pacote jinja2 (pip install jinja2)
def descricão(df):
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
    resumo = pd.DataFrame({
        'Coluna': df.columns,
        'Tipo': df.dtypes.values,
        'Quantidade de Dados Não Vazios': df.notna().sum().values,
        'Quantidade de Dados Vazios': df.isna().sum().values,
        'Valores Únicos': df.nunique(),
        'Porcentagem de Valor Vazios (%)': (df.isna().mean() * 100).round(2).values
        
    })

    styled = (resumo.style
        .set_properties(**{
            'background-color': "#0f010194", 
            'border-color': 'black',
            'text-align': 'center'
        })
        .background_gradient(subset=['Porcentagem de Valor Vazios (%)'], cmap='Reds')
        .bar(subset=['Quantidade de Dados Vazios'], color='#BE0804')
        .set_table_styles([
            {
                'selector': 'th',
                'props': [
                    ('background-color', '#0d253f'),
                    ('color', 'white'),
                    ('text-align', 'center'),
                    ('font-size', '12px')
                ]
            }
        ])
    )
    return styled
#------------------------------------------------------------------------------------------------
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

    plt.figure(figsize=(14, 6))
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

    plt.figure(figsize=(10, 5))
    sns.barplot(
        x=vendas_por_mes.index,
        y=vendas_por_mes.values
    )

    plt.title(f'Quantidade de Vendas por Mês do ano de 2011')
    plt.xlabel('Mês')
    plt.ylabel('Quantidade Vendida')

    sns.despine()
    plt.show()
#---------------------------------------------------------------------
def plot_rfm_segmentos(df):
    """
    Plota a distribuição de clientes por segmentos RFM.

    Parâmetros:
    - df: DataFrame contendo os segmentos
    """

    # Dicionário de cores personalizado
    cores = {
        "Bronze": "#CD7F32",
        "Prata": "#C0C0C0",
        "Ouro": "#FFD700",
        "Platinum": "#8C8E90"
    }

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

    # Estilo
    sns.set(style="darkgrid")

    plt.figure(figsize=(10,5))

    sns.barplot(
        data=segment_counts,
        x="RFM_Segment",
        y="Count",
        hue="RFM_Segment",
        dodge=False,
        palette=cores,
        legend=False
    )

    plt.title("Distribuição de Clientes por Segmentos do RFM")
    plt.xlabel("Segmentos do RFM")
    plt.ylabel("Número de Clientes")

    plt.tight_layout()
    plt.show()
#----------------------------------------------------------------------------------
def plot_segmentos_rfm(df):
    """
    Plota a distribuição dos segmentos RFM destacando um segmento específico.

    Parâmetros:
    - df: DataFrame com os segmentos
    """

    # Contagem ordenada
    segment_counts = (
        df["Segmento Clientes"]
        .value_counts()
        .sort_index()
    )

    # Criar paleta pastel base
    base_palette = sns.color_palette("Paired", len(segment_counts))

    sns.set_theme(style="whitegrid")

    plt.figure(figsize=(12,5))

    ax = sns.barplot(
        x=segment_counts.index,
        y=segment_counts.values,
        hue=segment_counts.index,
        palette=base_palette
    )

    plt.title("Comparando os Segmentos do RFM", fontsize=16, weight="bold")
    plt.xlabel("Segmento RFM")
    plt.ylabel("Número de Clientes")


    sns.despine()
    plt.tight_layout()
    plt.show()
#----------------------------------------------------------------------------
def plot_heatmap_correlacao_rfm(df):
    """
    Plota a matriz de correlação dos scores RFM para um segmento específico.

    Parâmetros:
    - df: DataFrame com dados RFM
    """

    # Filtrar segmento
    df_segmento = df[df["Segmento Clientes"] == "VIP"]

    # Calcular correlação
    correlation_matrix = df_segmento[["Recency Score", "Frequency Score", "Monetary Score"]].corr()

    # Estilo
    sns.set_theme(style="white")

    plt.figure(figsize=(6, 5))

    sns.heatmap(
        correlation_matrix,
        annot=True,
        fmt=".2f",
        cmap="RdBu_r",
        center=0,
        linewidths=0.5,
        cbar_kws={"label": "Correlação"}
    )

    plt.title(f"Matriz de Correlação RFM - VIP", 
              fontsize=14, weight="bold")

    plt.tight_layout()
    plt.show()
