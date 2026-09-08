import streamlit as st
import pandas as pd
import plotly.express as px
st.set_page_config(
    page_title='Dashboard de Dados',
    layout='wide'
)
st.title('Dashboard de Dados')
st.markdown(
    'Esse Dashboard foi feito por: Marcos Mariano 2CDD01, '
    'Thiago Daparé 2CDD01, Matheus Costa Queiroz 2CDD01'
)
arquivo = st.file_uploader(
    'Envie um arquivo CSV',
    type=['csv']
)
if arquivo is not None:
    df = pd.read_csv(arquivo)
    df = df.drop_duplicates()
    df['População'] = pd.to_numeric(
        df['População'],
        errors='coerce'
    )
    df['Homicídios'] = pd.to_numeric(
        df['Homicídios'],
        errors='coerce'
    )
    df['Taxa /100K/ano'] = pd.to_numeric(
        df['Taxa /100K/ano'],
        errors='coerce'
    )
    st.subheader('Visualização dos dados')
    st.dataframe(df.head())
    col1, col2 = st.columns(2)
    col1.metric(
        'Quantidade de Bairros',
        df['Bairro'].nunique()
    )
    col2.metric(
        'Quantidade de informações obtidas',
        df.shape[1]
    )
    Bairro = df['Bairro'].dropna().unique().tolist()
    opcoes = ['Todos'] + Bairro
    st.sidebar.header('Filtros para bairro específico')
    bairro_escolhido = st.sidebar.selectbox(
        'Bairro:',
        opcoes
    )
    população_mínima = st.sidebar.slider(
        'Mínimo de população:',
        0.0,
        200000.0,
        0.0
    )
    if bairro_escolhido == 'Todos':
        df_filtrado = df.copy()
    else:
        df_filtrado = df[
            df['Bairro'] == bairro_escolhido
        ]
    df_filtrado = df_filtrado[
        df_filtrado['População'] >= população_mínima
    ]
    st.subheader('Dados filtrados')
    st.dataframe(df_filtrado)
    grafico_Homicídios = px.bar(
        df_filtrado,
        x='Bairro',
        y='Taxa /100K/ano',
        title='Valor da Taxa de Homicídios por Bairro nos últimos 3 anos'
    )
    st.plotly_chart(
        grafico_Homicídios,
        use_container_width=True
    )
    st.markdown('''
    O gráfico mostra as diferenças nas taxas de homicídio entre
    os bairros de São Paulo. A Sé apresenta a maior taxa,
    enquanto o Cursino não registrou homicídios nos últimos
    três anos. Os bairros apresentam taxas variadas, sem
    relação direta aparente entre população e número de homicídios.
    ''')
    grafico_pizza = px.pie(
        df_filtrado,
        names='Bairro',
        values='Homicídios',
        title='Homicídios por bairro'
    )
    st.plotly_chart(
        grafico_pizza,
        use_container_width=True
    )
    st.markdown('''
    Este gráfico apresenta a distribuição dos homicídios
    registrados nos últimos 3 anos entre os bairros analisados.
    Cada fatia representa um bairro, e o tamanho da fatia indica
    a participação daquele bairro no total de homicídios.
    ''')
    st.title('Perguntas')
    st.markdown('''
    **1. Qual informação aparece?**

    Gráfico sobre a segurança de cada bairro.

    **2. Qual é o maior valor?**

    O maior valor é o bairro Sé.

    **3. Existe algum valor muito diferente?**

    Sim. O bairro Cursino não tem nenhum homicídio registrado
    nos últimos três anos.

    **4. Existe aumento ou diminuição?**

    Não. Os bairros mantêm suas respectivas taxas de homicídios.

    **5. Existem diferenças entre categorias?**

    Sim. Existem bairros que têm mais casos de homicídios do que outros.

    **6. Existe algum padrão aparente?**

    Não existe relação direta entre quantidade de pessoas e
    homicídios em determinados bairros.
    ''')
    st.markdown('''
1. O que investigamos?
                
Nosso tema escolhido foi segurança, utilizamos dados de homicídios dos bairros centrais de São Paulo, e pesquisamos sobre o tema

                
2. Qual base utilizamos?
                
Utilizamos o site Crime Brasil com os dados do IBGE
                
3. O que os dados mostraram?
                
Mostram que a parte central de São Paulo tem muitos casos de homicídios
                
4. Onde a IA ajudou?
                
Foi utilizada a Inteligência Artificial para analisar o código, organizar os dados e responder perguntas.
            ''')
    st.title('Perguntas Gerais')
    st.markdown('''
Por que os bairros centrais lideram o ranking de taxa por habitante?
 
Ocorre devido ao "efeito do denominador". Bairros como Sé, Brás e República têm poucos moradores fixos, mas recebem um enorme fluxo de pessoas todos os dias. Como a taxa divide os crimes pela quantidade de moradores cadastrados, a conta infla artificialmente o resultado final por 100 mil habitantes.
 
Por que os bairros com menor taxa são mais seguros e quais são eles?
 
Eles são mais seguros por reunirem maior infraestrutura urbana, patrulhamento, vigilância privada, uso de solo estritamente residencial e menor incidência de disputas territoriais de crime organizado.                
''')