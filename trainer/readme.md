# TC5 - Trainer

Este repositório é projetado para gerar um modelo PKL (Pickle) usando a classe `CustomLightFm`. A classe `CustomLightFm` implementa uma versão personalizada do algoritmo LightFM, que é amplamente utilizado para construir o sistemas de recomendação utilizado pela API.

## Visão Geral

O principal objetivo deste projeto é fornecer uma maneira simples de treinar um modelo de recomendação que pode ser salvo e reutilizado posteriormente. O modelo é treinado com dados de interação entre usuários e noticias e pode ser utilizado para fazer recomendações personalizadas.

## Funcionalidades

- Implementação personalizada do algoritmo LightFM
- Capacidade de salvar o modelo treinado no formato PKL para uso futuro

## Como utilizar

Para começar a usar este repositório, siga as instruções abaixo:

### Pré-requisitos

Certifique-se de ter o seguinte instalado:

- Python 3.9 (importante)
- Pacotes Python necessários (listados em `requirements.txt`)

### Executando com Docker

1. Construa a imagem Docker:

   ```bash
   docker build -t trainer .
   ```

2. Instale os pacotes necessários:

   ```bash
   docker run trainer
   ```

### Executando com docker compose

1. Suba os serviços: 

   ```bash
   docker-compose up --build
   ```



