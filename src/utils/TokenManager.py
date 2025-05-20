import jwt
from datetime import datetime,timedelta,timezone

class TokenManager:

    #Metodo estatico para crear el token
    @staticmethod
    def create_token(email,tiempo,secret_key,step):
        
        #Recibe el email al que se enviará el token, 
        # el tiempo de expiracion en minutos y el secret_key 
        # del jwt y el step que será para que pagina es
        token=jwt.encode(
            payload={
                'email':email,'step': step,'exp':datetime.now(timezone.utc)+timedelta(minutes=tiempo)
            },
            key=secret_key,algorithm='HS256'
        )

        return token
    

    @staticmethod
    def validate_token(token,secret_key):
        try:
            #Decodea el token para ver si es valido y lo retorna
            token_decode=jwt.decode(token,key=secret_key,algorithms=['HS256'])

            return token_decode


        #Si el token no es válido, o ha expirado, devolvemos None
        except jwt.exceptions.DecodeError:
            return None
        except jwt.exceptions.ExpiredSignatureError:
            return None

