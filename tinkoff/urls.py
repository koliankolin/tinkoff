from tinkoff.constants import PRODUCTION

SANDBOX_API_URL = 'https://api-invest.tinkoff.ru/openapi/sandbox'
PRODUCTION_API_URL = 'https://api-invest.tinkoff.ru/openapi/'
API_URL = PRODUCTION_API_URL if PRODUCTION else SANDBOX_API_URL

