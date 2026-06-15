from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        [PublicIPSensor(coordinator)],
        True,
    )


class PublicIPSensor(
    CoordinatorEntity,
    SensorEntity,
):
    """Representation of the public IP sensor."""

    _attr_name = "Public IP"
    _attr_unique_id = "public_ip"
    _attr_icon = "mdi:ip-network"

    @property
    def native_value(self):
        return self.coordinator.data["ip"]

    @property
    def extra_state_attributes(self):
        return {
            "provider": self.coordinator.data["provider"],
        }
