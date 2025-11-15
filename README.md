# 📘 README – Sistema de Control Difuso para Ventilador (Flask + scikit-fuzzy)

## 🧩 1. Descripción General
Este proyecto implementa un **sistema de control difuso** para determinar la **velocidad de un ventilador** a partir de dos entradas:

- **Temperatura (°C)**
- **Humedad (%)**

El sistema aplica lógica difusa para generar una salida entre **0 y 100 %**, mostrando el resultado en una **interfaz web desarrollada con Flask**.

---

## 📌 2. Especificación de Requisitos

### ✔ Requisitos Funcionales
1. La aplicación debe recibir valores de temperatura y humedad.
2. Debe ejecutar un sistema difuso que calcule la velocidad del ventilador.
3. Debe mostrar los resultados en una página web.
4. Debe permitir recalcular introduciendo nuevos valores.
5. La aplicación debe manejar errores y entradas inválidas.

### ✔ Requisitos No Funcionales
1. Debe ejecutarse localmente en un entorno virtual.
2. El sistema debe ser fácil de usar y modificar.
3. El código debe estar organizado siguiendo buenas prácticas de Flask.
4. La respuesta del sistema debe ser rápida (< 1 segundo).

---

## 🏛️ 3. Arquitectura de la Solución

La estructura propuesta del proyecto es:

```
/control_difuso
│── app.py                  # Lógica principal y rutas Flask
│── fuzzy_controller.py     # Control difuso con skfuzzy
│── requirements.txt        # Dependencias
│── /templates
│     └── index.html        # Interfaz web
│── /static
      └── style.css         # Estilos opcionales
```

### 🔄 Flujo del sistema
1. El usuario ingresa temperatura y humedad en la interfaz.
2. Flask envía esos datos al módulo `fuzzy_controller.py`.
3. El sistema difuso procesa las entradas y obtiene la velocidad.
4. Flask retorna el resultado en pantalla.

---

## 🧱 4. Descripción de Módulos

### **1. app.py**
- Inicializa Flask.
- Define la ruta principal `/`.
- Recibe datos del formulario.
- Llama al controlador difuso.
- Renderiza la página HTML con el resultado.

### **2. fuzzy_controller.py**
- Contiene:
  - Funciones de membresía
  - Reglas difusas
  - Motor de inferencia
  - Defuzzificación
- Retorna la velocidad del ventilador entre 0 y 100.

### **3. templates/index.html**
- Formulario para ingresar temperatura y humedad.
- Muestra el resultado del cálculo.

### **4. static/style.css (opcional)**
- Maneja estilos visuales.

---

## ⚠️ 5. Manejo de Excepciones

### ✔ Validación de datos
Evita valores vacíos o no numéricos.

```python
try:
    temperatura = float(request.form['temp'])
    humedad = float(request.form['hum'])
except ValueError:
    return render_template("index.html", error="Ingresa valores numéricos válidos.")
```

### ✔ Errores HTTP personalizados

```python
@app.errorhandler(404)
def error_404(e):
    return "Página no encontrada", 404

@app.errorhandler(500)
def error_500(e):
    return "Error interno del servidor", 500
```

### ✔ Errores en el sistema difuso

```python
try:
    velocidad = calcular_velocidad(temperatura, humedad)
except Exception as e:
    return render_template("index.html", error="Ocurrió un error en el controlador difuso.")
```

---



## Ejemplo de Uso

### Valores de Entrada
- **Temperatura:** 28°C  
- **Humedad:** 45%

### Resultado
El sistema calcula la velocidad como salida y genera gráficos que representan las funciones de membresía y el proceso de defuzzificación.

#### Gráficos Generados

1. **Funciones de Membresía - Temperatura**
   ![Funciones de Membresía - Temperatura](static/mf_temp_TIMESTAMP.png)

2. **Funciones de Membresía - Humedad**
   ![Funciones de Membresía - Humedad](static/mf_hum_TIMESTAMP.png)

3. **Funciones de Membresía - Velocidad**
   ![Funciones de Membresía - Velocidad](static/mf_vel_TIMESTAMP.png)

4. **Salida - Velocidad (Defuzzificación)**
   ![Salida - Velocidad](static/output_TIMESTAMP.png)

## ▶️ 6. Guía de Ejecución

### **1. Crear entorno virtual**
```bash
python -m venv venv
```

### **2. Activar entorno virtual**
**Windows**
```bash
venv\Scripts\activate
```

**Linux / Mac**
```bash
source venv/bin/activate
```

### **3. Instalar dependencias**
```bash
pip install -r requirements.txt
```

O manual:

```bash
pip install flask scikit-fuzzy numpy
```

### **4. Ejecutar la aplicación**
```bash
python app.py
```

### **5. Abrir en navegador**
```
http://127.0.0.1:5000
```

---

## 📄 7. Notas Finales
- La lógica difusa puede ampliarse con más reglas.
- Flask permite escalar el proyecto fácilmente.
- Para producción, no usar `debug=True`.

