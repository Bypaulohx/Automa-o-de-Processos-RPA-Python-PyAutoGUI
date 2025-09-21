from __future__ import annotations
import json
import os
import pandas as pd
from typing import Dict, Any
from .actions import setup_pyautogui, click_point, type_text, wait
from ..utils.logger import get_logger

log = get_logger("runner")

def run(config_path: str = "config/config.json", coords_path: str = "config/coords.json", csv_path: str = "data/input.csv", dry_run: bool = False) -> None:
    if not os.path.exists(coords_path):
        raise FileNotFoundError(f"Coordenadas não encontradas em {coords_path}. Execute: python src/main.py calibrate")
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    with open(coords_path, "r", encoding="utf-8") as f:
        coords = json.load(f)

    safety = config.get("safety", {})
    setup_pyautogui(failsafe=safety.get("failsafe", True), pause=safety.get("pause", 0.2))

    delays = config.get("delays", {})
    between_keys = float(delays.get("between_keys", 0.01))
    between_fields = float(delays.get("between_fields", 0.4))
    after_submit = float(delays.get("after_submit", 1.0))

    df = pd.read_csv(csv_path, dtype=str).fillna("")
    log.info(f"Total de registros: {len(df)}")

    text_fields = [f for f in config["fields"] if f.get("type","text") == "text"]
    submit_field = next((f for f in config["fields"] if f.get("type") == "button"), None)
    if submit_field is None:
        raise ValueError("Campo do tipo 'button' não encontrado em config.fields. Adicione um com name='submit'.")

    for idx, row in df.iterrows():
        log.info(f"Processando linha {idx+1}/{len(df)}…")
        for field in text_fields:
            name = field["name"]
            value = str(row.get(name, ""))
            point = coords.get(name)
            if point is None:
                log.warning(f"Sem coordenadas para '{name}', pulando…")
                continue
            if dry_run:
                log.info(f"[DRY-RUN] Clicaria {name} em ({point['x']},{point['y']}) e digitária: {value}")
            else:
                click_point((point["x"], point["y"]))
                if value:
                    type_text(value, interval=between_keys)
                wait(between_fields)
        # Submit
        point = coords.get(submit_field["name"])
        if point:
            if dry_run:
                log.info(f"[DRY-RUN] Clicaria SUBMIT em ({point['x']},{point['y']})")
            else:
                click_point((point["x"], point["y"]))
                wait(after_submit)
        else:
            log.warning("Sem coordenadas para o botão de envio.")
    log.info("Concluído!")
