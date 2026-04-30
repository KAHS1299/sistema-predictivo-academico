import pandas as pd
import numpy as np

# Configuración para reproducibilidad
np.random.seed(42)

# Generar 1000 registros basados en tus 3 clústeres previos
n_points = 1000

# Clúster 1: Bajo rendimiento (Ventas 1-50)
c1_n = 350
c1_x = np.random.randint(1, 51, c1_n)
c1_y = c1_x * 23 + np.random.normal(0, 50, c1_n)

# Clúster 2: Rendimiento Medio (Ventas 51-120)
c2_n = 400
c2_x = np.random.randint(51, 121, c2_n)
c2_y = c2_x * 20 + np.random.normal(0, 100, c2_n)

# Clúster 3: Alto rendimiento (Ventas 121-250)
c3_n = 250
c3_x = np.random.randint(121, 251, c3_n)
c3_y = c3_x * 18 + np.random.normal(0, 150, c3_n)

# Combinar todo
df = pd.DataFrame({
    'Products_Sold (X)': np.concatenate([c1_x, c2_x, c3_x]),
    'Profit (Y)': np.concatenate([c1_y, c2_y, c3_y])
})

# Limpiar valores negativos y redondear
df['Profit (Y)'] = df['Profit (Y)'].clip(lower=10).round(2)

# Guardar como Excel (requiere pip install openpyxl)
df.to_excel('kmeans_dataset.xlsx', index=False)
print("¡Archivo kmeans_dataset.xlsx creado con 1000 registros!")