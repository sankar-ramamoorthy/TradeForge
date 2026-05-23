# How To Set Up Provider Keys

TradeForge stores provider credentials in a local encrypted registry named
`.keys.enc`. The registry is decrypted only through `TRADEFORGE_MASTER_KEY`,
which must live in the OS environment, not in Git and not in `.env`.

## 1. Generate the master key

Run this once:

```powershell
uv run python scripts\manage_credentials.py generate-master-key
```

Copy the printed value into your OS environment for the current session:

```powershell
$env:TRADEFORGE_MASTER_KEY = "<generated-value>"
```

For persistent local use on Windows, set it in your user environment:

```powershell
[Environment]::SetEnvironmentVariable(
  "TRADEFORGE_MASTER_KEY",
  "<generated-value>",
  "User"
)
```

Open a new terminal after setting a persistent user variable.

If you run TradeForge through Docker Compose, the shell that launches
`docker compose` must also have `TRADEFORGE_MASTER_KEY` available. Compose
passes that host value into the `tradeforge` container at startup and will
fail fast if it is missing.

## 2. Register provider credentials

Run the commands for the providers you use:

```powershell
uv run python scripts\manage_credentials.py register polygon --api-key "<polygon-key>"
uv run python scripts\manage_credentials.py register alpaca --api-key "<alpaca-key>" --secret-key "<alpaca-secret>"
uv run python scripts\manage_credentials.py register alpha_vantage --api-key "<alpha-vantage-key>"
uv run python scripts\manage_credentials.py register fmp --api-key "<fmp-key>"
uv run python scripts\manage_credentials.py register finqual --api-key "<finqual-key>"
```

This creates or updates `.keys.enc` in the project root. The file contains
encrypted payloads, not plaintext provider keys.

### LiteLLM advisory credentials

TradeForge talks to LiteLLM through the same encrypted credential registry. If
the backend runs on the host, register LiteLLM with `localhost`:

```powershell
$env:LITELLM_MASTER_KEY = "sk-tradeforge-local-dev"
uv run python scripts\manage_credentials.py register litellm `
  --base-url "http://localhost:4000" `
  --api-key $env:LITELLM_MASTER_KEY `
  --default-model "tradeforge-groq-70b"
```

If the backend runs inside Docker Compose, register the Compose service URL
instead:

```powershell
uv run python scripts\manage_credentials.py register litellm `
  --base-url "http://litellm:4000" `
  --api-key $env:LITELLM_MASTER_KEY `
  --default-model "tradeforge-groq-70b"
```

Start the optional LiteLLM service with:

```powershell
$env:GROQ_API_KEY = "<groq-key>"
docker compose --profile advisory up -d litellm
```

`litellm_config.yaml` reads provider API keys from environment variables such
as `GROQ_API_KEY` and `NVIDIA_NIM_API_KEY`. Do not put provider keys in the
config file.

## 3. Select a market provider when needed

`yfinance` remains the default and does not require credentials.

To run with a credentialed market provider:

```powershell
$env:TRADEFORGE_MARKET_PROVIDER = "polygon"
```

or:

```powershell
$env:TRADEFORGE_MARKET_PROVIDER = "alpaca"
```

Then start the backend normally.

## Rotation

Rotate a provider credential by registering that provider again with the new
value:

```powershell
uv run python scripts\manage_credentials.py register polygon --api-key "<new-polygon-key>"
```

For Alpaca:

```powershell
uv run python scripts\manage_credentials.py register alpaca --api-key "<new-alpaca-key>" --secret-key "<new-alpaca-secret>"
```

The new encrypted credential replaces the prior record for that provider.

If the master key itself must rotate, generate a new master key, preserve the
old key long enough to decrypt existing credentials, and re-register each
provider under the new key before retiring the old environment value.

## Revocation

When a provider key is revoked:

1. Revoke it at the provider first.
2. Register the replacement credential if the provider remains in use.
3. If the provider is no longer used, remove `.keys.enc` only after confirming
   you no longer need any stored provider credentials, then rebuild the file by
   registering only active providers.

Credential status fields exist in the runtime model for future replay-aware
history, but M10C uses local encrypted storage rather than an event-sourced
credential lifecycle.

## Never commit or log secrets

Do not commit:

- `.keys.enc`
- any file named `TRADEFORGE_MASTER_KEY`
- provider API keys or provider secret keys

Do not paste decrypted keys into logs, shell history, issue text, screenshots,
or documentation. If a secret is exposed, revoke it at the provider and rotate
it immediately.
