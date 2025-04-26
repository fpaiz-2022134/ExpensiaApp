from modules import login as log

#Elegir la opcion
while True:
    opcion = log.menu_login()
    if opcion == "1":
        log.iniciar_sesion()
        
    elif opcion == "2":
        log.registrar_usuario()
    else:
        log.print("Opción inválida. Intenta de nuevo.")

    continuar = input("\n¿Deseas realizar otra acción? (s/n): ")
    if continuar.lower() != "s":
        print("¡Vuelve pronto!")
        break
