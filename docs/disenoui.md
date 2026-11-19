# Especificación de interfaz — UDH Becas y Bienestar

Requisitos de diseño definidos para el sistema. Cada módulo nuevo debe construir sus
pantallas siguiendo este documento.

## Identidad visual
- Sistema institucional de la **Universidad de Huánuco (UDH)**. Logo oficial en `frontend/img/`
  (`udhescudo.png`, `udhmarca.png`, `favicon.png`).
- **Referencia visual aprobada:** el prototipo `becas-udh.html` (guardarlo en `docs/referencia/`).
  Barra lateral verde bosque, área de trabajo con tarjetas planas y el dorado del escudo solo
  para marcar lo importante (barra de la opción activa, contadores, destacados).
- Colores (tokens en `frontend/css/styles.css`): verde marca `--brand #0A6B4F`, verde oscuro de
  navegación `--side #073B2B`, dorado `--gold #C99A2E`, fondo `--bg #F2F6F3`, texto `--fg #10231B`.
  Gráficos: serie única `--series-1` y paleta categórica `--cat-1..5` en orden fijo
  (verde, dorado, azul, naranja, violeta; validada en ambos modos). Más de 5 categorías se agrupan en "Otras".
- Estados con chips de punto: `c-ok`, `c-warn`, `c-bad`, `c-info`, `c-gold`, `c-mute`.
- Tipografías: Bricolage Grotesque (títulos) y Figtree (texto).
- Universidad seria, confiable, moderna y profesional. **No** futurista, **no** neón,
  **no** aspecto de aplicación comercial.
- Modo claro y oscuro (botón sol/luna; sin preferencia guardada sigue al sistema). Colores oscuros en `:root[data-theme="dark"]`.
- Responsive, accesible, limpia y fácil de usar. Identidad coherente en todas las pantallas.

## Estructura
- Logo UDH y nombre "Universidad de Huánuco" en la parte superior de la barra lateral; barra superior con ruta de navegación, notificaciones y perfil del usuario.
- Menú lateral (estudiante): Inicio, Becas, Mis postulaciones, Mis becas,
  Bienestar universitario, Mis citas, Seguimiento, Notificaciones, Mi perfil.
- Menú lateral (administración): Panel institucional, Facultades, Escuelas, Estudiantes
  y las opciones de administración de cada módulo nuevo.

## Dashboard del estudiante
Saludo al estudiante, resumen de postulaciones, becas disponibles, estado de postulación,
próxima cita, notificaciones y accesos rápidos.

## Becas
- **Tarjeta de beca:** nombre, tipo, porcentaje de beneficio, convocatoria, fecha de inicio y fin,
  cupos disponibles, estado y botón "Ver detalles".
- **Detalle de beca:** descripción, beneficio, requisitos, reglas de aplicación, convocatoria,
  fechas, cupos y botón "Postular".

## Postulación
- Flujo visual por pasos: 1. Datos de postulación · 2. Requisitos · 3. Documentos ·
  4. Confirmación · 5. Evaluación · 6. Resultado.
- Badges de estado: REGISTRADA, EN EVALUACIÓN, APROBADA, RECHAZADA.

## Bienestar universitario
- Secciones: Psicología y Orientación universitaria.
- Solicitar cita eligiendo profesional, fecha, hora, modalidad (presencial/virtual) y motivo.
- Estados de cita: PROGRAMADA, ATENDIDA, CANCELADA, NO ASISTIÓ.
- Seguimiento de casos con **línea de tiempo**: ABIERTO → EN PROCESO → CERRADO.

## Seguimiento de becas
Promedio académico, cumplimiento de condiciones, observaciones, responsable y estado de la beca.

## Dashboard institucional (administrador)
Estadísticas de becas disponibles, postulaciones, becas aprobadas, becas rechazadas,
becarios vigentes, citas de bienestar y casos abiertos. Usar tablas, gráficos, tarjetas,
filtros y badges.
