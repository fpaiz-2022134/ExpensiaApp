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

    # Cargar facturas pendientes
    if os.path.exists('bills.csv'):
        try:
            df_bills = pd.read_csv('bills.csv')
            facturas_pendientes.extend([f for f in df_bills.to_dict('records') if f.get('aprobada') is None])
        except Exception as e:
            print(f"Error al cargar facturas: {e}")

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
    """Guarda las facturas pendientes en el archivo CSV"""
    try:
        pd.DataFrame(facturas_pendientes).to_csv('bills.csv', index=False)
    except Exception as e:
        print(f"Error al guardar facturas: {e}")