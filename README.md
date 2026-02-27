![Badge de Concluido](https://img.shields.io/badge/status-Em_Andamento-orange?style=for-the-badge)

# Introdução
Neste projeto de estudo de caso, analiso um conhecido conjunto de dados de vendas no varejo online. O dataset reúne informações detalhadas sobre transações, produtos e clientes, permitindo uma visão abrangente do comportamento de compra.

> [!NOTE]
> O dataset original está disponível no site do **Kaggle** - [Online Retail Transaction Data](https://www.kaggle.com/datasets/thedevastator/online-retail-transaction-data/data)

Os dados serão utilizados como base para aplicar, na prática, conceitos teóricos aprendidos em análise de dados. Embora o próprio Kaggle sugira diferentes abordagens para exploração desse conjunto, neste projeto o foco estará na segmentação de clientes e na análise de vendas, com ênfase na aplicação do modelo RFM e posteriormente na construção de clusters.

# Roadmap do Projeto
Este projeto teve como objetivo analisar o comportamento de clientes a partir de um dataset, aplicando técnicas de segmentação para identificar padrões de consumo e apoiar estratégias de marketing direcionadas.

1. **Entendimento e Exploração dos Dados**

Inicialmente, foi realizada uma análise exploratória abrangente do dataset, contemplando:
- Avaliação qualitativa e quantitativa das variáveis
- Verificação de tipos de dados
- Identificação de valores ausentes
- Análise de inconsistências e registros discrepantes
Também foi conduzida uma análise temporal das transações, permitindo compreender padrões de compra ao longo do tempo.

2. **Tratamento e Preparação dos Dados**

Nesta etapa foram aplicadas técnicas de pré-processamento, incluindo:
- Remoção e tratamento de transações negativas e canceladas
- Tratamento de valores nulos
- Ajustes e padronização das variáveis relevantes
- Construção das métricas necessárias para análise RFM
O objetivo foi garantir a qualidade e consistência dos dados antes da modelagem.

3. **Segmentação com RFM**

Foi aplicada a metodologia RFM (Recency, Frequency e Monetary), técnica amplamente utilizada para segmentação de clientes com base em comportamento de compra. Essa abordagem permitiu identificar:
- Clientes de alto valor
- Clientes recorrentes
- Clientes em risco de inatividade
- Segmentos com potencial de retenção

4. **Clusterização com Machine Learning**

Após a segmentação inicial, foi implementado um modelo de clusterização utilizando algoritmos de Machine Learning, com o objetivo de agrupar clientes com características semelhantes. Para definição do número ideal de clusters, foi utilizado o Método do Cotovelo (Elbow Method), permitindo identificar o ponto de equilíbrio entre complexidade do modelo e variabilidade explicada. Essa etapa possibilitou uma segmentação orientada por dados, complementando a análise RFM manual.

5. **Visualização e Interpretação dos Resultados**

Todas as análises foram acompanhadas de visualizações gráficas para facilitar a interpretação dos resultados e apoiar tomadas de decisão estratégicas.

> Código Fonte: [main](https://github.com/rrafahenrique/Case-Study-Online-Retail-Transaction-Data/blob/master/main.ipynb)

