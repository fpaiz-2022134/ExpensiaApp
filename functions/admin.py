from data.program_data import facturas_pendientes, usuarios
from data.data_handler import guardar_usuarios, guardar_facturas
import pandas as pd
from datetime import date, datetime
import numpy as np
import matplotlib as plt

from graphics.visualizaciones import (
    graficar_tasa_aprobacion,
    graficar_distribucion_gastos,
    graficar_tiempo_respuesta,
    graficar_top_usuarios
)
def ver_facturas_pendientes():
    print("\n --- Facturas Pendientes ---")
    for i, factura in enumerate(facturas_pendientes):
        if factura.get('aprobada') is not True or False:
            print(f"{i + 1}. Número factura: {factura['numero_factura']} Usuario: {factura['usuario']}, Categoría: {factura['categoria']}, Monto: Q{factura['monto']}, Aprobada: {factura['aprobada']}")
        
        # Función para aprobar facturas
def aprobar_facturas():
    ver_facturas_pendientes()
    idx = int(input("¿Qué factura deseas procesar? Ingresa el número: ")) - 1
    
    if 0 <= idx < len(facturas_pendientes):
        factura = facturas_pendientes[idx]
        decision = input("¿Deseas aprobar esta factura? s/n: ").lower()
        
        factura['aprobada'] = True if decision == 's' else False
        
        if factura['aprobada']:
            factura['fecha_aprobacion'] = date.today().isoformat()
        
        for f in usuarios[factura['usuario']]['facturas']:
            if f['numero_factura'] == factura['numero_factura']:
                f['aprobada'] = factura['aprobada']
                if factura['aprobada']:
                    f['fecha_aprobacion'] = factura['fecha_aprobacion']
                break

        if factura['aprobada']:
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
       # print("3. Buscar por estado")
        print("3. Volver al menú principal")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == '1':
            criterio = 'numero_factura'
            valor = input("Ingrese el número de factura: ").strip()
        elif opcion == '2':
            criterio = 'usuario'
            valor = input("Ingrese el nombre de usuario: ").strip()
        #elif opcion == '3':
         #   criterio = 'estado'
          #  valor = input("Ingrese el estado (aprobado, rechazado, pendiente): ").strip().lower()
           # if valor not in ['aprobado', 'rechazado', 'pendiente']:
            #    print("Estado no válido. Sólo puede ser 'aprobado', 'rechazado' o 'pendiente'.")
             #   continue
        elif opcion == '3':
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
            
            
def tiempo_respuesta_promedio():
    tiempos = []
    for user_data in usuarios.values():
        if 'facturas' in user_data:
            for factura in user_data['facturas']:
                if factura.get('aprobada') and factura.get('fecha_emision') and factura.get('fecha_aprobacion'):
                    fecha_emision = datetime.strptime(factura['fecha_emision'], "%Y-%m-%d")
                    fecha_aprob = datetime.strptime(factura['fecha_aprobacion'], "%Y-%m-%d")
                    delta = (fecha_aprob - fecha_emision)
                    tiempos.append(delta.days)
    
    return sum(tiempos)/len(tiempos) if tiempos else 0

def top_usuarios_por_facturas():
    """El top 5 usuarios con más facturas enviadas"""
    usuarios_conteo = []
    
    for username, data in usuarios.items():
        num_facturas = 0
        if 'facturas' in data:
            num_facturas = len(data['facturas'])
        usuarios_conteo.append((username, num_facturas))
    def obtener_conteo(item):
        return item[1]
    usuarios_conteo.sort(key=obtener_conteo, reverse=True)
    return usuarios_conteo[:5]

def top_usuarios_por_saldo():
    """El top 5 usuarios con mayor saldo utilizado"""
    usuarios_saldo = []
    for username, data in usuarios.items():
        saldo_total = 0
        if 'facturas' in data:
            for factura in data['facturas']:
                saldo_total += factura['monto']
        usuarios_saldo.append((username, saldo_total))
    def obtener_saldo(item):
        return item[1]
    usuarios_saldo.sort(key=obtener_saldo, reverse=True)
    return usuarios_saldo[:5]



def mostrar_top_usuarios():
    print("\n=== TOP 5 USUARIOS ===")

    print("\n Top Usuarios con más facturas enviadas:")
    top_facturas = top_usuarios_por_facturas()
    
    for posicion, (usuario, cantidad) in enumerate(top_facturas, 1):
        print(f"{posicion}. {usuario}: {cantidad} facturas")
    print("\n Usuarios con mayor saldo utilizado:")
    top_saldo = top_usuarios_por_saldo()
    
    for posicion, (usuario, saldo) in enumerate(top_saldo, 1):
        print(f"{posicion}. {usuario}: Q{saldo:.2f}")
        
        
def menu_visualizaciones():
    while True:
        print("\n--- Visualizaciones ---")
        print("1. Tasa de aprobación por usuario")
        print("2. Distribución de gastos por categoría")
        print("3. Tiempo de respuesta promedio")
        print("4. Top 5 usuarios")
        print("5. Volver al menú principal")
        
        opcion = input("Seleccione una opción: ").strip()
        
        if opcion == '1':
            graficar_tasa_aprobacion()
        elif opcion == '2':
            graficar_distribucion_gastos()
        elif opcion == '3':
            graficar_tiempo_respuesta()
        elif opcion == '4':
            graficar_top_usuarios()
        elif opcion == '5':
            break
        else:
            print("Opción no válida. Intente nuevamente.")