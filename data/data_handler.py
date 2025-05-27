import pandas as pd
from data.program_data import usuarios, facturas_pendientes
import os

def cargar_datos():
    """Carga los datos desde los archivos CSV al iniciar el programa"""
    global usuarios, facturas_pendientes
    
    # Cargar usuarios
    if os.path.exists('users.csv'):
        try:
            df_users = pd.read_csv('users.csv')
            for _, row in df_users.iterrows():
                usuarios[row['usuario']] = {
                    'contraseña': row['contraseña'],
                    'rol': row['rol'],
                    'perfil': eval(row['perfil']),
                    'facturas': eval(row['facturas']),
                    'saldo': row['saldo']
                }
        except Exception as e:
            print(f"Error al cargar usuarios: {e}")

    # Cargar facturas pendientes (solo las no aprobadas)
    if os.path.exists('bills.csv'):
        try:
            df_bills = pd.read_csv('bills.csv')
            # Solo cargar facturas no aprobadas como pendientes
            facturas_pendientes.extend(
                [f for f in df_bills.to_dict('records') if not f.get('aprobada')]
            )
        except Exception as e:
            print(f"Error al cargar facturas pendientes: {e}")

def guardar_usuarios():
    """Guarda los usuarios en el archivo CSV"""
    try:
        data = []
        for usuario, info in usuarios.items():
            data.append({
                'usuario': usuario,
                'contraseña': info['contraseña'],
                'rol': info['rol'],
                'perfil': str(info['perfil']),
                'facturas': str(info['facturas']),
                'saldo': info['saldo']
            })
        pd.DataFrame(data).to_csv('users.csv', index=False)
    except Exception as e:
        print(f"Error al guardar usuarios: {e}")

def guardar_facturas():
    """Guarda las facturas en sus respectivos archivos"""
    try:
        # Primero cargamos todas las facturas existentes de total_bills.csv
        todas_facturas = []
        if os.path.exists('total_bills.csv'):
            df_total = pd.read_csv('total_bills.csv')
            todas_facturas = df_total.to_dict('records')
        
        # Actualizamos con las facturas pendientes actuales
        df_pendientes = pd.DataFrame(facturas_pendientes)
        
        # Juntamos todas las facturas (pendientes y aprobadas)
        todas_facturas = [f for f in todas_facturas if f.get('aprobada') is True] + \
                         df_pendientes.to_dict('records')
        
        # Guardamos en bills.csv solo las pendientes
        df_pendientes.to_csv('bills.csv', index=False)
        
        # Guardamos en total_bills.csv todas las facturas
        pd.DataFrame(todas_facturas).to_csv('total_bills.csv', index=False)
        
    except Exception as e:
        print(f"Error al guardar facturas: {e}")