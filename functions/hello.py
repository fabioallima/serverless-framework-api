import json


def hello(event, context):
    """
    Função hello original - retorna mensagem de boas-vindas
    """
    body = {
        "message": "Go Serverless v4.0! Your function executed successfully!",
    }

    response = {"statusCode": 200, "body": json.dumps(body)}

    return response
