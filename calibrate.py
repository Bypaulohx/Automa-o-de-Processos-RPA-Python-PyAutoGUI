from __future__ import annotations
import json
import time
from typing import Dict, Any
import pyautogui
from .actions import wait
from ..utils.logger import get_logger

log = get_logger("calibrate")

def countdown(sec: int = 3, label: str = "") -> None:
    for s in range(sec, 0, -1):
        log.info(f"{label} Capture em {s}…")
        time.sleep(1)

def capture_position(prompt: str) -> dict:
    log.info(f"Posicione o mouse sobre: {prompt}")
    countdown(3, label="[CALIBRAR]")
    x, y = pyautogui.position()
    log.info(f"Capturado {prompt} em ({x}, {y})")
    return {"x": x, "y": y}

def run(config_path: str = "config/config.json", out_path: str = "config/coords.json") -> None:
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    coords = {}
    log.info("Iniciando calibração de campos. Não mova/janelas durante o processo.")
    for field in config["fields"]:
        name = field["name"]
        desc = field.get("description", name)
        pos = capture_position(f"'{desc}'")
        coords[name] = pos
        wait(0.3)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(coords, f, ensure_ascii=False, indent=2)
    log.info(f"Calibração salva em {out_path}")
