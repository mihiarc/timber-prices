"""
Alternative download script using httpx with better HTTP/2 support.
"""

import asyncio
from pathlib import Path
import httpx
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

# Base URL pattern for NH DRA stumpage value PDFs
BASE_URL = "https://www.revenue.nh.gov/sites/g/files/ehbemt736/files/inline-documents/sonh/municipal-property/"

# Known PDF URLs
PDF_URLS = [
    "avg-stump-val-10-24-03-25.pdf",  # October 2024 - March 2025
    "avg-stump-val-04-24-09-24.pdf",  # April 2024 - September 2024
    "avg-stump-val-10-23-03-24.pdf",  # October 2023 - March 2024
    "avg-stump-val-04-23-09-23.pdf",  # April 2023 - September 2023
]


async def download_pdf_async(client: httpx.AsyncClient, url: str, output_path: Path) -> bool:
    """Download a PDF file asynchronously.

    Args:
        client: httpx AsyncClient instance
        url: Full URL to the PDF file
        output_path: Local path to save the PDF

    Returns:
        True if download was successful, False otherwise
    """
    try:
        console.print(f"[cyan]Downloading:[/cyan] {url}")

        response = await client.get(url, follow_redirects=True)
        response.raise_for_status()

        # Check if we got HTML instead of PDF (error page)
        content_type = response.headers.get('content-type', '')
        if 'html' in content_type.lower():
            console.print(f"[yellow]Received HTML instead of PDF (likely blocked)[/yellow]")
            return False

        output_path.write_bytes(response.content)
        console.print(f"[green]Saved:[/green] {output_path} ({len(response.content)} bytes)")
        return True

    except httpx.HTTPStatusError as exception:
        console.print(f"[yellow]HTTP error downloading {url}:[/yellow] {exception}")
        return False
    except Exception as exception:
        console.print(f"[yellow]Failed to download {url}:[/yellow] {exception}")
        return False


async def main():
    """Main async execution function."""
    console.print("\n[bold blue]NH DRA PDF Downloader (httpx)[/bold blue]\n")

    # Setup directories
    data_dir = Path("/Users/mihiarc/landuse-model/forest-rents/data/raw/nh_dra")
    pdf_dir = data_dir / "pdfs"
    pdf_dir.mkdir(parents=True, exist_ok=True)

    # Configure httpx client with browser-like headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Cache-Control': 'max-age=0',
    }

    downloaded_count = 0

    async with httpx.AsyncClient(
        headers=headers,
        timeout=30.0,
        follow_redirects=True,
    ) as client:
        for pdf_filename in PDF_URLS:
            url = BASE_URL + pdf_filename
            output_path = pdf_dir / pdf_filename

            if await download_pdf_async(client, url, output_path):
                downloaded_count += 1

            # Small delay between requests
            await asyncio.sleep(2)

    console.print(f"\n[bold]Downloaded {downloaded_count}/{len(PDF_URLS)} PDFs successfully[/bold]")

    if downloaded_count > 0:
        console.print("\n[green]You can now run:[/green]")
        console.print("  uv run python scripts/parse_nh_stumpage.py")
    else:
        console.print("\n[yellow]No PDFs were downloaded. The site may be blocking automated access.[/yellow]")
        console.print("[yellow]Please try manually downloading PDFs from:[/yellow]")
        console.print("https://www.revenue.nh.gov/taxes-glance/timber-tax/average-stumpage-value-information")


if __name__ == "__main__":
    asyncio.run(main())
