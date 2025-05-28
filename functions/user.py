from datetime import date
from data.program_data import usuarios, facturas_pendientes, validar_numero
from data.data_handler import guardar_usuarios, guardar_facturas
import pandas as pd
import streamlit as st


# Menú principal para el usuario
def menu_usuario():
    st.title("         EXPENSIA         ")

# Muestra el dashboard del usuario
def mostrar_dashboard(usuario):
    facturas = usuarios.get(usuario, {}).get('facturas', [])
    total_facturas = len(facturas) if facturas else 0

    st.markdown("""
    <style>
        .dashboard-container {
            max-width: 600px;
            margin: 40px auto;
            font-family: sans-serif;
            text-align: center;
            color: #333;
        }
        .metric-card {
            background: #fff;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            width: 250px;
            margin: 0 auto 30px;
        }
        .metric-number {
            font-size: 64px;
            font-weight: bold;
            color: #0078d7;
            margin: 20px 0 10px;
        }
        .metric-label {
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 20px;
            text-transform: uppercase;
            color: #555;
        }
        div.stButton > button {
            background-color: #0078d7;
            color: white;
            border-radius: 20px;
            padding: 12px 30px;
            font-weight: 600;
            cursor: pointer;
            border: none;
            font-size: 16px;
            margin: 0 auto;
            display: block;
        }
        div.stButton > button:hover {
            background-color: #005a9e;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='dashboard-container'>", unsafe_allow_html=True)
    st.markdown(f"""
        <div>
                <center>
            <h1>Hola, {usuario} 👋</h1>
            <p>Bienvenido a tu panel de control en EXPENSIA</p>
        </div>
        <div class='metric-card'>
            <p class='metric-number'>{total_facturas}</p>
            <p class='metric-label'>Facturas Enviadas</p>
            </center>
        </div>
    """, unsafe_allow_html=True)


    st.markdown("</div>", unsafe_allow_html=True)


        
def enviar_factura(usuario):
    st.subheader("---- ENVIAR FACTURA")
    st.write("A continuación, deberás ingresar distintos datos para un envío correcto...\n")


    with st.form("form_factura"):
        numero_factura = st.text_input("Número de factura")
        proveedor = st.text_input("Nombre del proveedor")
        monto = st.text_input("Monto")
        moneda_utilizada = st.text_input("Moneda utilizada (Q)", value="Q")
        categoria = st.text_input("Categoría del gasto (comida, transporte, etc)")
        descripcion = st.text_area("Describe el gasto realizado")
        submitted = st.form_submit_button("Enviar Factura")

        
    if submitted:
        if not validar_numero(numero_factura):
            numero_factura= int(numero_factura)
            st.error("El número de factura debe ser un número entero.")
            return
        if not validar_numero(monto):
            st.error("El monto debe ser un número válido.")
            return
    
    factura = {
            'usuario': usuario,
            'numero_factura': numero_factura,
            'proveedor': proveedor,
            'fecha_emision': date.today().isoformat(),
            'monto': float(monto),
            'moneda_utilizada': moneda_utilizada,
            'categoria': categoria,
            'descripcion': descripcion,
            'aprobada': None
        }
    
    usuarios[usuario]['facturas'].append(factura)
    facturas_pendientes.append(factura)

    guardar_usuarios()
    guardar_facturas()

    st.success("La factura fue enviada al administrador exitosamente.")


def ver_saldo(usuario):
    saldo = usuarios[usuario]['saldo']
    st.info(f"\nSaldo disponible: Q{saldo:.2f}")

def gestionar_perfil(usuario):
    st.subheader("\n--- Perfil de Usuario ---")
    perfil = usuarios[usuario]['perfil']

    nombre = st.text_input("Nombre completo", value=perfil.get('nombre', ''))
    correo = st.text_input("Correo electrónico", value=perfil.get('correo', ''))

    if st.button("Actualizar Perfil"):
        perfil['nombre'] = nombre
        perfil['correo'] = correo
        guardar_usuarios()
        st.success("Perfil actualizado exitosamente.")
        
# ------------------------------
#    FUNCION PARA BUSCAR FACTURAS
# ------------------------------
def buscar_facturas(criterio, valor, usuario_actual):
    try:
        df = pd.read_csv('bills.csv')

        if criterio not in df.columns:
            st.error(f"Criterio '{criterio}' no encontrado en las columnas.")
            return []

        # Filtramos solo las facturas del usuario actual
        df_filtrado = df[df['usuario'].astype(str).str.lower() == usuario_actual.lower()]

        # Filtrar por el criterio elegido
        coincidencias = df_filtrado[df_filtrado[criterio].astype(str).str.lower() == str(valor).lower()]

        return coincidencias.to_dict('records')

    except FileNotFoundError:
        st.error("El archivo 'bills.csv' no existe.")
        return []

    except Exception as e:
        st.error(f"Error al buscar facturas: {e}")
        return []

def buscar_facturas_interactivo(usuario_actual):
    
    st.subheader("Buscar Factura")
    opciones = {
        "Núnmero de factura": "numero_factura"
    }    
    
    opcion = st.selectbox("Selecciona un criterio de búsqueda:", list(opciones.keys()) )
    valor = st.text_input("Ingrese el valor para buscar:")
    
    if st.button("Buscar"):
        criterio = opciones[opcion]
        resultados = buscar_facturas(criterio, valor, usuario_actual)
        
        if resultados:
            st.success(f"Se encontraron {len(resultados)} factura(s):")
            for idx, factura in enumerate(resultados, 1):
                st.markdown(f"Factura {idx}:")
                for key, val in factura.items():
                    st.markdown(f"- {key}: {val}")
                st.markdown("----")
        else:
            st.warning("No se encontraron facturas con ese criterio.")
    
    