# Evaluación Habilidad Transversal

Este proyecto permite crear un formulario interactivo en Google Sheets utilizando Google Apps Script. Los usuarios podrán seleccionar un curso, completar una evaluación y guardar sus respuestas.

## Requisitos Previos

- Una cuenta de Google.
- Una hoja de cálculo (Google Sheet) creada en Google Drive.

## Pasos para Implementar el Script

### 1. Configuración Inicial

1. Abre Google Sheets.
2. Ve a **Extensiones > Apps Script**.

### 2. Agregar el Código del Proyecto

1. En la interfaz de Apps Script, borra cualquier código existente en `Code.gs`.
2. Crea los siguientes archivos y copia el contenido correspondiente:

   - **`Code.gs`**: Contiene la lógica principal del servidor.
   - **`forms.html`**: Contiene el diseño y la lógica del formulario interactivo.

### 3. Configurar la Hoja de Cálculo

La hoja principal debe tener las siguientes columnas en la primera fila (no es necesario que estén en orden):

```
Curso, LLAVE, SECCIONES, HabilidadesTransversales, SignificadoHT, Implementacion, QuienEvalua
```

- Llena los datos correspondientes a los cursos en las filas siguientes.

### 6. Implementar el Proyecto

1. En Apps Script, ve a **Implementar > Nueva implementación**.
2. Selecciona **Aplicación web**.
3. Configura:
   - **Descripción**: Ingresa un nombre para identificar el proyecto.
   - **Quién tiene acceso**: Cambia a "Cualquiera con el enlace".
4. Haz clic en **Implementar**.
5. Copia la URL proporcionada.

### 7. Uso del Formulario

- Comparte la URL con los usuarios o insértala en un sitio web.
- Los usuarios podrán interactuar con el formulario, seleccionar un curso y guardar sus respuestas.

## Soporte

Si tienes alguna pregunta o problema, abre un issue o contacta al administrador.