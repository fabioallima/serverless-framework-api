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

# Serverless Framework Python HTTP API on AWS

Este template demonstra como criar uma API HTTP simples com Python rodando no AWS Lambda e API Gateway usando o Serverless Framework.

Este template não inclui nenhum tipo de persistência (banco de dados). Para exemplos mais avançados, confira o [repositório serverless/examples](https://github.com/serverless/examples/) que inclui exemplos com DynamoDB, Mongo, Fauna e outros.

## Uso

### Deploy Manual

```
serverless deploy
```

Após o deploy, você deve ver uma saída similar a:

```
Deploying "aws-python-http-api" to stage "dev" (us-east-1)

✔ Service deployed to stack aws-python-http-api-dev (85s)

endpoint: GET - https://6ewcye3q4d.execute-api.us-east-1.amazonaws.com/
functions:
  hello: aws-python-http-api-dev-hello (2.3 kB)
```

_Nota_: Na forma atual, após o deploy, sua API é pública e pode ser invocada por qualquer pessoa. Para deploys em produção, você pode querer configurar um autorizador. Para detalhes sobre como fazer isso, consulte a [documentação de eventos http](https://www.serverless.com/framework/docs/providers/aws/events/apigateway/).

### Invocation

Após o deploy bem-sucedido, você pode chamar a aplicação criada via HTTP:

```
curl https://xxxxxxx.execute-api.us-east-1.amazonaws.com/
```

Que deve resultar em uma resposta similar à seguinte:

```json
{
  "message": "Go Serverless v4.0! Your function executed successfully!"
}
```

### Local development

Você pode invocar sua função localmente usando o seguinte comando:

```
serverless invoke local --function hello
```

Que deve resultar em uma resposta similar à seguinte:

```json
{
  "statusCode": 200,
  "body": "{\n  \"message\": \"Go Serverless v4.0! Your function executed successfully!\"}"
}
```

Alternativamente, também é possível emular o API Gateway e Lambda localmente usando o plugin `serverless-offline`. Para fazer isso, execute o seguinte comando:

```
serverless plugin install -n serverless-offline
```

Isso irá adicionar o plugin `serverless-offline` às `devDependencies` no arquivo `package.json` e também adicioná-lo aos `plugins` no `serverless.yml`.

Após a instalação, você pode iniciar a emulação local com:

```
serverless offline
```

Para saber mais sobre as capacidades do `serverless-offline`, consulte seu [repositório GitHub](https://github.com/dherault/serverless-offline).

### Bundling dependencies

Caso você queira incluir dependências de terceiros, você precisará usar um plugin chamado `serverless-python-requirements`. Você pode configurá-lo executando o seguinte comando:

```
serverless plugin install -n serverless-python-requirements
```

Executar o comando acima irá automaticamente adicionar `serverless-python-requirements` à seção `plugins` no seu arquivo `serverless.yml` e adicioná-lo como uma `devDependency` no arquivo `package.json`. O arquivo `package.json` será automaticamente criado se não existir. Agora você poderá adicionar suas dependências ao arquivo `requirements.txt` (`Pipfile` e `pyproject.toml` também são suportados, mas requerem configuração adicional) e elas serão automaticamente injetadas no pacote Lambda durante o processo de build. Para mais detalhes sobre a configuração do plugin, consulte a [documentação oficial](https://github.com/UnitedIncome/serverless-python-requirements).

## GitHub Actions - Deploy Automático

Este projeto está configurado para fazer deploy automático usando GitHub Actions sempre que houver push para a branch principal.

### Pré-requisitos

1. **Conta AWS** com permissões para:
   - Lambda
   - API Gateway
   - CloudFormation
   - IAM (para criar roles)

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
4. Acesse o endpoint da API gerado
