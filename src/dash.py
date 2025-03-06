from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly.utils import PlotlyJSONEncoder
import json
from . import db
from .models import Voos

dash = Blueprint('dash', __name__)

# função para obter os mercados e contagem de voos com RPK não nulo (mas pode ser 0)
# serve para popular o dropdown de mercados
def get_markets_with_counts():
    results = db.session.execute(
        db.select(
            Voos.mercado,
            db.func.count(Voos.rpk)
        ).where(Voos.rpk != None)
        .group_by(Voos.mercado)
        .order_by(Voos.mercado)
    ).all()
    return [(market, count) for market, count in results]

# função para obter o ano mínimo e máximo do banco de dados
# serve para limitar o seletor de data
def get_date_range():
    results = db.session.execute(
        db.select(
            db.func.min(Voos.ano), 
            db.func.max(Voos.ano)
        ).where(Voos.rpk != None)
    ).first()

    min_date = f'{results[0]}-01'
    max_date = f'{results[1]}-12'
    
    return min_date, max_date

# função para extrair os dados do banco de dados e criar a visualização
def create_visualization(market, start_year, start_month, end_year, end_month):
    # fazemos uma filtragem inicial só por ano, e aí filtramos por mês com a conveniência do datetime
    results = db.session.execute(
        db.select(
            Voos.ano, 
            Voos.mes, 
            Voos.rpk
        ).where(
            Voos.mercado == market,
            Voos.ano >= start_year,
            Voos.ano <= end_year,
            Voos.rpk != None
        ).order_by(Voos.ano, Voos.mes)
    )
    
    # inicializamos a dataframe e criamos uma coluna data para facilitar o tratamento e visualização
    df = pd.DataFrame(results.fetchall(), columns=['ano', 'mes', 'rpk'])
    df['date'] = pd.to_datetime({'year' : df['ano'], 'month': df['mes'], 'day': 1})
    
    # filtramos por mês usando datetime
    start_date = pd.Timestamp(year=start_year, month=start_month, day=1)
    end_date = pd.Timestamp(year=end_year, month=end_month, day=1)
    df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    
    # criamos a figura usando o plotly e a coluna em datetime
    # notávelmente o plotly já permite filtrar por data no eixo x pois é interativo,
    # mas ainda é útil filtrar via SQL para reduzir a quantidade de dados em memória
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['date'], y=df['rpk'], mode='markers', marker={'color': '#0B3142'}))

    fig.update_layout(
        title='Evolução Temporal de RPK',
        height=600,
        xaxis_title='Data',
        yaxis_title='RPK'
    )

    # o plotly tende a centrar o gráfico nos dados, então forçamos ele a mostrar o intervalo completo
    # isso permite que os gráficos sejam mais comparáveis entre si
    # subtraímos e somamos dos limites para que seja mais fácil ver os pontos extremos
    x_start = start_date - pd.DateOffset(months=2)
    x_end = end_date + pd.DateOffset(months=2)
    fig.update_xaxes(
        range=[x_start, x_end]
    )
    
    # criamos uma tabela com os dados para renderizar em HTML
    table_data = df.to_dict('records')
    
    # serializamos os dados da figura para JSON, para renderizar no plotly.js
    graph_data = json.dumps(fig, cls=PlotlyJSONEncoder)
    
    return graph_data, table_data

# rota principal do dashboard
@dash.route('/', methods=['GET'])
@login_required
def index():
    # obtemos os mercados e datas para popular o dropdown e limitar o seletor de data
    markets_with_counts = get_markets_with_counts()
    min_date, max_date = get_date_range()
    
    # obtemos os resultados das get requests para filtrar os dados
    # senão, deixamos como padrão o primeiro mercado e as datas min e max
    market = request.args.get('market', markets_with_counts[0][0])
    start_date = request.args.get('start_date', min_date)
    end_date = request.args.get('end_date', max_date)
    
    start_year, start_month = [int(x) for x in start_date.split('-')]
    end_year, end_month = [int(x) for x in end_date.split('-')]

    graph_json, table_data = create_visualization(
        market, 
        start_year, start_month,
        end_year, end_month
    )
    
    return render_template('dash.html',
                         markets=markets_with_counts,
                         min_date=min_date,
                         max_date=max_date,
                         selected_market=market,
                         selected_start_date=start_date,
                         selected_end_date=end_date,
                         graph_json=graph_json,
                         table_data=table_data)