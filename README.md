# moex-feed

Public mirror of Moscow Exchange daily results and the latest price for the Chinese yuan (CNYRUB_TOM), refreshed hourly on weekdays by GitHub Actions.

- `data/moex_cny.csv` — daily results since 2013: open, high, low, close, weighted average price, number of trades
- `data/latest.json` — latest price and its update time

Source: [Moscow Exchange ISS](https://iss.moex.com) — free delayed data. Mirrored as is for non-commercial use; all rights to the data belong to Moscow Exchange. No warranty of completeness or accuracy.

Why a mirror: the exchange's API is often unreachable from servers outside Russia, while GitHub-hosted runners can usually reach it.
