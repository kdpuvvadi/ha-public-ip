from datetime import timedelta
import logging

from aiohttp import ClientSession

from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import DOMAIN, PROVIDERS, SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)


class PublicIPCoordinator(DataUpdateCoordinator):
    """Coordinator for fetching public IP."""

    def __init__(self, hass, session: ClientSession):
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=SCAN_INTERVAL),
        )

        self._session = session

    async def _async_update_data(self):
        """Fetch data from providers."""

        last_error = None

        for provider_name, url in PROVIDERS.items():
            try:
                async with self._session.get(
                    url,
                    timeout=10,
                ) as response:
                    response.raise_for_status()

                    ip = (await response.text()).strip()

                    return {
                        "ip": ip,
                        "provider": provider_name,
                    }

            except Exception as err:
                last_error = err
                continue

        raise UpdateFailed(
            f"All providers failed: {last_error}"
        )
