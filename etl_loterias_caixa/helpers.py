from pathlib import Path
import tempfile
import subprocess

def normalize_excel_with_libreoffice(path: Path) -> None:
    path = path.resolve()

    with tempfile.TemporaryDirectory() as tmp:

        tmpdir = Path(tmp)
        input_file = tmpdir / path.name
        output_file = tmpdir / 'normalized' / path.name

        # Copy original file into temp
        input_file.write_bytes(path.read_bytes())

        # Run LibreOffice: input != output
        subprocess.run(
            [
                "libreoffice",
                "--headless",
                "--calc",
                "--convert-to", "xlsx",
                input_file.name,
                "--outdir", 'normalized',
            ],
            cwd=tmpdir,
            check=True,
        )
        
        output_file.replace(path)
