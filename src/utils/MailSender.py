from flask_mail import Message


class MailSender:

    #Método para enviar mensajes de bienvenida
    @classmethod
    def welcome_message(cls,current_app,username,email):

        #El asunto
        asunto='Bienvenido a KraftBoost'

        #Mensaje de bienvenida
        html='''
            <h1>¡Saludos {}!</h1>
            <p>Gracias por haber elegido nuestra tienda para comprar tu material</p>
            <p>¡No dudes en que, te ayudaremos a lograr tus objetivos!</p>
        '''.format(username)

        #Estructura básica para enviar el mensaje, usando el current 
        # app que traeré de las rutas, porque no puedo usarlo fuera de las rutas
        Mensaje=Message(subject=asunto,
              sender=current_app.config['MAIL_USERNAME'],
              recipients=[email])

        #Añadimos el html al mensaje
        Mensaje.html=html

        #El correo se envia
        current_app.config['mail'].send(Mensaje)