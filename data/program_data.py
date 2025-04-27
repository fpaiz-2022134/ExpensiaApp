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
        return entrada
    else:
        print("Entrada inválida: solo se permiten números.")
        return None