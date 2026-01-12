# 🚀 Guía Rápida: Desplegar en GitHub Pages

Esta guía te llevará paso a paso para tener tu app funcionando en menos de 5 minutos.

## ✅ Requisitos previos

- Cuenta de GitHub (gratis)
- Git instalado en tu PC
- Los archivos de este proyecto

## 📝 Pasos

### 1. Crear repositorio en GitHub

1. Ve a https://github.com/new
2. Nombre del repositorio: `proyeccion-mora` (o el que prefieras)
3. Descripción: "App para proyección de mora con Chain Ladder"
4. Visibilidad: **Público** o **Privado** (ambos funcionan con Pages)
5. ❌ NO marques "Add a README file"
6. Click en "Create repository"

### 2. Subir archivos

**Opción A: Desde tu computadora (recomendado)**

```bash
# 1. Abre terminal en la carpeta donde tienes los archivos
cd ruta/a/la/carpeta

# 2. Inicializa Git
git init

# 3. Agrega todos los archivos
git add .

# 4. Haz el primer commit
git commit -m "Initial commit: PyScript mora projection app"

# 5. Conecta con tu repo de GitHub (reemplaza TU-USUARIO y proyeccion-mora)
git remote add origin https://github.com/TU-USUARIO/proyeccion-mora.git

# 6. Sube los archivos
git branch -M main
git push -u origin main
```

**Opción B: Directamente en GitHub (más simple)**

1. En tu nuevo repositorio, click "uploading an existing file"
2. Arrastra todos los archivos:
   - index.html
   - style.css
   - app.py
   - script.js
   - pyscript.toml
   - README.md
   - ejemplo.csv
   - .gitignore
3. Scroll down y click "Commit changes"

### 3. Activar GitHub Pages

1. En tu repositorio, ve a **Settings** (⚙️)
2. En el menú izquierdo, click en **Pages**
3. En "Source", selecciona:
   - Branch: `main`
   - Folder: `/ (root)`
4. Click **Save**
5. Espera 1-2 minutos

### 4. ¡Acceder a tu app!

Tu app estará disponible en:

```
https://TU-USUARIO.github.io/proyeccion-mora/
```

Reemplaza:
- `TU-USUARIO` con tu nombre de usuario de GitHub
- `proyeccion-mora` con el nombre de tu repositorio

## 🎉 ¡Listo!

Ahora puedes:
1. Compartir la URL con tu equipo
2. Cargar CSV y proyectar cohortes
3. Todo el procesamiento será local (seguro)

## 🔄 Actualizar la app

Si modificas archivos localmente:

```bash
git add .
git commit -m "Update: descripción de cambios"
git push origin main
```

GitHub Pages se actualiza automáticamente en 1-2 minutos.

## 📱 Compartir con el equipo

Simplemente comparte la URL:
```
https://TU-USUARIO.github.io/proyeccion-mora/
```

**Ventajas:**
- ✅ No necesitan instalar nada
- ✅ Funciona en cualquier navegador
- ✅ Sus datos nunca se comparten
- ✅ Siempre tendrán la última versión

## ❓ Problemas comunes

### "404 - There isn't a GitHub Pages site here"

**Solución:** Espera 2-3 minutos más. El primer despliegue tarda.

### "PyScript is loading..."

**Solución:** Primera carga toma 10-15 segundos (descarga pandas). Espera o refresca (F5).

### Los cambios no se ven

**Solución:** Haz "hard refresh":
- Windows: `Ctrl + F5`
- Mac: `Cmd + Shift + R`

### Error al subir archivos por terminal

**Solución:** Verifica que Git esté instalado:
```bash
git --version
```

Si no está instalado, descarga desde https://git-scm.com/

## 🔐 Seguridad

### ¿Es seguro hacer el repo público?

**SÍ.** Solo estás compartiendo el **código** de la app, NO tus datos:
- ✅ El código es público (como Excel o una calculadora)
- ✅ Los datos CSV quedan en cada usuario
- ✅ NUNCA subas CSVs con datos reales al repo

### ¿Alguien puede ver mis proyecciones?

**NO.** Cuando alguien usa tu app:
1. Descarga el código (HTML/JS/Python)
2. Carga SU propio CSV en SU navegador
3. Todo se procesa localmente
4. Nadie más puede ver sus datos

## 📞 Ayuda

Si tienes problemas:
1. Revisa la consola del navegador (F12 → Console)
2. Verifica que todos los archivos estén subidos
3. Asegúrate que GitHub Pages esté activado en Settings

---

**¿Preguntas?** Abre un issue en el repositorio.
