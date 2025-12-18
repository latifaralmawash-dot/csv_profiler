import sys
import csv
import json
from pathlib import Path


from .profiler import profile_row, render_markdown

def main():
    
    if len(sys.argv) < 3:
        print("Usage: python -m csv_profiler.cli profile <csv_file> [--out-dir <dir>]")
        return

    command = sys.argv[1]
    input_file = Path(sys.argv[2])

    if command == "profile":
        if not input_file.exists():
            print(f" Error: File '{input_file}' not found.")
            return

        print(f"🔍 Analyzing {input_file}...")

       
        try:
            with open(input_file, encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                data = list(reader)
            
            if not data:
                print(" File is empty.")
                return

            
            report = profile_row(data)

            
            out_dir = Path("outputs")
            if "--out-dir" in sys.argv:
                idx = sys.argv.index("--out-dir")
                out_dir = Path(sys.argv[idx + 1])
            
            out_dir.mkdir(exist_ok=True)

           
            json_path = out_dir / f"{input_file.stem}_report.json"
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(report, f, indent=4)

           
            md_path = out_dir / f"{input_file.stem}_report.md"
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(render_markdown(report))

            print(f"✅ Success! Reports generated in '{out_dir}' folder.")
            print(f"   - JSON: {json_path.name}")
            print(f"   - MD:   {md_path.name}")

        except Exception as e:
            print(f" An error occurred: {e}")

if __name__ == "__main__":
    main()
import json
import time
import typer
from pathlib import Path

from csv_profiler.io import read_csv_rows
from csv_profiler.profiling import profile_rows
from csv_profiler.render import render_markdown

app = typer.Typer()

@app.command(help="Profile a CSV file and write JSON + Markdown")
def profile(
    input_path: Path = typer.Argument(..., help="Input CSV file"),
    out_dir: Path = typer.Option(Path("outputs"), "--out-dir", help="Output folder"),
    report_name: str = typer.Option("report", "--report-name", help="Base name for outputs"),
    preview: bool = typer.Option(False, "--preview", help="Print a short summary"),
):
    ...  # (implementation)

if __name__ == "__main__":
    app()