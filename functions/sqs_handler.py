import json
import logging

# Configurar logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


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
