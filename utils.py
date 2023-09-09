import logging
import random

import httpx

from models import GeoIpApi, GeoIpApiRtypeEnum

logger = logging.getLogger(__name__)

GEOIP_API = {
    "country.is": GeoIpApi(
        url="https://country.is/{ip}",
        rtype=GeoIpApiRtypeEnum.json,
        lookup="country",
    ),
    "ip2c.org": GeoIpApi(
        url="https://ip2c.org/{ip}",
        rtype=GeoIpApiRtypeEnum.text,
        delimiter=";",
        lookup="1",  # index
    ),
    "geoplugin.net": GeoIpApi(
        url="https://www.geoplugin.net/json.gp?ip={ip}",
        rtype=GeoIpApiRtypeEnum.json,
        lookup="geoplugin_countryCode",
    ),
}


async def ip_to_country(ip: str) -> str:
    """Return the country code (alpha-2) for an IP address."""
    if not ip:
        return ""

    geoip_api = GEOIP_API.get(random.choice(list(GEOIP_API.keys())))
    if not geoip_api:
        return ""

    # build the url
    url = geoip_api.url.format(ip=ip)

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
        except httpx.HTTPError as e:
            logger.info(f"Error getting country code for {ip}: {e}")
            return ""

    country = ""  # alpha-2 country code, i.e. "AU"
    # parse the response and lookup the country code
    if geoip_api.rtype == GeoIpApiRtypeEnum.json:
        country = response.json().get(geoip_api.lookup, "")
    elif geoip_api.rtype == GeoIpApiRtypeEnum.text:
        country = response.text.split(geoip_api.delimiter)[int(geoip_api.lookup)]

    return country
