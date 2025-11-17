import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path

# Obter dados 
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_PATH = BASE_DIR / 'dados' / 'painel_solar.csv'

def calcular_rendimento():
    """Calcula o rendimento médio por hora dos paineis solares
        
       returns: 
        dict: Dados processados prontos para Json
    """
    
    # puxar os dados do arquivo csv
    df = pd.read_csv(DATA_PATH)
    
    # Calcula rendimento
    area_painel = 10 # m^2 
    df['potencia_incidente_kw'] = (df['radiacao_wm2'] * area_painel) / 1000
    df['porcentagem_rendimento'] = (df['potencia_kw'] / df['potencia_incidente_kw'])