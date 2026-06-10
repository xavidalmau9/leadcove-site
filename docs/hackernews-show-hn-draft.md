# Hacker News Show HN — draft

> For Xavi to post when he's ready. HN voice: technical, low-puffery, honest about limitations, opens with what you built and why. Title under 80 chars. First comment is the most important — it's where the story expands.

## Suggested submission

**Title**

```
Show HN: LeadCove – property-owner data for real estate agents
```

**URL**

```
https://leadcove.io
```

**Text** (optional — most Show HN posts do better with just a URL + comment)

Leave blank if posting. Use the first comment for the story.

## First-comment text (post this within 60 seconds of submission)

```
LeadCove founder here. Quick context for HN.

The problem: real estate agents working cold listings (expireds, FSBOs,
absentee owners) need to resolve a property address into a usable
contact record — owner name, phone, email, DNC status, the human behind
an LLC. The standard workflow is to switch between four to seven
different consumer-records sites (TruePeopleSearch, Spokeo,
BeenVerified, etc.) plus the county property appraiser and the state
Secretary of State for LLC unmasking. Average agent on a 40-row weekly
expired-listing list spends 2-3 hours on the lookup workflow before
they've dialed anything.

What we built: single-screen tool. Drop a CSV of addresses, every
owner is resolved in the background with phone numbers (each flagged
against the national DNC registry plus state-level DNC lists where
they exist), emails, and the registered LLC officer when the property
is held by an entity. One credit per successful match — no charge on
misses, which matters at scale because the consumer-records sites all
charge per query regardless of outcome.

What's not great about it:
- We're newer than the legacy tools (BatchLeads, PropStream). Smaller
  user base. Less YouTube content.
- We don't bundle a CRM. We integrate with Follow Up Boss directly;
  for other CRMs it's CSV export.
- Power tier covers ~1,500 paid hits/month before credit packs are
  needed. If you're a wholesaler running 50K-row monthly lists,
  BatchLeads is sized better.

Free public lookup (no signup): https://leadcove.io/free-lookup.html
— anyone can test the data quality on a real address before signing up.

7-day trial on the Starter tier, $0 charged on day 1, $29/mo after if
you don't cancel. We don't store any payment data ourselves; checkout
runs through Stripe.

Honest comparison page with eight competing tools (we wrote it
trying to be fair):
https://leadcove.io/blog/skip-tracing-tools-comparison.html

Happy to answer technical questions, business questions, anything.
```

## Why this format works on HN

1. **No marketing puffery in the title.** Lowercase descriptor after "Show HN:" — that's the genre convention.
2. **First comment owns the story.** HN voters check the first comment before voting. A good one with context, honest limitations, and a try-it link materially lifts the post.
3. **"What's not great about it" section.** HN rewards honesty. Listing weaknesses inoculates against criticism in replies.
4. **Free, no-signup test link.** Lets HN readers verify the claim without friction. Cuts skeptical "this is just a paywall" comments.
5. **Comparison link to ourselves losing to others in some scenarios.** Signals we're not selling — we're describing.

## What to do after submitting

- **Don't reply to every comment.** Pick the top 5 substantive threads. Reply with detail; don't go defensive on the troll-style ones.
- **Don't upvote your own.** HN rate-limits this and detection is automatic.
- **Don't ask friends to upvote.** Same.
- **Watch the time of day.** Best window: weekday 6am-9am Pacific (= 9am-12pm Eastern). Avoid weekends. Posts that don't get traction in the first 60 minutes generally don't recover.
- **Update the comment if you said something wrong.** Edit window is 2 hours. HN respects "EDIT: actually, X" additions.

## If it lands

- Watch GA4 for the spike. Expect ~5-15K visits over 24h if it makes the front page; 30-50K if it stays for a day. Conversion to trial is typically 0.5-2% of HN traffic — they're skeptical and technical, not the core target audience.
- The far bigger value is the **link from news.ycombinator.com**, which Google + every AI training set indexes heavily. The LLM-citation pool benefit compounds for years.

## If it doesn't land

- Don't repost the same URL — HN catches duplicates. If we change the angle materially (a different feature launch, a real milestone), a future Show HN is fine 3-6 months later.
- The comment quality matters even on a post that doesn't make the front page. People searching HN later still find it.

## Adjacent angles for follow-up Show HN posts (months later)

- **"Show HN: I scraped the FL DBPR public licensee list to find every real estate agent"** — technical story about the data work.
- **"Show HN: We rewrote our normalizer after losing 13 columns silently for 3 weeks"** — postmortem-as-launch, the kind of thing HN loves.
- **"Show HN: Our admin dashboard now disagrees with itself less"** — wry, founder-voice, technical.

Built 2026-06-10 as part of the LLM/AI traffic playbook.
