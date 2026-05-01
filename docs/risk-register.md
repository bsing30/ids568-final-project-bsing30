# Risk Register

| Category | Risk | Likelihood | Severity | Mitigation |
|---|---|---:|---:|---|
| Bias | Under-representation of minority issue phrasing | Medium | High | Balanced synthetic augmentation and monthly fairness slice review |
| Robustness | Prompt drift increases misroutes during product launches | High | Medium | Drift-triggered retraining and release freeze if score > 0.25 |
| Privacy | PII leakage in logs or embeddings | Low | High | Redaction middleware and 30-day retention limit |
| Compliance | Routing explanations insufficient for audit | Medium | Medium | Structured decision trace and approval workflow logging |
| Security | Prompt injection through retrieval artifacts | Medium | High | Retrieval source allowlist, content sanitization, and fallback policy |
| Compliance | Insufficient human review for high-impact misroutes | Medium | High | Tiered HITL escalation + review SLAs described in `docs/cto-memo.md`; log decisions in `logs/audit-trail.jsonl` |
