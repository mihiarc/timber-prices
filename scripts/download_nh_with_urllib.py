"""
Download NH DRA PDFs using urllib with custom SSL context.
"""

import ssl
import urllib.request
from pathlib import Path
from rich.console import Console

console = Console()

BASE_URL = "https://www.revenue.nh.gov/sites/g/files/ehbemt736/files/inline-documents/sonh/municipal-property/"

PDF_URLS = [
    "avg-stump-val-10-24-03-25.pdf",
    "avg-stump-val-04-24-09-24.pdf",
]


def download_pdf(url: str, output_path: Path) -> bool:
    """Download a PDF file using urllib."""
    try:
        console.print(f"[cyan]Downloading:[/cyan] {url}")

        # Create custom SSL context
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = True
        ssl_context.verify_mode = ssl.CERT_REQUIRED

        # Create request with headers
        request = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }
        )

        # Open URL with custom SSL context
        with urllib.request.urlopen(request, context=ssl_context, timeout=30) as response:
            content = response.read()

            # Check content type
            content_type = response.headers.get('Content-Type', '')
            if 'html' in content_type.lower():
                console.print(f"[yellow]Received HTML instead of PDF (likely blocked)[/yellow]")
                console.print(f"Content preview: {content[:200]}")
                return False

            output_path.write_bytes(content)
            console.print(f"[green]Saved:[/green] {output_path} ({len(content)} bytes)")
            return True

    except urllib.error.HTTPError as error:
        console.print(f"[yellow]HTTP error {error.code}:[/yellow] {error.reason}")
        return False
    except Exception as exception:
        console.print(f"[yellow]Failed:[/yellow] {exception}")
        return False


def main():
    """Main function."""
    console.print("\n[bold blue]NH DRA PDF Downloader (urllib)[/bold blue]\n")

    data_dir = Path("/Users/mihiarc/landuse-model/forest-rents/data/raw/nh_dra")
    pdf_dir = data_dir / "pdfs"
    pdf_dir.mkdir(parents=True, exist_ok=True)

    downloaded_count = 0
    for pdf_filename in PDF_URLS:
        url = BASE_URL + pdf_filename
        output_path = pdf_dir / pdf_filename

        if download_pdf(url, output_path):
            downloaded_count += 1

    console.print(f"\n[bold]Downloaded {downloaded_count}/{len(PDF_URLS)} PDFs[/bold]")


if __name__ == "__main__":
    main()
