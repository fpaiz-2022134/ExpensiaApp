from data import program_data




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
#Inicio de Sesión
def iniciar_sesion():
    print("\n--- Inicio de sesión ---")
    usuario = input("Nombre de usuario: ")
    contraseña = input("Contraseña: ")
    if usuario in program_data.usuarios and program_data.usuarios[usuario]['contraseña']== contraseña:
        print("¡Inicio de sesión exitoso!")
        return usuario
    else:
        print("Usuario o contraseña incorrectos.")
        return None