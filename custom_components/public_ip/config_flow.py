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
                        default="auto",
                    ): vol.In(PROVIDERS)
                }
            ),
        )

    @staticmethod
    def async_get_options_flow(config_entry):
        return PublicIPOptionsFlow(config_entry)


class PublicIPOptionsFlow(
    config_entries.OptionsFlow
):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(
        self,
        user_input=None,
    ):
        if user_input is not None:
            return self.async_create_entry(
                title="",
                data=user_input,
            )

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_PROVIDER,
                        default=self.config_entry.options.get(
                            CONF_PROVIDER,
                            self.config_entry.data.get(
                                CONF_PROVIDER,
                                "auto",
                            ),
                        ),
                    ): vol.In(PROVIDERS)
                }
            ),
        )
