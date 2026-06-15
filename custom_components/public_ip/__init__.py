from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN
from .coordinator import PublicIPCoordinator

PLATFORMS = ["sensor"]


async def async_setup_entry(hass, entry):
    """Set up Public IP from a config entry."""

    hass.data.setdefault(DOMAIN, {})

    session = async_get_clientsession(hass)

    coordinator = PublicIPCoordinator(
    hass=hass,
    entry=entry,
    session=session,
)

    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(
        entry,
        PLATFORMS,
    )

    return True


async def async_unload_entry(hass, entry):
    """Unload a config entry."""

    unload_ok = await hass.config_entries.async_unload_platforms(
        entry,
        PLATFORMS,
    )

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
