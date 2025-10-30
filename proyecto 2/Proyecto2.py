# ==============================================
# Análisis de Recompra en Campaña de Marketing
# Dataset: Mini_Proyecto_Clientes_Promociones.xlsx
# ==============================================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import classification_report, confusion_matrix

# --- 1️⃣ Carga de datos ---
df = pd.read_excel("C:/Users/colat/OneDrive/Escritorio/IA 2°año/modelizado de mineria de datos/Proyecto/Proyecto2/Mini_Proyecto_Clientes_Promociones.xlsx")

# --- 2️⃣ Limpieza y transformación ---
df['Genero'] = df['Genero'].map({'F': 0, 'M': 1})
df['Recibio_Promo'] = df['Recibio_Promo'].map({'Si': 1, 'No': 0})
df['Recompra'] = df['Recompra'].map({'Si': 1, 'No': 0})

# Eliminamos filas sin valor de recompra
df.dropna(subset=['Recompra'], inplace=True)

# --- 3️⃣ Gráfico 1: Boxplot de Monto Promocional vs Recompra ---
plt.figure(figsize=(8, 5))
sns.boxplot(data=df, x='Recompra', y='Monto_Promo', palette='coolwarm')
plt.title('Distribución de Monto Promocional según Recompra', fontsize=14)
plt.xlabel('Recompra (0 = No, 1 = Sí)')
plt.ylabel('Monto Promocional')
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.show()

# --- 4️⃣ Gráfico 2: Tasa de Recompra según Recepción de Promoción ---
plt.figure(figsize=(7, 5))
sns.barplot(
    data=df,
    x='Recibio_Promo',
    y='Recompra',
    estimator=lambda x: sum(x) / len(x),  # calcula porcentaje
    palette='viridis'
)
plt.title('Tasa de Recompra según Recepción de Promoción', fontsize=14)
plt.xlabel('Recibió Promoción (0 = No, 1 = Sí)')
plt.ylabel('Porcentaje de Recompra')
plt.ylim(0, 1)
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.show()

# --- 5️⃣ Modelo de Árbol de Decisión ---
X = df.drop(['Cliente_ID', 'Recompra'], axis=1)
y = df['Recompra']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

modelo = DecisionTreeClassifier(max_depth=4, random_state=42)
modelo.fit(X_train, y_train)
y_pred = modelo.predict(X_test)

print("📊 MATRIZ DE CONFUSIÓN:\n", confusion_matrix(y_test, y_pred))
print("\n📋 REPORTE DE CLASIFICACIÓN:\n", classification_report(y_test, y_pred))

# --- 6️⃣ Visualización del Árbol ---
plt.figure(figsize=(12, 6))
plot_tree(modelo, feature_names=X.columns, class_names=["No Recompra", "Recompra"], filled=True)
plt.title("Árbol de Decisión — Recompra de Clientes", fontsize=14)
plt.show()

