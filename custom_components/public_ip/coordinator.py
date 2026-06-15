from datetime import timedelta
import logging

from aiohttp import ClientSession

from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import (
    CONF_PROVIDER,
    DOMAIN,
    PROVIDERS,
    SCAN_INTERVAL,
)

_LOGGER = logging.getLogger(__name__)


class PublicIPCoordinator(DataUpdateCoordinator):
    def __init__(
        self,
        hass,
        entry,
        session: ClientSession,
    ):
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(
                seconds=SCAN_INTERVAL
            ),
        )

        self.entry = entry
        self.session = session

    async def _async_update_data(self):
        provider = self.entry.data[CONF_PROVIDER]

        if provider == "auto":
            urls = [
                url
                for key, url in PROVIDERS.items()
                if key != "auto"
            ]
        else:
            urls = [PROVIDERS[provider]]

        last_error = None

        for url in urls:
            try:
                async with self.session.get(
                    url,
                    timeout=10,
                ) as response:
                    response.raise_for_status()

                    return {
                        "ip": (await response.text()).strip(),
                        "provider": provider,
                        "url": url,
                    }

            except Exception as err:
                last_error = err

        raise UpdateFailed(
            f"Unable to update: {last_error}"
        )
