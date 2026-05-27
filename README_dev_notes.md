# Dev Notes (internal)

Internal notes for this example repo. Public, but not the focus of the repo.

## Source actors (Apify, user johnvc)
- Yelp Search API: slug `yelp-search-api`, actor ID `LkdRlXNXYaYcO7f01`
- Yelp Business Details API: slug `yelp-place-api`, actor ID `vOPAbDdSkn2ggeWU5`
- Yelp Reviews API: slug `yelp-reviews-api`, actor ID `iTiaAgy1XorGxqnqD`

The three chain: Search returns `place_ids`; the first (encoded) id feeds Business Details and Reviews. The Reviews API requires the encoded id, not the human-readable alias.

## MCP server URL (suite)
```
https://mcp.apify.com/?tools=actors,docs,johnvc/yelp-search-api,johnvc/yelp-place-api,johnvc/yelp-reviews-api
```

## Referral codes
- Apify: every `apify.com` link carries `?fpr=9n7kx3` (docs., mcp., console. exempt).
- Cursor: `cursor.com` links carry `?code=XQP4VBLI3NNX`.
- Claude: TODO - no real Claude referral code yet. The `claude.ai` / `claude.com` links use the literal `CLAUDE_REFERRAL` placeholder. Find-and-replace once a real code exists.

## Screenshots - TODO (currently placeholders)
The four files under `screenshots/` are blank placeholders. Replace each with a real
screenshot from the Apify MCP configurator. Open this URL in a browser:
`https://mcp.apify.com/?tools=actors,docs,johnvc/yelp-search-api,johnvc/yelp-place-api,johnvc/yelp-reviews-api`
then capture each client's setup tab:
- `screenshots/01-claude-cowork-desktop.png` - Claude Desktop / Connectors config
- `screenshots/02-claude-code.png` - Claude Code `claude mcp add` command
- `screenshots/03-claude-website.png` - claude.ai Connectors / custom connector
- `screenshots/04-cursor.png` - Cursor `.cursor/mcp.json` snippet

## Reference links
- Apify MCP: https://docs.apify.com/platform/integrations/mcp
- Claude Desktop + Apify: https://docs.apify.com/platform/integrations/claude-desktop
- Claude Code MCP: https://code.claude.com/docs/en/mcp
- Apify Python client: https://docs.apify.com/api/client/python/
- uv: https://docs.astral.sh/uv/

Last Updated: 2026.05.27
