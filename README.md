¡Claro que sí! Aquí tienes un **README.md** ideal para tu repositorio. Este archivo explica cómo configurar, ejecutar y usar tu bot de Telegram para recordatorios. 🚀

---

## **Telegram Reminder Bot**

¡Bienvenido a **Telegram Reminder Bot**! 🤖  
Este es un bot de Telegram que utiliza inteligencia artificial (OpenAI) para analizar recordatorios en lenguaje natural y programarlos automáticamente. 🎉 Soporta tanto tareas únicas como recurrentes, ajustándose a las zonas horarias y asignando emojis contextuales a cada notificación.

---

### **Características principales** ✨
- Integra **OpenAI** (GPT) para interpretar recordatorios en lenguaje natural.
- Soporta **tareas recurrentes y únicas**.
- **Emojis automáticos** basados en el contenido del recordatorio.
- Detecta la zona horaria y configura el idioma relacionado durante la configuración inicial.
- Desplegable en **Docker**, compatible con **Portainer**.

---

### **Requisitos previos** 📋
1. Tener **Docker** y **Docker Compose** instalados en tu sistema.
2. Tener una cuenta de Telegram:
   - Crear un bot en Telegram usando [@BotFather](https://t.me/BotFather) para obtener el **Telegram Bot Token**.
3. Tener una cuenta en OpenAI:
   - Generar una **API Key** desde [OpenAI Platform](https://platform.openai.com/).

---

### **Instalación y configuración** 🔧

#### **1. Clonar el repositorio**
Clona este repositorio en tu máquina local o servidor donde usarás Docker:

```bash
git clone https://github.com/tu_usuario/telegram-reminder-bot.git
cd telegram-reminder-bot
```

#### **2. Configurar variables de entorno**
Crea un archivo llamado `.env` en el directorio raíz del proyecto y agrega las claves necesarias:

```plaintext
TELEGRAM_BOT_TOKEN=tu_token_de_telegram
OPENAI_API_KEY=tu_api_key_openai
```

Reemplaza:
- `tu_token_de_telegram` con el token generado por **BotFather**.
- `tu_api_key_openai` con tu clave de API de OpenAI.

#### **3. Construir y ejecutar el contenedor Docker**
Usa los siguientes comandos para construir y ejecutar el bot dentro de Docker:

```bash
docker-compose build
docker-compose up -d
```

¡Eso es todo! Tu bot estará ejecutándose en segundo plano. 🎉

#### **4. Verificar los logs (opcional)**
Si deseas ver los registros del bot para confirmar que todo funciona correctamente:

```bash
docker-compose logs -f
```

---

### **Uso del bot** 🤖

#### **1. Iniciar el bot**
Busca tu bot en Telegram, abre el chat y escribe `/start`. El bot te dará la bienvenida y te pedirá configurar la zona horaria.

#### **2. Configurar zona horaria e idioma**
Usa el comando `/set_timezone` para asignar tu zona horaria con tu ciudad y país (esto también configura el idioma automáticamente).

**Ejemplo:**
```
/set_timezone Buenos Aires Argentina
```

#### **3. Crear un recordatorio único**
Escribe un recordatorio en lenguaje natural, como:
```
Recuérdame enviar el mail a las 15:00 de mañana.
```
El bot lo interpretará y lo configurará automáticamente.

#### **4. Crear un recordatorio recurrente**
También puedes crear recordatorios repetitivos, como:
```
Todos los jueves a las 09:00, recuérdame ir al gimnasio.
```
El bot configurará el recordatorio para repetirse cada jueves a esa hora.

---

### **Ejemplos de interacción** 💬

❓ Usuario:
```
/start
```

🤖 Bot:
```
¡Hola! 👋 Bienvenido a tu bot de recordatorios inteligentes.
Configura tu zona horaria con:
`/set_timezone Ciudad País`
Por ejemplo:
`/set_timezone Madrid España`
```

---

❓ Usuario:
```
/set_timezone Buenos Aires Argentina
```

🤖 Bot:
```
✅ Zona horaria configurada correctamente: Buenos Aires Argentina 🌍.
🌐 Idioma detectado: Español.
```

---

❓ Usuario:
```
Recuérdame llamar al médico mañana a las 10:00.
```

🤖 Bot:
```
✅ Recordatorio único configurado para: 2023-10-17 10:00 ART.
```

---

❓ Usuario:
```
Todos los lunes a las 8:00 AM, recuérdame comprar flores para la oficina.
```

🤖 Bot:
```
✅ Recordatorio recurrente configurado: Todos los lunes a las 08:00.
```

---

### **Cómo detener el bot** 🛑
Si necesitas detener el bot por alguna razón, usa el siguiente comando:

```bash
docker-compose down
```

---

### **Personalización futura** 🛠️

Algunas ideas para extender y personalizar este bot:
- Soporte para idiomas adicionales.
- Integraciones con otras plataformas (Google Calendar, etc.).
- Configuración de notificaciones avanzadas (por ejemplo, recordatorios múltiples o notificaciones antes del evento).

---

### **Contribuciones** 🤝
¡Contribuciones son bienvenidas! Si tienes alguna idea, abre un issue o envía un pull request. 🎉

---

### **Licencia** 📜
Este proyecto está licenciado bajo la [MIT License](LICENSE).

---