import streamlit as st
import streamlit.components.v1 as components
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
from data.program_data import usuarios
from data.data_handler import cargar_datos

def safe_rerun():
    st.rerun()


# Cargar datos al inicio
cargar_datos()

# Inicializar variables de sesión
if 'usuario' not in st.session_state:
    st.session_state.usuario = None
if 'rol' not in st.session_state:
    st.session_state.rol = None
if 'pagina' not in st.session_state:
    st.session_state.pagina = 'menu'
if 'mostrar_registro' not in st.session_state:
    st.session_state.mostrar_registro = False

def logout():
    st.session_state.usuario = None
    st.session_state.rol = None
    st.session_state.pagina = 'menu'

# Menú principal
if st.session_state.pagina == 'menu':
    with st.container():
        st.markdown(
            """
            <div style='text-align: center;'>
                <h1 style='color:#4CAF50;'>EXPENSIA</h1>
                <h4>¡Bienvenido a la mejor aplicación de viáticos de Guatemala!</h4>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")

    if not st.session_state.mostrar_registro:
        st.markdown("### <center>Iniciar sesión:", unsafe_allow_html=True)

        usuario = iniciar_sesion()

        st.markdown("¿Primera vez? Regístrate abajo")
        if st.button("Crear cuenta nueva", key="mostrar_registro_btn"):
            st.session_state.mostrar_registro = True

        if usuario:
            st.success(f"¡Bienvenido, {usuario}!")
            st.session_state.usuario = usuario
            st.session_state.rol = usuarios[usuario]['rol']
            st.session_state.pagina = 'usuario' if st.session_state.rol == 'usuario' else 'admin'
            safe_rerun()

    else:
        st.markdown("### Registro de nuevo usuario")

        registrado = registrar_usuario()

        if registrado:
            st.success("¡Registro exitoso! Ya puedes iniciar sesión.")
            st.session_state.mostrar_registro = False
        else:
            st.info("¿Ya tienes cuenta?")
            if st.button(" Volver al login", key="volver_btn"):
                st.session_state.mostrar_registro = False


# Interfaz usuario
elif st.session_state.pagina == 'usuario':
    st.sidebar.title("Menú Usuario")
    opcion = st.sidebar.selectbox("Opciones", [
        "Ver dashboard",
        "Enviar factura",
        "Ver saldo",
        "Gestionar perfil",
        "Buscar factura",
        "Cerrar sesión"
    ])

    if opcion == "Ver dashboard":
        mostrar_dashboard(st.session_state.usuario)
    elif opcion == "Enviar factura":
        enviar_factura(st.session_state.usuario)
    elif opcion == "Ver saldo":
        ver_saldo(st.session_state.usuario)
    elif opcion == "Gestionar perfil":
        gestionar_perfil(st.session_state.usuario)
    elif opcion == "Buscar factura":
        buscar_facturas_usuario(st.session_state.usuario)
    elif opcion == "Cerrar sesión":
        logout()
        safe_rerun()

# Interfaz admin
elif st.session_state.pagina == 'admin':
    st.sidebar.title("Menú Administrador")
    opcion = st.sidebar.selectbox("Opciones", [
        "Ver facturas pendientes",
        "Procesar factura",
        "Buscar factura",
        "Estadísticas de aprobación",
        "Top usuarios",
        "Visualizaciones gráficas",
        "Cerrar sesión"
    ])

    if opcion == "Ver facturas pendientes":
        ver_facturas_pendientes()
    elif opcion == "Procesar factura":
        aprobar_facturas()
    elif opcion == "Buscar factura":
        buscar_facturas_interactivo_admin()
    elif opcion == "Estadísticas de aprobación":
        tiempo_respuesta_promedio()
    elif opcion == "Top usuarios":
        mostrar_top_usuarios()
    elif opcion == "Visualizaciones gráficas":
        menu_visualizaciones()
    elif opcion == "Cerrar sesión":
        logout()
        safe_rerun()