# moex-feed

Public mirror of Moscow Exchange daily results and the latest price for the Chinese yuan (CNYRUB_TOM), refreshed hourly on weekdays by GitHub Actions.

- `data/moex_cny.csv` — daily results since 2013: open, high, low, close, weighted average price, number of trades
- `data/latest.json` — latest price and its update time

Source: [Moscow Exchange ISS](https://iss.moex.com) — free delayed data. Mirrored as is for non-commercial use; all rights to the data belong to Moscow Exchange. No warranty of completeness or accuracy.

`certs/russian_trusted_root_ca.pem` — the root certificate of the Russian Ministry of Digital Development, which issued the exchange's TLS certificate. It is trusted only for requests to the exchange (SHA-256 `D2:6D:2D:02:31:B7:C3:9F:92:CC:73:85:12:BA:54:10:35:19:E4:40:5D:68:B5:BD:70:3E:97:88:CA:8E:CF:31`, matches the official file published by Gosuslugi).

Why a mirror: the exchange's API is often unreachable from servers outside Russia (its certificate chain is not trusted there by default, and connections sometimes time out), while GitHub-hosted runners can usually reach it.
