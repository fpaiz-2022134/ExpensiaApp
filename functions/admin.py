from data.program_data import facturas_pendientes, usuarios
from data.data_handler import guardar_usuarios, guardar_facturas
import pandas as pd
from datetime import date, datetime
from graphics import app_visualizaciones
import streamlit as st

def ver_facturas_pendientes():
    st.write("### Facturas Pendientes")
    for i, factura in enumerate(facturas_pendientes):
        if factura.get('aprobada') not in [True, False]:
            st.write(f"{i + 1}. Número factura: {factura['numero_factura']} | Usuario: {factura['usuario']} | Categoría: {factura['categoria']} | Monto: Q{factura['monto']} | Aprobada: {factura['aprobada']}")

def aprobar_facturas():
    ver_facturas_pendientes()
    idx = st.number_input("Número de factura a procesar", min_value=1, max_value=len(facturas_pendientes), step=1) - 1
    
    if st.button("Procesar factura"):
        if 0 <= idx < len(facturas_pendientes):
            factura = facturas_pendientes[idx]
            decision = st.radio("¿Deseas aprobar esta factura?", ("Sí", "No"))
            
            factura['aprobada'] = True if decision == "Sí" else False
            if factura['aprobada']:
                factura['fecha_aprobacion'] = date.today().isoformat()
            
            for f in usuarios[factura['usuario']]['facturas']:
                if f['numero_factura'] == factura['numero_factura']:
                    f['aprobada'] = factura['aprobada']
                    if factura['aprobada']:
                        f['fecha_aprobacion'] = factura['fecha_aprobacion']
                    break

            if factura['aprobada']:
                usuarios[factura['usuario']]['saldo'] += factura['monto']
                st.success(f"La factura ha sido aprobada. Fecha de aprobación: {factura['fecha_aprobacion']}. Saldo actualizado.")
            else:
                st.warning("La factura ha sido denegada, saldo no modificado.")
            
            guardar_usuarios()
            guardar_facturas()
            facturas_pendientes.pop(idx)
        else:
            st.error("Número de factura inválido.")

def buscar_facturas(criterio, valor):
    try:
        df = pd.read_csv('bills.csv')
        if criterio not in df.columns:
            st.error(f"Criterio '{criterio}' no encontrado en las columnas.")
            return []
        coincidencias = df[df[criterio].astype(str).str.lower() == str(valor).lower()]
        return coincidencias.to_dict('records')
    except FileNotFoundError:
        st.error("El archivo 'bills.csv' no existe.")
        return []
    except Exception as e:
        st.error(f"Error al buscar facturas: {e}")
        return []

def buscar_facturas_interactivo_admin():
    opcion = st.radio("Buscar facturas por:", ["Número de factura", "Usuario", "Volver"])
    
    if opcion == "Número de factura":
        valor = st.text_input("Ingrese número de factura:")
        if st.button("Buscar"):
            resultados = buscar_facturas('numero_factura', valor)
            if resultados:
                for r in resultados:
                    st.write(r)
            else:
                st.info("No se encontraron facturas.")
    elif opcion == "Usuario":
        valor = st.text_input("Ingrese nombre de usuario:")
        if st.button("Buscar"):
            resultados = buscar_facturas('usuario', valor)
            if resultados:
                for r in resultados:
                    st.write(r)
            else:
                st.info("No se encontraron facturas.")
    else:
        st.info("Volviendo al menú principal.")

def tiempo_respuesta_promedio():
    tiempos = []
    for user_data in usuarios.values():
        if 'facturas' in user_data:
            for factura in user_data['facturas']:
                if factura.get('aprobada') and factura.get('fecha_emision') and factura.get('fecha_aprobacion'):
                    fecha_emision = datetime.strptime(factura['fecha_emision'], "%Y-%m-%d")
                    fecha_aprob = datetime.strptime(factura['fecha_aprobacion'], "%Y-%m-%d")
                    delta = (fecha_aprob - fecha_emision)
                    tiempos.append(delta.days)
    promedio = sum(tiempos) / len(tiempos) if tiempos else 0
    st.write(f"Tiempo de aprobación promedio: **{promedio:.2f} días**")

def top_usuarios_por_facturas():
    usuarios_conteo = []
    for username, data in usuarios.items():
        num_facturas = len(data.get('facturas', []))
        usuarios_conteo.append((username, num_facturas))
    usuarios_conteo.sort(key=lambda x: x[1], reverse=True)
    return usuarios_conteo[:5]

def top_usuarios_por_saldo():
    usuarios_saldo = []
    for username, data in usuarios.items():
        saldo_total = sum(f.get('monto', 0) for f in data.get('facturas', []))
        usuarios_saldo.append((username, saldo_total))
    usuarios_saldo.sort(key=lambda x: x[1], reverse=True)
    return usuarios_saldo[:5]

def mostrar_top_usuarios():
    st.write("### Top 5 Usuarios por Facturas Enviadas")
    for i, (usuario, cantidad) in enumerate(top_usuarios_por_facturas(), 1):
        st.write(f"{i}. {usuario}: {cantidad} facturas")
    st.write("### Top 5 Usuarios por Saldo Utilizado")
    for i, (usuario, saldo) in enumerate(top_usuarios_por_saldo(), 1):
        st.write(f"{i}. {usuario}: Q{saldo:.2f}")

def menu_visualizaciones():
    app_visualizaciones.mostrar_menu_visualizaciones()
