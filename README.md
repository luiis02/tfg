
# TakeThis

**Sistema orientado a servicios para la mejora de la gestión de pedidos en locales de hostelería mediante Inteligencia Artificial y Asistentes Virtuales**

Autor: Luis Alcalde García  
Fecha: Septiembre de 2024  

---

## 📑 Índice

1. [Descripción General](#descripción-general)
2. [Características](#características)
3. [Tecnologías Usadas](#tecnologías-usadas)
    - [Back-end](#back-end)
    - [Front-end](#front-end)
    - [Hardware](#hardware)
4. [Instalación](#instalación)
5. [Casos de Uso](#casos-de-uso)
6. [Objetivos](#objetivos)
7. [Requisitos del Sistema](#requisitos-del-sistema)
8. [Estructura del Proyecto](#estructura-del-proyecto)
9. [Metodología de Desarrollo](#metodología-de-desarrollo)
10. [Licencia](#licencia)
11. [Agradecimientos](#agradecimientos)

---

## 📖 Descripción General

**TakeThis** es una plataforma integral para la digitalización de locales de hostelería. Permite la gestión de cartas, pedidos, secciones y mesas, incorporando herramientas de Inteligencia Artificial, asistentes virtuales y arquitectura orientada a servicios (SOA). Con ella se busca reducir tiempos de espera, mejorar la experiencia del cliente y facilitar la administración del negocio.

---

## 🚀 Características

- Gestión de cartas, platos, secciones y mesas en tiempo real.
- Realización de pedidos mediante QR o por voz.
- Recomendaciones inteligentes usando algoritmos AHP.
- Clasificación automática de imágenes de platos.
- Generación automática de descripciones y precios recomendados.
- Clasificación de peticiones HTTP como medida de seguridad.
- Asistente de voz integrado con hardware propio.
- Chatbot para empleados usando OpenAI.

---

## 🛠️ Tecnologías Usadas

### Back-end
- Python 3.10+
- Flask
- SQLite (desarrollo) / MariaDB (producción)
- TensorFlow, Keras
- REST API
- MicroPython y C++ para ESP32

### Front-end
- HTML, CSS, JavaScript
- Twig (plantillas)
- Responsive Design para móviles/tablets

### Hardware
- ESP32
- Micrófono MAX9814
- Servidor Linux (Ubuntu Server o Rocky Linux)

---

## ⚙️ Instalación

```bash
git clone https://github.com/usuario/takethis.git
cd takethis
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
flask run
```

Para configurar el asistente virtual:
- Programa el ESP32 con el firmware en `assistant/esp32/`
- Conecta el micrófono MAX9814

---

## 📊 Casos de Uso

- El cliente escanea un QR y realiza su pedido desde el móvil.
- El asistente virtual permite pedir sin necesidad de un smartphone.
- El personal consulta dudas al chatbot.
- El sistema sugiere platos automáticamente.
- Administración de platos y cartas por parte del personal.

---

## 🎯 Objetivos

### General

Desarrollar una plataforma integral para gestionar locales de restauración y optimizar la toma de decisiones mediante IA.

### Específicos

- Análisis de soluciones actuales y tecnologías.
- Estudio y aplicación de arquitecturas orientadas a servicios.
- Desarrollo de un asistente virtual autónomo.
- Implementación de clasificadores IA para seguridad e imágenes.
- Desarrollo de un algoritmo de recomendación de platos.

---

## 💻 Requisitos del Sistema

- Python 3.10+
- Node.js (opcional para frontend avanzado)
- ESP32 + MAX9814
- Servidor con al menos 4GB RAM y 20GB SSD
- OpenAI API Key (para chatbot)

---

## 📁 Estructura del Proyecto

```
takethis/
├── backend/
│   ├── app.py
│   ├── models/
│   ├── routes/
├── frontend/
│   ├── templates/
│   ├── static/
├── assistant/
│   └── esp32/
├── tests/
├── README.md
└── requirements.txt
```

---

## 🧪 Metodología de Desarrollo

Se utilizó una combinación de **SCRUM** y **Kanban**:

- 12 sprints semanales
- Uso de Trello para gestión de tareas
- Story Points para medir tiempos
- Entrega progresiva de funcionalidades

---

## 📄 Licencia

Este proyecto se encuentra publicado bajo una licencia libre.

---

## 🙏 Agradecimientos

A todas las personas que ayudaron en el desarrollo del proyecto.  
Especial mención al Bar Vílchez, fuente de inspiración para TakeThis.  
Gracias también a profesores, amigos y familiares por el apoyo constante.

---

Desarrollado por Luis Alcalde García · Universidad de Granada · ETSIIT
