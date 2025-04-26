from datetime import date
from authentication.login import usuarios 


def menu_usuario():
    print("         EXPENSIA         ")
    
    
def enviar_factura(usuario):
    print(" ---- ENVIAR FACTURA")
    print("A countinuación, deberás ingresar distintos datos para un envío correcto..")
    numero_factura = input("Número de factura: ")
    proveedor = input("Nombre del proveedor: ")
    fecha_emision = date.now
    monto = input("Monto: ")
    moneda_utilizada = ("Moneda utilizada (Q): ")
    categoria = input('Ingresa la categoría del gasto realizado (comida, transporte, etc) : ')
    descripcion = input("Justifica tu respuesta anterior")
    print("")
    
    factura = {
        'usuario': usuario,
        'categoria': categoria,
        'monto': monto,
        'aprobada': None
    }