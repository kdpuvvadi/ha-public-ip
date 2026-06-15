from urllib.parse import urlparse

from homeassistant.components.sensor import (
    SensorEntity,
)
from homeassistant.helpers.device_registry import (
    DeviceInfo,
)
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
)

from .const import DOMAIN


async def async_setup_entry(
    hass,
    entry,
    async_add_entities,
):
    coordinator = hass.data[DOMAIN][
        entry.entry_id
    ]

    async_add_entities(
        [PublicIPSensor(coordinator)]
    )


class PublicIPSensor(
    CoordinatorEntity,
    SensorEntity,
):
    _attr_has_entity_name = True
    _attr_name = "Public IP"
    _attr_unique_id = "public_ip_address"
    _attr_icon = "mdi:ip-network"

    @property
    def native_value(self):
        return self.coordinator.data["ip"]

    @property
    def extra_state_attributes(self):
        return {
            "provider": self.coordinator.data[
                "provider"
            ],
            "provider_url": self.coordinator.data[
                "url"
            ],
            "last_checked": self.coordinator.data[
                "last_checked"
            ],
        }

    @property
    def device_info(self):
        url = self.coordinator.data["url"]

        parsed = urlparse(url)

        configuration_url = (
            f"{parsed.scheme}://{parsed.netloc}"
        )

        return DeviceInfo(
            identifiers={
                (DOMAIN, "internet")
            },
            name="Internet Connection",
            manufacturer="KD Puvvadi",
            model="Public IP Service",
            configuration_url=configuration_url,
        )
