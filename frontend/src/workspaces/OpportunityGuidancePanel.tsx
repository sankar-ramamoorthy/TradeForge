export function OpportunityGuidancePanel() {
  return (
    <section className="opportunity-guidance-panel" aria-label="Opportunity guidance">
      <div className="panel-heading">
        <p className="eyebrow">Reasoning Guide</p>
        <span className="field-authority-badge authority-advisory">Advisory</span>
      </div>
      <div className="opportunity-guidance-grid">
        <div>
          <dt>What confirms this setup?</dt>
          <dd>Identify the evidence that would make the idea more credible.</dd>
        </div>
        <div>
          <dt>What would invalidate it?</dt>
          <dd>Define the condition that would make the setup no longer worth pursuing.</dd>
        </div>
        <div>
          <dt>What is still missing?</dt>
          <dd>Separate missing information from information that remains uncertain.</dd>
        </div>
        <div>
          <dt>What still requires judgment?</dt>
          <dd>Keep discretionary interpretation explicit before building the thesis.</dd>
        </div>
      </div>
    </section>
  );
}
