from authentication.login import iniciar_sesion, registrar_usuario
from functions.user import (
    mostrar_dashboard,
    enviar_factura,
    ver_saldo,
    gestionar_perfil,
    buscar_facturas_interactivo as buscar_facturas_usuario
)
from functions.admin import (
    ver_facturas_pendientes,
    aprobar_facturas,
    buscar_facturas_interactivo_admin,
    tiempo_respuesta_promedio,
    mostrar_top_usuarios,
    menu_visualizaciones
)
from data.program_data import usuarios, validar_numero
from data.data_handler import cargar_datos

cargar_datos()

def mostrar_menu():
    print("             EXPENSIA        ")
    print("¡Bienvenido a la mejor aplicación de viáticos de Guatemala!")
    print("1. Iniciar sesión")
    print("2. Registrarse")
    print("3. Salir del programa") 
    
    return validar_numero(input("Elige una opción: "))

while True:
    opcion = mostrar_menu()
    
    if opcion == 1:
        usuario = iniciar_sesion()

        if usuario:            
            if usuarios[usuario]['rol'] == 'usuario':
                while True:
                    print("\n1. Ver dashboard")
                    print("2. Enviar factura")
                    print("3. Ver saldo")
                    print("4. Gestionar perfil")
                    print("5. Buscar factura")
                    print("6. Cerrar sesión")
                    
                    op = validar_numero(input("Elige una opción: "))
                    
                    if op == 1:
                        mostrar_dashboard(usuario)
                    elif op == 2:
                        enviar_factura(usuario)
                    elif op == 3:
                        ver_saldo(usuario)
                    elif op == 4:
                        gestionar_perfil(usuario)
                    elif op == 5:
                        buscar_facturas_usuario(usuario)
                    elif op == 6:
                        print("¡Gracias por usar el programa!")
                        break
                    else:
                        print("La opción escogida es incorrecta, vuelve a intentarlo.")
            else:  # Admin
                while True:
                    print("\n1. Ver las facturas pendientes")
                    print("2. Procesar factura")
                    print("3. Buscar factura")
                    print("4. Estadísticas de tiempo de aprobación ")
                    print("5. Mostrar top usuarios")
                    print("6. Gráficas de las estadísticas importantes")
                    print("7. Cerrar sesión")

                    op = validar_numero(input("Elige una opción: "))
                    
                    if op == 1:
                        ver_facturas_pendientes()
                    elif op == 2:
                        aprobar_facturas()
                    elif op == 3:
                        buscar_facturas_interactivo_admin()
                    elif op == 4:
                        print("El tiempo de aprobación promedio es: ", tiempo_respuesta_promedio(), "dias")
                    elif op == 5:
                        mostrar_top_usuarios()
                    elif op == 6:
                        menu_visualizaciones()
                    elif op == 7:
                        print("Gracias por usar el programa crack.")
                        break
                    else:
                        print("La opción escogida es incorrecta, vuelve a intentarlo.")
                        
    elif opcion == 2:
        registrar_usuario()
        
    elif opcion == 3:
        break
    else:
        print("La opción escogida es incorrecta, vuelve a intentarlo.")
