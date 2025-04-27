usuarios = {}
facturas_pendientes = []

#funcion para validar que lo ingresado sea texto y no alfanúmerico
def validar_texto(texto):
    if texto.isalpha():
        print("El texto es válido.")
        return True
    else:
        print("El texto no es válido. Solo se permiten letras.")
        return False
#funcion para validar que lo ingresado sea númerico
def validar_numerico(texto):
    if texto.isdigit():
        print("El texto es numérico.")
        return True
    else:
        print("El texto no es numérico. Solo se permiten dígitos.")
        return False
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
        return entrada
    else:
        print("Entrada inválida: solo se permiten números.")
        return None