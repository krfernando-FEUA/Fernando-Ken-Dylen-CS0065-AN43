# LoopGuard - Listener-friendly English speaking script

23 core slides. 1,150 spoken words. Approximately 9:44 at 125 words per minute, including 32 seconds of pauses.

Read the spoken paragraphs. Presenter cues and sources are not read aloud.

## Speaker allocation

| Presenter | Core slides | Spoken words | Estimated time |
| --- | --- | ---: | --- |
| Ken | 1-5 | 231 | 2:00 |
| Maersk | 6-10 | 256 | 2:09 |
| Rey | 11-14 | 204 | 1:43 |
| Alvin | 15-19 | 251 | 2:08 |
| Nads | 20-23 | 208 | 1:45 |

Nads also handles optional slides 24-26: 171 words, approximately 1:25, outside the core presentation.

**Timing note:** The core estimate is 9:44 at 125 words per minute, including 32 seconds for comprehension pauses and speaker handoffs. Rehearse aloud; individual delivery speeds vary. Optional slides 24-26 and performing a full live demonstration are outside this estimate.

**Evidence note:** Code slides refer to real project source excerpts presented inside a macOS/VS Code-style frame. Window styling is a presentation treatment, not evidence of macOS execution. The KNIME capture is genuine: four native nodes executed and the exported CSV contains six expected Friendship Fair classifications. This is a baseline Rule Engine check, separate from the advanced Python engine.

## Slide 01 - LoopGuard

**Speaker:** Ken

**Timing:** 0:00-0:22. 41 words.

Good day. Imagine spending twenty coins to make a gift, then selling it for twenty-four. You gain four coins. If you keep repeating this, was that reward planned? LoopGuard helps game designers answer that question before changing their prices or rewards.

**Presenter cue:** Pause after the four-coin gain so the audience can picture the transaction.

**Pause:** 2 seconds.

**Sources:**

- docs/PROJECT.md
- README.md

## Slide 02 - The economy design problem

**Speaker:** Ken

**Timing:** 0:22-0:50. 55 words.

Here is how that example works. Twenty coins buy two ribbons. The player turns both ribbons into one gift, then sells it for twenty-four coins. We call that complete sequence a route because it starts and ends with coins. The problem is whether its four-coin gain can repeat in a way the designer never intended.

**Presenter cue:** Speak the exchange sequence slowly, with a short beat between buying, crafting and selling.

**Pause:** 2 seconds.

**Sources:**

- docs/PROJECT.md
- loopguard/engine.py

## Slide 03 - The designer's decision

**Speaker:** Ken

**Timing:** 0:50-1:14. 46 words.

LoopGuard gives the designer three kinds of advice. Correct means adjust a problematic price or reward. Preserve means keep a planned reward with known limits. Investigate means check missing information or a possible weakness. Each recommendation includes a reason. The designer still decides what to change.

**Presenter cue:** Separate the three decisions with brief pauses; say what each action means.

**Pause:** 2 seconds.

**Sources:**

- loopguard/engine.py
- loopguard/rules.json

## Slide 04 - Friendship Fair

**Speaker:** Ken

**Timing:** 1:14-1:36. 44 words.

Our setting is an invented Sanrio fair. My Melody's shop makes the gift. Kuromi and Keroppi handle a separate charm exchange. Cinnamoroll and Pompompurin represent the café. These characters help us remember the shops. We invented their prices and rules for this classroom project.

**Presenter cue:** Establish the fictional setting. The character names are shop labels, not separate system concepts.

**Pause:** 1 seconds.

**Sources:**

- data/scenarios.json
- docs/ASSETS.md

## Slide 05 - Python, Streamlit and KNIME

**Speaker:** Ken

**Timing:** 1:36-2:00. 45 words.

The designer uses Streamlit, our Python application's interface, to enter prices and read recommendations. Python calculates the exchanges and checks thirty-five written rules. KNIME is a visual workflow tool that makes separate decisions from Python's calculated facts. Maersk will explain how those facts become advice.

**Presenter cue:** Finish the handoff, then allow Maersk to begin. Pronounce KNIME as 'nime', rhyming with 'time'.

**Pause:** 2 seconds.

**Sources:**

- README.md
- app.py
- knime/README.md

## Slide 06 - Facts the system needs

**Speaker:** Maersk

**Timing:** 2:00-2:26. 52 words.

Thanks, Ken. Start with the gift: what does it cost, and what does it return? The designer also enters whether the reward is planned, how often a trade is allowed, and how long players must wait. A blank limit means we do not know. Entering zero explicitly means there is no limit.

**Presenter cue:** Stress the difference between an unknown limit and a confirmed absence of a limit.

**Pause:** 1 seconds.

**Sources:**

- loopguard/engine.py
- loopguard/tables.py

## Slide 07 - How the inference works

**Speaker:** Maersk

**Timing:** 2:26-2:52. 53 words.

Python checks these entries, then connects the trades to find routes like our ribbon-to-gift example. It calculates what each complete route costs and returns. Next, the rules ask whether the gain is intended and what restricts repetition. That separates two questions: can the player earn coins, and should the designer allow that reward?

**Presenter cue:** Pause between the calculation question and the design decision.

**Pause:** 1 seconds.

**Sources:**

- loopguard/engine.py

## Slide 08 - Exact batches in Python

**Speaker:** Maersk

**Timing:** 2:52-3:14. 43 words.

Python must respect complete trades. If a gift requires two ribbons, half a recipe cannot count as a finished gift. The code finds the smallest combination of whole trades that works and keeps fractions exact, so rounding does not create a false profit.

**Presenter cue:** Explain the job of the code in full. Reading function names aloud is unnecessary.

**Pause:** 1 seconds.

**Sources:**

- loopguard/engine.py:168-180

## Slide 09 - Rules that turn facts into advice

**Speaker:** Maersk

**Timing:** 3:14-3:40. 52 words.

The rules turn the result into advice. If a profitable route is unintended and has no limits, flag it for correction. If it is planned and limited, preserve it. If important facts are missing, ask for evidence. This is our expert system: written decision rules applied to facts, with the reasoning recorded.

**Presenter cue:** Leave a beat before defining 'expert system'; the preceding examples explain the definition.

**Pause:** 1 seconds.

**Sources:**

- loopguard/rules.json
- loopguard/engine.py

## Slide 10 - How the rules make a decision

**Speaker:** Maersk

**Timing:** 3:40-4:09. 56 words.

Our decision code also distinguishes an unlimited planned reward from an unlimited accidental one. It rates the planned reward as high concern and the accidental reward as critical. A planned, limited reward can be preserved. Missing-information checks happen first, so an unknown limit is never silently treated as unlimited. Rey will apply this to our examples.

**Presenter cue:** Use 'planned' and 'accidental' consistently. Pause for the speaker handoff.

**Pause:** 2 seconds.

**Sources:**

- loopguard/engine.py:312-323

## Slide 11 - The Friendship Gift route

**Speaker:** Rey

**Timing:** 4:09-4:34. 51 words.

Thanks, Maersk. Our gift turns twenty coins into two ribbons, then one gift, then twenty-four coins. The designer marks the four-coin gain as unintended and confirms there are no limits or waiting times. LoopGuard flags it as critical. Both the extra coins and the unrestricted repetition explain why it needs correction.

**Presenter cue:** Repeat the familiar sequence calmly, then explain the conditions that make it a problem.

**Pause:** 1 seconds.

**Sources:**

- data/scenarios.json
- loopguard/engine.py

## Slide 12 - Baseline audit results

**Speaker:** Rey

**Timing:** 4:34-5:00. 51 words.

Now consider charms. Eight coins buy a stamp, which becomes a charm worth twelve coins. Each account can buy only two stamps daily, but can pass items to other accounts. Could several accounts combine purchases? LoopGuard flags that concern for investigation. It has not proven that players can bypass the limit.

**Presenter cue:** Explain the stamp-to-charm trade before its restriction. Transfers create a question, not proof of a bypass.

**Pause:** 1 seconds.

**Sources:**

- data/scenarios.json
- loopguard/engine.py

## Slide 13 - An intentional café reward

**Speaker:** Rey

**Timing:** 5:00-5:25. 50 words.

The café shows why profit alone is not a problem. Ten coins buy two beans, which make a latte worth fourteen coins. This reward is planned. The café allows only three payouts daily across the whole fair. Each player waits an hour between payouts. LoopGuard recommends keeping this controlled reward.

**Presenter cue:** Explain the shared daily limit and each player's waiting time separately.

**Pause:** 1 seconds.

**Sources:**

- data/scenarios.json
- loopguard/rules.json

## Slide 14 - Missing information changes the answer

**Speaker:** Rey

**Timing:** 5:25-5:52. 52 words.

Now suppose the designer leaves the gift's limits blank. We still know it earns four coins, but we cannot tell how often it can repeat. LoopGuard requests more information. Its daily simulation says 'No estimate', which means insufficient information, not zero earnings. Alvin will show how a designer can use these decisions.

**Presenter cue:** Pause after 'No estimate' and explain its meaning before handing over.

**Pause:** 2 seconds.

**Sources:**

- data/scenarios.json
- loopguard/engine.py

## Slide 15 - The Streamlit workbench

**Speaker:** Alvin

**Timing:** 5:52-6:18. 53 words.

Thanks, Rey. In Streamlit, the designer enters or loads the shop prices, runs a check, and reads why a route was flagged. They can edit the prices, preview a fix, or undo a change. They can also export the project to a file, so their entered prices and rules can be reopened later.

**Presenter cue:** Describe the designer's actions as a sequence. Tab names are not needed to follow it.

**Pause:** 1 seconds.

**Sources:**

- app.py
- README.md

## Slide 16 - A correction the designer can preview

**Speaker:** Alvin

**Timing:** 6:18-6:40. 44 words.

For the gift, we can preview reducing the selling price to twenty coins. Spending twenty and receiving twenty removes the gain. The preview checks a copy before applying changes. A daily limit works differently: the four-coin gain remains, but it can happen fewer times.

**Presenter cue:** Pause between changing the amount earned and limiting how often it is earned.

**Pause:** 1 seconds.

**Sources:**

- loopguard/engine.py
- app.py

## Slide 17 - One-day simulation

**Speaker:** Alvin

**Timing:** 6:40-7:10. 57 words.

We also estimate a day's earnings before that correction. Of ten requested runs, gifts complete all ten, earning forty extra coins. Charms stop at two runs, earning eight. The café stops at three, earning twelve. We assume one account, enough starting money and supplies, and initially unused shared limits. Earnings are not reused to fund more trades.

**Presenter cue:** Pair each completed-run count with its gain. Pause between the three examples.

**Pause:** 2 seconds.

**Sources:**

- loopguard/engine.py:430-447
- data/scenarios.json

## Slide 18 - KNIME rule workflow

**Speaker:** Alvin

**Timing:** 7:10-7:36. 52 words.

KNIME makes a separate decision from the same calculated facts. Python exports facts such as profit and limits. KNIME reads them, applies rules to choose a category and urgency, then saves its decisions. Streamlit checks that both sets of results cover the same routes and current prices and rules before comparing them.

**Presenter cue:** Say that KNIME receives facts, not Python's verdicts. Its role is a separate rule check.

**Pause:** 1 seconds.

**Sources:**

- knime/README.md
- knime/run_workflow.py

## Slide 19 - Native KNIME execution

**Speaker:** Alvin

**Timing:** 7:36-7:59. 45 words.

We ran KNIME manually. All four workflow steps executed, and its six decisions matched the expected results for our starting Friendship Fair example. That verifies this particular run. Python still handles finding routes, calculating trades, previewing fixes, and simulation. Nads will explain our wider checks.

**Presenter cue:** State the verified result and its limit clearly, then hand over to Nads.

**Pause:** 2 seconds.

**Sources:**

- knime/README.md
- knime/LoopGuard Friendship Fair/workflow.knime
- ../../work/loopguard-presentation/evidence-assets/knime-workflow-executed.png

## Slide 20 - Four demonstration scenarios

**Speaker:** Nads

**Timing:** 7:59-8:28. 57 words.

Thanks, Alvin. We prepared four versions of the fair. Friendship Fair is the starting example. Balanced Market corrects the unintended gains. Missing Telemetry deliberately removes information, so the system should ask questions. Festival Rush raises the gift payout and removes café limits. Changing the facts lets us check whether the same rules produce the appropriate different advice.

**Presenter cue:** Explain each scenario name when introducing it; do not rely on the audience reading a table.

**Pause:** 1 seconds.

**Sources:**

- data/scenarios.json
- tests/test_engine.py

## Slide 21 - Evaluation

**Speaker:** Nads

**Timing:** 8:28-8:51. 47 words.

Our October twenty-fifth record reports one hundred sixteen passing tests. They check calculations, decisions, data exchange, and Streamlit interactions. These functions behaved as expected in those tests. To learn whether game designers actually find the system useful, we still need trials with people and realistic game data.

**Presenter cue:** Present the test count as a recorded result, then distinguish software checks from user evaluation.

**Pause:** 1 seconds.

**Sources:**

- docs/VERIFICATION.md
- tests/test_engine.py
- tests/test_tables.py
- tests/test_knime_contract.py
- tests/test_streamlit_app.py

## Slide 22 - Scope and next steps

**Speaker:** Nads

**Timing:** 8:51-9:19. 56 words.

This prototype checks routes of up to six trades, within fixed search limits. Each trade converts one kind of item into one other kind. Changing demand, scarce stock, and random rewards are outside its scope. A clean result applies only to the entered rules and search performed. Broader KNIME checks and game-designer feedback are next steps.

**Presenter cue:** Make the practical limit clear: no flagged route is not a guarantee about an entire real game.

**Pause:** 1 seconds.

**Sources:**

- loopguard/engine.py:20-22
- loopguard/engine.py:425
- docs/PROJECT.md

## Slide 23 - Classroom demonstration

**Speaker:** Nads

**Timing:** 9:19-9:44. 48 words.

We followed the gift from a four-coin gain to a correction. Reducing its selling price to twenty coins removes that gain. Keeping the original price but leaving limits unknown produces a request for information instead. LoopGuard helps designers understand the recommendation before changing their game's rewards. Thank you.

**Presenter cue:** This closes the timed explanation. The missing-information example keeps the original twenty-four-coin payout. Perform a full live demo only with extra time, or substitute it for the earlier walkthrough.

**Pause:** 2 seconds.

**Sources:**

- README.md
- data/scenarios.json
- app.py

## Slide 24 - Appendix: five-member roles

**Speaker:** Nads

**Optional appendix:** Outside core timing. 45 words.

Building this system involves five work areas: writing the decision rules, implementing Python calculations, building the KNIME workflow, creating the Streamlit interface, and testing and documentation. Together, these take an example from a written policy to an application whose calculations and explanations can be checked.

**Presenter cue:** Optional. Discuss actual contributions accurately; do not infer development ownership from speaking assignments.

**Pause:** 1 seconds.

**Sources:**

- docs/PROJECT.md

## Slide 25 - Appendix: defense questions

**Speaker:** Nads

**Optional appendix:** Outside core timing. 77 words.

Why is this an expert system? It applies written decision rules to supplied facts and explains the result. Why not train a model? Our decision criteria are already explicit, so training data is unnecessary for this prototype. Why Sanrio? Familiar characters make the invented shops easier to remember. Is every profit an exploit? No. Our café intentionally rewards players within known limits. What does KNIME add? A separate visual rule workflow whose six starting-example decisions we verified.

**Presenter cue:** Optional questions. Read only the relevant question and answer. The complete set is not part of the ten-minute talk.

**Pause:** 1 seconds.

**Sources:**

- docs/PROJECT.md
- loopguard/engine.py
- knime/README.md

## Slide 26 - Sources and acknowledgments

**Speaker:** Nads

**Optional appendix:** Outside core timing. 49 words.

Our calculations and decisions can be checked against the project's code, written rules, example data, and verification record. We used official Python, Streamlit, and KNIME documentation. The characters belong to Sanrio. This is an unofficial classroom project, and the shops, prices, and trading rules were invented for our examples.

**Presenter cue:** Optional acknowledgments. Use this section when sources or credits are requested.

**Pause:** 1 seconds.

**Sources:**

- docs/ASSETS.md
- docs/PROJECT.md
- docs/VERIFICATION.md
- https://www.sanrio.co.jp/characters/
