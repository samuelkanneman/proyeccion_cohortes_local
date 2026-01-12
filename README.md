# Proyección de Mora - Chain Ladder (PyScript)

🔒 **Procesamiento 100% Local** - Tus datos nunca salen de tu navegador

Aplicación web para proyectar mora futura de cohortes usando metodología Chain Ladder. Construida con PyScript para ejecutar Python directamente en el navegador.

## 🌟 Características

- **Seguridad total**: Los datos se procesan localmente en el navegador
- **Sin instalación**: Solo necesitas un navegador web moderno
- **Interfaz intuitiva**: Carga CSV, selecciona parámetros y visualiza
- **Visualizaciones interactivas**: Gráficos con Plotly.js
- **Exportación**: Descarga resultados en CSV

## 🚀 Despliegue en GitHub Pages

### Opción 1: Desde tu repositorio existente

1. **Clonar o crear repositorio:**
   ```bash
   # Si es nuevo
   mkdir proyeccion-mora
   cd proyeccion-mora
   git init
   
   # Si ya existe
   cd tu-repo-existente
   ```

2. **Copiar archivos:**
   ```bash
   # Copiar todos los archivos de esta carpeta:
   # - index.html
   # - style.css
   # - app.py
   # - script.js
   # - pyscript.toml
   # - README.md
   # - .gitignore
   ```

3. **Subir a GitHub:**
   ```bash
   git add .
   git commit -m "Add proyeccion mora app"
   git push origin main
   ```

4. **Activar GitHub Pages:**
   - Ve a tu repositorio en GitHub
   - Settings → Pages
   - Source: Deploy from a branch
   - Branch: `main` → carpeta: `/ (root)`
   - Click "Save"

5. **Acceder a tu app:**
   - URL: `https://tu-usuario.github.io/nombre-repo/`
   - Espera 1-2 minutos para el primer despliegue

### Opción 2: Fork rápido

1. Haz fork de este repositorio
2. Activa GitHub Pages en Settings
3. ¡Listo! Tu app estará en `https://tu-usuario.github.io/proyeccion-mora/`

## 📂 Estructura de Archivos

```
proyeccion-mora/
├── index.html          # Página principal
├── style.css          # Estilos
├── app.py             # Lógica Python (PyScript)
├── script.js          # JavaScript para UI
├── pyscript.toml      # Configuración PyScript
├── README.md          # Este archivo
└── .gitignore         # Archivos a ignorar en Git
```

## 📊 Uso

### 1. Preparar CSV

Tu archivo debe tener este formato:

```csv
;2023-01;2023-02;2023-03;2023-04
2023-01;5,2%;8,1%;10,5%;12,3%
2023-02;;6,3%;9,2%;11,5%
2023-03;;;7,1%;10,2%
```

**Requisitos:**
- Separador: punto y coma (`;`)
- Primera columna: cohortes (YYYY-MM)
- Primera fila: períodos (YYYY-MM)
- Valores: mora >90d en % (acepta `5,2%` o `5.2%`)

### 2. Usar la Aplicación

1. **Cargar CSV**: Click en "Seleccionar archivo CSV"
2. **Configurar**: 
   - Selecciona cohorte a proyectar
   - Desliza para definir MOB objetivo
3. **Proyectar**: Click en "🚀 Proyectar"
4. **Explorar**: 
   - Visualizaciones interactivas
   - Tabla detallada con intervalos
   - Factores de desarrollo
5. **Exportar**: Descarga resultados en CSV

## 🔒 Seguridad y Privacidad

### ¿Los datos van a algún servidor?

**NO.** Cuando usas esta aplicación:

1. El código HTML/JS se descarga de GitHub Pages (solo código)
2. PyScript se ejecuta **en tu navegador**
3. Cargas el CSV **desde tu computadora**
4. Todo el procesamiento ocurre **localmente**
5. Los datos **NUNCA se envían** a ningún servidor

### Ventajas vs Streamlit Cloud

| Aspecto | Esta App (PyScript) | Streamlit Cloud |
|---------|---------------------|-----------------|
| Código en GitHub | ✅ Sí | ✅ Sí |
| Datos en la nube | ❌ No | ⚠️ Sí |
| Procesamiento | 🖥️ Tu navegador | ☁️ Servidor cloud |
| Privacidad | ✅ Total | ⚠️ Limitada |

### ¿Es seguro para datos sensibles?

**SÍ.** Es como usar Excel o una calculadora en tu PC:
- El software (app) es público
- Los datos (CSV) son privados y locales
- Perfecto para datos confidenciales de crédito

## 🛠️ Desarrollo Local

Si quieres probar localmente antes de subir a GitHub:

```bash
# Opción 1: Python HTTP Server
python -m http.server 8000

# Opción 2: Node.js HTTP Server
npx http-server

# Luego abre: http://localhost:8000
```

## 📦 Tecnologías

- **PyScript 2024.1.1**: Python en el navegador
- **Plotly.js 2.27.0**: Visualizaciones interactivas
- **Pandas + NumPy**: Procesamiento de datos
- **HTML5 + CSS3**: Interfaz moderna

## 🔄 Actualizaciones

Para actualizar la app después del primer despliegue:

```bash
# Modifica archivos localmente
git add .
git commit -m "Update: descripción cambios"
git push origin main

# GitHub Pages se actualiza automáticamente en 1-2 min
```

## 🐛 Troubleshooting

### La app no carga

- **Verifica URL**: Debe ser `https://usuario.github.io/repo/`
- **Espera**: Primer despliegue toma 2-3 minutos
- **Force refresh**: Ctrl+F5 (o Cmd+Shift+R en Mac)

### Error al cargar CSV

- **Encoding**: Asegúrate que sea UTF-8
- **Separador**: Debe ser punto y coma (`;`)
- **Formato fechas**: YYYY-MM exacto

### PyScript no inicia

- **Abre consola**: F12 → Console tab
- **Verifica errores**: Revisa mensajes en rojo
- **Conexión internet**: PyScript descarga paquetes al inicio

### Procesamiento lento

- **Primera carga**: PyScript descarga pandas (~10-15 seg)
- **Archivos grandes**: CSV >1000 filas puede tardar
- **Navegador**: Chrome/Firefox funcionan mejor

## 📝 Metodología

La aplicación usa **Chain Ladder** para proyectar:

1. **Calcula factores**: Analiza cómo evolucionó la mora entre MOBs en cohortes históricas
2. **Promedia**: Obtiene factores promedio con desviación estándar
3. **Proyecta**: Aplica factores a la cohorte objetivo

**Ejemplo**: 
- Históricamente mora pasó de 10% (MOB 5) a 13% (MOB 6) → Factor 1.3
- Se aplica: Si cohorte actual tiene 12% en MOB 5 → Proyección MOB 6 = 15.6%

## 📞 Soporte

Para issues o preguntas:
1. Abre un issue en GitHub
2. Incluye: navegador, mensaje de error, CSV de ejemplo (sin datos sensibles)

## 📄 Licencia

Este proyecto es de uso interno para CONMEGA ACE - Credit Management Department.

---

**Desarrollado por:** Kanneman, Samuel 
**Versión:** 1.0.0  
**Última actualización:** Enero 2026  
**Contacto:** Samuel - Data Scientist Credit Specialist
