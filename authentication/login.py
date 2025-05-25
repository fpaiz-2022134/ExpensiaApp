import streamlit as st
from data import program_data
from data.data_handler import guardar_usuarios

# Inicializar estado de intentos fallidos
if 'intentos_fallidos' not in st.session_state:
    st.session_state.intentos_fallidos = 0

MAX_INTENTOS = 5

def iniciar_sesion():
    st.subheader("Iniciar sesión")

    usuario = st.text_input("Nombre de usuario", key="login_usuario")
    contraseña = st.text_input("Contraseña", type="password", key="login_contraseña")
    login_btn = st.button("Iniciar sesión")

    if login_btn:
        if st.session_state.intentos_fallidos >= MAX_INTENTOS:
            st.error("Demasiados intentos fallidos. Contacta a un administrador o IT.")
            return

        if usuario in program_data.usuarios and program_data.usuarios[usuario]['contraseña'] == contraseña:
            st.success("¡Inicio de sesión exitoso!")
            st.session_state.intentos_fallidos = 0
            # Guardamos el usuario para que main.py lo detecte
            st.session_state.usuario_actual = usuario
        else:
            st.session_state.intentos_fallidos += 1
            st.error("Usuario o contraseña incorrectos.")
            st.info(f"Intentos fallidos: {st.session_state.intentos_fallidos}/{MAX_INTENTOS}")

def registrar_usuario():
    st.subheader("Registro de usuario")

    usuario = st.text_input("Elija su nombre de usuario", key="registro_usuario")
    contraseña = st.text_input("Elija una contraseña", type="password", key="registro_contraseña")
    rol = st.selectbox("Seleccione su rol", ['usuario', 'admin'], key="registro_rol")

    clave_admin = ""
    if rol == 'admin':
        clave_admin = st.text_input("Ingrese la clave especial de administrador", type="password", key="registro_clave_admin")

    registrar_btn = st.button("Registrarse")

    if registrar_btn:
        if usuario in program_data.usuarios:
            st.warning("Este usuario ya existe. Intente con otro.")
        else:
            if rol == 'admin' and clave_admin != "clave123":
                st.warning("Clave incorrecta. Será registrado como 'usuario'.")
                rol = 'usuario'

            program_data.usuarios[usuario] = {
                'contraseña': contraseña,
                'rol': rol,
                'perfil': {},
                'facturas': [],
                'saldo': 0
            }
            guardar_usuarios()
            st.success("¡Registro exitoso!")
