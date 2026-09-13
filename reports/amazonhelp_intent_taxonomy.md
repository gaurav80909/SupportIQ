# AmazonHelp Intent Taxonomy Report

## Overview
This taxonomy defines 10 core customer-support intents discovered empirically from **168,811** `@AmazonHelp` customer-brand conversation pairs in the Twitter Customer Support (TWCS) dataset (`data/raw/twcs.csv`), analyzing **129,352** English-language customer interactions.

Unlike Apple's device- and OS-centric taxonomy, Amazon's inquiries are heavily driven by retail logistics, fulfillment speed, order modifications, subscriptions (Prime), digital hardware/ecosystem services, and account security.

---

## Discovered Intent Taxonomy (10 Intents)

| # | Intent Name | Description | Approx. Count | % of Turn-Pairs |
|---|---|---|---|---|
| 1 | `delivery_delay_and_tracking` | Delayed shipments, carrier transit lags, tracking number queries, missed delivery dates. | 15,378 | 11.9% |
| 2 | `refunds_and_billing_charges` | Missing/delayed refunds, duplicate charges, unexpected debits, GST/tax calculation issues. | 7,108 | 5.5% |
| 3 | `general_service_inquiry` | Escalations, call-center IVR complaints, requests to talk to a supervisor or human agent. | 6,343 | 4.9% |
| 4 | `returns_and_replacements` | Return requests, scheduling pickup, return shipping labels, product exchanges. | 5,373 | 4.2% |
| 5 | `digital_content_and_devices` | Kindle e-books, Fire TV/stick, Echo/Alexa skills, Prime Music streaming, app stability. | 3,721 | 2.9% |
| 6 | `order_cancellation_and_modification` | Order cancellations, unintended auto-cancellations, delivery address changes before dispatch. | 2,791 | 2.2% |
| 7 | `damaged_defective_or_wrong_item` | Items received damaged, broken, missing parts, tampered packaging, or wrong model delivered. | 2,470 | 1.9% |
| 8 | `prime_membership_and_benefits` | Prime subscription inquiries, renewal billing, trial expiration, guaranteed delivery benefits. | 1,732 | 1.3% |
| 9 | `payment_and_gift_cards` | Declined payment methods, gift card redemptions, promo code errors, checkout failures. | 1,268 | 1.0% |
| 10 | `account_access_and_security` | Locked accounts, password resets, OTP/2FA issues, unauthorized credential changes. | 1,220 | 0.9% |

---

## Intent Details & Real Representative Examples

### 1. `delivery_delay_and_tracking`
- **Description:** Inquiries about delayed shipments, missing tracking updates, transit delays, carrier ETA discrepancies, or packages not arriving by the promised date.
- **Representative Real Examples:**
  - *"I can only give you item tracking no 226108405848 #donttrustamazon"*
  - *"tracking says my package was delivered at 11:39am but it is nowhere to be found and it's impossible to get ahold of a customer service agent on the phone."*
  - *"Your correspondence does NOT address the problem. I am not interested in knowing WHY order is delayed , just refund my amount without excuse"*

### 2. `refunds_and_billing_charges`
- **Description:** Questions regarding refund status, turnaround times, cashback, unexpected debits, overbilling, tax/GST issues, or duplicate card charges.
- **Representative Real Examples:**
  - *"Hi i want to purchase oneplus 5 paying through sbi debit card will i get cashback later"*
  - *"I have filled in the form as advised by you. Can you sort it out ASAP and recompense as promised AND refunded."*
  - *"Well, I have ordered with prime product with extra charge. Therefore why would your customer wait for 4long hours???"*

### 3. `general_service_inquiry`
- **Description:** General customer service escalation, complaints about call center/IVR delays, requests to speak with supervisors or human representatives.
- **Representative Real Examples:**
  - *"reaching to Ur customer service is more pathetic... The call gets cut everytime, don't want stupid IVR"*
  - *"Third class service ever n ever..my 500 cashback still not credited promised date is already over..bad customer service"*
  - *"made 2 times call to the customer support,every once I call they just update the status. How come one courier left from a place twice aday."*

### 4. `returns_and_replacements`
- **Description:** Requests to return orders, schedule courier pickup, obtain return mailing labels, or exchange products for a replacement.
- **Representative Real Examples:**
  - *"instead of replacing the product with the same price you guys are asking me to place the new one. Strange. #disappointed #Amazon"*
  - *"Hey if you are going to drop wiper blades from S&S maybe make sure the ones you suggest as a replacement fit my vehicle?"*
  - *"Brands do claim this but how many actually live up to it. Struggling with for more than 20 days now for a replacement."*

### 5. `digital_content_and_devices`
- **Description:** Issues and inquiries concerning Kindle e-books, Fire TV / Firestick, Echo & Alexa skills, Prime Music streaming, or app crashes.
- **Representative Real Examples:**
  - *"I can not seem to have the option of writing a review for Alexa skills can you guide"*
  - *"Got an for my birthday. Keep saying 'please' to Alexa. Hope that helps me when the machines rise up. Wonder if she'll remember. #Skynet"*
  - *"If you’ve locked my account how the hell am I supposed to use my Echo?"*

### 6. `order_cancellation_and_modification`
- **Description:** Requests to cancel orders, inquiries about automatic system cancellations, or requests to modify shipping addresses before dispatch.
- **Representative Real Examples:**
  - *"Thanks! You've just turned my super-excited 7yo into a very sad 7yo by screwing up #XBoxOne dvy - order & #AmazonPrime cancelled"*
  - *"Really would like your help to resolve the issue with my order. Serious flaw in your automated system cancelled my order..."*
  - *"horrible service Ordered cancelled by urside and i got msg that it has been denied,irrespective of delivery attempts"*

### 7. `damaged_defective_or_wrong_item`
- **Description:** Reports of items received damaged, defective, broken, tampered/unsealed packaging, missing components, or entirely wrong items delivered.
- **Representative Real Examples:**
  - *"Purchased a new mobile from Amazon and it's faulty."*
  - *"Hi team still pick up has not happened for my damaged crockery."*
  - *"Item delivered against myOrder # 405-0883454-3951510 One 5 plus is empty box with soap. I need redressal."*

### 8. `prime_membership_and_benefits`
- **Description:** Questions and issues related to Amazon Prime memberships, renewal billing, trial expirations, Prime Video access, or guaranteed delivery perks.
- **Representative Real Examples:**
  - *"I have prime and wanted to make use of a two hour delivery in New York but app isn't recognising me as a prime member. Prime video app still does though"*
  - *"- Order# 408-3265294-3245900,I haven't recevied my product yet, nobody is giving the date ,i am a prime member"*
  - *"I'm a prime member and I paid extra for next day shipping"*

### 9. `payment_and_gift_cards`
- **Description:** Problems with payment card processing, gift card redemptions, promo code acceptance, wallet balances, or checkout payment failures.
- **Representative Real Examples:**
  - *"please add the option to use two payment methods. It denied my payment because my gift card did not cover it."*
  - *"my acount is lock and i cant use my gift card what do i do"*
  - *"did the sonos play:1 promo end? I thought tomorrow was last day. Your site is not accepting the promo code. Please advise!"*

### 10. `account_access_and_security`
- **Description:** Inability to sign in, account locks, unauthorized credential changes, password reset issues, or two-factor authentication (OTP) errors.
- **Representative Real Examples:**
  - *"hello, someone hacked my amazon account and changed my email and password. I have the email to prove it. Please help me"*
  - *"Cheating by amazon. No one is solving. Need help. Did shopping of 5 lac & account blocked with no reason. No answer."*
  - *"my account has been locked after a password attempt. I then made a new password to log in but it says it's still locked"*
