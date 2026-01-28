"""CLI interface for Content Agent."""

import typer
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from pathlib import Path
from typing import Optional

from .config import get_settings, get_substacks
from .fetcher import SubstackFetcher
from .generator import ContentGenerator
from .output import MarkdownWriter, JSONExporter, CSVExporter

app = typer.Typer(
    name="content-agent",
    help="Transform Substack posts into platform-optimized social media content.",
    add_completion=False,
)
console = Console()


@app.command()
def generate(
    url: Optional[str] = typer.Option(
        None,
        "--url", "-u",
        help="Specific article URL to process (default: latest from all Substacks)"
    ),
    platform: Optional[str] = typer.Option(
        None,
        "--platform", "-p",
        help="Generate only for specific platform (linkedin, twitter, notes)"
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Preview without saving files"
    ),
    output_dir: Optional[str] = typer.Option(
        None,
        "--output", "-o",
        help="Output directory (default: ./output)"
    ),
):
    """Generate social media content from Substack articles."""
    try:
        settings = get_settings()
    except Exception as e:
        console.print(f"[red]Error loading settings: {e}[/red]")
        console.print("[yellow]Make sure you have a .env file with ANTHROPIC_API_KEY set.[/yellow]")
        raise typer.Exit(1)

    if output_dir:
        settings.output_dir = output_dir

    substacks = get_substacks()

    console.print(Panel.fit(
        "[bold blue]Content Agent[/bold blue]\n"
        "Transforming your Substack into social gold ✨",
        border_style="blue"
    ))

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        # Fetch articles
        fetch_task = progress.add_task("Fetching articles...", total=None)

        with SubstackFetcher(substacks) as fetcher:
            if url:
                article = fetcher.fetch_article_by_url(url)
                articles = [article] if article else []
            else:
                articles = fetcher.fetch_latest_posts(limit=1)

        progress.update(fetch_task, completed=True)

        if not articles:
            console.print("[red]No articles found to process.[/red]")
            raise typer.Exit(1)

        # Process each article
        generator = ContentGenerator(settings)
        markdown_writer = MarkdownWriter(settings.output_dir)
        json_exporter = JSONExporter(settings.output_dir)
        csv_exporter = CSVExporter(settings.output_dir)

        for article in articles:
            console.print(f"\n[bold]Processing:[/bold] {article.title}")
            console.print(f"[dim]Source: {article.source_substack}[/dim]")
            console.print(f"[dim]Words: {article.word_count}[/dim]")

            # Generate content
            gen_task = progress.add_task("Generating content...", total=None)
            week = generator.generate_week(article)
            progress.update(gen_task, completed=True)

            if dry_run:
                console.print("\n[yellow]DRY RUN - Preview only[/yellow]")
                _show_preview(week)
            else:
                # Write outputs
                write_task = progress.add_task("Writing files...", total=None)

                folder_path = markdown_writer.write_week(week)
                json_exporter.export_week(week, folder_path)
                csv_exporter.export_week(week, folder_path)

                progress.update(write_task, completed=True)

                console.print(f"\n[green]✓ Generated {week.total_posts} posts[/green]")
                console.print(f"[green]✓ Output saved to: {folder_path}[/green]")

                # Show summary table
                _show_summary(week, folder_path)


@app.command()
def list_sources():
    """List configured Substack sources."""
    substacks = get_substacks()

    table = Table(title="Configured Substacks")
    table.add_column("Name", style="cyan")
    table.add_column("URL", style="blue")
    table.add_column("Category", style="green")
    table.add_column("RSS", style="dim")

    for sub in substacks:
        table.add_row(sub.name, sub.url, sub.category, sub.rss)

    console.print(table)


@app.command()
def preview(
    url: str = typer.Argument(..., help="Article URL to preview"),
):
    """Preview article content before generating."""
    substacks = get_substacks()

    with SubstackFetcher(substacks) as fetcher:
        article = fetcher.fetch_article_by_url(url)

    if not article:
        console.print("[red]Could not fetch article.[/red]")
        raise typer.Exit(1)

    console.print(Panel.fit(
        f"[bold]{article.title}[/bold]\n\n"
        f"Source: {article.source_substack}\n"
        f"Category: {article.category}\n"
        f"Words: {article.word_count}\n"
        f"URL: {article.url}",
        title="Article Preview",
        border_style="blue"
    ))

    console.print("\n[bold]Content Preview (first 500 chars):[/bold]")
    console.print(article.content[:500] + "...")


def _show_preview(week):
    """Show a preview of generated content."""
    console.print("\n[bold]LinkedIn Posts Preview:[/bold]")
    for post in week.linkedin_posts[:2]:
        console.print(Panel(
            post.content[:300] + "..." if len(post.content) > 300 else post.content,
            title=f"Day {post.day_number} - {post.post_type.value}",
            border_style="blue"
        ))

    console.print("\n[bold]Twitter Posts Preview:[/bold]")
    for post in week.twitter_posts[:2]:
        content = post.formatted_content
        console.print(Panel(
            content[:280] + "..." if len(content) > 280 else content,
            title=f"Day {post.day_number} - {post.post_type.value}",
            border_style="cyan"
        ))


def _show_summary(week, folder_path: Path):
    """Show summary of generated content."""
    table = Table(title="\nGenerated Content Summary")
    table.add_column("Platform", style="cyan")
    table.add_column("Posts", style="green")
    table.add_column("Files", style="blue")

    table.add_row(
        "LinkedIn",
        str(len(week.linkedin_posts)),
        str(folder_path / "linkedin")
    )
    table.add_row(
        "Twitter",
        str(len(week.twitter_posts)),
        str(folder_path / "twitter")
    )
    table.add_row(
        "Substack Notes",
        str(len(week.notes_posts)),
        str(folder_path / "notes")
    )

    console.print(table)

    console.print("\n[bold]Export Files:[/bold]")
    console.print(f"  • Markdown: {folder_path / 'all_posts.md'}")
    console.print(f"  • JSON (n8n): {folder_path / 'schedule.json'}")
    console.print(f"  • CSV (Buffer): {folder_path / 'buffer_linkedin.csv'}")
    console.print(f"  • CSV (Typefully): {folder_path / 'typefully_twitter.csv'}")


if __name__ == "__main__":
    app()
