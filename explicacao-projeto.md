# Projeto de Aprendizado Docker

Este projeto foi desenvolvido para ajudar no aprendizado de Docker por meio
da construção de uma aplicação simples composta por multi-containers.
Ele demonstra conceitos importantes do Docker através de um exemplo prático
que pode ser executado localmente.

## O que é este projeto?

Este é um aplicativo simples de mural de mensagens, no qual os usuários podem:

- Visualizar mensagens publicadas por outros usuários
- Adicionar suas próprias mensagens

> Embora a aplicação seja simples, sua construção utilizando Docker demonstra diversos conceitos importantes de containers e boas práticas.

## Componentes do Projeto

A aplicação é composta por três partes principais (containers):

### 1. **Frontend** - O que o usuário vê no navegador

- Um site simples desenvolvido com HTML, CSS e JavaScript
- Executado em um container com servidor web **Nginx**
- Responsável pela interface com o usuário
- Comunica-se com a API do backend

### 2. **Backend** - Processamento das requisições e gerenciamento dos dados

- Uma API desenvolvida em **Python com FastAPI**
- Utiliza **Uvicorn** como servidor ASGI
- Processa as requisições recebidas do frontend
- Valida e processa os dados
- Comunica-se com o banco de dados PostgreSQL

### 3. **Database** - Armazenamento das mensagens

- Um banco de dados **PostgreSQL**
- Responsável por armazenar as mensagens
- Mantém os dados persistentes utilizando **Docker Volumes**

## Conceitos de Docker que vamos aprender

Ao explorar este projeto, você aprenderá sobre:

- **Docker Containers**: ambientes isolados que empacotam tudo o que uma aplicação precisa para funcionar
- **Docker Images**: modelos utilizados para criar containers
- **Docker Compose**: ferramenta utilizada para definir e executar aplicações compostas por múltiplos containers
- **Multi-stage Builds**: criação de imagens Docker mais eficientes e seguras
- **Container Networking**: como os containers se comunicam entre si
- **Volumes & Persistence**: como armazenar dados que permanecem disponíveis mesmo após reinicializações dos containers
- **Environment Variables**: configuração dos containers sem alterar o código da aplicação
- **Docker Best Practices**: práticas relacionadas à segurança, eficiência e organização

## Estrutura do Projeto

```text
docker-multi-container/

├── docker-compose.yml      # Define todos os serviços e como eles trabalham juntos
├── .env                    # Variáveis de ambiente do projeto
├── README.md               # Documentação principal
├── frontend/               # Site com o qual os usuários interagem
│   ├── Dockerfile
│   ├── nginx.conf
│   └── public/             # Arquivos HTML, CSS e JavaScript
│
├── backend/                # Serviço da API
│   ├── Dockerfile
│   ├── requirements.txt    # Dependências Python
│   └── app/                # Código da aplicação FastAPI
│
└── database/               # Banco de dados PostgreSQL
    ├── Dockerfile
    └── init.sql            # Script de inicialização do banco

```

## Como Começar

### 1. Pré-requisitos

Antes de executar o projeto, certifique-se de ter instalado:

- [Docker](https://docs.docker.com/get-docker/)
- Docker Compose, que já está incluído nas versões atuais do Docker

Verifique se o Docker está instalado:

```bash
docker --version
docker compose version

```

### 2. Executar a aplicação

Clone este repositório:

```bash
git clone <repository-url>
```
Acesse o diretório do projeto:

```bash
cd docker-multi-container
```

Inicie todos os serviços:

```bash
docker compose up -d
```

Para construir ou atualizar as imagens antes de iniciar os containers:
```bash
docker compose up -d --build
```

### 3. Acessar a aplicação

Abra o navegador e acesse:

http://localhost:8082

Você deverá visualizar o mural de mensagens.

A aplicação possui três serviços principais:

```
Frontend (Nginx)
       │
       ▼
Backend (FastAPI)
       │
       ▼
PostgreSQL

```

### 4. Acessar a documentação da API

O backend foi desenvolvido utilizando FastAPI, que gera automaticamente
uma documentação interativa da API.

A documentação Swagger pode ser acessada em:

http://localhost:<porta-do-backend>/docs

A documentação alternativa utilizando ReDoc está disponível em:

http://localhost:<porta-do-backend>/redoc

A interface `/docs` permite visualizar e testar os endpoints da API diretamente pelo navegador.

## 5. Visualizar logs e status

Para verificar o status dos containers:
```bash
docker compose ps
```

Para visualizar os logs de todos os serviços:

```bash
docker compose logs
```

Para visualizar os logs de um serviço específico:

```bash
docker compose logs backend
```

Para acompanhar os logs do backend em tempo real:

```bash
docker compose logs -f backend
```

### 6. Parar a aplicação

Para parar os containers:

```bash
docker compose down
```

Esse comando remove os containers e as redes criadas pelo Docker Compose, mas mantém os volumes.

Para remover também os volumes:

```bash
docker compose down -v
```

Atenção: o parâmetro `-v` remove os volumes, incluindo os dados persistidos do PostgreSQL.

## Networking

Este projeto utiliza duas redes Docker:

**frontend-network:** conecta o container do Frontend (Nginx) ao Backend (FastAPI).
**backend-network:** conecta o Backend (FastAPI) ao banco de dados PostgreSQL.

Essa configuração demonstra como:

- Isolar serviços que não precisam se comunicar diretamente.
- Controlar a comunicação entre os containers.
- Evitar que o banco de dados seja acessado diretamente pelo frontend.
- Separar a camada de apresentação da camada de aplicação e da camada de dados.

O fluxo de comunicação é:
```
┌───────────────┐
│    Nginx      │
│   Frontend    │
└───────┬───────┘
        │
        │ frontend-network
        ▼
┌───────────────┐
│    FastAPI    │
│    Backend    │
└───────┬───────┘
        │
        │ backend-network
        ▼
┌───────────────┐
│  PostgreSQL   │
│   Database    │
└───────────────┘
```
## Persistência de Dados

A aplicação utiliza dois Docker Volumes:

### 1. postgres-data

Armazena os arquivos do banco de dados PostgreSQL.

Isso garante que as mensagens não sejam perdidas quando os containers forem reiniciados ou recriados.

### 2. backend-logs

Armazena os logs da aplicação backend.

Isso facilita:

- Debugging
- Monitoramento
- Análise de erros
- Persistência dos logs entre reinicializações dos containers
- Como os Dados Fluem pela Aplicação

Quando o usuário utiliza a aplicação:

- Visualizando mensagens
- O navegador carrega o frontend a partir do container Nginx.
- O JavaScript realiza uma requisição para a API FastAPI.
- O FastAPI recebe a requisição.
- O backend consulta o banco de dados PostgreSQL.
- O PostgreSQL retorna os dados.
- O FastAPI processa e retorna a resposta.
- O frontend recebe e exibe as mensagens no navegador

```
Browser
   │
   ▼
Nginx
   │
   ▼
FastAPI
   │
   ▼
PostgreSQL
   │
   ▼
FastAPI
   │
   ▼
Frontend
   │
   ▼
Browser
```

## Adicionando uma mensagem

- O usuário digita uma mensagem no frontend.
- O JavaScript envia a mensagem para a API FastAPI.
- O FastAPI recebe e valida os dados.
- O backend envia os dados para o PostgreSQL.
- O PostgreSQL armazena a mensagem.
- O FastAPI retorna uma resposta.
- O frontend atualiza a lista de mensagens


## Caminho de Aprendizado

Uma forma recomendada de explorar este projeto:

- Comece entendendo a arquitetura geral da aplicação.
- Analise o arquivo docker-compose.yml para entender como os serviços estão conectados.
- Examine o Dockerfile de cada serviço.
- Explore a configuração do Nginx.
- Analise a API desenvolvida com FastAPI.
- Examine o requirements.txt e as dependências Python.
- Explore o script init.sql utilizado pelo PostgreSQL.
- Analise as redes Docker utilizadas pelos containers.
- Explore os volumes utilizados para persistência.
- Modifique partes da aplicação para aprofundar seu aprendizado.

## Comandos Docker para Experimentar
- Listar containers em execução

```bash
docker ps
```

- Visualizar os logs de um container

`docker logs <container-id>`

- Acessar um container

`docker exec -it <container-id> sh`

- Listar volumes

`docker volume ls`

- Inspecionar um volume
`docker volume inspect postgres-data`

- Listar redes

`docker network ls`

- Ver os containers conectados a uma rede

`docker network inspect frontend-network`

Ver os serviços do Docker Compose

`docker compose ps`

- Reconstruir as imagens

`docker compose build`

- Reiniciar os serviços

`docker compose restart`

- Próximos Passos

Depois de compreender este projeto, a gente pode:

- Adicionar uma nova funcionalidade à aplicação.
- Criar novos endpoints utilizando FastAPI.
- Adicionar testes automatizados com pytest.
- Implementar validação de dados utilizando Pydantic.
- Adicionar migrations utilizando Alembic.
- Adicionar um quarto serviço, como Redis para cache.
- Implementar autenticação na API.
- Criar pipelines de CI/CD utilizando GitHub Actions.
- Adicionar análise de vulnerabilidades utilizando Trivy.
- Aprender sobre orquestração de containers utilizando Kubernetes.

### Troubleshooting

Se encontrar algum problema:

1. Verifique o status dos containers
`docker compose ps`

2. Consulte os logs

`docker compose logs`

Ou consulte os logs de um serviço específico:

`docker compose logs backend`

3. Reconstrua as imagens

`docker compose up -d --build`

4. Verifique as portas

Certifique-se de que todas as portas utilizadas pelo projeto
estão disponíveis na sua máquina.

5. Verifique os recursos do Docker

Certifique-se de que o Docker possui recursos suficientes de:

- CPU
- Memória
- Armazenamento

6. Reinicie os containers

Se necessário, pare e inicie novamente os serviços:

```bash
docker compose down
docker compose up -d
```
