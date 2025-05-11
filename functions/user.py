from datetime import date
from data.program_data import usuarios, facturas_pendientes, validar_numero
from data.data_handler import guardar_usuarios, guardar_facturas
import pandas as pd

# Menú principal para el usuario
def menu_usuario():
    print("         EXPENSIA         ")

# Muestra el dashboard del usuario
def mostrar_dashboard(usuario):
    print("------ FACTURAS ENVIADAS ----\n")
    for factura in usuarios[usuario]['facturas']:
        print(f"Categoría: {factura['categoria']}, Monto: {factura['monto']}, Aprobada: {factura['aprobada']}")

# Permite al usuario enviar una factura
def enviar_factura(usuario):
    print("---- ENVIAR FACTURA")
    print("A continuación, deberás ingresar distintos datos para un envío correcto...\n")

    while True:
        numero_factura = input("Número de factura: ")
        if validar_numero(numero_factura):
            numero_factura = int(numero_factura)
            break
        else:
            print("El número de factura debe ser un número entero. Intenta de nuevo.")

    proveedor = input("Nombre del proveedor: ")
    fecha_emision = date.today().isoformat()

    while True:
        monto = input("Monto: ")
        if validar_numero(monto):
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

    usuarios[usuario]['facturas'].append(factura)
    facturas_pendientes.append(factura)

    print("La factura fue enviada al administrador exitosamente.")
    guardar_usuarios()
    guardar_facturas()

# Muestra el saldo disponible del usuario
def ver_saldo(usuario):
    saldo = usuarios[usuario]['saldo']
    print(f"\nSaldo disponible: Q{saldo:.2f}")

# Permite al usuario gestionar su perfil
def gestionar_perfil(usuario):
    print("\n--- Perfil de Usuario ---")
    perfil = usuarios[usuario]['perfil']

    continuar = input("\n¿Deseas editar los campos de tu perfil? (s/n): ")
    if continuar.lower() == "s":
        nombre = input("Nombre completo: ")
        correo = input("Correo electrónico: ")
        perfil['nombre'] = nombre
        perfil['correo'] = correo
        print("El perfil ha sido actualizado exitosamente.")
        guardar_usuarios()
# ------------------------------
#    CALCULAR PROMEDIO DE SALDO (PENDIENTE)
# ------------------------------

# Función para calcular el promedio de saldo de todos los usuarios
""" def calcular_promedio_saldo():
    total_saldo = 0
    num_usuarios = len(usuarios)

    if num_usuarios == 0:
        print("No hay usuarios registrados.")
        return

    for usuario in usuarios.values():
        total_saldo += usuario['saldo']

    promedio = total_saldo / num_usuarios
    print(f"\nEl promedio de saldo de todos los usuarios es: Q{promedio:.2f}")

    # Calcular el promedio de saldo de todos los usuarios
    calcular_promedio_saldo() """

# ------------------------------
#    FUNCION PARA BUSCAR FACTURAS
# ------------------------------
def buscar_facturas(criterio, valor, usuario_actual):
    try:
        df = pd.read_csv('bills.csv')

        if criterio not in df.columns:
            print(f"Criterio '{criterio}' no encontrado en las columnas.")
            return []

        # Filtramos solo las facturas del usuario actual
        df_filtrado = df[df['usuario'].astype(str).str.lower() == usuario_actual.lower()]

        # Filtrar por el criterio elegido
        coincidencias = df_filtrado[df_filtrado[criterio].astype(str).str.lower() == str(valor).lower()]

        return coincidencias.to_dict('records')

    except FileNotFoundError:
        print("El archivo 'bills.csv' no existe.")
        return []

    except Exception as e:
        print(f"Error al buscar facturas: {e}")
        return []

def buscar_facturas_interactivo(usuario_actual):
    while True:
        print("\n------ Buscar Factura ------")
        print("Seleccione un criterio de búsqueda:")
        print("1. Número de factura")
        print("2. Estado (aprobado, rechazado, pendiente)")
        print("3. Volver al menú principal")
        
        opcion = input("Opción: ").strip()

        if opcion == '1':
            criterio = 'numero_factura'
            valor = input("Ingrese el número de factura: ").strip()
        
        elif opcion == '2':
            criterio = 'estado'
            valor = input("Ingrese el estado (aprobado, rechazado, pendiente): ").strip().lower()
            if valor not in ['aprobado', 'rechazado', 'pendiente']:
                print("Estado no válido. Intente con 'aprobado', 'rechazado' o 'pendiente'.")
                continue

        elif opcion == '3':
            print("Regresando al menú principal...")
            break

        else:
            print("Opción no válida. Intente de nuevo.")
            continue

        # Buscar y mostrar resultados
        resultados = buscar_facturas(criterio, valor, usuario_actual)
        if resultados:
            print(f"\nSe encontraron {len(resultados)} factura(s):\n")
            for idx, factura in enumerate(resultados, 1):
                print(f"Factura {idx}:")
                for key, val in factura.items():
                    print(f"  {key}: {val}")
                print("-" * 30)
        else:
            print("No se encontraron facturas con ese criterio.")
