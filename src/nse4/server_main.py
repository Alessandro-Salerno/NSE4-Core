# NSE4 Core
# Copyright (C) 2023 - 2025 Alessandro Salerno

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import json
import logging

from nse4.server_commands import ExchangePriviledgedCommandHandler, ExchangeUserCommandHandler
from unet.server import UNetAuthenticatedHandler, UNetAuthenticationHandler, UNetServer
from nse4.exdb import EXCHANGE_DATABASE
from nse4.scheduler import MarketScheduler
from nse4.global_market import GlobalMarket
from nse4.historydb import HistoryDB
from nse4.event_engine import EventEngine
import nse4.scripting as scripting


class ExchangeAuthenticatedHandler(UNetAuthenticatedHandler):
    def __init__(self, socket: any,
                 user: str,
                 user_command_handler=ExchangeUserCommandHandler(),
                 admin_command_handler=ExchangePriviledgedCommandHandler(),
                 parent=None) -> None:
        
        super().__init__(socket, user, user_command_handler, admin_command_handler, parent)


class ExchangeAuthenticationHandler(UNetAuthenticationHandler):
    def __init__(self, socket: any,
                 authenticated_handler=ExchangeAuthenticatedHandler,
                 parent=None) -> None:
        
        super().__init__(socket, authenticated_handler, parent)

    def on_login(self, username: str):
        EXCHANGE_DATABASE.add_user(username=username)

    def on_signup(self, username: str):
        EXCHANGE_DATABASE.add_user(username=username)


def main():
    print(
"""NSE4 Server 4.0.3 Copyright (C) 2023 - 2025 Alessandro Salerno
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
""")

    # Instantiate exchange database
    logging.basicConfig(format='[%(process)d]    [%(asctime)s  %(levelname)s]\t%(message)s', level=logging.INFO)
    logging.info("Loading data...")
    exdb = EXCHANGE_DATABASE
    history = HistoryDB()
    logging.info("All loaded! Starting components...")

    mkt = GlobalMarket()
    logging.info("Order Matching Engine started!")

    server = UNetServer(connection_handler_class=ExchangeAuthenticationHandler)
    logging.info("MCom/UNet TCP Server started!")

    scripting.load_all_scripts()
    logging.info("Loaded all scripts!")

    s = MarketScheduler()
    logging.info("Starting event loop...")
    events = EventEngine()
    s.start_scheduler()


if __name__ == '__main__':
    main()
