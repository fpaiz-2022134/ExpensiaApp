# graphics/app_visualizaciones.py

import streamlit as st
from .visualizaciones import (
    graficar_tasa_aprobacion,
    graficar_distribucion_gastos,
    graficar_tiempo_respuesta,
    graficar_top_usuarios
)

def mostrar_menu_visualizaciones():
    st.title("Visualizaciones")
    
    opciones = {
        "Tasa de aprobación por usuario": graficar_tasa_aprobacion,
        "Distribución de gastos por categoría": graficar_distribucion_gastos,
        "Tiempo de respuesta promedio": graficar_tiempo_respuesta,
        "Top 5 usuarios": graficar_top_usuarios
    }

    seleccion = st.selectbox("Selecciona una visualización:", list(opciones.keys()))
    
    if seleccion:
        fig = opciones[seleccion]()
        if fig:
            st.pyplot(fig)
        else:
            st.warning("No hay datos suficientes para generar la gráfica.")
