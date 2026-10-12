# Data handling

**The values you check are not stored.** Emails, phone numbers, IPs and domains sent to Veriq are processed in memory to produce the result and then discarded. They are not written to the database, used for training, or shared.

What Veriq does store:

| Data | Why |
| --- | --- |
| Account email | Login, billing receipts |
| API key, as a one-way hash | Authenticating requests; the raw key is shown to you once |
| Usage counts (check type, count, time) | Credit metering and your dashboard |
| Payment reference, plan, amount | Billing records (card details are handled by Paystack, never by Veriq) |

Bulk CSV uploads are processed in memory and returned to you; the file is not kept.

Live lookups query public DNS and RDAP servers, which see the domain being looked up, as with any DNS query.

Questions or deletion requests: fredrickaffoh81@gmail.com. Full policy: https://veriq-u2at.onrender.com/privacy
