import logging
import random

import httpx
from fastapi import Request

from models import GeoIpApi, GeoIpApiRtypeEnum

logger = logging.getLogger("inspector.utils")

GEOIP_API = {
    "country.is": GeoIpApi(
        url="https://api.country.is/{ip}",
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
        url="http://www.geoplugin.net/json.gp?ip={ip}",
        rtype=GeoIpApiRtypeEnum.json,
        lookup="geoplugin_countryCode",
    ),
}


def request_to_ip(request: Request) -> str:
    logger.debug("Getting IP address from request...")

    # get the ip address of the client. First check the proxy headers, then the client host
    client_ip = request.client.host if request.client else ""
    proxy_ip = request.headers.get("x-forwarded-for", "")
    ip = proxy_ip or client_ip

    logger.debug(f"Returning {ip=}")
    return ip


async def ip_to_country(ip: str) -> str:
    logger.debug(f"Getting country code for {ip}...")
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
        country = response.json().get(geoip_api.lookup) or ""
    elif geoip_api.rtype == GeoIpApiRtypeEnum.text:
        country = response.text.split(geoip_api.delimiter)[int(geoip_api.lookup)] or ""

    logger.debug(f"Returning {country=}")
    return country
