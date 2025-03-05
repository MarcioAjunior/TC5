# API

Este repositório contém uma API desenvolvida com **FastAPI** para servir um modelo de recomendação de notícias.
A API se conecta a um banco de dados PostgreSQL utilizando **psycopg2** e expõe diversas rotas definidas no arquivo `main.py`.

## Estrutura da api

- **`utils/`**: Contém os arquivos PKL utilizados pela API, bem como funções utilitárias.
- **`main.py`**: Arquivo principal onde estão definidas as rotas da API.

## Rotas da API

A API expõe as seguintes rotas:

### `POST /predict`
- **Descrição**: Rerotorna uma lista de predições para o usuário informado como entrada. Além disso permite a utilização de Heuristicas para recomendação.
- **Entrada**:
  ```json
  {
    "user_id": "LSKxsecX-csmklLKC23M23-D22d3i2mkl",
    "use_heuristic": false,
    "qtty_recommendations": 5
  }
- **Resposta**:
  ```json
  { "prediction": [{"id":"kwCD3k3d-2mclsSCEJAQP-S2D3NghSQiD3", "title": "Noticia 1", "subtitulo": "Noticia 1", "url": "noticia1.com.br"}, ...] }
  ```

### `POST /add_news`
- **Descrição**: Recebe informações sobre uma noicía e adiciona-a ao banco de dados e ao modelo.
- **Entrada**:
  ```json
  {
    "title": "Nova Notícia",
    "subtitle": "Subtítulo da Notícia",
    "boody": "Corpo da Notícia",
    "url": "https://www.exemplo.com/nova-noticia"
  }
  ```
- **Resposta**:
  ```json
  {
    "news": "kwCF3V3k3d-2mcldsasSCEJAQP-S2D84FdRhSQiD3"
  }
  ```

### `POST /add_user`
- **Descrição**: Registra um noco usuário no banco de dados e ao modelo.
- **Entrada**:
  ```json
  {
    "nome": "Novo Usuário",
  }
  ```
- **Resposta**:
  ```json
  {
    "user": "d3xXJ4ascXW-2mcldsC34dQAQP-S2D8BBgt1SQiD3"
  }
  ```

### `POST /fit`
- **Descrição**: Rota disponibilizada para permitir retreinar o modelo.
- **Entrada**:
  ```json
  {
    "fit": true,
    "len_train": 10000 // Tamanho do dataset de treino
  }
  ```
- **Resposta**:
  ```json
  {
    "stated": true // Iniciado processo de treinamento
  }
  ```

### `POST /read_news`
- **Descrição**: Registra uma nova interação de um usuário com uma notícia. Alterando o embedding desse usuário.
- **Entrada**:
  ```json
  {
    "user_id": "65DKckwlc-596SEyJcdCQ-sdXAwad5ce9",
    "news_id": "fdse93Cels-cmwErv4PcE-Kdl34S0o23",
  }
  ```
- **Resposta**:
  ```json
  {
    "read": 5 // Iniciado processo de treinamento
  }
  ```

## Executando com Docker

1. Construa a imagem Docker:
   ```sh
   docker build -t api .
   ```
2. Execute o contêiner:
   ```sh
   docker run -p 8000:8000 api
   ```

## Executando com docker compose

1. Suba os serviços:
   ```sh
   docker-compose up --build
   ```


