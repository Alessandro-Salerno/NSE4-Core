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


import logging
import importlib.util
from pathlib import Path
from typing import Type

from order_matching.execution import Execution


class ExchangeScriptEvent:
    LOAD = 1
    SETTLE = 2
    SETTLE_DONE = 3
    MONEY_TRANSFER = 4
    ASSET_TRANSFER = 5
    ORDER_PLACED = 6
    TRADE_EXECUTED = 7


class ExchangeInvalidEventException(Exception):
    def __init__(self, event) -> None:
        super().__init__(event)


class ExchangeScriptHandle:
    def on_load(self):
        return

    def on_settle(self):
        return

    def on_settle_done(self):
        return

    def on_money_transfer(self, sender: str, dest: str, amount: float):
        return

    def on_asset_transfer(self, sender: str, dest: str, ticker: str, amount: int):
        return

    def on_order_placed(self, issuer: str, execution: int, ticker: str, amount: int, price: float):
        return

    def on_trade_executed(self, buyer: str, seller: str, ticker: str, amount: int, price: float):
        return


script_handles: list[ExchangeScriptHandle] = []
scripts_dir = Path("./scripts")

def load_all_scripts():
    for file in scripts_dir.glob("*.py"):
        if file.name.startswith("_"):
            continue  # skip private modules like __init__.py, _helper.py

        module_name = file.stem  # filename without .py
        try:
            spec = importlib.util.spec_from_file_location(module_name, file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        except:
            logging.error(f"Failed to load script {module_name}")


def exchange_script(handle: Type[ExchangeScriptHandle]):
    handle_ins = handle()
    handle_ins.on_load()
    script_handles.append(handle_ins)


def invoke_scripts(event, **kwargs):
    for handle in script_handles:
        match event:
            case ExchangeScriptEvent.LOAD:
                handle.on_load()
            case ExchangeScriptEvent.SETTLE:
                handle.on_settle()
            case ExchangeScriptEvent.SETTLE_DONE:
                handle.on_settle_done()
            case ExchangeScriptEvent.MONEY_TRANSFER:
                handle.on_money_transfer(**kwargs)
            case ExchangeScriptEvent.ASSET_TRANSFER:
                handle.on_asset_transfer(**kwargs)
            case ExchangeScriptEvent.ORDER_PLACED:
                handle.on_order_placed(**kwargs)
            case ExchangeScriptEvent.TRADE_EXECUTED:
                handle.on_trade_executed(**kwargs)
            
            case _:
                raise ExchangeInvalidEventException(event)

