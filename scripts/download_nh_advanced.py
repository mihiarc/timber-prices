"""
Advanced download script for New Hampshire stumpage price data.

This script tries multiple approaches to bypass Akamai bot protection:
1. httpx with browser-like headers and HTTP/2
2. cloudscraper (anti-bot scraping library)
3. requests with session and retry logic
"""

import time
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

# Base URL and PDF files
BASE_URL = "https://www.revenue.nh.gov/sites/g/files/ehbemt736/files/inline-documents/sonh/municipal-property/"
PDF_URLS = [
    "avg-stump-val-10-24-03-25.pdf",  # October 2024 - March 2025
    "avg-stump-val-04-24-09-24.pdf",  # April 2024 - September 2024
    "avg-stump-val-10-23-03-24.pdf",  # October 2023 - March 2024
    "avg-stump-val-04-23-09-23.pdf",  # April 2023 - September 2023
    "avg-stump-val-10-22-03-23.pdf",  # October 2022 - March 2023
    "avg-stump-val-04-22-09-22.pdf",  # April 2022 - September 2022
    "avg-stump-val-10-21-03-22.pdf",  # October 2021 - March 2022
    "avg-stump-val-04-21-09-21.pdf",  # April 2021 - September 2021
]


def try_httpx_download(url: str, output_path: Path) -> bool:
    """Try downloading with httpx using HTTP/2 and browser headers."""
    try:
        import httpx

        console.print(f"[cyan]Trying httpx with HTTP/2:[/cyan] {url}")

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
        }

        with httpx.Client(http2=True, headers=headers, timeout=30.0, follow_redirects=True) as client:
            response = client.get(url)
            response.raise_for_status()

            # Check if we got HTML (bot protection)
            content_type = response.headers.get('content-type', '')
            if 'html' in content_type.lower():
                console.print(f"[yellow]Got HTML instead of PDF (likely bot protection)[/yellow]")
                return False

            output_path.write_bytes(response.content)
            console.print(f"[green]Success with httpx! Saved to:[/green] {output_path}")
            return True

    except ImportError:
        console.print("[yellow]httpx not installed[/yellow]")
        return False
    except Exception as exception:
        console.print(f"[yellow]httpx failed:[/yellow] {exception}")
        return False


def try_cloudscraper_download(url: str, output_path: Path) -> bool:
    """Try downloading with cloudscraper (anti-bot library)."""
    try:
        import cloudscraper

        console.print(f"[cyan]Trying cloudscraper:[/cyan] {url}")

        scraper = cloudscraper.create_scraper(
            browser={
                'browser': 'chrome',
                'platform': 'darwin',
                'desktop': True
            }
        )

        response = scraper.get(url, timeout=30)
        response.raise_for_status()

        # Check if we got HTML (bot protection)
        content_type = response.headers.get('content-type', '')
        if 'html' in content_type.lower():
            console.print(f"[yellow]Got HTML instead of PDF (likely bot protection)[/yellow]")
            return False

        output_path.write_bytes(response.content)
        console.print(f"[green]Success with cloudscraper! Saved to:[/green] {output_path}")
        return True

    except ImportError:
        console.print("[yellow]cloudscraper not installed[/yellow]")
        return False
    except Exception as exception:
        console.print(f"[yellow]cloudscraper failed:[/yellow] {exception}")
        return False


def try_requests_with_session(url: str, output_path: Path) -> bool:
    """Try downloading with requests using session and retry logic."""
    try:
        import requests
        from requests.adapters import HTTPAdapter
        from urllib3.util.retry import Retry

        console.print(f"[cyan]Trying requests with session:[/cyan] {url}")

        session = requests.Session()

        # Configure retry strategy
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
        }

        response = session.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        # Check if we got HTML (bot protection)
        content_type = response.headers.get('content-type', '')
        if 'html' in content_type.lower():
            console.print(f"[yellow]Got HTML instead of PDF (likely bot protection)[/yellow]")
            return False

        output_path.write_bytes(response.content)
        console.print(f"[green]Success with requests! Saved to:[/green] {output_path}")
        return True

    except Exception as exception:
        console.print(f"[yellow]requests failed:[/yellow] {exception}")
        return False


def download_pdf_multi_attempt(url: str, output_path: Path) -> bool:
    """Try multiple download methods in sequence."""

    # Method 1: httpx with HTTP/2
    if try_httpx_download(url, output_path):
        return True

    time.sleep(2)

    # Method 2: cloudscraper
    if try_cloudscraper_download(url, output_path):
        return True

    time.sleep(2)

    # Method 3: requests with session
    if try_requests_with_session(url, output_path):
        return True

    return False


def main():
    """Main execution function."""
    console.print("\n[bold blue]Advanced NH Stumpage PDF Downloader[/bold blue]\n")

    # Setup directories
    data_dir = Path("/Users/mihiarc/landuse-model/forest-rents/data/raw/nh_dra")
    data_dir.mkdir(parents=True, exist_ok=True)

    pdf_dir = data_dir / "pdfs"
    pdf_dir.mkdir(exist_ok=True)

    console.print("[bold]Attempting to download PDFs using multiple methods[/bold]\n")

    successful_downloads = []
    failed_downloads = []

    for pdf_filename in PDF_URLS:
        console.print(f"\n[bold cyan]Processing: {pdf_filename}[/bold cyan]")
        url = BASE_URL + pdf_filename
        output_path = pdf_dir / pdf_filename

        if download_pdf_multi_attempt(url, output_path):
            successful_downloads.append(pdf_filename)
        else:
            failed_downloads.append(pdf_filename)
            console.print(f"[red]All methods failed for {pdf_filename}[/red]")

        # Be polite - wait between files
        time.sleep(3)

    # Summary
    console.print(f"\n[bold]Download Summary[/bold]")
    console.print(f"[green]Successful: {len(successful_downloads)}[/green]")
    console.print(f"[red]Failed: {len(failed_downloads)}[/red]")

    if successful_downloads:
        console.print("\n[green]Successfully downloaded:[/green]")
        for filename in successful_downloads:
            console.print(f"  - {filename}")

    if failed_downloads:
        console.print("\n[red]Failed to download:[/red]")
        for filename in failed_downloads:
            console.print(f"  - {filename}")
        console.print("\n[yellow]These files may need to be downloaded manually.[/yellow]")
        console.print(f"[yellow]Visit: https://www.revenue.nh.gov/taxes-glance/timber-tax/average-stumpage-value-information[/yellow]")


if __name__ == "__main__":
    main()
