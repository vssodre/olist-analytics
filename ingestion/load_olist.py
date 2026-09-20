"""Carrega os CSVs do dataset Olist (Kaggle) no DuckDB, schema raw."""
from pathlib import Path

import duckdb

CSV_DIR = Path("data/raw/olist")
DB_PATH = "data/olist.duckdb"


def table_name(path: Path) -> str:
    name = path.stem
    if name.startswith("olist_"):
        name = name[len("olist_"):]
    if name.endswith("_dataset"):
        name = name[: -len("_dataset")]
    return name


def main() -> None:
    files = sorted(CSV_DIR.glob("*.csv"))
    if not files:
        raise SystemExit(
            f"Nenhum CSV encontrado em {CSV_DIR}. "
            "Baixe o dataset do Kaggle e copie os arquivos para essa pasta."
        )
    con = duckdb.connect(DB_PATH)
    con.execute("CREATE SCHEMA IF NOT EXISTS raw")
    for path in files:
        table = table_name(path)
        con.execute(
            f"""
            CREATE OR REPLACE TABLE raw.{table} AS
            SELECT *, current_timestamp AS _loaded_at
            FROM read_csv_auto('{path.as_posix()}', header = true)
            """
        )
        total = con.execute(f"SELECT count(*) FROM raw.{table}").fetchone()[0]
        print(f"raw.{table}: {total} linhas")
    con.close()


if __name__ == "__main__":
    main()