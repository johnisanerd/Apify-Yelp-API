"""
Yelp API: A Quick Start Example (3-actor suite)
See more at: https://apify.com/johnvc/yelp-search-api?fpr=9n7kx3

This script shows how to call the Yelp API on Apify from Python and read its
structured JSON output. The suite is designed to chain together:

  1. Yelp Search API            -> ranked business listings for a query + location
  2. Yelp Business Details API  -> the full profile for a place_id from the search
  3. Yelp Reviews API           -> the reviews for that same place_id

Inputs are kept small (one query, one page, one place) so your first run stays
cheap. Raise these once you have your own API key and know your budget.

Get your free Apify API key at: https://apify.com?fpr=9n7kx3
"""

import os

from apify_client import ApifyClient
from dotenv import load_dotenv

load_dotenv()

# Initialize the Apify client with your API token (read from .env)
client = ApifyClient(os.getenv("APIFY_API_TOKEN"))

# ---------------------------------------------------------------------------
# 1. SEARCH: find ranked Yelp businesses for a query in a location.
#    Inputs are kept small (max_pages=1, one query) to keep this first run cheap.
#    Raise max_pages once you know your budget.
# ---------------------------------------------------------------------------
search_input = {
    "search_term": "coffee",
    "location": "New York, NY",
    "sort_by": "rating",   # recommended | rating | review_count
    "max_pages": 1,        # one page is about 10 businesses
}
print(f"1. Searching Yelp for '{search_input['search_term']}' in {search_input['location']}...")
search_run = client.actor("johnvc/yelp-search-api").call(run_input=search_input)
search_items = list(client.dataset(search_run.default_dataset_id).iterate_items())

businesses = search_items[0].get("organic_results", []) if search_items else []
print(f"   Found {len(businesses)} businesses on page 1. Top matches:")
for biz in businesses[:5]:
    print(f"   - {biz.get('title')} (rating={biz.get('rating')}, reviews={biz.get('reviews')}, {biz.get('price')})")

# Grab the first business's ENCODED place id: the first entry of its place_ids
# array. That id feeds the Business Details and Reviews APIs below.
first_place_id = None
if businesses and businesses[0].get("place_ids"):
    first_place_id = businesses[0]["place_ids"][0]
print(f"   Using place_id: {first_place_id}\n")

if first_place_id:
    # -----------------------------------------------------------------------
    # 2. BUSINESS DETAILS: the full profile for that place.
    #    Pass a list of place_ids to look up several businesses in one run.
    # -----------------------------------------------------------------------
    print("2. Fetching the full business profile...")
    place_run = client.actor("johnvc/yelp-place-api").call(
        run_input={"place_ids": [first_place_id]}
    )
    place_items = list(client.dataset(place_run.default_dataset_id).iterate_items())
    profile = place_items[0].get("place_results") if place_items else None
    if profile:
        print(f"   {profile.get('name')} | {profile.get('phone')} | {profile.get('address')}")
        print(f"   rating={profile.get('rating')} reviews={profile.get('reviews')} price={profile.get('price')}\n")

    # -----------------------------------------------------------------------
    # 3. REVIEWS: the reviews for that same place (one page is up to 49 reviews).
    # -----------------------------------------------------------------------
    print("3. Fetching the most recent reviews...")
    reviews_run = client.actor("johnvc/yelp-reviews-api").call(
        run_input={"place_id": first_place_id, "sort_by": "date_desc", "max_pages": 1}
    )
    reviews_items = list(client.dataset(reviews_run.default_dataset_id).iterate_items())
    reviews = reviews_items[0].get("reviews", []) if reviews_items else []
    print(f"   Got {len(reviews)} reviews. A few of the latest:")
    for rev in reviews[:3]:
        reviewer = (rev.get("user") or {}).get("name")
        text = (rev.get("comment") or {}).get("text", "") or ""
        print(f"   - {rev.get('rating')} stars by {reviewer}: {text[:80]}")
