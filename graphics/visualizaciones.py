# visualizaciones.py
import matplotlib.pyplot as plt
from data import program_data
import numpy as np
from datetime import datetime

def graficar_tasa_aprobacion():
    """
    Grafica la tasa de aprobación (facturas aprobadas / total facturas) * 100 por usuario
    """
    usuarios_data = []
    tasas_aprobacion = []
    
    for usuario, data in program_data.usuarios.items():
        if 'facturas' in data and data['facturas']:
            total_facturas = len(data['facturas'])
            aprobadas = sum(1 for f in data['facturas'] if f.get('aprobada') is True)
            tasa = (aprobadas / total_facturas) * 100 if total_facturas > 0 else 0
            usuarios_data.append(usuario)
            tasas_aprobacion.append(tasa)
    
    if not usuarios_data:
        print("No hay datos suficientes para graficar la tasa de aprobación.")
        return
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(usuarios_data, tasas_aprobacion, color='skyblue')
    
    # Añadir los valores en las barras
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                 f'{height:.1f}%',
                 ha='center', va='bottom')
    
    plt.title('Tasa de Aprobación por Usuario')
    plt.xlabel('Usuarios')
    plt.ylabel('Tasa de Aprobación (%)')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

def graficar_distribucion_gastos():
    """
    Grafica el monto total gastado por categoría
    """
    categorias = {}
    
    for data in program_data.usuarios.values():
        if 'facturas' in data:
            for factura in data['facturas']:
                if factura.get('aprobada') is True:
                    categoria = factura.get('categoria', 'Sin categoría')
                    monto = factura.get('monto', 0)
                    categorias[categoria] = categorias.get(categoria, 0) + monto
    
    if not categorias:
        print("No hay datos suficientes para graficar la distribución de gastos.")
        return
    
    # Ordenar categorías por monto descendente
    categorias_ordenadas = dict(sorted(categorias.items(), key=lambda item: item[1], reverse=True))
    
    plt.figure(figsize=(10, 6))
    plt.pie(categorias_ordenadas.values(), labels=categorias_ordenadas.keys(), 
            autopct='%1.1f%%', startangle=140)
    plt.title('Distribución de Gastos por Categoría')
    plt.axis('equal')
    plt.tight_layout()
    plt.show()

def graficar_tiempo_respuesta():
    """
    Grafica los días promedio entre envío y aprobación por usuario
    """
    usuarios_data = []
    tiempos_promedio = []
    
    for usuario, data in program_data.usuarios.items():
        if 'facturas' in data:
            tiempos = []
            for factura in data['facturas']:
                if factura.get('aprobada') and 'fecha_emision' in factura and 'fecha_aprobacion' in factura:
                    # Ya que las fechas están en formato ISO (YYYY-MM-DD)
                    fecha_emision = datetime.strptime(factura['fecha_emision'], "%Y-%m-%d")
                    fecha_aprob = datetime.strptime(factura['fecha_aprobacion'], "%Y-%m-%d")
                    delta = (fecha_aprob - fecha_emision).days
                    tiempos.append(delta)
            
            if tiempos:
                promedio = sum(tiempos) / len(tiempos)
                usuarios_data.append(usuario)
                tiempos_promedio.append(promedio)
    
    if not usuarios_data:
        print("No hay datos suficientes para graficar el tiempo de respuesta.")
        return
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(usuarios_data, tiempos_promedio, color='lightgreen')
    
    # Añadir los valores en las barras
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                 f'{height:.1f} días',
                 ha='center', va='bottom')
    
    plt.title('Tiempo Promedio de Respuesta por Usuario')
    plt.xlabel('Usuarios')
    plt.ylabel('Días promedio')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

def graficar_top_usuarios():
    """
    Grafica el top 5 de usuarios por facturas enviadas y saldo utilizado
    """
    
    usuarios_facturas = []
    num_facturas = []
    
    for usuario, data in program_data.usuarios.items():
        if 'facturas' in data:
            usuarios_facturas.append(usuario)
            num_facturas.append(len(data['facturas']))
    
    # Ordenar y tomar top 5
    indices_ordenados = np.argsort(num_facturas)[::-1][:5]
    usuarios_facturas_top = [usuarios_facturas[i] for i in indices_ordenados]
    num_facturas_top = [num_facturas[i] for i in indices_ordenados]
    
    
    usuarios_saldo = []
    saldos = []
    
    for usuario, data in program_data.usuarios.items():
        if 'facturas' in data:
            saldo_total = sum(f['monto'] for f in data['facturas'] if f.get('aprobada') is True)
            usuarios_saldo.append(usuario)
            saldos.append(saldo_total)
    
    
    indices_ordenados_saldo = np.argsort(saldos)[::-1][:5]
    usuarios_saldo_top = [usuarios_saldo[i] for i in indices_ordenados_saldo]
    saldos_top = [saldos[i] for i in indices_ordenados_saldo]
    
    # Crear figura con dos subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Gráfico de facturas
    ax1.bar(usuarios_facturas_top, num_facturas_top, color='orange')
    ax1.set_title('Top 5 Usuarios por Facturas Enviadas')
    ax1.set_xlabel('Usuarios')
    ax1.set_ylabel('Número de Facturas')
    ax1.tick_params(axis='x', rotation=45)
    
    
    for i, v in enumerate(num_facturas_top):
        ax1.text(i, v + 0.5, str(v), ha='center')
    
    # Gráfico de saldo
    ax2.bar(usuarios_saldo_top, saldos_top, color='purple')
    ax2.set_title('Top 5 Usuarios por Saldo Utilizado')
    ax2.set_xlabel('Usuarios')
    ax2.set_ylabel('Saldo Total (Q)')
    ax2.tick_params(axis='x', rotation=45)
    
    
    for i, v in enumerate(saldos_top):
        ax2.text(i, v + 0.5, f'Q{v:.2f}', ha='center')
    
    plt.tight_layout()
    plt.show()