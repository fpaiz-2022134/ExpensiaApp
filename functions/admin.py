from data.program_data import facturas_pendientes, usuarios
from data.data_handler import guardar_usuarios, guardar_facturas
import pandas as pd
import datetime as date

def ver_facturas_pendientes():
    print("\n --- Facturas Pendientes ---")
    for i, factura in enumerate(facturas_pendientes):
        print(f"{i + 1}. Usuario: {factura['usuario']}, Categoría: {factura['categoria']}, Monto: Q{factura['monto']}, Aprobada: {factura['aprobada']}")
        
        
def aprobar_facturas():
    ver_facturas_pendientes()
    idx = int(input("¿Qué factura deseas procesar? Ingresa el número: ")) -1
    
    if 0 <= idx < len(facturas_pendientes):
        factura = facturas_pendientes[idx]
        decision = input("¿Deseas aprobar esta factura? s/n: ").lower()
        
        factura['aprobada'] = True if decision == 's' else False
        
        if factura['aprobada']:
            usuarios[factura['usuario']]['saldo'] = factura['monto']
            print("La factura ha sido aprobada exitosamente.")
            print("Importante: Al usuario se le ha agregado el monto a su saldo.") 
        else:
            print("La factura ha sido denegada, no se le ha sumado saldo al usuario.")
        
        
        facturas_pendientes.pop(idx)           
    
    else:
        print("La factura escogida es inválida o no se encuentra registrada.")
        
        # Función para aprobar facturas
def aprobar_facturas():
    ver_facturas_pendientes()
    idx = int(input("¿Qué factura deseas procesar? Ingresa el número: ")) - 1
    
    if 0 <= idx < len(facturas_pendientes):
        factura = facturas_pendientes[idx]
        decision = input("¿Deseas aprobar esta factura? s/n: ").lower()
        
        factura['aprobada'] = True if decision == 's' else False
        
        if factura['aprobada']:
            # Agregar la fecha de aprobación
            factura['fecha_aprobacion'] = date.today().isoformat()
            # Actualizar el saldo del usuario
            usuarios[factura['usuario']]['saldo'] += factura['monto']
            print(f"La factura ha sido aprobada exitosamente. Fecha de aprobación: {factura['fecha_aprobacion']}")
            print("Importante: Al usuario se le ha agregado el monto a su saldo.") 
        else:
            print("La factura ha sido denegada, no se le ha sumado saldo al usuario.")
        guardar_usuarios()
        guardar_facturas()
        # Eliminar la factura aprobada de la lista de pendientes
        facturas_pendientes.pop(idx)           
    
    else:
        print("La factura escogida es inválida o no se encuentra registrada.")


# ------------------------------
#    FUNCION PARA BUSCAR FACTURAS (ADMIN)
# ------------------------------
def buscar_facturas(criterio, valor):
    try:
        df = pd.read_csv('bills.csv')
        if criterio not in df.columns:
            print(f"Criterio '{criterio}' no encontrado en las columnas.")
            return []

        coincidencias = df[df[criterio].astype(str).str.lower() == str(valor).lower()]
        return coincidencias.to_dict('records')

    except FileNotFoundError:
        print("El archivo 'bills.csv' no existe.")
        return []

    except Exception as e:
        print(f"Error al buscar facturas: {e}")
        return []

# ------------------------------
#    FUNCION DE BÚSQUEDA INTERACTIVA (ADMIN)
# ------------------------------
def buscar_facturas_interactivo_admin():
    while True:
        print("\n        Buscar Factura       ")
        print("1. Buscar por número de factura")
        print("2. Buscar por usuario")
        print("3. Buscar por estado")
        print("4. Volver al menú principal")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == '1':
            criterio = 'numero_factura'
            valor = input("Ingrese el número de factura: ").strip()
        elif opcion == '2':
            criterio = 'usuario'
            valor = input("Ingrese el nombre de usuario: ").strip()
        elif opcion == '3':
            criterio = 'estado'
            valor = input("Ingrese el estado (aprobado, rechazado, pendiente): ").strip().lower()
            if valor not in ['aprobado', 'rechazado', 'pendiente']:
                print("Estado no válido. Sólo puede ser 'aprobado', 'rechazado' o 'pendiente'.")
                continue
        elif opcion == '4':
            break
        else:
            print("Opción no válida. Intente nuevamente.")
            continue

        resultados = buscar_facturas(criterio, valor)
        if resultados:
            print(f"\nSe encontraron {len(resultados)} factura(s):")
            for factura in resultados:
                print(factura)
        else:
            print("No se encontraron facturas con ese criterio.")
