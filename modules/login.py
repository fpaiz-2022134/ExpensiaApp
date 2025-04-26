usuarios = {}

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
    if usuario in usuarios:
        print("Este usuario ya existe. Intente con otro.")
    else:
        contraseña = input("Eliga una contraseña: ")
        usuarios[usuario] = contraseña
        print("¡Registro exitoso!")
#Inicio de Sesion
def iniciar_sesion():
    print("\n--- Inicio de sesión ---")
    usuario = input("Nombre de usuario: ")
    contraseña = input("Contraseña: ")
    if usuario in usuarios and usuarios[usuario] == contraseña:
        print("¡Inicio de sesión exitoso!")
    else:
        print("Usuario o contraseña incorrectos.")