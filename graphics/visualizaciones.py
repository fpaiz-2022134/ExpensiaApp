# graphics/visualizaciones.py

import matplotlib.pyplot as plt
from data import program_data
import numpy as np
from datetime import datetime

def graficar_tasa_aprobacion():
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
        return None
    
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(usuarios_data, tasas_aprobacion, color='skyblue')
    
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height, f'{height:.1f}%', ha='center', va='bottom')
    
    ax.set_title('Tasa de Aprobación por Usuario')
    ax.set_xlabel('Usuarios')
    ax.set_ylabel('Tasa de Aprobación (%)')
    ax.set_xticklabels(usuarios_data, rotation=45, ha='right')
    plt.tight_layout()
    return fig

def graficar_distribucion_gastos():
    categorias = {}
    
    for data in program_data.usuarios.values():
        if 'facturas' in data:
            for factura in data['facturas']:
                if factura.get('aprobada') is True:
                    categoria = factura.get('categoria', 'Sin categoría')
                    monto = factura.get('monto', 0)
                    categorias[categoria] = categorias.get(categoria, 0) + monto
    
    if not categorias:
        return None
    
    categorias_ordenadas = dict(sorted(categorias.items(), key=lambda item: item[1], reverse=True))
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.pie(categorias_ordenadas.values(), labels=categorias_ordenadas.keys(),
           autopct='%1.1f%%', startangle=140)
    ax.set_title('Distribución de Gastos por Categoría')
    ax.axis('equal')
    plt.tight_layout()
    return fig

def graficar_tiempo_respuesta():
    usuarios_data = []
    tiempos_promedio = []
    
    for usuario, data in program_data.usuarios.items():
        if 'facturas' in data:
            tiempos = []
            for factura in data['facturas']:
                if factura.get('aprobada') and 'fecha_emision' in factura and 'fecha_aprobacion' in factura:
                    fecha_emision = datetime.strptime(factura['fecha_emision'], "%Y-%m-%d")
                    fecha_aprob = datetime.strptime(factura['fecha_aprobacion'], "%Y-%m-%d")
                    delta = (fecha_aprob - fecha_emision).days
                    tiempos.append(delta)
            
            if tiempos:
                promedio = sum(tiempos) / len(tiempos)
                usuarios_data.append(usuario)
                tiempos_promedio.append(promedio)
    
    if not usuarios_data:
        return None
    
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(usuarios_data, tiempos_promedio, color='lightgreen')
    
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f} días', ha='center', va='bottom')
    
    ax.set_title('Tiempo Promedio de Respuesta por Usuario')
    ax.set_xlabel('Usuarios')
    ax.set_ylabel('Días promedio')
    ax.set_xticklabels(usuarios_data, rotation=45, ha='right')
    plt.tight_layout()
    return fig

def graficar_top_usuarios():
    usuarios_facturas = []
    num_facturas = []
    
    for usuario, data in program_data.usuarios.items():
        if 'facturas' in data:
            usuarios_facturas.append(usuario)
            num_facturas.append(len(data['facturas']))
    
    if not usuarios_facturas:
        return None
    
    import numpy as np
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
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    ax1.bar(usuarios_facturas_top, num_facturas_top, color='orange')
    ax1.set_title('Top 5 Usuarios por Facturas Enviadas')
    ax1.set_xlabel('Usuarios')
    ax1.set_ylabel('Número de Facturas')
    ax1.tick_params(axis='x', rotation=45)
    for i, v in enumerate(num_facturas_top):
        ax1.text(i, v + 0.5, str(v), ha='center')
    
    ax2.bar(usuarios_saldo_top, saldos_top, color='purple')
    ax2.set_title('Top 5 Usuarios por Saldo Utilizado')
    ax2.set_xlabel('Usuarios')
    ax2.set_ylabel('Saldo Total (Q)')
    ax2.tick_params(axis='x', rotation=45)
    for i, v in enumerate(saldos_top):
        ax2.text(i, v + 0.5, f'Q{v:.2f}', ha='center')
    
    plt.tight_layout()
    return fig
