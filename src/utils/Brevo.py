import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from dotenv import load_dotenv
import os

# Cargar variables del entorno (.env)
load_dotenv()

# Configurar el cliente Brevo
configuration=sib_api_v3_sdk.Configuration()
configuration.api_key['api-key']=os.getenv('BREVO_API_KEY')

# Instancia global del cliente
api_instance=sib_api_v3_sdk.TransactionalEmailsApi(
    sib_api_v3_sdk.ApiClient(configuration)
)
