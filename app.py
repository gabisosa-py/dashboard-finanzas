import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar datos
@st.cache_data
def cargar_datos():
    df = pd.read_csv("transacciones.csv", encoding="latin1", sep=",")
    df.columns = df.columns.str.strip()
    df["Monto"] = pd.to_numeric(df["Monto"], errors="coerce")
    return df

df = cargar_datos()

# Calcular totales
total_ingresos = df[df["Tipo"] == "Ingreso"]["Monto"].sum()
total_gastos = df[df["Tipo"] == "Gasto"]["Monto"].sum()
balance_final = total_ingresos + total_gastos

# Configurar la app
st.title("📊 Dashboard de Finanzas Personales")
st.write("Visualiza tus ingresos y gastos de forma sencilla.")

# Mostrar resumen financiero
st.header("💰 Resumen Financiero")
st.metric(label="Total de Ingresos", value=f"${total_ingresos:,.2f}")
st.metric(label="Total de Gastos", value=f"${total_gastos:,.2f}")
st.metric(label="Balance Final", value=f"${balance_final:,.2f}")

# Gráficos
st.header("📈 Visualización de Datos")

# 📌 Gráfico de Ingresos vs. Gastos
fig, ax = plt.subplots(figsize=(6, 4))
ax.bar(["Ingresos", "Gastos"], [total_ingresos, abs(total_gastos)], color=["green", "red"])
ax.set_title("Comparación de Ingresos y Gastos")
st.pyplot(fig)

# 📌 Gráfico de Gastos por Categoría
st.subheader("Gastos por Categoría")
gastos_por_categoria = df[df["Tipo"] == "Gasto"].groupby("Categoria")["Monto"].sum()

fig, ax = plt.subplots(figsize=(7, 5))
gastos_por_categoria.plot(kind="bar", color="tomato", ax=ax)
ax.set_title("Gastos por Categoría")
plt.xticks(rotation=45)
st.pyplot(fig)

# 📌 Mostrar la tabla de datos
st.header("📋 Detalle de Transacciones")
st.dataframe(df)

# 📌 Botón para descargar el resumen en Excel
@st.cache_data
def convertir_a_excel(df):
    return df.to_excel("transacciones_procesadas.xlsx", index=False)

if st.button("📂 Descargar Reporte en Excel"):
    convertir_a_excel(df)
    st.success("✅ Archivo 'transacciones_procesadas.xlsx' generado con éxito!")
