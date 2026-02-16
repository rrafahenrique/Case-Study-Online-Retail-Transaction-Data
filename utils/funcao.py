import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
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