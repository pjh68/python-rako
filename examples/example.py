import asyncio
import logging
import sys
from asyncio import Task

from python_rako import Bridge, BridgeDescription, discover_bridge
from python_rako.helpers import get_dg_listener

_LOGGER = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

async def listen_for_state_updates(bridge):
    """Listen for state updates worker method."""
    async with get_dg_listener(bridge.port) as listener:
        while True:
            message = await bridge.next_pushed_message(listener)
            if message:
                # Do stuff with the message
                _LOGGER.debug(message)
   


def main():
    logging.basicConfig(level=logging.DEBUG)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # Find the bridge
    bridge_desc: BridgeDescription = loop.run_until_complete(
        asyncio.gather(discover_bridge())
    )[0]
    print(bridge_desc)

    # Listen for state updates in the lights
    bridge = Bridge(**bridge_desc)
    #task: Task = loop.create_task(listen_for_state_updates(bridge))
    # Stop listening
    #task.cancel()

    loop.run_until_complete(listen_for_state_updates(bridge))
    


if __name__ == "__main__":
    main()
    while True:
        pass
