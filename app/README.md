# TC5 - Aplicação Demonstrativa da API

Este repositório contém uma aplicação demonstrativa que ilustra como funciona a API. O objetivo é fornecer um guia passo a passo para a instalação e configuração da aplicação utilizando o Next.js.

## Pré-requisitos

Antes de começar, você precisará ter o seguinte instalado em sua máquina:

- [Node.js](https://nodejs.org/) (versão 12 ou superior)
- [npm](https://www.npmjs.com/) (geralmente instalado junto com o Node.js)

## Executando com Docker

1. Construa a imagem Docker:
   ```sh
   docker build -t app .
   ```
2. Execute o contêiner:
   ```sh
   docker run -p 3000:3000 api
   ```

## Executando com docker compose

1. Suba os serviços:
   ```sh
   docker-compose up --build
   ```

