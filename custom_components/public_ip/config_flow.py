import voluptuous as vol

from homeassistant import config_entries

from .const import (
    CONF_PROVIDER,
    DOMAIN,
    PROVIDERS,
)


class PublicIPConfigFlow(
    config_entries.ConfigFlow,
    domain=DOMAIN,
):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if self._async_current_entries():
            return self.async_abort(
                reason="single_instance"
            )

        if user_input is not None:
            return self.async_create_entry(
                title="Public IP",
                data=user_input,
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_PROVIDER,
                        default="ipify",
                    ): vol.In(PROVIDERS)
                }
            ),
        )
