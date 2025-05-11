from data import program_data
from data.data_handler import guardar_usuarios  

def menu_login():
    print("¡Bienvenido a la mejor aplicacion de viaticos de Guatemala!")
    print("1. Iniciar sesión")
    print("2. Registrarse")
    opcion = input("Eliga una de las siguientes opciónes (1 o 2): ")
    return opcion

#Registrar usuario
def registrar_usuario():
    print("\n--- Registro ---")
    usuario = input("Elija su nombre de usuario: ")
    if usuario in program_data.usuarios:
        print("Este usuario ya existe. Intente con otro.")
    else:
        contraseña = input("Elija una contraseña: ")
        rol = input("¿Es 'admin' o 'usuario'? ").strip().lower()

        if rol not in ['admin', 'usuario']:
            print("El rol ingresado no es válido, no registrado.")
            return None
        
        # Si quiere registrarse como usuario tendra que poner la clave especifica
        if rol == 'admin':
            clave_admin = input("Ingrese la clave especial de administrador: ")
            clave_correcta = "clave123"  

            if clave_admin != clave_correcta:
                print("Clave incorrecta. Será registrado como 'usuario'.")
                rol = 'usuario'

        program_data.usuarios[usuario] = {
            'contraseña': contraseña,
            'rol': rol,
            'perfil': {},
            'facturas': [],
            'saldo': 00
        }
        guardar_usuarios()
        print("¡Registro exitoso!")


#Bloqueo de usuario si se intentan mas de 5 veces
intentos_fallidos = 0
max_intentos = 5

def iniciar_sesion():
    global intentos_fallidos
    print("\n--- Inicio de sesión ---")
    
    """ if intentos_fallidos >= max_intentos:
        print("Demasiados intentos fallidos. Contacta a un administrador o IT.")
        return """

    usuario = input("Nombre de usuario: ")

    while True:
        contraseña = input("Contraseña: ")
        if usuario in program_data.usuarios and program_data.usuarios[usuario]['contraseña'] == contraseña:
            print("¡Inicio de sesión exitoso!")
            intentos_fallidos = 0
            return usuario
        else:
            print("Usuario o contraseña incorrectos.")
            intentos_fallidos += 1
            print(f"Intentos fallidos: {intentos_fallidos}/{max_intentos}")
            if intentos_fallidos >= max_intentos:
                print("\nHas excedido el número de intentos permitidos.")
                print("Debes contactar a un administrador o IT para desbloquear tu cuenta.")
                break