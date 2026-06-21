"""SSL helper for www.aqhi.gov.hk.

The server presents only its leaf certificate and omits the intermediate
``Hongkong Post e-Cert SSL CA 3 - 17``. Browsers and curl recover from this via
AIA fetching, but Python's ``ssl`` module does not, so Home Assistant fails with
``unable to get local issuer certificate``. The intermediate's root
(``Hongkong Post Root CA 3``) is already trusted by ``certifi``, so supplying the
intermediate below lets the chain verify normally — no need to disable
verification. Intermediate valid until 2032-06-03.
"""

import ssl

from homeassistant.core import HomeAssistant

from .const import DOMAIN

HK_POST_INTERMEDIATE_PEM = """-----BEGIN CERTIFICATE-----
MIIFtzCCA5+gAwIBAgIUPbGA72/4X3qJXRZEW5/J/D3vu8cwDQYJKoZIhvcNAQEL
BQAwbzELMAkGA1UEBhMCSEsxEjAQBgNVBAgTCUhvbmcgS29uZzESMBAGA1UEBxMJ
SG9uZyBLb25nMRYwFAYDVQQKEw1Ib25na29uZyBQb3N0MSAwHgYDVQQDExdIb25n
a29uZyBQb3N0IFJvb3QgQ0EgMzAeFw0yNTAzMjAwNzQwMjRaFw0zMjA2MDMwNDA3
NTBaMHoxCzAJBgNVBAYTAkhLMRIwEAYDVQQIEwlIb25nIEtvbmcxEjAQBgNVBAcT
CUhvbmcgS29uZzEWMBQGA1UEChMNSG9uZ2tvbmcgUG9zdDErMCkGA1UEAxMiSG9u
Z2tvbmcgUG9zdCBlLUNlcnQgU1NMIENBIDMgLSAxNzCCASIwDQYJKoZIhvcNAQEB
BQADggEPADCCAQoCggEBAIagJaH0N6+HN+9jlWGSk8cajAmkcma40f97saznEfrH
1H1boG6FWDSRZ4Gc0AbPVS3PWEW1nMX9DujF5fnhRYQZeuwviJGbIlEhTYuvF7N/
TXPQN1SP+bq1eJIkn0kdhtaWOIajq5vGEHvQ6CFZEE/yEWlrKnH0FNXpRx2Yj7bN
+UKOTz5XkABuSV0QYqm6UDt5kRDFE9t/ChshTABxGsEM2vpe9LvKemsuOBtw0lee
0I6MOsl0/kSN4kpoLjPeqqGHai3nUXCA+qWp+m+zwdR2OYTxl/TDBZp8wDLKhJTk
/AFayjUwl1I+qTnU0WjppV5vwhc5vFBdZGM+RtrFPlkCAwEAAaOCAT4wggE6MBIG
A1UdEwEB/wQIMAYBAf8CAQAwbgYIKwYBBQUHAQEEYjBgMDcGCCsGAQUFBzAChito
dHRwOi8vd3d3MS5lQ2VydC5nb3YuaGsvcm9vdC9yb290X2NhXzMuY3J0MCUGCCsG
AQUFBzABhhlodHRwOi8vb2NzcDEuZUNlcnQuZ292LmhrMBEGA1UdIAQKMAgwBgYE
VR0gADAOBgNVHQ8BAf8EBAMCAQYwEwYDVR0lBAwwCgYIKwYBBQUHAwEwHwYDVR0j
BBgwFoAUF53NHovWOStw01zUoLgfsAD8xWEwPAYDVR0fBDUwMzAxoC+gLYYraHR0
cDovL2NybDEuZUNlcnQuZ292LmhrL2NybC9Sb290Q0EzQVJMLmNybDAdBgNVHQ4E
FgQUkjewcJyOeduzGRO4m6UywLfWJ2IwDQYJKoZIhvcNAQELBQADggIBAAysgBs5
p5c7mhlMv60XKJR7QZS5hHb9JO/37DX/6EWpRVRm6Nyq6NS423k55szhAcdxn3YM
q+89pVrTGZMUWniSFs+/j88i835zNBD0/pD80uMTGYm7UMLQ167BfGfq0kCtwMgW
hZHKNhQaGTfNbz3KR4JS14DdslOqLMALoyAVaOenvHJrbzse6qxpepmqQehrU7QM
317Ba+NKcw3XId1qpUiQPRg886+x7+0NOQ1/kXZMV5UOcxFBFbOVx8Utr2n34FU1
7SsAVAxXT0YJ1K5TV31/c0+WSnSjSj91xRnZj0iVubu+XEPXq2moMpITMnNcfZk/
Op8HGXy29LJBw+UZe0YwvAt9mIhip3HUdlhhuP96JRuMGoOTr6RC63v5t8QrdjI9
eo3ts8lxRqUFdawx1bVdUhcOoK+ru81oIfsmNNfJunutdnwofH+zL4xr0MWF7wpx
vBt1zxleeNxya4rVrmaapJz+Jibqclwg0MJXDGcSRZl4lhH0AOcIA3gLRQqX50rI
WYQ0D+5DOtqyIqwGfmGl3fH0R0+TgR7fiYvMMmEecbCP4VCANEmfscOW/R0mSsn4
D7zjnEIvJMHHARQrv2sfRopUa2fYj6QBqkjwx4NterNDG0ICSXfsUW8Ryg0NjR85
Xp3bKm2PvCNZwVnGQORqX2E4tf436Pir0M8Z
-----END CERTIFICATE-----"""

_SSL_CONTEXT_KEY = f"{DOMAIN}_ssl_context"


def _build_ssl_context() -> ssl.SSLContext:
    context = ssl.create_default_context()
    context.load_verify_locations(cadata=HK_POST_INTERMEDIATE_PEM)
    return context


async def async_get_ssl_context(hass: HomeAssistant) -> ssl.SSLContext:
    """Return a cached SSL context that trusts the missing HK Post intermediate.

    Building the context reads the system trust store, so it runs in the
    executor to avoid blocking the event loop.
    """
    context = hass.data.get(_SSL_CONTEXT_KEY)
    if context is None:
        context = await hass.async_add_executor_job(_build_ssl_context)
        hass.data[_SSL_CONTEXT_KEY] = context
    return context
