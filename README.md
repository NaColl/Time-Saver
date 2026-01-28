# Content Agent - Personal Time-Saving Assistant

Transform your weekly Substack posts into 21 platform-optimized social media posts with one command.

## What It Does

```
1 Substack Post → 7 LinkedIn + 7 Twitter + 7 Substack Notes
```

Each post is optimized for its platform with proven engagement formats:

| Platform | Post Types |
|----------|-----------|
| **LinkedIn** | Hook, Story, Listicle, Question, Contrarian, How-To, CTA |
| **Twitter/X** | Single Tweets, Threads (5-7 tweets), CTA Tweets |
| **Substack Notes** | Conversational insights, quotes, discussions |

## Quick Start

### 1. Install

```bash
cd Time-Saver
pip install -e .
```

### 2. Configure

```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

### 3. Generate Content

```bash
# Generate from your latest Substack posts
content-agent generate

# Generate from a specific article
content-agent generate --url "https://theinterneteconomy.xyz/p/your-article"

# Preview before generating
content-agent generate --dry-run
```

## Output

Each run creates an organized folder:

```
output/2026-01-28_your-article-slug/
├── README.md              # Schedule overview
├── linkedin/
│   ├── day_1_monday_hook.md
│   ├── day_2_tuesday_story.md
│   └── ... (7 posts)
├── twitter/
│   ├── day_1_monday_tweet.md
│   ├── day_2_tuesday_thread.md
│   └── ... (7 posts)
├── notes/
│   └── ... (7 posts)
├── all_posts.md           # Everything in one file
├── schedule.json          # Machine-readable for n8n
├── buffer_linkedin.csv    # Import to Buffer
└── typefully_twitter.csv  # Import to Typefully
```

## Posting Workflow

Since you don't have API access to LinkedIn/X:

### Twitter/X
1. Use [Typefully](https://typefully.com) (free tier available)
2. Import `typefully_twitter.csv` to schedule posts
3. Supports threads natively

### LinkedIn
1. Use [Buffer](https://buffer.com) free tier, OR
2. Copy-paste from markdown files (character count included)

### Substack Notes
1. Copy-paste from notes folder
2. Each note is formatted for easy posting

## CLI Commands

```bash
# Generate content from latest posts
content-agent generate

# Generate from specific URL
content-agent generate --url "https://..."

# Generate for one platform only
content-agent generate --platform linkedin

# Preview without saving
content-agent generate --dry-run

# Custom output directory
content-agent generate --output ./my-content

# List configured Substacks
content-agent list-sources

# Preview an article
content-agent preview "https://..."
```

## n8n Workflows

The `n8n/workflows/` folder includes ready-to-import automations:

### Content Automation
- **content_generation.json** - Weekly content generation pipeline

### Investment Professional Tools
- **earnings_calendar_monitor.json** - Earnings alerts for your watchlist
- **sec_filing_alerts.json** - SEC 8-K, 10-K, 10-Q filing alerts
- **stock_price_alerts.json** - Price threshold & movement alerts
- **financial_report_generator.json** - Weekly portfolio P&L reports

See `n8n/workflows/README.md` for setup instructions.

## Configuration

### Environment Variables

```bash
# Required
ANTHROPIC_API_KEY=sk-ant-xxxxx

# Optional (defaults shown)
CLAUDE_MODEL=claude-sonnet-4-20250514
TIMEZONE=Europe/Helsinki
POST_TIME=17:00
OUTPUT_DIR=./output
```

### Adding/Changing Substacks

Edit `src/content_agent/config.py`:

```python
DEFAULT_SUBSTACKS = [
    SubstackSource(
        name="The Internet Economy",
        url="https://theinterneteconomy.xyz",
        category="general"
    ),
    SubstackSource(
        name="Automated Alpha",
        url="https://automatedalpha.substack.com",
        category="investment"
    ),
    # Add more here
]
```

## Content Optimization

The prompts are optimized based on what works on each platform:

### LinkedIn
- **Hook posts**: Bold opening statement, curiosity gap, reveal, close
- **Story posts**: Scene setting, challenge, turning point, lesson
- **Listicles**: Number + promise, scannable bullets, clear takeaways
- **Contrarian**: Challenge common wisdom with evidence

### Twitter/X
- **Single tweets**: Under 280 chars, punchy, quotable
- **Threads**: Strong hook, one point per tweet, summary + CTA

### Voice Guidelines (baked into prompts)
- Authoritative but approachable
- Data-driven with specific examples
- Contrarian when appropriate
- Practical and actionable
- No emojis unless source uses them
- Minimal hashtags (end only)

## Cost

Using Claude Sonnet:
- ~$0.25 per article processed
- ~$2-3/month for weekly publishing

## Project Structure

```
Time-Saver/
├── src/content_agent/
│   ├── main.py           # CLI interface
│   ├── config.py         # Configuration
│   ├── fetcher/          # RSS/article fetching
│   ├── generator/        # AI content generation
│   ├── prompts/          # Platform-specific prompts
│   ├── models/           # Data models
│   └── output/           # Writers (MD, JSON, CSV)
├── n8n/workflows/        # n8n automation templates
├── output/               # Generated content
└── tests/
```

## License

MIT
