# const.py

DOMAIN = "public_ip"

SCAN_INTERVAL = 3600

PROVIDERS = {
    "auto": None,
    "ifconfig": "https://ifconfig.me/ip",
    "ipify": "https://api.ipify.org",
    "icanhazip": "https://icanhazip.com",
    "amazon": "https://checkip.amazonaws.com",
}

CONF_PROVIDER = "provider"
