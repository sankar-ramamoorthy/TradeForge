type Props = {
  symbol: string;
  stage: string | null;
  subtitle: string;
};

export function InstrumentIdentityBanner({ symbol, stage, subtitle }: Props) {
  return (
    <section className="instrument-identity-banner" aria-label="Instrument identity">
      <div>
        <p className="eyebrow">Instrument</p>
        <h2>{symbol}</h2>
      </div>
      <div>
        <p>{subtitle}</p>
        <span className="instrument-stage-badge">{stage ?? "Unstaged"}</span>
      </div>
    </section>
  );
}
