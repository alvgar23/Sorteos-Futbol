# Sorteos de fútbol

Colección de programas Python para realizar sorteos de fútbol y experimentar con la creación de calendarios de liga. El repositorio conserva distintas etapas del proyecto, sin reescribir los programas originales.

## Contenido

| Carpeta | Archivo | Qué hace |
| --- | --- | --- |
| `sorteos/2020/` | `sorteo_futbol_automatico_v1.py` | Versión de consola para sortear eliminatorias o grupos de cuatro a partir de un archivo de equipos y bombos. |
| `sorteos/2025/` | `sorteo_futbol_automatico_v2.py` | Aplicación gráfica con Tkinter: carga equipos, sortea grupos o eliminatorias y exporta resultados a CSV. |
| `liga/2020/` | `sorteo_liga.py` | Primer intento de generar un calendario de liga a una vuelta, sin repetir enfrentamientos. |
| `liga/2020/` | `sorteo_liga_f.py` | Reorganización del generador de liga en funciones; conserva problemas de ejecución y de lógica. |
| `datos/` | `datos_equipos.txt`, `datos_equipos - grupo.txt` | Ejemplos de equipos, países y bombos. |

Las fechas se toman de las cabeceras de los scripts: noviembre-diciembre de 2020 y noviembre de 2025. No implican que todas las versiones funcionen correctamente.

## Sorteos: dos etapas

### Versión de consola (2020)

`sorteos/2020/sorteo_futbol_automatico_v1.py` pregunta cuántos equipos debe contener cada bombo y si el sorteo será de eliminatorias (`e`) o grupos (`g`). Extrae equipos aleatoriamente y muestra el resultado en la terminal. El código presupone repartos adecuados de equipos y no comprueba restricciones de país.

**Importante:** el script lee `datos_equipos.txt` desde el directorio de ejecución y trata **cada línea completa** como un equipo. Por tanto, el archivo de ejemplo actual, que contiene `Equipo,País,Bombo`, no se interpreta por columnas en esta versión.

### Versión gráfica (2025)

`sorteos/2025/sorteo_futbol_automatico_v2.py` abre una ventana con tres acciones: cargar un `.txt`, realizar el sorteo y exportar a CSV. Permite seleccionar **Groups** o **Eliminations**.

Formato de entrada (una línea por equipo):

```text
Real Madrid,Spain,1
Chelsea,England,1
Atlético de Madrid,Spain,2
Villarreal,Spain,2
```

- **Grupos:** distribuye equipos por bombos y procura evitar que coincidan países, pero **no garantiza** que se cumplan todas las restricciones. Si los bombos tienen distinto tamaño, coloca los sobrantes después.
- **Eliminatorias:** enfrenta equipos del bombo 1 con equipos de los demás bombos, intentando evitar coincidencias de país. Si no encuentra rival compatible, permite el cruce. Con cantidades desiguales puede producir partidos incompletos o de más de dos equipos; no es un cuadro eliminatorio validado.
- **CSV:** guarda el último sorteo con las columnas `Group/Match`, `Team`, `Country` y `Pot`.

Utiliza únicamente módulos de la biblioteca estándar de Python (`tkinter`, `csv`, `random`). Necesita una instalación de Python con Tkinter y un entorno gráfico.

## Calendarios de liga (2020)

Los dos scripts de `liga/2020/` intentan construir jornadas de una liga a una vuelta, con cada equipo jugando como máximo una vez por jornada y sin repetir enfrentamientos.

**Estado real:** son prototipos inacabados. `sorteo_liga.py` reconoce en sus propios comentarios que no consigue evitar repeticiones y que modifica jornadas anteriores. `sorteo_liga_f.py` divide el trabajo en funciones, pero incluye llamadas con argumentos inconsistentes y otras condiciones problemáticas. **No deben considerarse generadores de calendarios funcionales.**

Ambos esperan encontrar `datos_equipos.txt` en el directorio desde el que se ejecuten. Los ejemplos actuales contienen nueve equipos, mientras que el planteamiento de jornadas y partidos está pensado principalmente para cantidades pares; esto añade otra limitación para probarlos.

## Cómo probar los programas

1. Instala Python 3. Para la versión gráfica, comprueba que Tkinter esté disponible.
2. Desde la raíz del repositorio, abre una terminal.
3. Ejecuta la versión gráfica con `python sorteos/2025/sorteo_futbol_automatico_v2.py`.
4. En la ventana, carga uno de los archivos de `datos/`, elige el modo y realiza el sorteo.

Para probar los programas de 2020, ten presente que buscan `datos_equipos.txt` en el directorio de trabajo: hay que copiar o preparar allí un archivo compatible con el formato esperado. Los scripts de liga pueden fallar o no finalizar correctamente.

## Conservación del proyecto

Esta organización separa **sorteos**, **calendarios de liga** y **datos de ejemplo**, manteniendo las dos versiones históricas del sorteo y ambos intentos de calendario. No se han corregido algoritmos, cambiado nombres internos ni añadido funcionalidades: el objetivo es documentar lo que existe y dejar claras sus limitaciones.
