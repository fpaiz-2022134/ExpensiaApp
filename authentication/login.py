from ..data import program_data

def menu_login():
    print("¡Bienvenido a la mejor aplicacion de viaticos de Guatemala!")
    print("1. Iniciar sesión")
    print("2. Registrarse")
    opcion = input("Eliga una de las siguientes opciónes (1 o 2): ")
    return opcion
#Registrar usuario
def registrar_usuario():
    print("\n--- Registro ---")
    usuario = input("Eliga su nombre de usuario: ")
    if usuario in program_data.usuarios:
        print("Este usuario ya existe. Intente con otro.")
    else:
        contraseña = input("Eliga una contraseña: ")
        rol = input("¿Es 'admin' o 'usuario'? ").strip().lower()
        
        if rol not in ['admin', 'usuario']:
            print("El rol ingresado no es válido, no registrado.")
            return None
        program_data.usuarios[usuario] = {
            'contraseña': contraseña,
            'rol': rol,
            'perfil': {},
            'facturas': [],
            'saldo': 00
        }
        print("¡Registro exitoso!")
#Inicio de Sesion
def iniciar_sesion():
    print("\n--- Inicio de sesión ---")
    usuario = input("Nombre de usuario: ")
    contraseña = input("Contraseña: ")
    if usuario in program_data.usuarios and program_data.usuarios[usuario] == contraseña:
        print("¡Inicio de sesión exitoso!")
    else:
        print("Usuario o contraseña incorrectos.")

#Bloqueo de usuario si se intentan mas de 5 veces
intentos_fallidos = 0
max_intentos = 5

def iniciar_sesion():
    global intentos_fallidos
    print("\n--- Inicio de sesión ---")
    if intentos_fallidos >= max_intentos:
        print("Demasiados intentos fallidos. Contacta a un administrador o IT.")
        return

    usuario = input("Nombre de usuario: ")
    contraseña = input("Contraseña: ")
    if usuario in usuarios and usuarios[usuario] == contraseña:
        print("¡Inicio de sesión exitoso!")
        intentos_fallidos = 0  # Reinicia los intentos después de un inicio exitoso
    else:
        print("Usuario o contraseña incorrectos.")
        intentos_fallidos += 1
        print(f"Intentos fallidos: {intentos_fallidos}/{max_intentos}")
        if intentos_fallidos >= max_intentos:
            print("\nHas excedido el número de intentos permitidos.")
            print("Debes contactar a un administrador o IT para desbloquear tu cuenta.")