import pandas as pd
import os

# Carpeta base
# Usar ruta raw string o construirla con os.path.join para evitar escapes de backslash
# He optado por usar os.path.join para mayor portabilidad
BASE = os.path.expanduser(r"~")
CARPETA = os.path.join(BASE, "OneDrive", "Escritorio", "IA 2°año", "modelizado de mineria de datos", "Proyecto", "Proyecto 1")


# Helpers para campos ID y generación de nuevos IDs
def is_id_field(field_name: str) -> bool:
    """Devuelve True si el nombre del campo parece ser un identificador (ej. 'id', 'id_cliente', 'ID')."""
    if not isinstance(field_name, str):
        return False
    n = field_name.strip().lower()
    # Reglas simples: empieza por 'id' o contiene 'id_' o termina en '_id' o es exactamente 'id'
    return n == "id" or n.startswith("id") or n.startswith("id_") or n.endswith("_id") or ("id" in n and n.startswith("id"))


def get_modifiable_fields(registro: dict) -> list:
    """Devuelve la lista de campos que pueden modificarse (excluye campos id)."""
    return [f for f in registro.keys() if not is_id_field(f)]


def generate_new_id(tabla: list, id_field: str):
    """Intenta generar un nuevo id entero a partir del máximo existente + 1.
    Si no puede, devuelve la longitud actual (como fallback) o cadena vacía si no aplica.
    """
    try:
        valores = [r.get(id_field) for r in tabla if id_field in r]
        nums = []
        for v in valores:
            try:
                nums.append(int(v))
            except Exception:
                # Ignorar valores no convertibles
                pass
        if nums:
            return max(nums) + 1
        else:
            return len(tabla) + 1
    except Exception:
        return ""

# Leer CSV y convertir en diccionarios ---
def cargar_tablas():
    tablas = {
    "clientes": pd.read_csv(os.path.join(CARPETA, "clientes.csv")).to_dict(orient="records"),
    "localidades": pd.read_csv(os.path.join(CARPETA, "localidades.csv")).to_dict(orient="records"),
    "provincias": pd.read_csv(os.path.join(CARPETA, "provincias.csv")).to_dict(orient="records"),
    "productos": pd.read_csv(os.path.join(CARPETA, "productos.csv")).to_dict(orient="records"),
    "clientes_mail": pd.read_csv(os.path.join(CARPETA, "clientes_mail.csv")).to_dict(orient="records"),
    "clientes_tel": pd.read_csv(os.path.join(CARPETA, "clientes_tel.csv")).to_dict(orient="records"),
    "rubros": pd.read_csv(os.path.join(CARPETA, "rubros.csv")).to_dict(orient="records"),
    "sucursales": pd.read_csv(os.path.join(CARPETA, "sucursales.csv")).to_dict(orient="records"),
    "facturaenc": pd.read_csv(os.path.join(CARPETA, "facturas_enc.csv")).to_dict(orient="records"),
    "facturadet": pd.read_csv(os.path.join(CARPETA, "facturas_det.csv")).to_dict(orient="records"),
    "ventas": pd.read_csv(os.path.join(CARPETA, "ventas.csv")).to_dict(orient="records"),

    }
    return tablas


# Guardar todas las tablas en CSV
def guardar_todo(tablas):
    print("\n Guardando todos los cambios (CSV)...")
    # Guardar CSV por cada tabla conocida (si existe en el dict)
    mapping = {
        "clientes": "clientes.csv",
        "localidades": "localidades.csv",
        "provincias": "provincias.csv",
        "productos": "productos.csv",
        "clientes_mail": "clientes_mail.csv",
        "clientes_tel": "clientes_tel.csv",
        "rubros": "rubros.csv",
        "sucursales": "sucursales.csv",
        "facturaenc": "facturas_enc.csv",
        "facturadet": "facturas_det.csv",
        "ventas": "ventas.csv",
    }

    for key, fname in mapping.items():
        if key in tablas:
            pd.DataFrame(tablas[key]).to_csv(os.path.join(CARPETA, fname), index=False)

    print(" Archivos CSV actualizados correctamente.\n")


def exportar_tabla_json(tabla, nombre):
    """Exporta una tabla (lista de dicts) a un archivo JSON en la carpeta CARPETA."""
    import json
    ruta = os.path.join(CARPETA, f"{nombre}.json")
    try:
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(tabla, f, ensure_ascii=False, indent=2)
        print(f" Tabla '{nombre}' exportada a {ruta}")
    except Exception as e:
        print(" Error exportando a JSON:", e)


def guardar_todo_json(tablas):
    """Guarda todas las tablas en archivos JSON en CARPETA."""
    print("\n Guardando todos los cambios (JSON)...")
    for nombre, tabla in tablas.items():
        exportar_tabla_json(tabla, nombre)
    print(" Archivos JSON actualizados correctamente.\n")


# Mostrar tabla con IDs 
def mostrar_tabla(tabla, nombre):
    if not tabla:
        print(f"\n--- {nombre.upper()} ---")
        print("No hay registros en esta tabla.")
        return

    # Obtener todas las claves del primer registro
    campos = list(tabla[0].keys())
    
    # Calcular el ancho máximo para cada columna
    anchos = {campo: len(str(campo)) for campo in campos}
    for registro in tabla:
        for campo in campos:
            anchos[campo] = max(anchos[campo], len(str(registro.get(campo, ''))))

    # Imprimir encabezado
    print(f"\n--- {nombre.upper()} ---")
    print("ID  " + " | ".join(f"{campo:<{anchos[campo]}}" for campo in campos))
    print("-" * (4 + sum(anchos.values()) + (len(campos) - 1) * 3))

    # Imprimir registros
    for i, registro in enumerate(tabla):
        valores = []
        for campo in campos:
            valor = str(registro.get(campo, ''))
            if valor.lower() == 'nan':
                valor = '-'
            valores.append(f"{valor:<{anchos[campo]}}")
        print(f"{i:2d}  " + " | ".join(valores))


# Menú de selección 
def menu():
    tablas = cargar_tablas()

    while True:
        nombres = list(tablas.keys())
        print("\n Tablas disponibles:")
        for i, nombre in enumerate(nombres, start=1):
            print(f"{i}. {nombre}")

        # Opciones globales
        print(f"{len(nombres) + 1}. Guardar todo (CSV)")
        print(f"{len(nombres) + 2}. Guardar todo (JSON)")
        print(f"{len(nombres) + 3}. Salir")

        try:
            opcion = int(input("\nElige una tabla por número: "))
        except ValueError:
            print(" Opción inválida.")
            continue

        # Manejar opciones globales
        if opcion == len(nombres) + 1:
            guardar_todo(tablas)
            continue

        if opcion == len(nombres) + 2:
            guardar_todo_json(tablas)
            continue

        if opcion == len(nombres) + 3:
            print(" Saliendo del programa.")
            break

        if opcion < 1 or opcion > len(nombres):
            print(" Número fuera de rango.")
            continue

        nombre_tabla = nombres[opcion - 1]
        tabla = tablas[nombre_tabla]
        mostrar_tabla(tabla, nombre_tabla)

        # Submenú por tabla
        while True:
            accion = input("\n(A)gregar / (M)odificar / (B)orrar / (E)xportar / (V)olver: ").strip().lower()

            if accion == "v":
                break

            elif accion == "a":
                # Agregar: no pedir campos identificadores (id)
                nuevo = {}
                campos = list(tabla[0].keys()) if tabla else []
                for campo in campos:
                    if is_id_field(campo):
                        # Generar id automáticamente si es posible
                        nuevo[campo] = generate_new_id(tabla, campo)
                    else:
                        nuevo[campo] = input(f"Ingrese {campo}: ")
                tabla.append(nuevo)
                print(" Registro agregado con ID", len(tabla) - 1)
                mostrar_tabla(tabla, nombre_tabla)

                # Preguntar si se desea guardar la tabla en CSV/JSON/both inmediatamente
                guardar_choice = input("Guardar cambios para esta tabla ahora? (C)SV / (J)SON / (B)oth / (N)o: ").strip().lower()
                if guardar_choice == 'c':
                    pd.DataFrame(tabla).to_csv(os.path.join(CARPETA, f"{nombre_tabla}.csv"), index=False)
                    print(" Guardado CSV de la tabla.")
                elif guardar_choice == 'j':
                    exportar_tabla_json(tabla, nombre_tabla)
                elif guardar_choice == 'b':
                    pd.DataFrame(tabla).to_csv(os.path.join(CARPETA, f"{nombre_tabla}.csv"), index=False)
                    exportar_tabla_json(tabla, nombre_tabla)

            elif accion == "m":
                try:
                    idx = int(input("Ingrese el ID del registro a modificar: "))
                except ValueError:
                    print(" Ingrese un número válido.")
                    continue

                if 0 <= idx < len(tabla):
                    campos_mod = get_modifiable_fields(tabla[idx])
                    if not campos_mod:
                        print(" No hay campos modificables en este registro.")
                        continue

                    print("Campos modificables:")
                    for i_c, campo in enumerate(campos_mod, start=1):
                        print(f"{i_c}. {campo} ({tabla[idx].get(campo)})")
                    print("T. Modificar todos los campos anteriores")
                    elec = input("Elija el número del campo a modificar (o 'T'): ").strip().lower()
                    if elec == 't':
                        for campo in campos_mod:
                            valor = input(f"{campo} ({tabla[idx].get(campo)}): ")
                            if valor:
                                tabla[idx][campo] = valor
                    else:
                        try:
                            sel = int(elec) - 1
                        except ValueError:
                            print(" Ingrese un número válido o 'T'.")
                            continue
                        if 0 <= sel < len(campos_mod):
                            campo = campos_mod[sel]
                            valor = input(f"{campo} ({tabla[idx].get(campo)}): ")
                            if valor:
                                tabla[idx][campo] = valor
                        else:
                            print(" Número de campo inválido.")

                    print(" Registro modificado.")
                    mostrar_tabla(tabla, nombre_tabla)

                    # Opciones de guardado al modificar
                    guardar_choice = input("Guardar cambios para esta tabla ahora? (C)SV / (J)SON / (B)oth / (N)o: ").strip().lower()
                    if guardar_choice == 'c':
                        pd.DataFrame(tabla).to_csv(os.path.join(CARPETA, f"{nombre_tabla}.csv"), index=False)
                        print(" Guardado CSV de la tabla.")
                    elif guardar_choice == 'j':
                        exportar_tabla_json(tabla, nombre_tabla)
                    elif guardar_choice == 'b':
                        pd.DataFrame(tabla).to_csv(os.path.join(CARPETA, f"{nombre_tabla}.csv"), index=False)
                        exportar_tabla_json(tabla, nombre_tabla)

                else:
                    print(" ID fuera de rango.")

            elif accion == "b":
                try:
                    idx = int(input("Ingrese el ID del registro a borrar (dejar vacío): "))
                except ValueError:
                    print(" Ingrese un número válido.")
                    continue

                if 0 <= idx < len(tabla):
                    # No borrar/alterar campos id: vaciar solo campos modificables
                    campos_no_id = get_modifiable_fields(tabla[idx])
                    for campo in campos_no_id:
                        tabla[idx][campo] = ""
                    print(f" Registro ID {idx} vaciado (campos no id).")
                    mostrar_tabla(tabla, nombre_tabla)

                    # Preguntar guardar tras borrar/vaciar campos
                    guardar_choice = input("Guardar cambios para esta tabla ahora? (C)SV / (J)SON / (B)oth / (N)o: ").strip().lower()
                    if guardar_choice == 'c':
                        pd.DataFrame(tabla).to_csv(os.path.join(CARPETA, f"{nombre_tabla}.csv"), index=False)
                        print(" Guardado CSV de la tabla.")
                    elif guardar_choice == 'j':
                        exportar_tabla_json(tabla, nombre_tabla)
                    elif guardar_choice == 'b':
                        pd.DataFrame(tabla).to_csv(os.path.join(CARPETA, f"{nombre_tabla}.csv"), index=False)
                        exportar_tabla_json(tabla, nombre_tabla)
                else:
                    print(" ID fuera de rango.")

            elif accion == "e":
                # Exportar tabla a JSON
                exportar_tabla_json(tabla, nombre_tabla)
                print(" Exportación completada.")

            else:
                print("Acción no válida.")


if __name__ == "__main__":
    menu()
