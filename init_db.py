import os
import pandas as pd
import sqlite3

DB_PATH = os.environ.get('DB_PATH', '/app/data/database.db')
DATA_URL = "https://sistemas.anac.gov.br/dadosabertos/Voos%20e%20opera%C3%A7%C3%B5es%20a%C3%A9reas/Dados%20Estat%C3%ADsticos%20do%20Transporte%20A%C3%A9reo/Dados_Estatisticos.csv"

def create_db():
    print("Baixando os dados da ANAC...")
    df = pd.read_csv(DATA_URL, sep=';', encoding='utf-8', skiprows=1)
    
    print("Processando os dados da ANAC...")
    gol_df = df[(df['EMPRESA_SIGLA'] == 'GLO') & (df['GRUPO_DE_VOO'] == 'REGULAR') & (df['NATUREZA'] == 'DOMÉSTICA')].copy()
    gol_df['MERCADO'] = gol_df.apply(
        lambda row: ''.join(sorted([row['AEROPORTO_DE_ORIGEM_SIGLA'], row['AEROPORTO_DE_DESTINO_SIGLA']])),
        axis=1
    )
    final_df = gol_df[['MERCADO', 'ANO', 'MES', 'RPK']]
    
    print(f"Criando database SQLite em {DB_PATH}...")
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        with open('schema.sql', 'r') as f:
            schema = f.read()
        cursor.executescript(schema)

        print("Salvando dados de voos na database...")
        final_df.to_sql('voos', conn, if_exists='append', index=False)

        conn.commit()
        print("Inicialização da database completa!")

if __name__ == '__main__':
    if not os.path.exists(DB_PATH):
        print("Database SQLite não encontrada. Criando-a a partir de dados web...")
        create_db()