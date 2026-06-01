# 🍴 Yelp API: Search, Business Details & Reviews (Python + MCP)

> The most efficient, reliable, and developer-friendly way to use the Yelp API on Apify, from Python or as an MCP tool in Claude and Cursor.

This is a quick-start for a three-part Yelp API suite. The actors are designed to chain: search for businesses, then pull full details and reviews for any result.

**Yelp Search API:** [apify.com/johnvc/yelp-search-api](https://apify.com/johnvc/yelp-search-api?fpr=9n7kx3) - ranked business listings for a query and location.
**Yelp Business Details API:** [apify.com/johnvc/yelp-place-api](https://apify.com/johnvc/yelp-place-api?fpr=9n7kx3) - full business profiles (hours, amenities, menus).
**Yelp Reviews API:** [apify.com/johnvc/yelp-reviews-api](https://apify.com/johnvc/yelp-reviews-api?fpr=9n7kx3) - ratings and review text for a business.

Each returns clean, structured JSON. The Search API returns a `place_ids` array on every business; feed the first (encoded) id into the Business Details and Reviews APIs to enrich any result. No browser automation, no captchas, predictable pay-per-use pricing.

## Video Walkthrough

[![Watch the walkthrough](https://img.youtube.com/vi/jREWahDGhJM/maxresdefault.jpg)](https://www.youtube.com/watch?v=jREWahDGhJM)

## Quick Start

### Prerequisites
- Python 3.11 or higher
- An Apify account and API key ([get a free key here](https://apify.com?fpr=9n7kx3))

1. **Clone the repository**
   ```bash
   git clone https://github.com/johnisanerd/Apify-Yelp-API.git
   cd Apify-Yelp-API
   ```

2. **Install dependencies with UV**
   ```bash
   # Install UV if you do not have it:
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # Install project dependencies:
   uv sync
   ```

3. **Configure your API key**
   ```bash
   cp .env.example .env
   # Edit .env and add your Apify API key
   # Get your free API key at: https://apify.com?fpr=9n7kx3
   ```

4. **Run the example**
   ```bash
   uv run python yelp-api-example.py
   ```

The example runs the full chain: it searches for coffee shops in New York, takes the top result's `place_id`, then fetches that business's full profile and its latest reviews. Inputs are kept small so your first run stays inexpensive.

### Alternative: set the API key directly
```bash
export APIFY_API_TOKEN="your_api_key_here"
uv run python yelp-api-example.py
```

## Why Use This Yelp API?

**One clean JSON contract.** Every endpoint returns structured, predictable JSON, so you spend your time using the data, not parsing HTML.

**Built to chain.** The Search API hands you `place_ids` for every business. Pass them straight into the Business Details and Reviews APIs to build a complete picture of any place.

**Reliable by design.** These are API-backed, not browser-driven, so there are no captchas and no layout breakage to babysit.

**Predictable pricing.** Pay-per-event billing means a search page, a business profile, or a page of reviews each cost a fixed, known amount.

**Agent-ready.** Every actor is available over MCP, so Claude and Cursor can call the Yelp API directly in natural language (setup below).

## Features

### Core Capabilities
- Ranked business listings by keyword and location, with sorting and category, price, and area filters.
- Full business profiles: rating, reviews, price, categories, phone, address, hours, amenities, popular items, and optional full menus.
- Review extraction: rating, full text, date, reviewer details, photos, owner replies, and helpful votes, with sorting and star filters.

### Data Quality
- Encoded and human-readable `place_ids` on every search result for easy chaining.
- The Search API also returns the available refinement filters (price, distance, neighborhoods, categories) so you can narrow follow-up queries.
- Pagination is handled for you with a simple `max_pages` control.

## Usage Examples

### Basic Example (Search)
```json
{
  "search_term": "coffee",
  "location": "New York, NY",
  "max_pages": 1
}
```

### Advanced Example (Search with filters)
```json
{
  "search_term": "steakhouse",
  "location": "Austin, TX",
  "sort_by": "rating",
  "category_filter": "steak",
  "attrs": "RestaurantsPriceRange2.2",
  "max_pages": 2
}
```

### Business Details (by place_id from a search result)
```json
{
  "place_ids": ["ED7A7vDdg8yLNKJTSVHHmg"],
  "full_menu": false
}
```

### Reviews (by encoded place_id)
```json
{
  "place_id": "ED7A7vDdg8yLNKJTSVHHmg",
  "sort_by": "date_desc",
  "rating": "5",
  "max_pages": 1
}
```

## Input Parameters

### Yelp Search API
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `location` | `str` | YES | - | City and state, address, or ZIP (e.g. `New York, NY`). |
| `search_term` | `str` | no | - | What to search for (e.g. `coffee`). Blank browses all in the location. |
| `category_filter` | `str` | no | - | Yelp category alias (e.g. `restaurants`). |
| `sort_by` | `str` | no | `recommended` | `recommended`, `rating`, or `review_count`. |
| `attrs` | `str` | no | - | Price and feature filters (e.g. `RestaurantsPriceRange2.2`). |
| `radius_filter` | `str` | no | - | Distance radius or neighborhood value. |
| `max_pages` | `int` | no | `1` | Pages to fetch (~10 businesses each). Each page is billed separately. |

### Yelp Business Details API
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `place_ids` | `list[str]` | YES | - | One or more Yelp place ids or aliases (from a search result). |
| `full_menu` | `bool` | no | `false` | Return the structured full menu instead of the profile. |
| `menu_name` | `str` | no | - | Which menu to fetch when a business has more than one. |
| `business_alert` | `bool` | no | `false` | Include the business alert message when present. |

### Yelp Reviews API
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `place_id` | `str` | YES | - | The encoded place id (first entry of a search result's `place_ids`). |
| `sort_by` | `str` | no | relevance | `relevance_desc`, `date_desc`, `date_asc`, `rating_desc`, `rating_asc`, `elites_desc`. |
| `rating` | `str` | no | - | Filter by stars, e.g. `5` or `4,5`. |
| `q` | `str` | no | - | Keep only reviews mentioning this keyword. |
| `max_pages` | `int` | no | `1` | Pages to fetch (up to 49 reviews each). |

## Output Format

**Search** returns one item per page, each with an `organic_results` array. Search results carry the `place_ids` you chain into the Business Details and Reviews APIs; rating, review counts, and price come back from the Business Details API.
```json
{
  "page_number": 1,
  "organic_results": [
    {
      "position": 1,
      "place_ids": ["gcEb-XsHQEZj7lxyOHJC3g", "mandarin-coffee-roastery-new-york"],
      "title": "Mandarin Coffee Roastery",
      "link": "https://www.yelp.com/biz/mandarin-coffee-roastery-new-york",
      "categories": [{ "title": "Coffee Roasteries" }, { "title": "Coffee & Tea Shops" }],
      "open_state": "Closed until 8:00 am",
      "thumbnail": "https://s3-media0.fl.yelpcdn.com/bphoto/.../ls.jpg"
    }
  ]
}
```

**Business Details** returns one item per place id, with a `place_results` profile:
```json
{
  "place_id": "maman-new-york-22",
  "place_results": {
    "name": "Maman",
    "rating": 3.9,
    "reviews": 897,
    "price": "$$",
    "phone": "(212) 226-0700",
    "address": "239 Centre St New York, NY 10013",
    "operation_hours": { "hours": [{ "day": "Mon", "hours": "7:30 AM - 6:00 PM" }] }
  }
}
```

**Reviews** returns one item per page, each with a `reviews` array:
```json
{
  "page_number": 1,
  "reviews": [
    {
      "rating": 5,
      "date": "2026-05-20T15:49:59Z",
      "user": { "name": "Jane D.", "location": "New York, NY" },
      "comment": { "text": "Perfect cup of coffee...", "language": "en" },
      "feedback": { "useful": 3, "funny": 0, "cool": 1 }
    }
  ]
}
```

---

## Use as an MCP tool

You can load the Yelp API as an MCP tool so assistants call it for you. The MCP server URL preloads all three Yelp actors:

```
https://mcp.apify.com/?tools=actors,docs,johnvc/yelp-search-api,johnvc/yelp-place-api,johnvc/yelp-reviews-api
```

Authenticate with OAuth in the browser when offered, or with your Apify API token (the same `APIFY_API_TOKEN` used by the Python example). Get a token at https://console.apify.com/settings/integrations and a free Apify account at https://apify.com?fpr=9n7kx3 .

## Install in Claude Cowork Desktop

![Install in Claude Cowork Desktop](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_claude_desktop.png)

Cowork is the desktop app's automation mode. To give it the Yelp API as a tool, add the Apify MCP server as a connector.

1. Open the Claude desktop app and go to **Settings → Connectors** (or **Settings → Developer → Edit Config** to edit `claude_desktop_config.json` directly).
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
2. Add the Apify MCP server, preloaded with the three Yelp actors:

```json
{
  "mcpServers": {
    "apify": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://mcp.apify.com/?tools=actors,docs,johnvc/yelp-search-api,johnvc/yelp-place-api,johnvc/yelp-reviews-api"
      ]
    }
  }
}
```

3. Restart the app. When Cowork first calls the tool, complete the OAuth prompt in your browser, or add your Apify API token in the connector settings to skip OAuth.
4. In a Cowork chat, confirm the tool is available and ask it to run the Yelp API.

Download the desktop app and start a free trial: https://claude.ai/referral/uIlpa7nPLg
More help: https://docs.apify.com/platform/integrations/claude-desktop

## Install in Claude Code

![Install in Claude Code](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_claude_code.png)

Claude Code is the command-line tool. Add the Yelp API's MCP server with one command:

```bash
claude mcp add --transport http apify \
  "https://mcp.apify.com/?tools=actors,docs,johnvc/yelp-search-api,johnvc/yelp-place-api,johnvc/yelp-reviews-api"
```

To use a token instead of browser OAuth:

```bash
claude mcp add --transport http apify \
  "https://mcp.apify.com/?tools=actors,docs,johnvc/yelp-search-api,johnvc/yelp-place-api,johnvc/yelp-reviews-api" \
  --header "Authorization: Bearer YOUR_APIFY_TOKEN"
```

Then verify with `claude mcp list`, or run `/mcp` inside a session. Ask Claude Code to call the Yelp API.

Try Claude Code free: https://claude.ai/referral/uIlpa7nPLg
Claude Code MCP docs: https://code.claude.com/docs/en/mcp

## Install in Claude (website)

![Install in Claude (website)](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_claude_ai.png)

On claude.ai you add Apify as a connector, then enable the Yelp API tools.

1. Go to **Settings → Connectors → Browse connectors** and search for **Apify MCP server**. Install it (enable or update if prompted).
2. When connecting, authenticate with your Apify API token, and enable the tools `johnvc/yelp-search-api`, `johnvc/yelp-place-api`, and `johnvc/yelp-reviews-api`.
3. In any chat, open **+ → Connectors** and turn on **Apify**.
4. Alternatively, choose **Add custom connector** and paste the full MCP URL `https://mcp.apify.com/?tools=actors,docs,johnvc/yelp-search-api,johnvc/yelp-place-api,johnvc/yelp-reviews-api`, using OAuth when prompted.
5. Ask Claude to run the Yelp API.

Open Claude on the web: https://claude.ai

## Install in Cursor

![Install in Cursor](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_cursor.png)

Cursor reads MCP servers from a project file at `.cursor/mcp.json`.

1. In your project, create `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "apify": {
      "url": "https://mcp.apify.com/?tools=actors,docs,johnvc/yelp-search-api,johnvc/yelp-place-api,johnvc/yelp-reviews-api"
    }
  }
}
```

2. If you prefer token auth over browser OAuth, add a header:

```json
{
  "mcpServers": {
    "apify": {
      "url": "https://mcp.apify.com/?tools=actors,docs,johnvc/yelp-search-api,johnvc/yelp-place-api,johnvc/yelp-reviews-api",
      "headers": { "Authorization": "Bearer YOUR_APIFY_TOKEN" }
    }
  }
}
```

3. Open **Cursor → Settings → MCP** and confirm the **apify** server is connected (green dot).
4. In Composer or Chat, ask Cursor to call the Yelp API.

New to Cursor? Get it here: https://cursor.com/referral?code=XQP4VBLI3NNX

## Install in ChatGPT

![Install in ChatGPT](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_ChatGPT.png)

ChatGPT connects to the Apify MCP server through Developer mode (available on ChatGPT Pro, Plus, Business, Enterprise, and Education plans).

1. Click your profile icon, then go to **Settings > Apps**. If you do not see a **Create app** button, open **Advanced settings** and enable **Developer mode**.
2. Click **Create app** and fill out the form:
   - **Name:** Apify
   - **MCP Server URL:** `https://mcp.apify.com/?tools=actors,docs,johnvc/yelp-search-api,johnvc/yelp-place-api,johnvc/yelp-reviews-api`
   - **Authentication:** OAuth
3. Click **Create** and authorize the connection with Apify.
4. To use the app in a conversation, click **+** in the chat, choose **Developer mode**, and select **Apify**.

More help: https://docs.apify.com/platform/integrations/mcp

---

[**Made with care**](https://apify.com/johnvc?fpr=9n7kx3)

*Use the Yelp API to power your data workflows with reliable, structured results.*

Last Updated: 2026.06.02
