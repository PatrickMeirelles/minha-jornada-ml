import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

URL = 'https://www.infomoney.com.br/tudo-sobre/fundos-imobiliarios/'


def buscar_noticias_fii(url=URL, max_noticias=20):
    """
    Busca as últimas notícias de FIIs no InfoMoney
    Args:
        url (str): URL da página de notícias de FIIs
        max_noticias (int): Quantidade máxima de notícias a buscar
    Returns:
        DataFrame com as notícias
    """
    print(f"Buscando notícias em: {url}")
    resp = requests.get(url)
    if resp.status_code != 200:
        print(f"Erro ao acessar a página: {resp.status_code}")
        return None
    soup = BeautifulSoup(resp.text, 'html.parser')

    noticias = []
    # Seletores baseados na estrutura dos cards de notícia
    cards = soup.find_all('div', {'data-ds-component': ['card-lg', 'card-sm']})
    for card in cards:
        # Título
        titulo_tag = card.find('h2')
        titulo = titulo_tag.get_text(strip=True) if titulo_tag else ''
        # Link
        link_tag = card.find('a', href=True)
        link = link_tag['href'] if link_tag else ''
        # Data/hora
        data_tag = card.find('div', class_='inline-flex')
        data = data_tag.get_text(strip=True) if data_tag else ''
        # Resumo
        resumo_tag = card.find('div', class_='md:line-clamp-3')
        resumo = resumo_tag.get_text(strip=True) if resumo_tag else ''
        if titulo and link:
            noticias.append({
                'titulo': titulo,
                'link': link,
                'data': data,
                'resumo': resumo
            })
        if len(noticias) >= max_noticias:
            break
    if not noticias:
        print('Nenhuma notícia encontrada.')
        return None
    df = pd.DataFrame(noticias)
    return df

def salvar_noticias_csv(df, nome_arquivo=None):
    """
    Salva o DataFrame de notícias em um arquivo CSV
    """
    if nome_arquivo is None:
        nome_arquivo = f'noticias_fii_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    df.to_csv(nome_arquivo, index=False, encoding='utf-8-sig')
    print(f'Arquivo salvo: {nome_arquivo}')

def main():
    print("=== SCRIPT DE BUSCA DE NOTÍCIAS DE FIIs ===")
    df = buscar_noticias_fii()
    if df is not None:
        print(df.head())
        salvar_noticias_csv(df)
    print("\n=== FIM DO SCRIPT ===")

if __name__ == "__main__":
    main()
