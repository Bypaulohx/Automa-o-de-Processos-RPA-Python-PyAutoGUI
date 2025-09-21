from __future__ import annotations
import argparse
import os
from rpa.calibrate import run as calibrate_run
from rpa.form_runner import run as runner_run

def main():
    parser = argparse.ArgumentParser(description="RPA de preenchimento em massa com PyAutoGUI")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p1 = sub.add_parser("calibrate", help="Captura as coordenadas dos campos/botão em tela")
    p1.add_argument("--config", default="config/config.json")

    p2 = sub.add_parser("run", help="Executa o preenchimento em massa a partir de um CSV")
    p2.add_argument("--config", default="config/config.json")
    p2.add_argument("--coords", default="config/coords.json")
    p2.add_argument("--csv", default="data/input.csv")
    p2.add_argument("--dry-run", action="store_true", help="Não clica/digita de verdade, apenas loga as ações")

    args = parser.parse_args()
    if args.cmd == "calibrate":
        calibrate_run(config_path=args.config, out_path="config/coords.json")
    elif args.cmd == "run":
        runner_run(config_path=args.config, coords_path=args.coords, csv_path=args.csv, dry_run=args.dry_run)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
