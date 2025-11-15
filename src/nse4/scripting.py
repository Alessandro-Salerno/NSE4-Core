
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


class NSEScriptEvent:
    LOAD = 1
    SETTLE = 2


class NSEInvalidEventException(Exception):
    def __init__(self, event) -> None:
        super().__init__(event)


class NSEScriptHandle:
    def on_load(self) -> bool:
        return True

    def on_settle(self) -> bool:
        return True


script_handles: list[NSEScriptHandle] = []
scripts_dir = Path("./nse-scripts")

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


def nse_script(handle: Type[NSEScriptHandle]):
    handle_ins = handle()
    handle_ins.on_load()
    script_handles.append(handle_ins)


def invoke_scripts(event) -> bool:
    for handle in script_handles:
        result = (lambda e: handle.on_load() if event == NSEScriptEvent.LOAD else
                            handle.on_settle() if event == NSEScriptEvent.SETTLE else
                            None)(event)
        if result is None:
            raise NSEInvalidEventException(event)
        if not result:
            return False
    
    return True

