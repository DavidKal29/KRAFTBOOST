class Product():

    def __init__(self,id,nombre,precio,marca,categoria,descripcion,imagen,stock=None,ventas=None,activo=None,fecha_registro=None):
        self.id=id
        self.nombre=nombre
        self.precio=precio
        self.nombre_marca=marca
        self.nombre_categoria=categoria
        self.descripcion=descripcion
        self.imagen=imagen
        self.stock=stock
        self.ventas=ventas
        self.activo=activo
        self.fecha_registro=fecha_registro