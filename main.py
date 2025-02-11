import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar el archivo CSV con el separador correcto
df = pd.read_csv("transacciones.csv", encoding="latin1", sep=",")

# Limpiar nombres de columnas (eliminar espacios extra)
df.columns = df.columns.str.strip()

# Convertir la columna "Monto" a valores numéricos
df["Monto"] = pd.to_numeric(df["Monto"], errors="coerce")

# Calcular totales
total_ingresos = df[df["Tipo"] == "Ingreso"]["Monto"].sum()
total_gastos = df[df["Tipo"] == "Gasto"]["Monto"].sum()
balance_final = total_ingresos + total_gastos  # Gastos son negativos

# Función para mostrar gráficos
def mostrar_graficos():
    sns.set_style("whitegrid")

    # 📌 Gráfico de Ingresos vs. Gastos
    plt.figure(figsize=(6, 4))
    plt.bar(["Ingresos", "Gastos"], [total_ingresos, abs(total_gastos)], color=["green", "red"])
    plt.title("Comparación de Ingresos y Gastos")
    plt.ylabel("Monto en $")
    plt.show()

    # 📌 Gráfico de Gastos por Categoría
    gastos_por_categoria = df[df["Tipo"] == "Gasto"].groupby("Categoria")["Monto"].sum()

    plt.figure(figsize=(7, 5))
    gastos_por_categoria.plot(kind="bar", color="tomato")
    plt.title("Gastos por Categoría")
    plt.ylabel("Monto en $")
    plt.xticks(rotation=45)
    plt.show()

# 📌 Menú Interactivo
while True:
    print("\n📌 Menú de Opciones:")
    print("1️⃣ Ver resumen financiero")
    print("2️⃣ Ver gráficos")
    print("3️⃣ Exportar datos")
    print("4️⃣ Salir")

    opcion = input("Selecciona una opción: ")

    if opcion == "1":
        print("\n💰 Resumen Financiero:")
        print(f"🔹 Total de Ingresos: ${total_ingresos:,.2f}")
        print(f"🔹 Total de Gastos: ${total_gastos:,.2f}")
        print(f"🔹 Balance Final: ${balance_final:,.2f}")
    elif opcion == "2":
        mostrar_graficos()
    elif opcion == "3":
        df.to_excel("transacciones_procesadas.xlsx", index=False)
        print("📂 Archivo 'transacciones_procesadas.xlsx' generado con éxito!")
    elif opcion == "4":
        print("👋 Saliendo del programa...")
        break
    else:
        print("❌ Opción no válida, intenta de nuevo.")
