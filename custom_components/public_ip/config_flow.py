from homeassistant import config_entries

from .const import DOMAIN


class PublicIPConfigFlow(
    config_entries.ConfigFlow,
    domain=DOMAIN,
):
    VERSION = 1

    async def async_step_user(
        self,
        user_input=None,
    ):
        if self._async_current_entries():
            return self.async_abort(
                reason="single_instance"
            )

        return self.async_create_entry(
            title="Public IP",
            data={},
        )
