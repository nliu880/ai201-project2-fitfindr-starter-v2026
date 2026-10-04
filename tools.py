"""
The three FitFindr tools.

Each one is a standalone function you can call and test on its own, before any
of them are wired into the loop. Build and test them one at a time — three
untested tools joined by a loop is one problem that looks like six, because you
can't tell which layer is lying to you.

    search_listings(description, size, max_price)  → list[dict]
    suggest_outfit(new_item, wardrobe)             → str
    create_fit_card(outfit, new_item)              → str

All three are stubs right now. They run and they do nothing — that's the
starting position and it's deliberate.

⚠️ Before you write any of them, fill in the **Tool Inventory** section of your
README (Milestone 2). Four lines per tool: what it does, each input with its
type, exactly what it returns, and what it returns when it has nothing to give.
That last line is what your loop branches on. "Returns a list" earns nothing —
the description has to say what is *in* the list.
"""

import config  # noqa: F401 — you'll use this in search_listings
from generate import generate
from utils.data_loader import load_listings

import regex as re


# ── Tool 1: search_listings ───────────────────────────────────────────────────

STOPWORDS = {
    'a', 'an', 'and', 'the', 'for', 'in', 'of'
}

def _keywords(text: str) -> set[str]:
    """
    Lowercase words worth matching on, removing stopwords
    text: item description or user request to be looked through for keywords
    """
    words = re.findall(r"[a-z0-9]+", (text or "").lower())
    return {w for w in words if w not in STOPWORDS and len(w) > 1}

def keyword_score(desc: str, listing: str) -> float:

    desc_keywords = _keywords(desc)
    list_keywords = _keywords(listing)

    score = 0

    for word in desc_keywords:
        if word in list_keywords:
            score += 1

    return score / len(desc_keywords)

def _size_tokens(text: str) -> set[str]:
    """Determine the garment size from text (search or item description), i.e. size L or waist 32 inches
    text: text from which to find the garment size
    """
    size_tags = []

    text = text.lower()
    text = re.sub(r"\/", " ", text) # replace / 

    size_tags += [tag[1:-1] for tag in re.findall(r"\([^)]*\)", text)] # find all parentheticals and remove parentheses 
    size_tags += re.findall(r"(?:m|x{0,2}[sl])", text) # find standalone sizes
    size_tags += re.findall(r"one size", text) # any one size fit all types
    size_tags += re.findall(r"w\d\d|l\d\d", text) # any waist or length measurements
    size_tags += re.findall(r"us \d{1,2}", text) # shoe sizes?
    
    print('description:', text)
    print('size tags:', size_tags)
    print()

    return set(size_tags)

def _size_matches(request: str, listing: str) -> bool:
    """
    request: user request
    listing_size: listing
    """
    if not request:
        return True
    
    listing_tokens = _size_tokens(listing)

    if 'one size' in listing_tokens:
        return True
    
    return bool(_size_tokens(request) & listing_tokens)

def categorize(desc: str) -> str:
    # idk...
    return category

def search_listings(
    description: str,
    size: str | None = None,
    max_price: float | None = None,
) -> list[dict]:
    """
    Search the listings data for items matching a description, and optionally a
    size and a price ceiling.

    This is the tool that doesn't call the model, which makes it the easiest one
    to test and the one to move onto MCP in unit 4.

    Args:
        description: keywords describing what the user wants
                     (e.g. "vintage graphic tee").
        size:        a size string to filter by, or None to skip size filtering.
                     Match case-insensitively — "M" should match "S/M".

                     ⚠️ Read the sizes in the data before you reach for a plain
                     substring test. `"s" in "us 9"` is True, and so is
                     `"l" in "xl"`. A filter that returns shoes when someone
                     asked for a small top reads like a broken search, and it
                     will quietly cost you in unit 4 when you test criterion 1.
                     What counts as a size match is part of your spec — decide
                     it and write it into your Tool Inventory.
        max_price:   maximum price, inclusive, or None to skip price filtering.

    Returns:
        A list of matching listing dicts, best match first.
        **Returns an empty list when nothing matches — an empty list, not None,
        and not an exception.** Your loop branches on this.

    Each listing dict has these fields:
        id, title, description, category, style_tags (list), size,
        condition, price (float), colors (list), brand (str or None), platform

    Note that `brand` is None for most listings. That is deliberate and
    realistic — thrift listings often have no brand. If something you write
    assumes a brand is always there, you will find out in unit 4.

    TODO:
        1. Load every listing with load_listings().
        2. Filter by max_price and by size, when each is provided.
        3. Score what's left by keyword overlap with `description`.
        4. Drop anything scoring zero.
        5. Sort by score, highest first, and return the listing dicts —
           at most config.SEARCH_RESULT_LIMIT of them.

    Test it from a terminal before you move on:
        python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"
    """    
    
    listings = load_listings()

    print('START:')
    print()

    # filter by type
    # item_type = categorize(description)
    # listings[:] = [listing for listing in listings if listing['category'] == item_type]

    # filter by size
    if size:
        listings[:] = [listing for listing in listings if _size_matches(size, listing['size'])]
    
    # filter by price
    if max_price:
            listings[:] = [listing for listing in listings if listing['price'] <= max_price]
    
    # print('FILTERED:')
    # for listing in listings:
    #     print(listing)

    scored = {}

    # score each listing
    for listing in listings:
        score = keyword_score(description, listing['description'])
        if score > 0:
            scored[listing['id']] = [score, listing]

    # if we have no matches at all
    if len(scored) == 0:
        return []

    #sort the listings
    scorted = {k: v for k, v in sorted(scored.items(), key = lambda item: item[1][0], reverse = True)}

    # print()
    # print()
    # print('SCORING: ')
    # print(scorted)
    # print()
    # print()

    final_list = [scorted[key][1] for key in scorted.keys()]

    if len(scorted) > config.SEARCH_RESULT_LIMIT:
        return final_list[:config.SEARCH_RESULT_LIMIT]
    else:
       return final_list


# ── Tool 2: suggest_outfit ────────────────────────────────────────────────────

def suggest_outfit(new_item: dict, wardrobe: dict) -> str:
    """
    Given a thrifted item and the user's wardrobe, suggest one or two outfits.

    This one calls the model, through `generate()`. You don't need to think
    about rate limits — the adapter handles pacing for you.

    Args:
        new_item: a listing dict — the item the user is considering.
        wardrobe: a wardrobe dict with an 'items' key holding a list of items.
                  **It may be empty.** Handle that.

    Returns:
        A non-empty string with outfit suggestions.
        With an empty wardrobe, return general styling advice rather than
        raising or returning "". Unit 4 has you trigger the empty wardrobe on
        purpose, so decide now what it should do.

    TODO:
        1. Check whether wardrobe['items'] is empty.
        2. If it is, ask the model for general styling ideas for this item.
        3. If it isn't, format the wardrobe items into the prompt and ask for
           specific combinations naming pieces the user already owns.
        4. Return the model's response.

    Test it from a terminal before you move on:
        python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"
    """

    if len(wardrobe['items']) == 0:
        return generate(f'Provide general styling tips for this item.: {new_item}')
    
    return generate(f'Given this new item: {new_item}, create outfit combinations with this wardrobe: {wardrobe}')


# ── Tool 3: create_fit_card ───────────────────────────────────────────────────

def create_fit_card(outfit: str, new_item: dict) -> str:
    """
    Write a short caption someone would actually post about the find.

    This calls the model too.

    Args:
        outfit:   the outfit suggestion string from suggest_outfit().
        new_item: the listing dict for the item.

    Returns:
        A two-to-four sentence caption.
        If `outfit` is empty or whitespace, return a descriptive message of the error rather
        than raising.

    The caption should read like a real post rather than a product description,
    mention the item and its price and platform once each, and be specific about
    the vibe.

    It should also come out **differently for different inputs**. If you run
    this three times on the same item and get three word-for-word identical
    strings, it's one of two things, and both are near the top of `config.py`:

        • CACHE_ENABLED — the adapter handed back an answer it already had
        • TEMPERATURE   — at 0.0 the model gives the same words every time

    TODO:
        1. Guard against an empty or whitespace-only `outfit`.
        2. Build a prompt with the item details and the outfit.
        3. Call generate() and return the response.

    Test it from a terminal before you move on:
        python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"
    """

    outfit = outfit.strip()

    if len(outfit) == 0:
        return "No outfit provided! Something cannot be created from nothing."

    prompt = f"Write a 2-4 sentence caption for this outfit ({outfit}), \
            where the new item is {new_item}. The caption should read like a real post rather than a product description. \
            Mention the new item, its price, and platform once each. Be specific about the vibe."

    return generate(prompt)