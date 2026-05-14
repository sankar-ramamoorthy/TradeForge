const STORAGE_KEY = "tradeforge.active_decision";

export type ActiveDecisionRecord = {
  decision_id: string;
  symbol: string;
  persona_id: string;
  persona_version: string;
  created_at: string;
};

export function getActiveDecision(): ActiveDecisionRecord | null {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return null;
    const parsed = JSON.parse(raw) as unknown;
    if (
      typeof parsed === "object" &&
      parsed !== null &&
      "decision_id" in parsed &&
      "symbol" in parsed &&
      typeof (parsed as Record<string, unknown>).decision_id === "string" &&
      typeof (parsed as Record<string, unknown>).symbol === "string"
    ) {
      return parsed as ActiveDecisionRecord;
    }
    return null;
  } catch {
    return null;
  }
}

export function setActiveDecision(record: ActiveDecisionRecord): void {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(record));
  } catch {
    // Storage quota exceeded or unavailable — fail silently
  }
}

export function clearActiveDecision(): void {
  try {
    localStorage.removeItem(STORAGE_KEY);
  } catch {
    // Fail silently
  }
}
