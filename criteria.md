# Acceptance criteria — FitFindr

Five criteria that say what "working" means for this agent, written in unit 3
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"The agent handles errors"* is an opinion.
*"When search returns nothing, the agent stops before calling the second tool,
in 5 of 5 tries"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter one. A reason that says something about your tools, your loop, or the
data earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

**Two are written for you. You write three.**

---

## 1. A matching query completes all three tools

Given a query that matches at least one listing, the agent completes all three
tool calls and returns a fit card — in at least 4 of 5 tries.

**Why this target:**
<!-- Why 4 of 5 and not 5 of 5? Something about your search, probably —
     "my search is a plain keyword match and some phrasings will miss" is a
     real answer. -->

The search for matching queries is through keyword matching, it is highly likely that some of the phrasings will not find a match according to my search function, hence we look for a successful run of all three tools 4/5 tries.

---

## 2. An impossible query stops before the second tool

Given a query that matches no listings, the agent stops before calling
`suggest_outfit` and returns a message naming what to change — 5 of 5 tries.

**Why this target:**
<!-- Why is 5 of 5 reasonable here when criterion 1 isn't? What's different
     about this path? -->

`search_listings` does not call the model, so an unsucessful search for matching listings is not expensive. `suggest_outfit` does, however, and it is not designed for non-existent listings. Calling the model on non-existent listings may cause loops, and will be undoubtedly expensive. We want to avoid this in all situations, hence this criterion calls for an impossible query to stop before the second tool 100% of the time.
---

## 3. In each situation where matching items are found, the item with the best match is successfully passed to `suggest_outfit`

<!-- YOU WRITE THIS ONE.

     How would you know that the item your search found is the same item the
     next tool received? Name something countable or observable.

     This is the criterion people find hardest, because state failure doesn't
     look like state failure — it looks like a tool problem. Something that
     compares session["selected_item"] against what actually reached
     suggest_outfit is the shape you're after. -->

**Why this target:**

We want to ensure that the same item found is the same one that the nex tool recieves. A check at the beginning of `suggest_outfit` will ensure the best matching item from `search_listings` to `suggest_outfit`. This check and match will occur each time `search_listings` and `suggest_outfit` are called; the closest match item found by `search_listings` and received by `suggest_outfit` are the same 5 of 5 tries, or 100% of the successful listing searches if one of the tries does not end up being successful. This should be a simple pass from one function to the next, so getting it right all the time should be easy.


---

## 4. All fit card captions are under 250 characters in length

<!-- YOU WRITE THIS ONE.

     The fit card calls a model, so the same input can produce different words
     each time. That's not a bug — it's the nature of the tool. So what would
     make it acceptable?

     Think about what you'd actually be unhappy to see. A caption that never
     mentions the price? Two different items producing the same opening
     sentence? A card longer than a caption anyone would post? Any of those can
     be turned into a number. -->

**Why this target:**

Captions for photos have a limited character count, one that the generated caption should abide by. This criterion asks that all generated captions are under 250 characters without requiring a specific number, 5/5 tries. If there is the case that what ends up being generated and returned is the error message for an empty `outfit`, 100% of **generated fit captions** are under 250 characters in length.



---

## 5. When given a query with a price limit, the items returned by `search_listings` respect that price limit

<!-- YOU WRITE THIS ONE TOO.

     Pick something you actually care about getting right. Speed, the empty
     wardrobe path, what happens when the model can't be reached, whether the
     search respects a price ceiling — anything, as long as it names a number
     or an observable outcome. -->

**Why this target:**

`search_listings` will return items that respect the max price limit 4/5 times. The method of searching the query will be through keyword and regex matching, so it is possible that the requested price will not be found correctly in some situations.
---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 4 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 4. Something about the fit card

         The fit card is different every time.

         **Why this target:** ...

         > **Revised in unit 4:** For 5 different items, the 5 fit cards share
         > no opening sentence.
         >
         > **Why revised:** "different" wasn't checkable — two cards that
         > differed by one word still counted. The new version is something I
         > can actually score.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said the empty search stops it 5 of 5 times, but I got 3 of 5,
            so 3 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
