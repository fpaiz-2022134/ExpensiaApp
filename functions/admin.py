from data.program_data import facturas_pendientes, usuarios
from datetime import datetime, date

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
            factura['fecha_aprobacion'] = datetime.now().date()
            
            print("La factura ha sido aprobada exitosamente.")
            print("Importante: Al usuario se le ha agregado el monto a su saldo.") 
        else:
            print("La factura ha sido denegada, no se le ha sumado saldo al usuario.")
        
        
        facturas_pendientes.pop(idx)           
    
    else:
        print("La factura escogida es inválida o no se encuentra registrada.")

def tiempo_respuesta_promedio():
    tiempos = []
    for user_data in usuarios.values():
        if 'facturas' in user_data:
            for factura in user_data['facturas']:
                if factura.get('aprobada') and factura.get('fecha_envio') and factura.get('fecha_aprobacion'):
                    delta = factura['fecha_aprobacion'] - factura['fecha_envio']
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
