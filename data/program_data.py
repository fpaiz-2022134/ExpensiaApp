usuarios = {}
facturas_pendientes = []

#funcion para validar que lo ingresado sea texto y no alfanúmerico
#funcion para validar que lo ingresado sea númerico

#si el valor es texto, devolver texto
#si es númerico, devolver númerico


def validar_texto(entrada):
    if entrada.isalpha():
        return entrada
    else:
        print("Entrada inválida: solo se permiten letras.")
        return None
    
def validar_numero(entrada):
    if entrada.isdigit():
        return int(entrada)
    else:
        print("Entrada inválida: solo se permiten números.")
        return None

# Función para calcular el promedio de saldo de todos los usuarios
def calcular_promedio_saldo():
    total_saldo = 0
    num_usuarios = len(usuarios)

    if num_usuarios == 0:
        print("No hay usuarios registrados.")
        return

    for usuario in usuarios.values():
        total_saldo += usuario['saldo']

    promedio = total_saldo / num_usuarios
    print(f"\nEl promedio de saldo de todos los usuarios es: Q{promedio:.2f}")
