
from authentication.login import iniciar_sesion, registrar_usuario
from functions.user import mostrar_dashboard, enviar_factura, ver_saldo, gestionar_perfil
from functions.admin import ver_facturas_pendientes, aprobar_facturas
from data.program_data import usuarios, validar_numero


def mostrar_menu():
    print("¡Bienvenido a la mejor aplicacion de viaticos de Guatemala!")
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
                    print("\n1. Ver dashboard\n2. Enviar factura\n3. Ver saldo\n4. Gestionar perfil\n5. Cerrar sesión")
                    
                    op = validar_numero(input("Opción: "))
                    
                    if op == 1:
                        mostrar_dashboard(usuario)
                    elif op == 2:
                        enviar_factura(usuario)
                    elif op == 3:
                        ver_saldo(usuario)
                    elif op == 4:
                        gestionar_perfil(usuario)
                    elif op == 5:
                        print("¡Gracias por usar el programa!")
                        break
                    else:
                        print("La opción escogida es incorrecta, vuelve a intentarlo.")
            else:
                while True:
                    print("\n 1. Ver las facturas pendientes \n 2.Procesar factura \n 3. Cerrar sesión")
                    op = int(validar_numero(input("Opción: ")))
                    
                    if op == 1:
                        ver_facturas_pendientes()
                    elif op== 2:
                        aprobar_facturas()
                    elif op == 3:
                        print("¡Gracias por usar el programa!")
                        break
                    else:
                        print("La opción escogida es incorrecta, vuelve a intentarlo.")
                        
    elif opcion == 2:
        registrar_usuario()
        
    elif opcion == 3:
        break
    else:
        print(print("La opción escogida es incorrecta, vuelve a intentarlo."))
