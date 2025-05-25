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

# Función segura para recargar la página, compatible con Streamlit 1.45.1
def safe_rerun():
    try:
        st.experimental_rerun()
    except AttributeError:
        components.html("<script>window.location.reload();</script>")

# Cargar datos al inicio
cargar_datos()

# Inicializar variables de sesión
if 'usuario' not in st.session_state:
    st.session_state.usuario = None
if 'rol' not in st.session_state:
    st.session_state.rol = None
if 'pagina' not in st.session_state:
    st.session_state.pagina = 'menu'

st.title("EXPENSIA")
st.subheader("¡Bienvenido a la mejor aplicación de viáticos de Guatemala!")

def logout():
    st.session_state.usuario = None
    st.session_state.rol = None
    st.session_state.pagina = 'menu'

# Menú principal
if st.session_state.pagina == 'menu':
    opcion = st.radio("Selecciona una opción:", ["Iniciar sesión", "Registrarse"])

    if opcion == "Iniciar sesión":
        usuario = iniciar_sesion()
        if usuario:
            st.success("Sesión iniciada correctamente.")
            st.session_state.usuario = usuario
            st.session_state.rol = usuarios[usuario]['rol']
            st.session_state.pagina = 'usuario' if st.session_state.rol == 'usuario' else 'admin'
            safe_rerun()

    elif opcion == "Registrarse":
        registrar_usuario()

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
        st.write(f"El tiempo de aprobación promedio es: **{tiempo_respuesta_promedio()} días**")
    elif opcion == "Top usuarios":
        mostrar_top_usuarios()
    elif opcion == "Visualizaciones gráficas":
        menu_visualizaciones()
    elif opcion == "Cerrar sesión":
        logout()
        safe_rerun()
