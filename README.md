<!--
title: 'AWS Simple HTTP Endpoint example in Python'
description: 'This template demonstrates how to make a simple HTTP API with Python running on AWS Lambda and API Gateway using the Serverless Framework.'
layout: Doc
framework: v4
platform: AWS
language: python
authorLink: 'https://github.com/serverless'
authorName: 'Serverless, Inc.'
authorAvatar: 'https://avatars1.githubusercontent.com/u/13742415?s=200&v=4'
-->

# Serverless Framework API - SNS/SQS Integration

Este projeto implementa uma arquitetura serverless usando AWS Lambda, API Gateway, SNS e SQS.

## Arquitetura

```
API Gateway → SNS Topic → SQS Queue → Lambda Function
```

### Fluxo de dados:
1. **API Gateway**: Recebe requisições HTTP POST
2. **Lambda (apiHandler)**: Processa a requisição e publica no tópico SNS
3. **SNS Topic**: Distribui mensagens para assinantes
4. **SQS Queue**: Recebe mensagens do SNS
5. **Lambda (sqsHandler)**: Processa mensagens da fila SQS

## Recursos AWS Criados

- **API Gateway**: Endpoint HTTP para receber requisições
- **SNS Topic**: Tópico para distribuição de mensagens
- **SQS Queue**: Fila principal para processamento
- **SQS Dead Letter Queue**: Fila para mensagens que falharam
- **IAM Roles**: Permissões necessárias para as funções Lambda

## Como usar

### 1. Deploy da aplicação

```bash
# Instalar dependências
npm install -g serverless

# Deploy
serverless deploy
```

### 2. Testar a API

Após o deploy, você receberá uma URL do API Gateway. Use-a para testar:

#### Teste da função hello (GET):
```bash
curl https://your-api-gateway-url.amazonaws.com/
```

#### Teste da API (POST):
```bash
curl -X POST https://your-api-gateway-url.amazonaws.com/api \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello World", "data": {"key": "value"}}'
```

### 3. Monitoramento

- **CloudWatch Logs**: Verifique os logs das funções Lambda
- **SQS Console**: Monitore mensagens na fila
- **SNS Console**: Verifique mensagens no tópico

## Estrutura do Projeto

```
├── serverless.yml                    # Configuração principal do Serverless Framework
├── handler.py                       # Arquivo de compatibilidade (importa das funções organizadas)
├── requirements.txt                 # Dependências Python
├── README.md                       # Este arquivo
├── functions/                      # Funções Lambda organizadas
│   ├── __init__.py                 # Torna a pasta um pacote Python
│   ├── hello.py                    # Função hello
│   ├── api_handler.py              # Função API Gateway → SNS
│   └── sqs_handler.py              # Função SQS → Processamento
└── serverless/                     # Configurações do Serverless organizadas
    ├── functions/                  # Configurações das funções Lambda
    │   ├── hello.yml               # Função hello (GET /)
    │   └── apiHandler.yml          # API completa (apiHandler + sqsHandler)
    └── resources/                  # Recursos AWS organizados
        ├── sns.yml                 # Recursos SNS (tópico e subscription)
        └── sqs.yml                 # Recursos SQS (filas e políticas)
```

## Funções Lambda

### hello
- **Trigger**: API Gateway HTTP GET `/`
- **Função**: Retorna mensagem de boas-vindas
- **Input**: Nenhum
- **Output**: Mensagem de sucesso

### apiHandler
- **Trigger**: API Gateway HTTP POST `/api`
- **Função**: Recebe requisições e publica no SNS
- **Input**: JSON body da requisição
- **Output**: Confirmação de envio

### sqsHandler
- **Trigger**: SQS Queue
- **Função**: Processa mensagens da fila
- **Input**: Mensagens SQS (que vieram do SNS)
- **Output**: Confirmação de processamento

## Configurações

### SQS
- **Visibility Timeout**: 60 segundos
- **Message Retention**: 14 dias
- **Dead Letter Queue**: Após 3 tentativas de processamento

### SNS
- **Subscription**: Automática para a fila SQS
- **Message Format**: JSON



## Limpeza

Para remover todos os recursos:

```bash
serverless remove
```

## GitHub Actions - Deploy Automático

Este projeto está configurado para fazer deploy automático usando GitHub Actions sempre que houver push para a branch principal.

### Pré-requisitos

1. **Conta AWS** com permissões para:
   - Lambda
   - API Gateway
   - CloudFormation
   - IAM (para criar roles)
   - SNS
   - SQS

2. **Conta Serverless Framework** (gratuita para projetos pessoais)

### Configuração dos Secrets

Você precisa configurar os seguintes secrets no seu repositório GitHub:

#### 1. Acesse as configurações do repositório
- Vá para `Settings` > `Secrets and variables` > `Actions`
- Clique em `New repository secret`

#### 2. Configure os secrets necessários

**AWS Credentials:**
- **AWS_ACCESS_KEY_ID**: Sua AWS Access Key ID
- **AWS_SECRET_ACCESS_KEY**: Sua AWS Secret Access Key

**Serverless Framework:**
- **SERVERLESS_ACCESS_KEY**: Sua chave de acesso do Serverless Framework

### Como obter as credenciais

#### AWS Credentials
1. Acesse o [AWS IAM Console](https://console.aws.amazon.com/iam/)
2. Crie um novo usuário ou use um existente
3. Anexe a política `AdministratorAccess` (ou uma política mais restrita)
4. Crie Access Keys
5. Copie o Access Key ID e Secret Access Key

#### Serverless Framework Access Key
1. Acesse [Serverless Dashboard](https://app.serverless.com/)
2. Vá para `Access Keys`
3. Crie uma nova Access Key
4. Copie a chave gerada

### Como funciona o workflow

O workflow criado em `.github/workflows/deploy.yml` irá:

1. **Trigger**: Executar quando houver push para `main` ou `master`
2. **Setup**: Configurar Python 3.12 e Node.js 18
3. **Instalação**: Instalar o Serverless Framework globalmente
4. **Credenciais**: Configurar as credenciais AWS
5. **Dependências**: Instalar dependências Python (se houver)
6. **Deploy**: Fazer deploy da aplicação para AWS
7. **Output**: Mostrar informações do deploy

### Personalização

#### Mudar a região AWS
Edite o arquivo `.github/workflows/deploy.yml` e altere:
```yaml
env:
  AWS_REGION: us-east-1  # Mude para sua região preferida
```

#### Adicionar dependências Python
1. Adicione suas dependências no arquivo `requirements.txt`
2. O workflow irá instalá-las automaticamente

#### Deploy apenas em tags
Para fazer deploy apenas quando criar uma tag, altere o trigger:
```yaml
on:
  push:
    tags:
      - 'v*'
```

### Troubleshooting

#### Erro de permissões AWS
- Verifique se as credenciais AWS estão corretas
- Confirme se o usuário AWS tem as permissões necessárias

#### Erro do Serverless Framework
- Verifique se o `SERVERLESS_ACCESS_KEY` está configurado corretamente
- Confirme se sua conta Serverless Framework está ativa

#### Erro de deploy
- Verifique os logs do GitHub Actions para mais detalhes
- Confirme se o `serverless.yml` está configurado corretamente

### Próximos passos para GitHub Actions

1. Configure os secrets no GitHub
2. Faça push para a branch `main`
3. Verifique se o deploy foi executado com sucesso
4. Acesse os endpoints da API gerados:
   - GET `/` - Função hello
   - POST `/api` - API que processa via SNS/SQS
