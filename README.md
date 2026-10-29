# pfma-nav-data

Datos gratuitos para PFMA NAV. No aptos como única fuente para navegación: consulta siempre el AIP y los NOTAM oficiales.

## Zonas (espacio aéreo)

Releases `zones-YYNN`, una por ciclo AIRAC, con `zones-index.json` y dos archivos por país (`CC.json`, `CC-points.json`): espacios aéreos, radioayudas, puntos de notificación y obstáculos.

Datos © [openAIP](https://www.openaip.net), CC BY-NC 4.0, procesados para PFMA NAV y de descarga gratuita.

## Mapa base

Releases `basemap-YYYYMMDD-HHMM`, con un archivo PMTiles por extracto de Geofabrik (esquema OpenMapTiles, hasta zoom 12): zonas urbanas, agua, ríos, rutas, nombres de lugares, cerros, pistas y aeródromos. El índice vigente es `basemap-index.json`, en la release `basemap-index`. Se regenera cada tres meses (workflow *Base map packages*).

© [OpenMapTiles](https://openmaptiles.org) © [colaboradores de OpenStreetMap](https://www.openstreetmap.org/copyright). Datos bajo licencia ODbL 1.0; esquema de mosaicos CC-BY 4.0. Generado con [Planetiler](https://github.com/onthegomap/planetiler) a partir de extractos de [Geofabrik](https://download.geofabrik.de).
