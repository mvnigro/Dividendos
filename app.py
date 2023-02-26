import yfinance as yf
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


st.set_page_config(page_title="Dividendos Fundos Imobiliários", page_icon=":bar_chart:", layout="wide")

# Título do aplicativo
st.title("Dividendos Fundos Imobiliários")

# Ler arquivo csv com a lista de tickers e adicionar sufixo ".SA"
tickers_df = pd.read_excel("fiis.xlsx")
tickers_list = [ticker + "11.SA" for ticker in tickers_df["Codigo"].tolist()]

# Adicione um menu para o usuário selecionar a ação
selected_ticker = st.selectbox('Selecione uma ação', tickers_list)


# Callback para extrair e exibir os dados da ação selecionada
@st.cache_data
def extract_data(ticker):
    # Obtenha a instância da ação usando yfinance
    stock = yf.Ticker(ticker)

    # Obtenha os dados de dividendos usando a propriedade 'dividends' do objeto Ticker
    dividends = stock.dividends
    dividends = dividends.sort_index(ascending=False)

    # Obtenha os dados de preços de fechamento usando a função history do objeto Ticker
    prices = stock.history(period='5y')['Close']
    prices = prices.sort_index(ascending=False)

    # Calcular o retorno mensal a partir dos preços de fechamento
    monthly_returns = prices.resample('M').ffill().pct_change()

    # Combine os dados de preços, dividendos e retornos mensais em uma tabela única
    df = pd.concat([prices, dividends, monthly_returns], axis=1)
    df.columns = ['Preço de Fechamento', 'Dividendos', 'Retorno Mensal']
    df = df.reset_index()
    df = df.rename(columns={'Date': 'Data'})
    df = df.sort_values('Data', ascending=False)

    return df, dividends, ticker



# Chame o callback com a ação selecionada
df, dividends, ticker = extract_data(selected_ticker)

# Imprima o ticker e a tabela combinada no Streamlit
st.info(f"Ticker: {ticker}")
st.write(df)

# Plot o gráfico de dividendo pela data
fig, ax = plt.subplots()
ax.bar(dividends.index, dividends.values)
ax.set_xlabel('Data')
ax.set_ylabel('Dividendos')
ax.set_title(f'Dividendos para {ticker}')
fig.set_size_inches(12, 6)
st.pyplot(fig)

# Plot o gráfico de retornos mensais ao longo do tempo usando Streamlit
st.line_chart(df.set_index('Data')['Preço de Fechamento'])
