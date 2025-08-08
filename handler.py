# handler.py - Arquivo principal para compatibilidade
# As funções estão agora organizadas em arquivos separados na pasta functions/

# Importar funções dos arquivos organizados
from functions.hello import hello
from functions.api_handler import api_handler
from functions.sqs_handler import sqs_handler

# Re-exportar para manter compatibilidade
__all__ = ['hello', 'api_handler', 'sqs_handler']
