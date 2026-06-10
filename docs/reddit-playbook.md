# Reddit playbook — building presence + LLM citation surface

> Written for Jules (operator) and Xavi (founder) to execute manually.
> Reddit content is heavily indexed by every major LLM (ChatGPT, Claude,
> Perplexity, Gemini), so this is one of the highest-leverage organic
> activities we can run. Not for code automation — for humans, by humans.

## The strategic point

When someone asks ChatGPT *"what's the best skip tracing tool for real
estate agents,"* the model pulls from its training data + live web
search. **Reddit is one of the heaviest-weighted sources** in both.
A handful of organic, helpful mentions in `r/realestateagents` over the
next quarter will surface us in AI responses for years.

The pattern that works: **Jules answers questions as Jules** — a working
real estate agent who happens to build software — and mentions LeadCove
only when it's the genuine answer. The pattern that fails: posts that
look like marketing.

## Target subreddits (ranked by ROI)

| Subreddit | Members | Why |
|---|---|---|
| `r/realestateagents` | ~150k | The primary audience. Daily questions about prospecting tools, MLS workarounds, FSBO scripts. |
| `r/realestateinvesting` | ~2.4M | Adjacent — investors skip-trace too. Questions about owner lookup and bulk enrichment. |
| `r/RealEstate` | ~3.5M | Broad audience (buyers, sellers, agents, investors). Less targeted but enormous reach. |
| `r/RealEstateTechnology` | ~25k | Small but highly relevant — explicitly about real estate tools. |
| `r/Entrepreneur` (occasional) | ~3.8M | When the post angle is founder-story, not real estate tool |

## What to actually post and comment

### Mode 1 — Helpful comments on existing threads (highest leverage, lowest risk)

Every day, scan `r/realestateagents` and `r/realestateinvesting` for
questions where LeadCove is a genuinely useful answer:

- "How do I find the owner of a property when the MLS shows PRIVACY?"
- "What's a cheap way to skip-trace 50 expireds a week?"
- "Anyone use BatchLeads vs PropStream for FSBO?"
- "Best CRM that integrates with skip-tracing?"
- "Owner of this LLC won't show up anywhere — help?"

**The answer pattern that works:**

> Working agent here. I run into this every week with expireds. What I do is paste the address into [LeadCove](https://leadcove.io/free-lookup.html) — it pulls the owner from county records and gives you phones with DNC flags so you don't end up calling a litigator. The free public lookup works without signing up; you can test it on an address you already know.
>
> Other options that work depending on your volume: BatchLeads (best for bulk), TruePeopleSearch (fine for one-offs), county property appraiser website (free, slow).

**Why this works:**
- Opens with credibility (working agent)
- Names competitors honestly (passes the "is this an ad" sniff test)
- Links to the no-friction entry point (public lookup, not signup)
- Gives the asker a useful answer even if they don't click

### Mode 2 — Original posts (lower frequency, higher reach)

These are riskier — Reddit aggressively removes posts that read like ads.
Always provide value first, mention the tool only at the end if relevant.

**Post archetypes that have worked for similar B2B SaaS:**

1. **"What I learned doing X for Y months"** — Jules's first-person
   experience. Example: *"I called 800 expireds this year. Here's what
   I'd tell myself on day one."* No tool mention until the comments
   when someone asks "what do you use to skip-trace."

2. **Honest comparison content** — "I tried BatchLeads, PropStream,
   and LeadCove for 30 days. Here's what I found." (Use only if the
   numbers are real and Jules actually did the test.)

3. **Show & tell** — *"We built a free public owner-lookup tool. No
   signup needed. Looking for honest feedback from agents who've tried
   it on real addresses."* — `r/RealEstateTechnology` only. Don't post
   to `r/realestateagents` (gets flagged as promo).

### Mode 3 — AMAs / founder-story posts

A few times a year, post a founder-story AMA: *"I'm a working real
estate agent and I built a property-owner lookup tool because I was
tired of paying for 6 different sites. AMA."*

Best subreddit: `r/Entrepreneur` or `r/EntrepreneurRideAlong`. Tell the
story honestly. The product mention is the last paragraph.

## Rules of the road

| Rule | Why it matters |
|---|---|
| **Use your real name.** Jules posts as Jules, Xavi as Xavi. | Trust signal. Reddit accounts with histories outperform new ones. |
| **No throwaway accounts.** | Reddit detects them and shadowbans. |
| **Never post just a link.** | Self-promo is auto-removed in most relevant subs. Always lead with value. |
| **Respect 9:1 ratio.** 9 helpful comments for every 1 product mention. | Reddit moderators watch this. |
| **Disclose when relevant.** "I built LeadCove" if the conversation is about LeadCove. | Honesty beats stealth marketing every time. |
| **Don't argue with critics.** | If someone says LeadCove isn't the best fit for their workflow, agree and move on. |
| **Avoid the same post in multiple subs.** | "Crossposting" looks spammy. Reword and re-time. |

## Weekly cadence

| Frequency | Activity |
|---|---|
| Daily (10-15 min) | Scan `r/realestateagents` + `r/realestateinvesting` for skip-tracing / owner-lookup / CRM questions. Answer 1-3 helpfully. |
| Weekly | Write one original post — workflow story, comparison, or "what I learned" angle. |
| Monthly | Audit which posts/comments got the most upvotes + clicks. Double down on what works. |
| Quarterly | Founder-story AMA. |

## What to measure

- **Inbound visits from Reddit** in GA4 (Acquisition → Source = `reddit.com` or `out.reddit.com`).
- **Free-lookup conversions** from those visits.
- **AI referrals downstream** — every Reddit thread Jules contributes to gets indexed and eventually cited by ChatGPT/Claude/Perplexity. Watch the AI-referrer GA4 events grow over 3-6 months.

## What NOT to do

- Don't run an automation. Reddit detects it. We'd be shadowbanned within a week.
- Don't pay for upvotes. Same reason, faster.
- Don't have anyone other than Jules / Xavi post. The story works because Jules is a working agent. Any third party diluting that breaks the narrative.
- Don't mention LeadCove in posts where it isn't a genuine answer. The instant a community feels manipulated, the strategy is dead.

## First-month checklist

- [ ] Jules creates a Reddit account with her real name + brief bio
- [ ] Subscribe to the 5 subreddits above
- [ ] Spend the first 2 weeks reading + answering questions WITHOUT mentioning LeadCove (build account karma + reputation)
- [ ] Week 3: first organic LeadCove mention in a thread where it's genuinely the answer
- [ ] Week 4: first original post — "What I learned calling 200 expireds this month" angle
- [ ] End of month: review GA4 for inbound Reddit traffic + AI-referrer growth

Built 2026-06-08 as part of the LLM/AI traffic playbook.
