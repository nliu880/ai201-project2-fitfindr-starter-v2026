# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> All three tools are stubs, so that last command will do nothing useful yet.
> That's the starting position.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

# Unit 3

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     This is your submission. Fill each section in as you finish the milestone
     it belongs to — don't leave it all to the end.

     Unit 3 asks for the first five sections. Unit 4 adds the five below them.
     Leave the unit 4 sections alone until then; they're here so you know
     what's coming.

     Everything is pasted as TEXT. No screenshots, no images, no video links.
     A typed block of output gets full credit; a picture of the same output
     gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Three or four sentences: what a user asks for, and what they get back. -->

A user searches for a clothing item with some description ("blue skirts under $20"), and based on their current wardrobe, is given suggestions on what to wear the closest item matching their search with and a picture caption to go along with the outfit. If no item is found based on the user's request, an empty list is returned from the search function, along with a message stating that nothing was found and suggestions on how to broaden the search. If the user has no wardrobe, this system will return general styling tips for the closest item matching their search. 

---

## Tool Inventory

<!-- Four lines per tool. This is worth 2 points and it's the single most
     common place students lose them.

     "Returns a list" earns NOTHING. The description has to say what is IN
     the list.

     The empty case isn't optional either — it's the thing your loop branches
     on, and if you don't decide it here you'll discover it as a crash in
     Milestone 5. -->

### `search_listings`

- **What it does:** This function searches listings for an item matching a description. It optionally takes a size and price ceiling.
- **Inputs:** `description` (string), `size` (string), `max_price` (float) <!-- name and type each: `max_price` (float), not "a price" -->
- **Returns:** The function returns a list of dictionaries, which represent matching items. They are sorted by best match. Each dictionary should have the following keys: `id`, `title`, `description`, `category`, `style_tags`, `size`, `condition`, `price`, `colors`, `brand`, and `platform`.
- **When it has nothing:** The function returns an empty list.

### `suggest_outfit`

- **What it does:** This function suggests an outfit or two, based on a given item and the user's wardrobe.
- **Inputs:** `new_item` (dictionary), `wardrobe` (dictionary)
- **Returns:** Depending on whether `wardrobe` is empty: if `wardrobe` is empty, the function will return general styling advice as a string. Otherwise, it returns a non-empty string with outfit suggestions. 
- **When it has nothing:** If `wardrobe['items']` is empty, the model will be asked for styling advice for `new_item` and return those ideas.

### `create_fit_card`

- **What it does:** This function writes a short caption that someone might use about a post with their clothing item find. 
- **Inputs:** `outfit` (string), `new_item` (dictionary)
- **Returns:** A two to four sentence string to be used a potential caption. If the `outfit` string is empty or just whitespace, this function should return a descriptive message saying so.
- **When it has nothing:** If the `outfit` string is empty or just whitespace, this function should return a descriptive message stating that `outfit` was empty.

---

## Planning Loop

<!-- Your branch rule, stated as a rule — the condition AND both paths — plus
     the file and function that holds it.

     Like this:
       "If search_listings returns an empty list, put a message in the session
        and stop. Otherwise take the first result and go to suggest_outfit."
        — agent.py::run_agent

     The grader checks your code against what you claim here, so the file and
     function have to be real. -->

**Branch rule:**
If `search_listings` returns an empty list, put a message in the session and stop. Otherwise, take the first result and go to `suggest_outfit`.

**Where it lives:** `agent.py::run_agent`

**How the query is parsed:** <!-- regex, string splitting, or asking the model — say which -->
The query is parsed through regex as it doesn't cost anything and will always return the same output every time. This makes troubleshooting query parsing easier as well.

**What moves through the session:** <!-- which fields, in what order -->
1. `parse_query`: parse the user query request for its description, and any sizing or max pricing
2. `search_listings`: find items matching the user's request and return them by closest match
3. `select_item`: select the closest matching item
4. `suggest_outfit`: create three outfits based on the user's wardrobe and the closest matching item
5. `create_fit_card`: create image caption for the closest matching item based off its vibe using the generated outfits, mentioning the price and platform of origin

---

## Sample Run

<!-- Two things go here.

     1. One FULL query and its output, pasted as text.
     2. Your three per-tool terminal tests — the command and what it printed. -->

**One full query**

```bash
$ python app.py ask 'vintage graphic tee under $30, size M'
[1] parse_query
      in:  vintage graphic tee under $30, size M
      out: dict with keys: description, size, max_price
[2] search_listings
      in:  dict with keys: description, size, max_price
      out: 3 items: Y2K Baby Tee — Butterfly Print, Mesh Long-Sleeve Top — Black, Vintage Knit Vest — Argyle Brown/Cream
      →    3 match(es)
[3] select_item
      out: Y2K Baby Tee — Butterfly Print ($18.0, depop)
[4] suggest_outfit
      in:  Y2K Baby Tee — Butterfly Print ($18.0, depop)
      out: Here are 3 outfit combinations featuring the new **Y2K Baby Tee — Butterfly Print** (`lst_002`) paired with it…
      →    10 wardrobe item(s)
[5] create_fit_card
      in:  Y2K Baby Tee — Butterfly Print ($18.0, depop)
      out: Bringing all the nostalgic early 2000s energy with this super cute Y2K Butterfly Print Baby Tee! Styled here t…

  Found:    Y2K Baby Tee — Butterfly Print — $18.0 on depop

  Outfit:   Here are 3 outfit combinations featuring the new **Y2K Baby Tee — Butterfly Print** (`lst_002`) paired with items fromyour existing wardrobe:

### Outfit 1: Classic Y2K Streetwear
*Lean into the 2000s aesthetic by balancing the fitted crop tee with baggy denim and chunky sneakers.*
* **Top:** Y2K Baby Tee — Butterfly Print (`lst_002`)
* **Bottom:** Baggy straight-leg jeans, dark wash (`w_001`)
* **Shoes:** Chunky white sneakers (`w_007`)
* **Accessories:** Black crossbody bag (`w_010`)
* **Vibe:** Casual, nostalgic, and effortless.

### Outfit 2: Edgy Contrast
*Play up the butterfly tee's vintage/cottagecore undertones by pairing it with heavy grunge and vintage elements.*
* **Top:** Y2K Baby Tee — Butterfly Print (`lst_002`)
* **Outerwear:** Vintage black denim jacket (`w_006`)
* **Bottom:** Wide-leg khaki trousers (`w_002`)
* **Shoes:** Black combat boots (`w_008`)
* **Accessories:** Brown leather belt (`w_009`)
* **Vibe:** Mixed-aesthetic streetwear with an earthy, grunge twist.

### Outfit 3: Sporty Off-Duty Layering
*Use the black cropped zip hoodie as an easy layering piece over the baby tee for cooler days, keeping the silhouette sharp and fitted.*
* **Top:** Y2K Baby Tee — Butterfly Print (`lst_002`)
* **Outerwear/Layer:** Black cropped zip hoodie (`w_005`) *(worn unzipped to show off the butterfly graphic)*
* **Bottom:** Baggy straight-leg jeans, dark wash (`w_001`)
* **Shoes:** Chunky white sneakers (`w_007`)
* **Accessories:** Black crossbody bag (`w_010`)
* **Vibe:** Sporty, comfortable, and throwback-approved.

  Fit card: Bringing all the nostalgic early 2000s energy with this super cute Y2K Butterfly Print Baby Tee! Styled here three different ways, but I'm obsessed with this effortless streetwear vibe paired with baggy dark wash denim and chunky sneakers. Grab thisgraphic tee over on my Depop for just $18 to complete your ultimate retro rotation. 🦋✨

2 model calls this session, 1351 prompt + 525 output tokens

```

**The three tools, tested one at a time**

```bash
$ python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"

[{'id': 'lst_002', 'title': 'Y2K Baby Tee — Butterfly Print', 'description': 'Super cute early 2000s baby tee with butterfly graphic. Fitted crop length. Tag says medium but fits like a small.', 'category': 'tops', 'style_tags': ['y2k', 'vintage', 'graphic tee', 'cottagecore'], 'size': 'S/M', 'condition': 'excellent', 'price': 18.0, 'colors': ['white', 'pink', 'purple'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_006', 'title': 'Graphic Tee — 2003 Tour Bootleg Style', 'description': 'Vintage-style bootleg tee with faded graphic. Slightly boxy fit. 100% cotton, soft and worn-in.', 'category': 'tops', 'style_tags': ['graphic tee', 'vintage', 'grunge', 'streetwear', 'band tee'], 'size': 'L', 'condition': 'good', 'price': 24.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_017', 'title': 'Mesh Long-Sleeve Top — Black', 'description': 'Sheer black mesh long-sleeve. Great for layering under a graphic tee or over a bralette. Stretchy material, fits true to size.', 'category': 'tops', 'style_tags': ['y2k', 'grunge', 'goth', 'layering'], 'size': 'S/M', 'condition': 'excellent', 'price': 15.0, 'colors': ['black'], 'brand': None, 'platform':'depop'}, {'id': 'lst_033', 'title': 'Vintage Band Tee — Faded Grey', 'description': 'Faded grey band-style tee with distressed graphic. Crew neck. Fits boxy. Well-loved but no holes or major damage.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'band tee', 'graphic tee', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 19.0, 'colors': ['grey', 'charcoal'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_011', 'title': 'Low-Rise Cargo Pants — Khaki', 'description': 'Y2K era low-rise cargo pants. Lots of pockets. Khaki color, slightly distressed at the hems. Great for layering with a long tee.', 'category': 'bottoms', 'style_tags': ['y2k', 'cargo', '2000s', 'streetwear'], 'size': 'W29', 'condition': 'fair', 'price': 27.0, 'colors': ['khaki', 'tan'], 'brand': None, 'platform': 'poshmark'}, {'id': 'lst_015', 'title': 'Vintage Graphic Hoodie — Faded Black', 'description': 'Faded black pullover hoodie with barely-visible vintage graphic on the chest. Cozy interior. Some pilling but adds to the worn-in look.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'graphic', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 26.0, 'colors': ['black', 'charcoal'], 'brand': None, 'platform': 'depop'}]

```

```bash
$ python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"

Here are three stylish outfit combinations featuring the new item (**Vintage Levi's 501 Jeans — `lst_001`**) paired with items from the existing wardrobe:

### Outfit 1: Casual Streetwear Classic
*A laid-back, effortless everyday look leaning into the jeans' vintage streetwear vibe.*
* **Top:** White ribbed tank top (`w_003`)
* **Outerwear:** Vintage black denim jacket (`w_006`)
* **Shoes:** Chunky white sneakers (`w_007`)
* **Accessories:** Black crossbody bag (`w_010`)
* **Why it works:** The crisp white tank creates a clean, timeless base against the medium wash denim. Layering the cropped black denim jacket adds depth and plays with textures, while the chunky sneakers tie the casual streetwear aesthetic together.

### Outfit 2: Cozy & Relaxed Proportions
*A comfortable, textured fit that balances fitted elements with oversized comfort.*
* **Top:** Oversized grey crewneck sweatshirt (`w_004`)
* **Shoes:** Black combat boots (`w_008`)
* **Accessories:** Brown leather belt (`w_009`)
* **Why it works:** Tucking the front of the oversized grey crewneck into the 501s creates a flattering silhouette despite the sweatshirt's drop-hip length. The brown leather belt adds a touch of classic contrast, and the black combat boots anchor the outfit with an edgy grunge finish.

### Outfit 3: Sporty Contrast
*A sharp, modern mix of athletic streetwear and classic Americana denim.*
* **Top:** Black cropped zip hoodie (`w_005`)
* **Shoes:** Chunky white sneakers (`w_007`)
* **Accessories:** Black crossbody bag (`w_010`)
* **Why it works:** The cropped cut of the black zip hoodie pairs naturally with the mid-to-high rise of the Levi's 501s, highlighting the waist. Matching the black hoodie with the black crossbody bag keeps the accessories cohesive, letting the medium blue denim pop against the dark tones.

```

```bash
$ python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"

Nothing beats the effortless, lived-in feel of a truly classic denim fit paired with crisp white kicks. These vintage Levi's 501s bring that ultimate effortless streetwear vibe with the best medium wash fade at the knees. Grab this exact pair over on my Depop for just $38 before they're gone!

```

---

## How I Used AI

<!-- Two specific moments. What you asked, what came back, what you changed.

     "I used Claude to help me code" is not enough.

     "I gave Claude my search_listings spec. It returned None on no match
     instead of an empty list, so I changed it" is the level we want. -->

**Moment 1**

- *What I asked for:* 
I used Claude in place of breakout room feedback: how to test my criteria and how informative/useful the error message is when `search_listings` doesn't find any matches.

- *What came back:* 
I recieved ideas on how to test my criteria and feedback on the produced error message for no matching search results. 

<!-- --> 
     1. "A matching query completes all three tools"
     Pick a query I expect to have real matches in the catalog, run it through the agent, and check that all three tools (`search_listings`, matching/scoring, `suggest_outfit` — whatever the three are named in this project) each actually execute and return a result, rather than the pipeline stopping early. Repeat with a few different matching queries to be reasonably sure it's not a fluke.

     2. "An impossible query stops before the second tool"
     Pick a query I expect to have zero matches (like the ballgown/XXS/$5 one), run it, and check that only the first tool runs — confirm the second and third tools are never invoked. I'd look at whatever execution trace/log shows which tools ran.

     3. "In each situation where matching items are found, the item with the best match is successfully passed to suggest_outfit"
     For every query that returns matches, independently determine which item is the best match (by whatever scoring/ranking the sentence implies), then check that that specific item — not just some item — is the one that shows up as input to `suggest_outfit`. I'd do this for multiple queries with multiple matches to make sure it's not accidentally picking the first or a random one instead of the actual best.

     4. "All fit card captions are under 250 characters in length"
     Generate fit cards across a range of queries (including ones likely to produce long captions), take every caption produced, and measure its character length. Confirm every single one is under 250 — not just a sample — since the criterion says "all."

     5. "When given a query with a price limit, the items returned by search_listings respect that price limit"
     Run queries that specify a price limit, take every item `search_listings` returns, and check each item's price against the stated limit. Confirm none exceed it. I'd vary the price limit across a few values to make sure it's enforced generally, not just for one number. --> 
 
 and

     Based on just that message, you'd have a reasonable next move: drop "designer ballgown" to just "ballgown" or "dress," remove the size filter (or try a nearby size), and raise the price limit above $5 since $5 for a ballgown is almost certainly unrealistic. The message tells you directly which of your three filters to relax.

     What you *wouldn't* know is whether the app handles synonyms, whether "size" means standard letter sizes or numeric, or what a realistic price range actually is for this catalog — you'd be guessing at those until you tried a search and saw what came back.

- *What I changed:* 
Based on the criterion testing feedback, I added a line to the session output produced by `agent.py` noting the length of the generated caption in `create_fit_card` after working through it originally. This additional note about the length will make it easier for me check if captions fulfill this criterion. 

The given feedback about the error message for no found items also brought up good syntax questions (Size M vs medium vs US 8 etc.). Further changes would have to be made to the query parsing and keyword/size matching functions to allow for these differences, which I am running out of time to do. I will keep it in mind for future projects. 

**Moment 2**

- *What I asked for:* I asked Claude for suggestions on how to determine the category of an item based on a description; I had thought to filter listing items by category as well (in addition to size and price) if possible. 
- *What came back:* I received three suggestions on how to handle this problem: keyword matching, positiong-weighted keyword matching, and passing it to the model to determine

     From just a description string, with no explicit category field, you'd generally have a few approaches:

     1. **Keyword/vocabulary matching** — build a list of garment-type nouns mapped to categories (e.g., "tee," "crewneck," "hoodie," "jacket" → tops; "jeans," "skirt," "trousers," "shorts" → bottoms; "sneakers," "boots," "heels" → shoes) and scan the title/description for the first or best match. This is what your `search_listings` sample output already relies on implicitly (every item has a `category` field, so somewhere upstream something — maybe just the data itself — already did this).

     2. **Position-weighted keyword matching** — same as above, but trust the title more than the description, since the title tends to name the item type directly ("Crewneck," "Cargo Pants") while the description tends to be style/vibe language that can mislead (like "college" in your earlier example).

     3. **Asking the model** — pass the description to the LLM and ask it to classify into one of your fixed category labels. More robust to phrasing you didn't anticipate, but costs a call and isn't deterministic.

     Given your README already states you're parsing queries with regex specifically because it's free and deterministic (line 104), a keyword-list approach for category would be consistent with that same reasoning — cheap, reproducible, and easy to debug when it misclassifies something like "crewneck."

- *What I changed:*
I am running out of time, a little, so I did not implement any of these suggestions. Suggestions 2 and 3 aren't really possible; user queries don't have a title naming the item and we want to avoid model calls entirely in `search_listings`, which is where this filtering would take place. 

Suggestion 1 has some merit, in which I would hardcode a hashmap or something that attributes specific types of clothing to categories (heels to shoes, windbreaker to jacket, etc.). Claude also connected it to other logic about regex searching mentioned earlier. This hashmap would be static, though, and limited to my current imagination. This is something for me to potentially implement in the future. My current keyword matching/scoring works fine for now. 

<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

# Unit 4

## Run Log — Before

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table
     into results/. Paste it here and fill in the verdicts. -->

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. matching query completes | PASS | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. impossible query stops early | PASS | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. best matching item successfully passed | PASS | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. fit_card captions are under 250 characters | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | (0/5) |
| 5. price limit enforced | PASS | PASS | PASS | PASS | PASS | PASS | MET (5/5) |

**Note:** The PASS/FAIL marks for criterions 3 and 4 are marked by taking into account all non-early stopping queries for that try. In other words, if a try is marked PASS, that means all scenarios that ran to completion (regardless of whether that is 5/5 scenarios or not) passed that criterion. A criterion is marked FAIL for a try if any one of the applicable scenarios did not meet the criterion.

**Real output from one try**, pasted as text, naming the file and function
that produced it:

**Note:**
The following is copied from output in the command line produced by `python run_eval.py --label before`. Only output from Try 1 is copied here.

```bash
% python run_eval.py --label before
Cache is OFF for this run — that's deliberate.

matching query completes  (example wardrobe)
  query: vintage graphic tee under $30
[1] parse_query
      in:  vintage graphic tee under $30
      out: dict with keys: description, size, max_price
[2] search_listings (via MCP)
      in:  {'description': 'vintage graphic tee', 'size': None, 'max_price': 30.0}
      out: 8 items: Graphic Tee — 2003 Tour Bootleg Style, Y2K Baby Tee — Butterfly Print, Vintage Graphic Hoodie — Faded Black … +5 more
      →    8 match(es)
[3] select_item
      out: Graphic Tee — 2003 Tour Bootleg Style ($24.0, depop)
[4] suggest_outfit
      in:  Graphic Tee — 2003 Tour Bootleg Style ($24.0, depop)
      out: Here are three outfit combinations featuring the new **Graphic Tee — 2003 Tour Bootleg Style** (`lst_006`) sty…
      →    10 wardrobe item(s)
[5] create_fit_card
      in:  Graphic Tee — 2003 Tour Bootleg Style ($24.0, depop)
      out: Channeling major 2000s concert vibes with this vintage-style bootleg tee, snagged for just $24 on Depop! I lov…
      →    373
  try 1: completed — fit card 373 chars
```
[ continued]
```bash
impossible query stops early  (example wardrobe)
  query: designer ballgown size XXS under $5
[1] parse_query
      in:  designer ballgown size XXS under $5
      out: dict with keys: description, size, max_price
[2] search_listings (via MCP)
      in:  {'description': 'designer ballgown', 'size': 'XXS', 'max_price': 5.0}
      out: [] (empty)
      →    0 match(es)
[3] branch
      →    search returned []: stopping before suggest_outfit
  try 1: stopped early — Nothing in the listings matched description 'designer ballgo
```
[ continued]
```bash
empty wardrobe  (empty wardrobe)
  query: denim jacket under $50
[1] parse_query
      in:  denim jacket under $50
      out: dict with keys: description, size, max_price
[2] search_listings (via MCP)
      in:  {'description': 'denim jacket', 'size': None, 'max_price': 50.0}
      out: 5 items: Denim Jacket — Light Wash, Cropped, 90s Track Jacket — Navy/White Stripe, High-Waisted Denim Shorts — Cutoff …+2 more
      →    5 match(es)
[3] select_item
      out: Denim Jacket — Light Wash, Cropped ($42.0, poshmark)
[4] suggest_outfit
      in:  Denim Jacket — Light Wash, Cropped ($42.0, poshmark)
      out: Here are some versatile styling tips for the **Wrangler Light Wash Cropped Denim Jacket**, tailored to its vin…
      →    0 wardrobe item(s)
[5] create_fit_card
      in:  Denim Jacket — Light Wash, Cropped ($42.0, poshmark)
      out: Leaning hard into that vintage streetwear energy with this cropped Wrangler light wash denim jacket—the ultima…
      →    273
  try 1: completed — fit card 273 chars
```
[ continued]
```bash
state criterion test  (example wardrobe)
  query: long sleeve green shirt
[1] parse_query
      in:  long sleeve green shirt
      out: dict with keys: description, size, max_price
[2] search_listings (via MCP)
      in:  {'description': 'long sleeve green shirt', 'size': None, 'max_price': None}
      out: 7 items: Silk Button-Down — Sage Green, Mesh Long-Sleeve Top — Black, Vintage Polo Shirt — Forest Green … +4 more
      →    7 match(es)
[3] select_item
      out: Silk Button-Down — Sage Green ($28.0, depop)
[4] suggest_outfit
      in:  Silk Button-Down — Sage Green ($28.0, depop)
      out: Here are 3 outfit combinations featuring the new **Silk Button-Down — Sage Green** (`lst_029`) styled with ite…
      →    10 wardrobe item(s)
[5] create_fit_card
      in:  Silk Button-Down — Sage Green ($28.0, depop)
      out: Three ways I'm styling this dreamy sage green silk button-down, from minimalist earth tones to 90s streetwear …
      →    213
  try 1: completed — fit card 213 chars
```
[continued]
```bash
price limit enforced  (example wardrobe)
  query: jeans under $36
[1] parse_query
      in:  jeans under $36
      out: dict with keys: description, size, max_price
[2] search_listings (via MCP)
      in:  {'description': 'jeans', 'size': None, 'max_price': 36.0}
      out: 2 items: Baggy Carpenter Jeans — Dark Wash, Straight Leg Black Jeans — Faded
      →    2 match(es)
[3] select_item
      out: Baggy Carpenter Jeans — Dark Wash ($36.0, depop)
  [rate limit] 15 requests used this minute. Waiting 34s. This is normal.
[4] suggest_outfit
      in:  Baggy Carpenter Jeans — Dark Wash ($36.0, depop)
      out: Here are three outfit combinations featuring the new item (**Baggy Carpenter Jeans — Dark Wash**, `lst_031`) p…
      →    10 wardrobe item(s)
[5] create_fit_card
      in:  Baggy Carpenter Jeans — Dark Wash ($36.0, depop)
      out: Channeling major 90s workwear vibes with these Baggy Carpenter Jeans in Dark Wash. Snagged them on Depop for j…
      →    268
  try 1: completed — fit card 268 chars
```

---

## Verdicts and Diagnoses

<!-- MET or MISSED per criterion against LAST UNIT's target, plus a sentence on
     how you decided.

     Then, for every miss: which of the four places it happened — a tool, the
     loop's branch, the session, or the model's output — AND the mechanism.

     Not a diagnosis:  "The fit card was bad."
     A diagnosis:      "The fit card criterion missed on 2 of 5 items. Both had
                        an empty brand field. My prompt puts the brand in the
                        first sentence, so the card opened with a blank and read
                        like a fragment. The tool worked; the prompt assumed a
                        field that isn't always there."

     Look for a pattern. Three misses on the same tool is one problem, not
     three. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**



---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->

**Happy path**

```bash
python app.py ask 'long sleeve green tshirt' --trace
[1] parse_query
      in:  long sleeve green tshirt
      out: dict with keys: description, size, max_price
[2] search_listings (via MCP)
      in:  {'description': 'long sleeve green tshirt', 'size': None, 'max_price': None}
      out: 6 items: Silk Button-Down — Sage Green, Mesh Long-Sleeve Top — Black, Vintage Polo Shirt — Forest Green … +3 more
      →    6 match(es)
[3] select_item
      out: Silk Button-Down — Sage Green ($28.0, depop)
[4] suggest_outfit
      in:  Silk Button-Down — Sage Green ($28.0, depop)
      out: Here are 3 outfit combinations featuring the **Silk Button-Down — Sage Green (`lst_029`)** paired with items f…
      →    10 wardrobe item(s)
[5] create_fit_card
      in:  Silk Button-Down — Sage Green ($28.0, depop)
      out: Obsessed with how this vintage sage green silk button-down ($28 on Depop) instantly elevates everything alread…
      →    342

  Found:    Silk Button-Down — Sage Green — $28.0 on depop

  Outfit:   Here are 3 outfit combinations featuring the **Silk Button-Down — Sage Green (`lst_029`)** paired with items from your existing wardrobe:

### Outfit 1: Effortless Earth Tones (Tonal & Minimal)
*Highlighting the sage green with complementary neutral earth tones for a soft, cottagecore-meets-minimalist look.*
* **Top (New):** Silk Button-Down — Sage Green (`lst_029`) — *worn fully buttoned or tucked in*
* **Bottom:** Wide-leg khaki trousers (`w_002`)
* **Accessory:** Brown leather belt (`w_009`)
* **Bag:** Black crossbody bag (`w_010`) 
* **Shoes:** Chunky white sneakers (`w_007`) or Black combat boots (`w_008`)
* **Vibe:** Relaxed, polished, earthy, and breezy.

### Outfit 2: The Casual Layer (Textured Streetwear Mix)
*Using the flowy silk button-down open as a lightweight layer over a basic fitted top, paired with denim for contrast.*
* **Base Top:** White ribbed tank top (`w_003`)
* **Layer (New):** Silk Button-Down — Sage Green (`lst_029`) — *worn unbuttoned and open*
* **Bottom:** Baggy straight-leg jeans, dark wash (`w_001`)
* **Accessory:** Brown leather belt (`w_009`)
* **Shoes:** Chunky white sneakers (`w_007`)
* **Vibe:** 90s casual, effortless, and comfortable with a great mix of structured denim and fluid silk.

### Outfit 3: Edgy Contrast (Vintage & Grunge Twist)
*Pairing the soft, feminine vintage sage silk with heavy black textures to lean into a cool, grunge-adjacent contrast.*
* **Top (New):** Silk Button-Down — Sage Green (`lst_029`)
* **Bottom:** Baggy straight-leg jeans, dark wash (`w_001`)
* **Outerwear:** Vintage black denim jacket (`w_006`) — *worn over the shoulders or unbuttoned shirt*
* **Shoes:** Black combat boots (`w_008`)
* **Bag:** Black crossbody bag (`w_010`)
* **Vibe:** Cool-girl grunge, vintage-inspired, and slightly moody.

  Fit card: Obsessed with how this vintage sage green silk button-down ($28 on Depop) instantly elevates everything already in my closet! Whether I'm styling it tucked into neutral trousers for a soft cottagecore vibe, wearing it open over a tank for 90s streetwear, or layering it with black denim for an edgy grunge twist, this flowy piece does it all.

2 model calls this session, 1421 prompt + 608 output tokens
```

**Empty searches**

- Empty search
     ```bash
     python app.py ask '$1 dior shirt'
     [1] parse_query
          in:  $1 dior shirt
          out: dict with keys: description, size, max_price
     [2] search_listings (via MCP)
          in:  {'description': 'dior shirt', 'size': None, 'max_price': 1.0}
          out: [] (empty)
          →    0 match(es)
     [3] branch
          →    search returned []: stopping before suggest_outfit

     Nothing in the listings matched description 'dior shirt', under $1.
     Things to change: try broader words — 'jacket' finds more than 'cropped corduroy jacket'; raise the price ceiling above $1.

     0 model calls this session
     ```
- Empty wardrobe
     ```bash
     python app.py ask 'vintage jacket' --empty-wardrobe
     (running with an empty wardrobe)
     [1] parse_query
          in:  vintage jacket
          out: dict with keys: description, size, max_price
     [2] search_listings (via MCP)
          in:  {'description': 'vintage jacket', 'size': None, 'max_price': None}
          out: 9 items: Vintage Levi's 501 Jeans — Medium Wash, 90s Track Jacket — Navy/White Stripe, Graphic Tee — 2003 Tour Bootleg Style … +6 more
          →    9 match(es)
     [3] select_item
          out: Vintage Levi's 501 Jeans — Medium Wash ($38.0, depop)
     [4] suggest_outfit
          in:  Vintage Levi's 501 Jeans — Medium Wash ($38.0, depop)
          out: Here are versatile styling tips for the **Vintage Levi's 501 Jeans (Medium Wash)**, tailored for a Depop/stree…
          →    0 wardrobe item(s)
     [5] create_fit_card
          in:  Vintage Levi's 501 Jeans — Medium Wash ($38.0, depop)
          out: Channel that effortless 90s streetwear energy with these vintage Levi's 501s, featuring the most gorgeous medi…
          →    362

     Found:    Vintage Levi's 501 Jeans — Medium Wash — $38.0 on depop

     Outfit:   Here are versatile styling tips for the **Vintage Levi's 501 Jeans (Medium Wash)**, tailored for a Depop/streetwear audience:

     ### **1. Casual Streetwear (The Everyday Look)**
     *   **Top:** An oversized graphic tee (band tee or vintage skate brand), slightly tucked in.
     *   **Footwear:** Classic white sneakers (like Nike Air Force 1s or Adidas Sambas).
     *   **Accessories:** A canvas tote bag, a silver chain necklace, and a baseball cap. 
     *   **Vibe:** Effortless, 90s-inspired daily wear.

     ### **2. Elevated Vintage / Smart-Casual**
     *   **Top:** A tucked-in ribbed black tank top or a crisp white button-down shirt (sleeves rolled up).
     *   **Layer:** An oversized leather blazer or a distressed brown suede jacket.
     *   **Footwear:** Black leather loafers or chunky platform boots.
     *   **Accessories:** A black leather belt with a statement buckle and minimalist silver rings.

     ### **3. Y2K / Grunge Aesthetic**
     *   **Top:** A cropped baby tee, a distressed knit sweater, or a mesh long-sleeve top.
     *   **Footwear:** Platform boots or beat-up Converse All-Stars.
     *   **Accessories:** A nylon shoulder bag (baguette style) and wire-rimmed sunglasses.

     ---

     ### **💡 Bonus Tips for Listing Photos (If you're selling on Depop):**
     *   **Show off the fit:** Since 501s are a classic straight-leg cut with a button fly, show them worn high-waisted with a belt to highlight the silhouette.
     *   **Highlight the wash:** Take close-up photos near natural light to show the authentic fading at the knees, as buyers love genuine vintage wear.

     Fit card: Channel that effortless 90s streetwear energy with these vintage Levi's 501s, featuring the most gorgeous medium wash and natural knee fading. Style them bagged out with a vintage graphic tee and Sambas for everyday wear, or dress them up with an oversized leather blazer and loafers. Grab this classic W30 L30 pair now on Depop for just $38 before they're gone!

     1 model calls this session, 1 served from cache, 586 prompt + 85 output tokens
     ```
- Model unavailable
     ```bash
     python app.py ask 'gothic boots'     
          [1] parse_query
               in:  gothic boots
               out: dict with keys: description, size, max_price
          [2] search_listings (via MCP)
               in:  {'description': 'gothic boots', 'size': None, 'max_price': None}
               out: 1 items: Suede Chelsea Boots — Tan
               →    1 match(es)
          [3] select_item
               out: Suede Chelsea Boots — Tan ($44.0, poshmark)
          [4] model unavailable
               →    stopping, search results kept

          The model couldn't be reached, so the outfit and caption steps didn't run. The search worked — 1 listing(s) were found. Check GEMINI_API_KEY in your .env, then run the same query again.
          What the service said: The model rejected your API key. Check GEMINI_API_KEY in your .env file, or create a fresh key at aistudio.google.com.

          1 model calls this session
     ```

**On the MCP move:** 
<!-- what changed in your code, and whether anything
behaved differently afterwards. If the rewire didn't work, say exactly where it
broke — the error text and the last thing that worked. That earns the point in
full. -->
Previously, we had directly called `search_listings` from `tools.py` to be used in `agent.py`. Now, we rework calling the tool by wrapping it in an MCP. There were no changes in the output. It is just a different way of calling the tool.

---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:**

**Which failure it was meant to fix:**

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it made things worse, say that. Honestly reported, that earns full
     credit and is more interesting than one that worked. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [ ] Run Log — Before, five criteria, five tries each
       [ ] Real output pasted underneath, naming file and function
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, naming a place AND a mechanism
       [ ] Loop Trace, with the MCP call visible in it
       [ ] All three failure modes triggered and handled
       [ ] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
