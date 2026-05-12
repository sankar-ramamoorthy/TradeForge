export type RuntimeStatus = {
  status: "ok";
  runtime: "tradeforge";
  boundary: "http";
  owns_domain_rules: false;
};

export async function fetchRuntimeStatus(
  signal?: AbortSignal
): Promise<RuntimeStatus> {
  const response = await fetch("/health", { signal });

  if (!response.ok) {
    throw new Error(`Runtime status request failed: ${response.status}`);
  }

  return response.json() as Promise<RuntimeStatus>;
}
