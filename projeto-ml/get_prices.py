import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt # type: ignore

def buscar_dados_fii(ticker='KNCR11.SA', periodo='1y'):
    """
    Busca dados de um FII usando yfinance
    
    Args:
        ticker (str): Ticker do FII (padrão: XPML11.SA)
        periodo (str): Período dos dados (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
    """
    try:
        print(f"Buscando dados do {ticker}...")
        fii = yf.Ticker(ticker)
        info = fii.info
        print(f"\n=== INFORMAÇÕES BÁSICAS DO {ticker} ===")
        print(f"Nome: {info.get('longName', 'N/A')}")
        print(f"Setor: {info.get('sector', 'N/A')}")
        print(f"Indústria: {info.get('industry', 'N/A')}")
        print(f"Preço atual: R$ {info.get('currentPrice', 'N/A')}")
        print(f"Variação: {info.get('regularMarketChangePercent', 'N/A')}%")
        print(f"Volume: {info.get('volume', 'N/A'):,}")
        print(f"Market Cap: R$ {info.get('marketCap', 'N/A'):,}")

        # Calcular período de exatamente um ano menos um dia
        data_fim = datetime.now().date() - timedelta(days=1)
        data_inicio = data_fim - timedelta(days=364)
        
        print(f"\n=== DADOS HISTÓRICOS DO {ticker} ===")
        print(f"Período: {data_inicio.strftime('%d/%m/%Y')} a {data_fim.strftime('%d/%m/%Y')}")
        print(f"(Exatamente 1 ano menos 1 dia)")
        
        # Buscar dados com datas específicas
        historico = fii.history(start=data_inicio, end=data_fim + timedelta(days=1))
        
        if not historico.empty:
            print(f"Total de dias: {len(historico)}")
            print(historico['Low'].min())
            
            print(f"\nPreço mais alto: R$ {historico['High'].max():.2f}")
            print(f"Preço mais baixo: R$ {historico['Low'].min():.2f}")
            print(f"Preço médio: R$ {historico['Close'].mean():.2f}")
            print(f"Volatilidade (desvio padrão): R$ {historico['Close'].std():.2f}")

            retorno_total = ((historico['Close'].iloc[-1] - historico['Close'].iloc[0]) / historico['Close'].iloc[0]) * 100
            print(f"Retorno total do período: {retorno_total:.2f}%")
            
            # Últimos 5 dias
            print(f"\nÚltimos 5 dias do {ticker}:")
            ultimos_5 = historico.tail(5)[['Close', 'Volume']]
            for data, row in ultimos_5.iterrows():
                print(f"  {data.strftime('%d/%m/%Y')}: R$ {row['Close']:.2f} (Vol: {row['Volume']:,.0f})")
            
            return historico, info
            
        else:
            print(f"Nenhum dado histórico encontrado para {ticker}.")
            return None, info
            
    except Exception as e:
        print(f"Erro ao buscar dados do {ticker}: {e}")
        return None, None

def plotar_grafico(historico, ticker):
    """
    Cria um gráfico com os preços de fechamento
    """
    if historico is not None and not historico.empty:
        plt.figure(figsize=(12, 6))
        plt.plot(historico.index, historico['Close'], linewidth=2)
        plt.title(f'Preços de Fechamento - {ticker}')
        plt.xlabel('Data')
        plt.ylabel('Preço (R$)')
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

def main():
    """
    Função principal
    """
    ticker = 'KNCR11.SA'
    print("=== SCRIPT DE BUSCA DE DADOS DE FII ===")
    print(f"Usando yfinance para buscar dados do {ticker}\n")
    
    # Buscar dados do FII
    historico, info = buscar_dados_fii(ticker, '1y')
    
    # Perguntar se quer ver o gráfico
    if historico is not None:
        resposta = input(f"\nDeseja visualizar o gráfico de preços do {ticker}? (s/n): ").lower()
        if resposta in ['s', 'sim', 'y', 'yes']:
            plotar_grafico(historico, ticker)
    
    print("\n=== FIM DO SCRIPT ===")

if __name__ == "__main__":
    main()