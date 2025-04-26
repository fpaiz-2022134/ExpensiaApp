from data.program_data import facturas_pendientes, usuarios

def ver_facturas_pendientes():
    print("\n --- Facturas Pendientes ---")
    for i, factura in enumerate(facturas_pendientes):
        print(f"{i + 1}. Usuario: {factura['usuario']}, Categoría: {factura['categoria']}, Monto: Q{factura['monto']}, Aprobada: {factura['aprobada']}")
        
        
def aprobar_facturas():
    ver_facturas_pendientes()
    idx = int(input("¿Qué factura deseas procesar? Ingresa el número: ")) -1
    
    if 0 <= idx < len(facturas_pendientes):
        factura = facturas_pendientes[idx]
        decision = input("¿Deseas aprobar esta factura? s/n").lower()
        
        factura['aprobada'] = True if decision == 's' else False
        
        if factura['aprobada']:
            usuarios[factura['usuario']]['saldo'] = factura['monto']
            
        print("La factura ha sido aprobada exitosamente.")
        print("Importante: Al usuario se le ha agregado el monto a su saldo.") 
        
        facturas_pendientes.pop(idx)           
    
    else:
        print("La factura escogida es inválida o no se encuentra registrada.")
        
        
