from flask_mail import Message


class MailSender:

    #Método para enviar mensajes de bienvenida
    @classmethod
    def welcome_message(cls,current_app,username,email):

        #El asunto
        asunto='Bienvenido a KraftBoost'

        #Mensaje de bienvenida
        html='''
            <h1>¡👋Saludos {}!</h1>
            <p>🛍️Gracias por haber elegido nuestra tienda para comprar tu material</p>
            <p>💪¡No dudes en que te ayudaremos a lograr tus objetivos!🚀</p>
        '''.format(username)

        #Estructura básica para enviar el mensaje, usando el current 
        # app que traeré de las rutas, porque no puedo usarlo fuera de las rutas
        Mensaje=Message(
            subject=asunto,
            sender=current_app.config['MAIL_USERNAME'],
            recipients=[email]
        )

        #Añadimos el html al mensaje
        Mensaje.html=html

        #El correo se envia
        current_app.config['mail'].send(Mensaje)

    #Metodo para resetear la contraseña
    @classmethod
    def reset_password_message(cls,current_app,email,ip,token):

        #El asunto
        asunto='Recuperación Contraseña'

        #Mensaje de recuperación
        html='''
            <p>🔧 Para recuperar tu contraseña, accede al siguiente enlace👇</p>
            <a href="{}auth/reset_password/{}">🔁 Reestablecer Contraseña</a>
        '''.format(ip,token)

        #Estructura básica para enviar el mensaje, usando el current 
        # app que traeré de las rutas, porque no puedo usarlo fuera de las rutas
        Mensaje=Message(subject=asunto,
              sender=current_app.config['MAIL_USERNAME'],
              recipients=[email])

        #Añadimos el html al mensaje
        Mensaje.html=html

        #El correo se envia
        current_app.config['mail'].send(Mensaje)


    #Metodo para confirmar que la contraseña ha sido cambiada
    @classmethod
    def password_changed(cls,current_app,email):

        #El asunto
        asunto='🔒Contraseña Actualizada con Éxito✅'

        #Mensaje de éxito
        html='''
            <h1>¡👋 Saludos!</h1>
            <p>🔐Tu contraseña ha sido cambiada con éxito🎉</p>
            <p>🙏Gracias una vez más por confiar en nosotros💙</p>
        '''

        #Estructura básica para enviar el mensaje, usando el current 
        # app que traeré de las rutas, porque no puedo usarlo fuera de las rutas
        Mensaje=Message(
            subject=asunto,
            sender=current_app.config['MAIL_USERNAME'],
            recipients=[email]
        )

        #Añadimos el html al mensaje
        Mensaje.html=html

        #El correo se envia
        current_app.config['mail'].send(Mensaje)

    
    # Método para confirmar el pedido
    @classmethod
    def confirmOrder(cls, current_app, email, username, pedido, productos, ip):
        print('Hemos entrado con exito aqui en el confirm order ajjajajaja')

        #Asunto del correo
        asunto='🛒 Tu pedido N-{} está en camino, {}!'.format(pedido.numero_pedido, username)

        #Dirección completa
        direccion_envio='{}, {}, {}'.format(pedido.domicilio, pedido.localidad, pedido.codigo_postal)

        #Construimos los productos en una tabla
        productos_html=''
        for producto in productos:
            total_producto = producto.precio
            
            productos_html+='''
                <tr style="border-bottom:1px solid #ddd;">
                    <td style="padding: 8px 12px;">{}</td>
                    <td style="padding: 8px 12px; text-align: center;">{}</td>
                    <td style="padding: 8px 12px; text-align: right;">{:.2f} €</td>
                </tr>
            '''.format(producto.nombre, producto.cantidad, total_producto)

        #HTML del correo
        html='''
            <div style="color: #333;">
                <h2>¡Gracias por tu pedido, {}! 🥳</h2>
                <p>Estamos preparando tu pedido con mucho cariño. Aquí tienes todos los detalles:</p>

                <p><strong>Número de Pedido:</strong> N-{}</p>
                <p><strong>Envío a:</strong> {}</p>

                <h3 style="margin-top: 30px;">🧾 Detalles de tu compra:</h3>
                <table style="width: 100%; border-collapse: collapse; background-color: #f9f9f9;">
                    <thead>
                        <tr style="background-color: #eee;">
                            <th style="padding: 10px; text-align: left;">Producto</th>
                            <th style="padding: 10px;">Cantidad</th>
                            <th style="padding: 10px; text-align: right;">Total</th>
                        </tr>
                    </thead>
                    <tbody>
                        {}
                    </tbody>
                </table>

                <p style="margin-top: 20px;"><strong>Total del Pedido:</strong> {} €</p>

                <h3 style="margin-top: 30px;">📦 Seguimiento de tu pedido:</h3>
                <p>Puedes revisar el estado de tu pedido en cualquier momento aquí:</p>
                <p><a href="{}profile/order/{}">Ver seguimiento del pedido</a></p>

                <p style="margin-top: 30px;">Gracias por confiar en <strong>KraftBoost</strong>❤️</p>
                <p>💪¡Estamos contigo en cada paso hacia tus objetivos!🚀</p>
            </div>
        '''.format(username,pedido.numero_pedido,direccion_envio,productos_html,pedido.precio_total,ip,pedido.numero_pedido)

        #Estructura básica para enviar el mensaje, usando el current 
        # app que traeré de las rutas, porque no puedo usarlo fuera de las rutas
        Mensaje=Message(
            subject=asunto,
            sender=current_app.config['MAIL_USERNAME'],
            recipients=[email]
        )

        Mensaje.html=html

        #Enviamos el correo
        current_app.config['mail'].send(Mensaje)


        print('Confirmacion enviada con exito')
