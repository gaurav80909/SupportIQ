# AppleSupport Data-Driven Intent Taxonomy Report

## 1. Executive Summary

This report defines an empirical, data-driven intent taxonomy derived directly from **106,645 customer support conversations** in `data/processed/AppleSupport_conversations.csv`. 

Through n-gram statistical profiling, TF-IDF term clustering, and semantic pattern discovery on the customer messages, we identified **11 mutually distinguishable customer-support intents** (10 high-specificity operational intents plus 1 general troubleshooting baseline). 

The dataset captures customer interactions with `@AppleSupport` during a critical timeframe (Q4 2017) characterized by:
- The release and iterative patching of **iOS 11** and **macOS High Sierra**.
- The hardware launches of **iPhone 8**, **iPhone 8 Plus**, and **iPhone X**.
- Widespread user-reported phenomena such as the infamous **iOS 11 autocorrect letter 'I' to 'A [?]' bug**, post-update battery degradation, and iPhone X OLED display inquiries.

---

## 2. Intent Distribution Overview

| Intent Name | Description Summary | Approx. Count | % of Dataset | Escalation Risk |
| :--- | :--- | :---: | :---: | :---: |
| **`software_update_os`** | OS upgrades, update download/install failures, and version regressions | 28,014 | 26.27% | Low (Automate with KB) |
| **`keyboard_autocorrect_messaging`** | Typing glitch (iOS 11 "I" bug), predictive text, iMessage/SMS delivery | 10,757 | 10.09% | Low (Known Workarounds) |
| **`battery_power_performance`** | Rapid battery drain, overheating, charging issues, sudden shutdowns, lag | 7,233 | 6.78% | Medium (Diagnostic check) |
| **`hardware_screen_audio_repair`** | Cracked screens, mic/speaker failure, Genius Bar, AppleCare warranty | 5,205 | 4.88% | High (Hardware dispatch) |
| **`itunes_apple_music_media`** | Apple Music streaming, playlist sync, missing libraries, song playback | 3,601 | 3.38% | Low (Settings / Sync steps) |
| **`app_store_app_crashes`** | App Store downloading, 3rd-party app crashes, launch failures | 2,785 | 2.61% | Medium (App vs OS isolation) |
| **`icloud_data_sync_backup`** | iCloud storage limits, photo library sync, backup/restore failures | 2,703 | 2.53% | Low (Storage / Cloud KB) |
| **`account_access_security`** | Apple ID login, locked/disabled accounts, 2FA codes, account takeover | 2,593 | 2.43% | **Critical (Always Escalate)** |
| **`connectivity_network`** | Wi-Fi dropouts, Bluetooth pairing, cellular data / "No Service", Hotspot | 2,409 | 2.26% | Medium (Network reset) |
| **`billing_subscriptions_payments`** | Unrecognized charges, refunds, subscription cancellations, Apple Pay | 2,342 | 2.20% | **High (Financial / Escalate)** |
| **`general_troubleshooting`** | Conversational follow-ups, short confirmations, general feedback | 39,003 | 36.57% | Medium (Context dependent) |
| **Total** | | **106,645** | **100.0%** | |

---

## 3. Detailed Taxonomy Specifications & Representative Real Examples

### 1. `software_update_os`
- **Scope:** Inquiries and complaints regarding operating system updates (iOS 11.x, macOS High Sierra, watchOS), update installation failures, software version compatibility, and issues arising immediately after an update.
- **Support Routing:** Routes to automated troubleshooting guides for update installation or known release notes.
- **Representative Real Examples from Dataset:**
  1. `"@AppleSupport The newest update. I️ made sure to download it yesterday."`
  2. `"Hey @AppleSupport and anyone else who upgraded to ios11.1, are y’all having issues with capital “I️” in the Mail app? As it puts in “A”?"`
  3. `"@AppleSupport I have the iPhone 6s Plus and just did the most recent update."`

---

### 2. `keyboard_autocorrect_messaging`
- **Scope:** Typing glitches, predictive text errors, autocorrect anomalies (dominated in this dataset by the viral iOS 11 glitch where typing capital "I" rendered an "A" followed by an [?] Unicode symbol), iMessage activation issues, and SMS text message delivery.
- **Support Routing:** High automation potential; provides known text replacement workarounds or points to upcoming minor point releases (e.g., iOS 11.1.1).
- **Representative Real Examples from Dataset:**
  1. `"Hello, internet. Can someone explain why this symbol keeps appearing on my phone and when I️ try to type the letter I️? Also @AppleSupport"`
  2. `"@AppleSupport tell me why I’ve updated my phone twice and I️ can’t type letter I️ without getting a letter A and a question mark"`
  3. `"@115858 creates amazing technology..... but talk to text still messes up 90% of what I will it to type..... #fixyourcrap"`

---

### 3. `battery_power_performance`
- **Scope:** Battery percentage dropping rapidly, device getting excessively hot/overheating, cable/adapter not charging, device shutting down at 20-30%, freezing, and interface lag.
- **Support Routing:** Provides battery health audit steps, background app refresh optimization, or recommends battery replacement service.
- **Representative Real Examples from Dataset:**
  1. `"I just need @115858 to do something about the battery life because it sucks ass"`
  2. `"@AppleSupport @116102 Battery life just got worst."`
  3. `"Question- @249 @115858 my iPhone6 dies very quick (have to charge it 3 times a day) my iPhone5 battery was faulty. Could this be the same?"`

---

### 4. `hardware_screen_audio_repair`
- **Scope:** Physical screen damage (cracks, lines, unresponsive touch digitizer), microphone/speaker muffling, physical buttons (home button, power button), camera hardware, warranty checks, and Genius Bar appointment bookings.
- **Support Routing:** Requires scheduling in-person repair, mail-in service, or AppleCare warranty evaluation. High likelihood of human agent handoff.
- **Representative Real Examples from Dataset:**
  1. `"@AppleSupport I just get a white screen and nothing loads. After a short time, it just closes/crashes. Thanks for the reply."`
  2. `"@AppleSupport why can’t I change ringer volume with the buttons? Whose dumb idea was it to change that and how do they still have a job?"`
  3. `"@AppleSupport ...cost for sending in for diagnosing a problem if it's out of warranty?"`

---

### 5. `itunes_apple_music_media`
- **Scope:** Apple Music streaming playback, disappearing offline songs or playlists, syncing media from Mac/PC iTunes to iPhone, and Podcast playback bugs.
- **Support Routing:** Digital media troubleshooting; guide user through iCloud Music Library toggling, re-authorizing iTunes, or restarting the Music app.
- **Representative Real Examples from Dataset:**
  1. `"@AppleSupport But this does not show the music stored on my phone like it did in os3. I do not want to store music on my phone."`
  2. `"@AppleSupport watchOs4 made my watch pointless Browsing music on my phone via the watch was 80% reason for buying it now it’s useless."`
  3. `"And why is my music NEVER in my control center?! @AppleSupport"`

---

### 6. `app_store_app_crashes`
- **Scope:** Third-party applications (YouTube, Twitter, Instagram, Snapchat, Spotify) or native apps crashing on launch, freezing during use, App Store downloads stuck on "Waiting" or "Pending", or inability to update apps.
- **Support Routing:** App troubleshooting (force close, offload app, re-install, check App Store server status).
- **Representative Real Examples from Dataset:**
  1. `"@AppleSupport Hi! What is going on? Has Youtube lost it? What can be done about it? Thanks for the support!"`
  2. `"@AppleSupport I've also forced the app to close from the background and reopened, no dice 🎲"`
  3. `"@AppleSupport no, my photos aren’t gone. why are there four (five actually, one isn’t pictured) albums in my photos all labeled twitter?"`

---

### 7. `icloud_data_sync_backup`
- **Scope:** iCloud storage full warnings, photos not uploading or syncing across devices, iCloud/iTunes backup failures ("Last Backup Could Not Be Completed"), and restoring data onto a new device.
- **Support Routing:** Guides user to manage storage tier, toggle iCloud Photos, or perform manual backup steps.
- **Representative Real Examples from Dataset:**
  1. `"@115858 Just updated iOS on iPhone7, now iCloud backup greyed out, cannot be turned on, says “Last Backup Never”"`
  2. `"@AppleSupport whenever I try to see the photos that I’ve just taken my #iphone6 shows me this. I’ve reset it, I’ve restored it... help?"`
  3. `"@AppleSupport I don’t know. I need the space though. How do I get rid of some snapshots"`

---

### 8. `account_access_security`
- **Scope:** Apple ID account recovery, forgotten password or passcode, account locked or disabled for security reasons, Two-Factor Authentication (2FA) verification code delivery failure, and unauthorized account access.
- **Support Routing:** **CRITICAL SAFETY / HIGH ESCALATION.** Due to privacy and security risk, automated systems must strictly adhere to verified recovery flows (iforgot.apple.com) and avoid autonomous credential operations.
- **Representative Real Examples from Dataset:**
  1. `"@AppleSupport Hello, I need some help regarding the region change on my Apple ID"`
  2. `"@AppleSupport how long does it take usually for account recovery to get back to you? It’s been about a week now."`
  3. `"@AppleSupport My wife made the mistake of updating to 11. How can we revert back? Her password keeper app is now dead. She can't access her passwords."`

---

### 9. `connectivity_network`
- **Scope:** Inability to join or maintain Wi-Fi connection, Bluetooth pairing failures with AirPods or car audio, cellular signal loss ("No Service" / "Searching"), LTE data speed issues, AirDrop, and Personal Hotspot.
- **Support Routing:** Guided network reset procedures (`Reset Network Settings`), carrier settings update verification, and Bluetooth pairing reset.
- **Representative Real Examples from Dataset:**
  1. `"@AppleSupport still no reliable Bluetooth on my iPhone 8+."`
  2. `"Is anyone else having problems with there iPhone 7 saying no service? @115858 @115714"`
  3. `"@AppleSupport The ‘Overlapping url over TIME on Free WiFi hotspots’ remains. v11.0.3. Not a WiFi problem; two different hotspots shown."`

---

### 10. `billing_subscriptions_payments`
- **Scope:** Disputed credit card charges, unexpected renewal of Apple Music/iCloud/App subscriptions, requests for refunds, payment method declined in App Store, and Apple Pay setup or transaction errors.
- **Support Routing:** **HIGH ESCALATION / HUMAN HANDOFF.** System should explain how to view active subscriptions (`reportaproblem.apple.com`) while escalating direct refund requests or billing disputes to human billing specialists.
- **Representative Real Examples from Dataset:**
  1. `"@AppleSupport I bought 2 iPhones X on Friday, but I don’t see any charge on my credit card. Do I should worry or it’s normal?"`
  2. `"@AppleSupport Help!! I need to update the payment method for my iPhone X pre-order. It won’t let me do it online"`
  3. `"@115858 My Q was: How was the delivery date in the cart 2 wks earlier than what’s on my receipt? #ServiceRecovery #SupplyChain #1standlastpreorder"`

---

### 11. `general_troubleshooting`
- **Scope:** Conversational turns, follow-up messages from ongoing threads (e.g., `"Yes I tried that"`, `"Ok done, now what?"`), expressions of gratitude or frustration, and ambiguous multi-issue queries that require clarifying questions.
- **Representative Real Examples from Dataset:**
  1. `"@AppleSupport Tried resetting my settings .. restarting my phone .. all that"`
  2. `"@AppleSupport I️ have an iPhone 7 Plus and yes I️ do"`
  3. `"@AppleSupport I️ need answers because it’s annoying 🙃"`

---

## 4. Architectural & Operational Recommendations

1. **Integration into Intent Classifier:**
   - Update `data/golden/taxonomy.json` and `src/intents/taxonomy.py` with these 11 data-backed classes to replace the initial generic placeholders.
2. **Escalation Policy Alignment:**
   - Map `account_access_security` and `billing_subscriptions_payments` to mandatory human escalation policies in `src/escalation/policy.py`.
3. **Golden Evaluation Set Construction:**
   - Stratify sampling for the 200-sample golden set across these 11 classes, ensuring adequate representation for high-impact classes (`account_access_security`, `billing_subscriptions_payments`, `hardware_screen_audio_repair`) alongside high-volume classes (`software_update_os`, `keyboard_autocorrect_messaging`).
