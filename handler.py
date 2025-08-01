import json
import boto3
import os
import logging

# Configurar logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Inicializar clientes AWS
sns_client = boto3.client('sns')

def hello(event, context):
    body = {
        "message": "Go Serverless v4.0! Your function executed successfully!",
    }

    response = {"statusCode": 200, "body": json.dumps(body)}

    return response

def api_handler(event, context):
    """
    Handler para requisições do API Gateway
    Recebe a requisição e publica no tópico SNS
    """
    try:
        logger.info(f"Evento recebido: {json.dumps(event)}")
        
        # Obter o corpo da requisição
        body = event.get('body', '{}')
        if isinstance(body, str):
            body = json.loads(body)
        
        # Obter o nome do tópico SNS do ambiente
        topic_arn = os.environ.get('SNSTopicArn')
        if not topic_arn:
            raise Exception("SNSTopicArn não configurado")
        
        # Publicar mensagem no SNS
        message = {
            'source': 'api_gateway',
            'timestamp': context.get_remaining_time_in_millis(),
            'data': body
        }
        
        response = sns_client.publish(
            TopicArn=topic_arn,
            Message=json.dumps(message),
            Subject='Mensagem do API Gateway'
        )
        
        logger.info(f"Mensagem publicada no SNS: {response['MessageId']}")
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'message': 'Mensagem enviada com sucesso para o SNS',
                'messageId': response['MessageId'],
                'data': body
            })
        }
        
    except Exception as e:
        logger.error(f"Erro no api_handler: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': 'Erro interno do servidor',
                'message': str(e)
            })
        }

def sqs_handler(event, context):
    """
    Handler para mensagens da fila SQS
    Processa mensagens que vieram do SNS
    """
    try:
        logger.info(f"Processando {len(event['Records'])} mensagens da SQS")
        
        for record in event['Records']:
            # Obter o corpo da mensagem SQS
            body = json.loads(record['body'])
            
            # Se a mensagem veio do SNS, o corpo contém a mensagem SNS
            if 'Message' in body:
                sns_message = json.loads(body['Message'])
                logger.info(f"Processando mensagem SNS: {sns_message}")
                
                # Aqui você pode adicionar sua lógica de processamento
                # Por exemplo, salvar no banco de dados, enviar email, etc.
                
                logger.info(f"Mensagem processada com sucesso: {sns_message.get('data', {})}")
            else:
                logger.info(f"Processando mensagem direta da SQS: {body}")
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': f'Processadas {len(event["Records"])} mensagens com sucesso'
            })
        }
        
    except Exception as e:
        logger.error(f"Erro no sqs_handler: {str(e)}")
        raise e  # Re-raise para que a mensagem volte para a fila
