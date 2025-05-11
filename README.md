# Sales Report API

Este projeto é uma API construída com **FastAPI** para ler um arquivo CSV de vendas, armazenar registros em um banco PostgreSQL hospedado no Supabase e gerar relatórios em JSON e PDF.

## Funcionalidades

- **Upload de CSV** (`POST /upload_csv`): envia um arquivo `vendas.csv` e insere registros na tabela `sales`.
- **Relatório JSON** (`GET /report`): retorna vendas agregadas por produto, melhor vendedor e total geral.
- **Relatório PDF** (`GET /report/pdf`): gera um PDF formatado do mesmo relatório.

## Tecnologias

- Python 3.12
- FastAPI
- Uvicorn
- SQLAlchemy
- PostgreSQL (Supabase)
- ReportLab (geração de PDF)
- Docker + Docker Compose

## Requisitos

- Docker e Docker Compose instalados

## Variáveis de ambiente

Defina um arquivo `.env` na raiz do projeto com:

```
DATABASE_URL=postgresql://postgres:<SENHA>@db.<ID>.supabase.co:5432/postgres?sslmode=require
```

> **Observações:**
> - Use a connection string da aba "psql" no Supabase.

## Como usar

1. Clone o repositório:
   ```bash
   git clone https://github.com/RafaelAbath/teste-mirantes
   cd teste-mirantes
   ```
2. Crie o `.env` com a variável `DATABASE_URL`.
3. Suba os containers:
   ```bash
   docker compose up --build -d
   ```
4. Acesse a documentação interativa swagger:
   ```
   http://localhost:8000/docs
   ```

## Endpoints


 POST   | `/upload_csv`  | Recebe o CSV e insere registros      |
 GET    | `/report`      | Retorna relatório em JSON            |
 GET    | `/report/pdf`  | Retorna relatório em PDF             |
 

## Testes

### Com `curl`

```bash
curl -F "file=@vendas.csv" http://localhost:8000/upload_csv
curl http://localhost:8000/report | jq
curl http://localhost:8000/report/pdf --output relatorio_vendas.pdf
```

### Automatizados (pytest)

1. Instale dependências de teste:
   ```bash
   pip install pytest httpx
   ```
2. Execute:
   ```bash
   pytest -q
   ```

## Dockerfile e Dependências do Sistema

O `Dockerfile` inclui instalação de:

- build-essential, python3-dev, pkg-config
- libcairo2-dev, meson, ninja-build (para gerar PDF)


