## 🎬 YouTube Downloader Local

**Descarga videos de YouTube usando tu propia conexión y potencia**

---

## ✨ Características

| Funcionalidad | Descripción |
|---------------|-------------|
| 🚀 **Descarga Directa** | Sin intermediarios, aprovecha el 100% de tu ancho de banda. |
| 🎯 **Múltiples Formatos** | Selector dinámico de calidad y resolución disponible. |
| 🔊 **Audio + Video** | Fusión automática de pistas mediante FFmpeg. |
| 💻 **100% Local** | Privacidad garantizada: todo se procesa en tu máquina. |

---

## 🔧 Prerrequisitos

- **Python 3.8 o superior**
- **FFmpeg** instalado y configurado en el sistema.

> **Nota:** Puedes descargar FFmpeg desde [ffmpeg.org](https://ffmpeg.org).

---

## 📥 Instalación

### 1. Clonar el repositorio:

```bash
git clone https://github.com/tuusuario/youtube-downloader-local.git
cd youtube-downloader-local
```

### 2. Instalar dependencias:

```bash
pip install flask yt-dlp
```

### 3. Configurar rutas:

> **IMPORTANTE:** Edita el archivo `app.py` (líneas 15 y 56) para actualizar la variable `ffmpeg_location` con la ruta de tu ejecutable.

---

## 🚀 Uso

Sigue estos pasos para poner en marcha tu descargador:

### 1. Lanzar el servidor:

```bash
python app.py
```

### 2. Acceder a la interfaz:

Abre tu navegador en `http://localhost:5000`

### 3. Proceso de descarga:

- Pega la URL de YouTube.
- Haz clic en **"Obtener formatos"**.
- Selecciona la calidad deseada.
- Presiona **"Descargar"**.

> **Info:** Todos los archivos finalizados se almacenarán automáticamente en la carpeta `/downloads`.

---

## 📁 Estructura del Proyecto

```
youtube-downloader-local/
├── app.py              # Backend Flask & Lógica de yt-dlp
├── index.html          # Interfaz de usuario (Frontend)
└── downloads/          # Directorio de salida de archivos
```

---

## 🐛 Troubleshooting

### ❌ Error: "FFmpeg not found"

Asegúrate de que la ruta en `app.py` apunte al archivo `ffmpeg.exe` (en Windows) o que esté en tu PATH global. Prueba ejecutando `ffmpeg -version` en tu terminal para confirmar que el sistema lo reconoce.

### 📦 Error: Módulo no encontrado

Asegúrate de haber instalado los requerimientos ejecutando: `pip install flask yt-dlp`. Si usas entornos virtuales, verifica que esté activado.

### 🛑 El video no se descarga

- Verifica que el video no tenga restricciones de edad o sea privado.
- Mantén la herramienta actualizada: `pip install -U yt-dlp`.

---

## ⚠️ Disclaimer

> **ADVERTENCIA:** Este proyecto tiene fines exclusivamente personales y educativos. El usuario es responsable de cumplir con los Términos de Servicio de YouTube y las leyes de derechos de autor vigentes en su país.

---

**Hecho con ❤️ usando Python, Flask y yt-dlp**

**¿Te sirvió el proyecto? ¡No olvides dejar una ⭐!**
