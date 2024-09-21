import os

def cargar_datos_transacciones():
    ruta_archivo = os.path.join(os.path.dirname(__file__), 'datos.dat')

    if not os.path.exists(ruta_archivo):
        print(f"Error: El archivo no está en la ruta: {ruta_archivo}")
        return []

    with open(ruta_archivo, "r") as archivo:
        lineas = archivo.readlines()

    lista_transacciones = []

    for linea in lineas:
        linea = linea.strip()
        if len(linea) < 55:
            continue

        fecha_venta = linea[:10].strip()
        nombre_producto = linea[10:40].strip()
        precio_unitario = float(linea[40:50].strip())

        try:
            cantidad_vendida = int(linea[50:55].strip())
        except ValueError:
            print(f"Error al convertir la cantidad en la línea: {linea}")
            continue

        transaccion = {
            "Fecha": fecha_venta,
            "Producto": nombre_producto,
            "Precio": precio_unitario,
            "Cantidad": cantidad_vendida
        }
        lista_transacciones.append(transaccion)

    return lista_transacciones

def mostrar_transacciones(transacciones):
    for transaccion in transacciones:
        print("Fecha:", transaccion['Fecha'])
        print("Producto:", transaccion['Producto'])
        print("Precio:", transaccion['Precio'])
        print("Cantidad:", transaccion['Cantidad'])
        print("-" * 40)

def calcular_total_transacciones(transacciones):
    total_importe = 0
    total_cantidades = 0
    for registro in transacciones:
        total_importe += registro['Precio'] * registro['Cantidad']
        total_cantidades += registro['Cantidad']
    return total_importe, total_cantidades

def contar_unidades_por_producto(transacciones):
    unidades_por_producto = {}
    for registro in transacciones:
        nombre_producto = registro['Producto']
        cantidad = registro['Cantidad']
        if nombre_producto in unidades_por_producto:
            unidades_por_producto[nombre_producto] += cantidad
        else:
            unidades_por_producto[nombre_producto] = cantidad
    return unidades_por_producto

def listar_unidades_vendidas_por_producto(unidades_totales):
    for producto, total in unidades_totales.items():
        print(f"Producto: {producto}, Unidades Vendidas: {total}")

def calcular_precio_promedio(transacciones):
    total_precio = {}
    total_cantidades = {}

    for registro in transacciones:
        nombre_producto = registro['Producto']
        precio = registro['Precio']
        cantidad = registro['Cantidad']

        if nombre_producto in total_precio:
            total_precio[nombre_producto] += precio * cantidad
            total_cantidades[nombre_producto] += cantidad
        else:
            total_precio[nombre_producto] = precio * cantidad
            total_cantidades[nombre_producto] = cantidad

    def mostrar_precios(promedios):
        for producto in promedios:
            promedio = promedios[producto] / total_cantidades[producto]
            print(f"Producto: {producto}, Precio Promedio: ${promedio:.2f}")

    mostrar_precios(total_precio)

def agrupar_ventas_por_mes(transacciones):
    resumen_mensual = {}
    for registro in transacciones:
        nombre_producto = registro['Producto']
        fecha = registro['Fecha']
        mes = fecha[5:7] + '-' + fecha[:4]
        cantidad = registro['Cantidad']

        if nombre_producto not in resumen_mensual:
            resumen_mensual[nombre_producto] = {}

        if mes in resumen_mensual[nombre_producto]:
            resumen_mensual[nombre_producto][mes] += cantidad
        else:
            resumen_mensual[nombre_producto][mes] = cantidad

    return resumen_mensual

def listar_resumen_mensual(resumen):
    for producto, meses in resumen.items():
        for mes, total in meses.items():
            print(f"Producto: {producto}, Mes: {mes}, Unidades Vendidas: {total}")

def generar_resumen_total(transacciones):
    total_cantidades = {}
    total_importes = {}

    for registro in transacciones:
        nombre_producto = registro['Producto']
        precio = registro['Precio']
        cantidad = registro['Cantidad']

        if nombre_producto in total_cantidades:
            total_cantidades[nombre_producto] += cantidad
            total_importes[nombre_producto] += precio * cantidad
        else:
            total_cantidades[nombre_producto] = cantidad
            total_importes[nombre_producto] = precio * cantidad

    for producto in total_cantidades:
        promedio = total_importes[producto] / total_cantidades[producto]
        print(f"-> Producto: {producto}, Precio Promedio: ${promedio:.2f}, Unidades Vendidas: {total_cantidades[producto]}, Importe Total: ${total_importes[producto]:.2f}")

# Ejecución principal
datos_transacciones = cargar_datos_transacciones()

if datos_transacciones:
    mostrar_transacciones(datos_transacciones)

    importe_total, cantidad_total = calcular_total_transacciones(datos_transacciones)
    print(f"Las transacciones totalizaron ${importe_total:.2f} en {cantidad_total} unidades")

    unidades_vendidas_totales = contar_unidades_por_producto(datos_transacciones)
    listar_unidades_vendidas_por_producto(unidades_vendidas_totales)

    calcular_precio_promedio(datos_transacciones)

    ventas_por_mensualidades = agrupar_ventas_por_mes(datos_transacciones)
    listar_resumen_mensual(ventas_por_mensualidades)

    generar_resumen_total(datos_transacciones)
