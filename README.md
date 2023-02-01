# globant-challenge

## Goal
Crear un WeatherAPI que cumpla con los siguientes requisitos
```
* Support the following endpoints GET /weather?city=$City&country=$Country
* City is a string. Example: Valledupar
* Country is a country code of two characters in lowercase. Example: co
* This endpoint should use an external API to get the proper info, here is an example: http://api.openweathermap.org/data/2.5/weather
* Deliver both Temperatures in Celsius and Fahrenheit
```
---

## Setup for development

Este proyecto se encuentra configurado con Docker y docker-compose, con la finalidad de agilizar un deployment LOCAL para mantener un entorno de desarrollo independiente. Es necesario verificar de tener Docker instalado

**1)** Clonar repositorio
```sh
git clone https://github.com/csanlucas/houm-challenge.git
```
**2)** Ingresar a la carpeta del proyecto y ejecutar docker-compose up, este comando realizará la configuración de las imágenes de Docker para backend y para la DB
```sh
cd globant-challenge
cp .env.example .env
cp .pgenv.example .pgenv
docker-compose up

# Por facilidad de setup, se encuentran en texto el valor de los secrets para el deployment local
```
**3)** Crear Database Caching, soportado por Django
```sh
docker-compose exec backend bash
python manage.py createcachetable
exit
```
---

## Solución planteada y uso
Se realiza el desarrollo de un REST Api haciendo uso del siguiente stack de tecnologías:

    - Python 3.10+
    - Django 4.1.5
    - Django-Rest-Framework 3.14.0

Manejo de entornos de desarrollo para agilizar el cambio de variables de accesso y settings de DRF dependiendo el entorno al que
se hará deployment

    - LOCAL
    - PROD

Gestión de archivos de secrets, como variables de entorno, idealmente sus valores no se hacen tracking en git pero en esta situación
para facilitar la ejecución del proyecto se hace tracking de *.example

### **USO**
Se debe realizar los request a los endpoints haciendo uso de algún cliente de HTTP, se recomienda utilizar *Postman*

#### [FUNCIONALIDAD 1] - Permita que la aplicación móvil mande las coordenadas del Houmer
* **URL** : http://localhost:8101/weather/?city=Bogota&country=co
* **Method** `GET`
* **Success Response:**
    * **Code** 200 <br/>
    **Content** 
    ```json
    {
        "location_name": "Bogota, CO",
        "temperature_celsius": "12.73 C",
        "temperature_fahrenheit": "54.91 F",
        "wind": "2.06 m/s, Northeast",
        "cloudiness": "20 %",
        "pressure": "1028 hpa",
        "humidity": "67%",
        "sunrise": "06:12",
        "sunset": "18:07",
        "geo_coordinates": "[4.6097, -74.0817]",
        "requested_time": "2023-02-01T09:20:48"
    }
    ```
---

### **TESTING**
```sh
docker-compose exec backend bash
python manage.py test
exit
```