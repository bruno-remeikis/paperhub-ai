# Paperhub AI

## Projeto

...

## Tecnologias utilizadas

...

## Get Started

### ⚙️ Configurações iniciais

Crie um arquivo chamado `.env` na raiz deste projeto.\
Neste arquivo, cole as variáveis abaixo e preencha-as ou altere-as de
acordo com sua necessidade.
```properties
GOOGLEAI_API_KEY=
FASTAPI_HOST=0.0.0.0
FASTAPI_PORT=8000
```

Para rodar a aplicação, é necessário ter o [Docker](https://www.docker.com/get-started/) instalado e rodando em sua máquina.

### 📦 Construir imagem
Antes de, de fato, rodarmos a aplicação, precisamos construir sua imagem Docker. Para isso, execute: 
```sh
docker compose build
```

**Obs.:** Este passo é necessário sempre que or arquivos Docker ou `requirements.txt` forem alterados

### 🚀 Rodar aplicação
Já tendo a imagem construída, para rodarmos a aplicação, execute: 
```sh
docker compose up
```