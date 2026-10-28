# Recap de AWS con Café 53

Este proyecto reúne fundamentos útiles para AWS Certified Cloud Practitioner y
los conecta con una aplicación real administrada mediante Terraform.

## Lo que ya practicaste

| Área | Servicio | Qué hiciste en Café 53 |
|---|---|---|
| Cómputo | AWS Lambda | Ejecutaste código bajo demanda sin administrar servidores. |
| APIs | API Gateway | Publicaste rutas HTTP para crear, consultar y listar órdenes. |
| Bases de datos | DynamoDB | Guardaste pedidos en una tabla NoSQL con capacidad bajo demanda. |
| Integración | EventBridge | Publicaste y enrutaste eventos de negocio. |
| Mensajería | SQS | Desacoplaste el ingreso de una orden de su procesamiento. |
| Resiliencia | SQS DLQ | Aislaste mensajes que fallen repetidamente. |
| Notificaciones | SNS | Publicaste el evento final `OrderReady`. |
| Almacenamiento | S3 | Alojaste el frontend en un bucket privado y versionado. |
| Entrega | CloudFront | Distribuiste el sitio mediante HTTPS y caché global. |
| DNS | Route 53 | Estudiaste cómo conectar un dominio personalizado a CloudFront. |
| Seguridad | IAM | Aplicaste permisos mínimos entre Lambda y otros servicios. |
| Observabilidad | CloudWatch | Creaste logs, métricas, alarmas y un dashboard. |
| Costos | AWS Budgets | Configuraste alertas de gasto real y previsto. |
| Infraestructura | Terraform | Versionaste y desplegaste la arquitectura como código. |

## Cómo leer el flujo

1. El navegador descarga el frontend desde CloudFront.
2. `POST /orders` entra por API Gateway e invoca Lambda.
3. Lambda valida la solicitud, escribe en DynamoDB y publica en EventBridge.
4. EventBridge envía el evento a SQS.
5. Otra Lambda consume el mensaje, cambia el pedido a `READY` y publica en SNS.
6. La interfaz consulta el estado y el historial mediante la API.

## Preguntas que ya puedes responder

- ¿Qué diferencia existe entre una región, una zona de disponibilidad y una ubicación edge?
- ¿Por qué SQS y EventBridge resuelven problemas distintos?
- ¿Qué ventaja tiene una arquitectura serverless para una carga pequeña e impredecible?
- ¿Por qué el bucket S3 permanece privado aunque el sitio sea público?
- ¿Qué diferencia existe entre una alarma de CloudWatch y un presupuesto de AWS?
- ¿Por qué un presupuesto avisa, pero no detiene automáticamente el gasto?
- ¿Qué significa aplicar el principio de privilegio mínimo en IAM?
- ¿Cuándo convendría usar RDS o Aurora en lugar de DynamoDB?

## Siguientes prácticas recomendadas

1. Añadir autenticación con Amazon Cognito para separar clientes y operadores.
2. Sustituir el listado pequeño basado en `Scan` por un índice consultable cuando
   el volumen crezca.
3. Conectar un dominio con Route 53 y un certificado ACM.
4. Suscribir un correo de prueba a SNS y confirmar el flujo de notificación.
5. Crear una alarma de uso del Free Tier además del presupuesto mensual.
