"""Test accessories for telnetlib3 project."""
# std imports
import logging

# local
import telnetlib3

# 3rd-party
import pytest
from pytest_asyncio.plugin import (
    unused_tcp_port,
    event_loop,
)

@pytest.fixture
def log():
    _log = logging.getLogger(__name__)
    _log.setLevel(logging.DEBUG)
    return _log


@pytest.fixture(scope="module", params=["127.0.0.1", "::1"])
def bind_host(request):
    return request.param


class TestTelnetServer(telnetlib3.TelnetServer):
    # we instruct our Test telnet client
    # to timeout if it receives no client data
    # for any duration more than 1/2 second.
    #
    # first, because as using asyncio, we should
    # be aggressively semaphore/signaling our await
    # calls.  we wish to force an idle condition otherwise.

    CONNECT_MINWAIT = 0.10
    CONNECT_MAXWAIT = 0.50
    CONNECT_DEFERRED = 0.01
    TTYPE_LOOPMAX = 2
    default_env = {
        'PS1': 'test-telsh %# ',
        'TIMEOUT': '1',
    }
    TIMEOUT_MULTIPLIER = 1


class TestTelnetClient(telnetlib3.TelnetClient):
    #: mininum on-connect time to wait for server-initiated negotiation options
    CONNECT_MINWAIT = 0.20
    CONNECT_MAXWAIT = 0.75
    CONNECT_DEFERRED = 0.01

    #: default client environment variables,
    default_env = {
        'COLUMNS': '80',
        'LINES': '24',
        'USER': 'test-client',
        'TERM': 'test-terminal',
        'CHARSET': 'ascii',
    }
