from datetime import date

from ..data.program_data import usuarios, facturas_pendientes



def menu_usuario():
    print("         EXPENSIA         ")
    
    

def mostrar_dashboard(usuario):
    print("------ FACTURAS ENVIADAS ----")
    print()
    for factura in usuarios[usuario]['facturas']:
        print(f"Categoría: {factura['categoria']}, Monto: {factura['monto']}, Aprobada: {factura['aprobada']}")
        


def enviar_factura(usuario):
    print("---- ENVIAR FACTURA")
    print("A continuación, deberás ingresar distintos datos para un envío correcto...")
    print()

    while True:
        numero_factura = input("Número de factura: ")
        if program_data.es_entero(numero_factura):
            numero_factura = int(numero_factura)
            break
        else:
            print("El número de factura debe ser un número entero. Intenta de nuevo.")

    proveedor = input("Nombre del proveedor: ")
    fecha_emision = date.day

    while True:
        monto = input("Monto: ")
        if program_data.es_numero(monto):
            monto = float(monto)
            break
        else:
            print("El monto debe ser un número válido. Intenta de nuevo.")

    moneda_utilizada = input("Moneda utilizada (Q): ")
    categoria = input("Ingresa la categoría del gasto realizado (comida, transporte, etc): ")
    descripcion = input("Justifica tu respuesta anterior, describe el gasto realizado: ")

    print("")
    
    factura = {
        'usuario': usuario,
        'numero_factura': numero_factura,
        'proveedor': proveedor,
        'fecha_emision': fecha_emision,
        'monto': monto,
        'moneda_utilizada': moneda_utilizada,
        'categoria': categoria,
        'descripcion': descripcion,        
        'aprobada': None
    }
    
    usuarios[usuario].append(factura)
    facturas_pendientes.append(factura)
    
    print("La factura fue enviada al administrador exitosamente.")
    
    
def ver_saldo(usuario):
    saldo = usuarios[usuario]('saldo')
    print( f"\nSaldo disponible: Q{saldo:.2}")
    
    
def gestionar_perfil(usuario):
    print("\n ---    Perfil de Usuario -----" )
    perfil =usuarios[usuario]['perfil']
    
    continuar = input("\n¿Deseas editar los campos de tu perfil? (s/n): ")
    if continuar.lower() != "s":
        perfil = usuarios[usuario]['perfil'] 
        nombre = input("Nombre completo: ")
        correo = input("Correo electrónico : " )
        
        perfil['nombre'] = nombre
        perfil['correo'] = correo
        
        print("El perfil ha sido actualizado exitosamente.")
    

