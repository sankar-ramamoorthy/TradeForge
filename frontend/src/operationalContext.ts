const STORAGE_KEY = "tradeforge.operational_context";

type OperationalContext = {
  watched_symbols: string[];
  last_known_stage: string | null;
};

function defaultContext(): OperationalContext {
  return { watched_symbols: [], last_known_stage: null };
}

export function getOperationalContext(): OperationalContext {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return defaultContext();
    const parsed = JSON.parse(raw) as unknown;
    if (typeof parsed === "object" && parsed !== null) {
      const p = parsed as Record<string, unknown>;
      return {
        watched_symbols: Array.isArray(p.watched_symbols)
          ? (p.watched_symbols as string[]).filter((s) => typeof s === "string")
          : [],
        last_known_stage:
          typeof p.last_known_stage === "string" ? p.last_known_stage : null,
      };
    }
    return defaultContext();
  } catch {
    return defaultContext();
  }
}

function saveContext(ctx: OperationalContext): void {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(ctx));
  } catch {
    // fail silently
  }
}

export function syncDecisionSymbol(symbol: string | null): void {
  if (!symbol) return;
  const upper = symbol.toUpperCase();
  const ctx = getOperationalContext();
  const rest = ctx.watched_symbols.filter((s) => s !== upper);
  saveContext({ ...ctx, watched_symbols: [upper, ...rest] });
}

export function addWatchedSymbols(symbols: string[]): void {
  if (symbols.length === 0) return;
  const ctx = getOperationalContext();
  const existing = new Set(ctx.watched_symbols);
  const incoming = symbols
    .map((s) => s.toUpperCase())
    .filter((s) => s.length > 0 && !existing.has(s));
  if (incoming.length === 0) return;
  saveContext({ ...ctx, watched_symbols: [...ctx.watched_symbols, ...incoming] });
}

export function getWatchedSymbolsString(): string {
  return getOperationalContext().watched_symbols.join(", ");
}

export function syncLastKnownStage(stage: string | null): void {
  const ctx = getOperationalContext();
  if (ctx.last_known_stage === stage) return;
  saveContext({ ...ctx, last_known_stage: stage });
}

export function clearOperationalContext(): void {
  try {
    localStorage.removeItem(STORAGE_KEY);
  } catch {
    // fail silently
  }
}
