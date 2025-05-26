import streamlit as st
from data import program_data
from data.data_handler import guardar_usuarios

MAX_INTENTOS = 5

def iniciar_sesion():
    usuario = st.text_input("Nombre de usuario", key="login_usuario")
    contraseña = st.text_input("Contraseña", type="password", key="login_contraseña")
    iniciar_btn = st.button("Iniciar sesión", key="login_btn")

    if 'intentos_fallidos' not in st.session_state:
        st.session_state.intentos_fallidos = 0

    if iniciar_btn:
        if st.session_state.intentos_fallidos >= MAX_INTENTOS:
            st.error("Demasiados intentos fallidos. Contacta a un administrador.")
            return None

        if usuario in program_data.usuarios and program_data.usuarios[usuario]['contraseña'] == contraseña:
            st.session_state.intentos_fallidos = 0
            return usuario  # Login correcto, devuelve usuario
        else:
            st.session_state.intentos_fallidos += 1
            st.error("Usuario o contraseña incorrectos.")
            st.info(f"Intentos fallidos: {st.session_state.intentos_fallidos}/{MAX_INTENTOS}")
            return None

    
    return None

def registrar_usuario():
    # Para evitar título duplicado, NO poner subheader aquí
    usuario = st.text_input("Nombre de usuario", key="registro_usuario")
    contraseña = st.text_input("Contraseña", type="password", key="registro_contraseña")
    repetir_contraseña = st.text_input("Repetir contraseña", type="password", key="registro_repetir")
    rol = st.selectbox("Tipo de usuario", ["usuario", "admin"], key="registro_rol")
    clave_admin = ""
    if rol == "admin":
        clave_admin = st.text_input("Clave admin", type="password", key="registro_clave_admin")

    registrar_btn = st.button("Registrarse", key="registro_btn")

    if registrar_btn:
        if not usuario or not contraseña or not repetir_contraseña:
            st.warning("Por favor, completa todos los campos.")
            return False

        if contraseña != repetir_contraseña:
            st.warning("Las contraseñas no coinciden.")
            return False

        if usuario in program_data.usuarios:
            st.warning("Este usuario ya existe. Intenta otro.")
            return False

        if rol == "admin" and clave_admin != "clave123":
            st.warning("Clave admin incorrecta. Se registrará como 'usuario'.")
            rol = "usuario"

        # Guardar nuevo usuario
        program_data.usuarios[usuario] = {
            'contraseña': contraseña,
            'rol': rol,
            'perfil': {},
            'facturas': [],
            'saldo': 0
        }
        guardar_usuarios()
        return True  # Registro exitoso

    return False