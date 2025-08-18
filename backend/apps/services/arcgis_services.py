from django.core.cache import cache
import json, logging, time, requests
from backend.settings import LOCATIONIQ_API_KEY, LOCATIONIQ_URL

logger = logging.getLogger(__name__)

class LocationIQGeocoder:
    """
        Geocodifica una dirección usando LocationIQ API con manejo avanzado de errores,
        caché y reintentos.
    """

    @staticmethod
    def geocode_address(address, region=None, comuna=None, max_retries=3, retry_delay=1):
        
        # realizamos la configuración de la API
        base_url = LOCATIONIQ_URL
        api_key = LOCATIONIQ_API_KEY

        # Creamos una clave de caché única para esta consulta
        cache_key = f"geocode_{address}_{region}_{comuna}"

        # construimos parámetros de búsqueda
        params = {
            'key': api_key,
            'q': address,
            'format': 'json',
            'addressdetails': 1,
            'normalizeaddress': 1,
            'countrycodes': 'cl', # buscamos solo en Chile
            'limit': 1
        }

        # Agregamos la región y comuna si están disponibles
        if region: 
            params['state'] = region
        if comuna: 
            params['city'] = comuna

        # Intentar hasta max_retries veces
        for attempt in range(max_retries):
            try:
                response = requests.get(base_url, params=params)
                
                # Manejar código 429 (Too Many Requests)
                if response.status_code == 429:
                    retry_after = int(response.headers.get('Retry-After', retry_delay))
                    logger.warning(f"Límite de API alcanzado. Reintentando en {retry_after} segundos...")
                    time.sleep(retry_after)
                    continue
                
                response.raise_for_status()
                
                data = response.json()

                if data:
                    print('Respuesta LocationIQ: ', data)
                    # Procesar la respuesta
                    first_result = data[0]
                    result = {
                        'display_name': first_result.get('display_name', ''),
                        'latitude': float(first_result.get('lat', 0)),
                        'longitude': float(first_result.get('lon', 0)),
                        'address_details': first_result.get('address', {}),
                        'comuna_api': first_result.get('address', {}).get('city', ''),
                        'region_api': first_result.get('address', {}).get('state', ''),
                        'importance': float(first_result.get('importance', 0)),
                        'raw_data': first_result
                    }
                    
                    # Validar calidad del resultado
                    if result['importance'] < 0.1:
                        return None
                    
                    cache.set(cache_key, result, 86400)
                    return result
                return None
            except requests.exceptions.RequestException as e:
                logger.error(f"Intento {attempt + 1} fallido. Error al geocodificar: {str(e)}")
                if attempt == max_retries - 1:
                    raise
                time.sleep(retry_delay * (attempt + 1))  # Espera exponencial
            except (IndexError, KeyError, ValueError, TypeError) as e:
                logger.error(f"Error procesando respuesta de geocodificación: {str(e)}")
                return None
        return None