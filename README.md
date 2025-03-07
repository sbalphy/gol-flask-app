# GOL - Visualização web de dados de voo

Projeto desenvolvido para o processo seletivo de Desenvolvedor - Python da GOL Linhas Aéreas.

Consiste num aplicativo web desenvolvido em Python (Flask). Ele processa os dados públicos de voo da ANAC dentro das especificações do case (voos domésticos regulares da GOL) numa database SQLite, e aí usa esses dados para visualizar o RPK (Revenue Passenger Kilometers, quantos quilômetros de passageiros pagos foram transportados) de diferentes mercados da GOL. Um mercado é definido como um par de aeroportos: e.g. SBAESBBR são todos os voos entre os aeroportos de SBAE (Bauru-Arealva) e SBBR (Internacional de Brasília), independentemente da direção.

O aplicativo possui autenticação básica (usuário e senha base são admin) usando Flask-Login e uma tabela em plaintext do SQLite. A visualização foi feita usando o Plotly (criada em Python e exportada para o plotly.js via JSON), o que permite que você interaja com os gráficos gerados (selecione uma porção para visualizar, etc). Além disso, você pode filtrar o mercado e range de datas que você deseja examinar. Usamos o Bootstrap para estilizar a página.

Para rodar o aplicativo, basta:

Clonar o repositório via Git:
```
git clone https://github.com/sbalphy/gol-flask-app.git
cd gol-flask-app
```
Buildar a imagem Docker definida na Dockerfile:
```
docker build . -t sbalphy/gol-flask-app:latest
```
(ou pullar do Docker Hub):
```
docker pull sbalphy/gol-flask-app:latest
```
e executar o compose.yml para levantar o container com o mapeamento de portas, variáveis de ambiente e mountpoints corretos:
```
docker compose up
```
Com o aplicativo funcional na sua máquina local, ele estará disponível na porta 5000 do localhost (localhost:5000 em qualquer web browser).

## Notas
A imagem está disponível no Docker Hub em https://hub.docker.com/repository/docker/sbalphy/gol-flask-app/general. Ela também está publicada no Microsoft Azure em https://gol-flask-app-eddeg0akcwfme0ha.brazilsouth-01.azurewebsites.net/. 

A database SQLite é montada no mountpoint /app/data associado ao diretório data. Ela está incluída no repositório e na imagem pois é pequena, mas ela também pode ser construída usando o script init_db.py. Uso de volumes/bind mounts permite persistência mesmo se decidirmos tratar com uma quantidade maior de dados.
