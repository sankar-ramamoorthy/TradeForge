# How To Set Up Provider Keys

TradeForge stores provider credentials in a local encrypted registry named
`.keys.enc`. The registry is decrypted only through `TRADEFORGE_MASTER_KEY`,
which must live in the OS environment, not in Git and not in `.env`.

## 1. Generate the master key

### Compose first-run UI

After `docker compose up --build`, open TradeForge and go to Provider
Governance. If no `TRADEFORGE_MASTER_KEY` and no `.keys.enc` exist, the
first-run setup panel can generate the master key in the browser. It shows the
key once and writes it to `.tradeforge/runtime.env`, which Docker Compose mounts
into the runtime container and Git ignores.

This is a local single-operator trust tradeoff: the key is not committed and is
not logged, but it is still a local plaintext runtime secret. Save the shown key
outside the repository. If `.keys.enc` already exists, first-run setup is
disabled because TradeForge cannot know whether the existing credential store
belongs to a different master key.

### CLI path

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

If you run TradeForge through Docker Compose without provider credentials,
`TRADEFORGE_MASTER_KEY` is optional. When you use encrypted provider
credentials, either use the first-run UI path above or make the key available to
the `tradeforge` container through the shell environment.

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

TradeForge talks to LiteLLM through the same encrypted credential registry. For
the managed Docker Compose runtime, register the internal LiteLLM service URL:

```powershell
$env:LITELLM_MASTER_KEY = "sk-tradeforge-local-dev"
uv run python scripts\manage_credentials.py register litellm `
  --base-url "http://litellm:4000" `
  --api-key $env:LITELLM_MASTER_KEY
```

LiteLLM is not exposed on `localhost:4000` by default. Browser and operator
workflows should reach advisory functions through TradeForge.

If you intentionally need temporary host access for local LiteLLM inspection,
start the debug override and use `http://localhost:4000` only for that debug
session:

```powershell
docker compose --profile advisory -f docker-compose.yml -f docker-compose.litellm-debug.yml up -d litellm
```

Provider Governance stores advisory model selection separately from the LiteLLM
gateway credential. Select explicit provider/model pairs through
`/workspaces/provider-governance`, for example provider `llm_groq` plus model
`groq/llama-3.1-70b-versatile`. This selection is operational configuration
only; it is not event-ledger truth.

### Downstream LLM provider secrets

M13B moves downstream model-provider key governance into TradeForge. Store
provider keys in `.keys.enc` with these provider IDs:

```powershell
uv run python scripts\manage_credentials.py register llm_groq --api-key "<groq-key>"
uv run python scripts\manage_credentials.py register llm_nvidia_nim --api-key "<nvidia-nim-key>"
uv run python scripts\manage_credentials.py register llm_openai --api-key "<openai-key>"
uv run python scripts\manage_credentials.py register llm_anthropic --api-key "<anthropic-key>"
uv run python scripts\manage_credentials.py register llm_google --api-key "<google-key>"
```

The UI/API only shows masked values. Runtime decryption occurs at the
composition boundary, where TradeForge resolves the selected provider ID and
adds the required `api_key` to that individual LiteLLM `/chat/completions`
request. Ollama is keyless and uses a configured API base instead of a stored
CredentialStore secret.

Start the optional LiteLLM service with:

```powershell
docker compose --profile advisory up -d litellm
```

LiteLLM remains stateless in the managed local runtime. Do not configure a
LiteLLM database for TradeForge provider secrets, do not use
`POST /config/update`, and do not put downstream provider API keys in LiteLLM
environment variables or `litellm_config.yaml`. TradeForge's governed
credential store is the authoritative owner of these secrets and supplies them
per request.

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
