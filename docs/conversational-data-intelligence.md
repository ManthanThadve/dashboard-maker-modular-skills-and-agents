# Governed Conversational Data Intelligence for Banking

## Purpose and problem

Business owners need timely answers from operational data without waiting for an analyst or learning SQL. A chat interface can make governed data accessible, but sending customer data to an external managed agent may violate bank policy. This proposal is an in-house platform that turns approved business questions into safe, evidence-backed analytics against the bank's governed data estate.

It is not a general-purpose chatbot or a replica of every BigQuery Agent feature. Its core job is:

`question -> business context -> approved data -> safe query -> results -> cited answer`

## Example: customer migration

For onboarding customers from legacy applications to a new banking application, a stakeholder may ask:

- How many customers have migrated, are new, in flight, or failed?
- What are the leading failure reasons by channel, region, or application version?
- Is migration completion high enough to begin offering lending products?

The platform must define terms consistently (for example, *migrated* means `migration_status = COMPLETED`), apply the requester's access rights, query only approved datasets, and show the query logic, freshness, and limitations with the answer.

## Conceptual Data Agent workflow

This follows the useful pattern of conversational analytics agents:

1. Interpret the question and any conversation context.
2. Retrieve relevant business definitions, table/view metadata, policies, and proven examples.
3. Select the authorized semantic model and analytical tool.
4. Generate an analytical plan and constrained SQL.
5. Validate, estimate, and execute the query against governed data.
6. Interpret the returned aggregate result; answer with definitions, citations, and follow-up prompts.
7. Record the full decision and execution trail.

## Proposed architecture

```text
Chat UI / API
  -> Identity, entitlement, and policy gateway
  -> Orchestrator agent
       -> Knowledge retrieval (glossary, metric catalog, metadata, verified queries)
       -> Tools: semantic query, SQL validator/executor, charting, explanation
  -> Governed analytics zone (BigQuery views / curated marts)
  -> Response with evidence, lineage, and audit event
```

The LLM plans and explains; deterministic services enforce authorization, query safety, and data access. The model should not receive unrestricted database credentials or raw sensitive records.

## Semantic and business knowledge layer

Maintain a versioned, owner-backed knowledge layer containing:

- business glossary, synonyms, approved dimensions, and metric formulas;
- logical semantic models mapped to curated views rather than raw source tables;
- table/column descriptions, lineage, refresh cadence, quality status, and sensitivity labels;
- policy rules such as minimum aggregation thresholds and permitted joins; and
- **verified queries**: reviewed question-to-SQL examples with expected interpretation, used as few-shot guidance and as reusable trusted answers.

Business owners approve definitions; data stewards own metadata and quality; engineering controls deployment and policy enforcement.

## Agent tools and RAG

Expose small, typed tools instead of broad database access: search catalog, retrieve metric definition, resolve authorized model, generate query plan, validate/estimate SQL, execute approved SQL, render chart, and retrieve prior verified query.

Use RAG primarily for compact, curated knowledge: glossary, policies, metadata summaries, query examples, and documentation. Retrieve by domain, user entitlement, dataset, and question intent. Do not use RAG as a substitute for current numerical results; facts and aggregates come from a live governed query.

## SQL generation and guardrails

Generate standard SQL only against an allowlist of semantic views/models. Parse and validate SQL before execution; reject DDL/DML, scripts, external connections, unapproved tables, unsafe joins, excessive complexity, and unsupported functions. Apply query parameterization, row/byte limits, timeouts, dry-run cost estimation, and result-size limits. Prefer an intermediate query plan for complex questions and require approval or analyst escalation for ambiguous logic.

## Authorization, security, and PII

Authenticate users through corporate SSO and propagate identity to the data layer. Enforce least privilege with dataset/view IAM, row-level and column-level security, policy tags, dynamic masking, and tenant/business-unit filters. Start with aggregate-only answers and deny or mask PII, account identifiers, and sensitive attributes by default. Apply k-anonymity/minimum-cell suppression and block reconstruction-prone drill-downs. Encrypt data in transit and at rest; keep prompts, retrieval context, and tool logs within approved bank-controlled boundaries.

## Analytics zone and GCP-oriented stack

Create a dedicated analytics zone of curated BigQuery marts and authorized views. Keep source systems and raw landing data separate; transform with Dataform or dbt and publish tested semantic views.

Recommended GCP-aligned components:

- **Data and governance:** BigQuery, Dataplex/Dataplex Catalog, Data Catalog-style metadata and policy tags, Cloud DLP, IAM, Cloud KMS, VPC Service Controls.
- **Transformations and quality:** Dataform or dbt, BigQuery data quality checks, lineage, and scheduled refreshes.
- **Agent and API:** Vertex AI (Gemini model hosted in the approved project), Cloud Run or GKE for orchestration/tool services, API Gateway/Apigee, Identity-Aware Proxy or corporate SSO integration.
- **Knowledge and search:** BigQuery metadata tables plus Vertex AI Vector Search or an approved vector store for curated documents/examples.
- **Operations:** Cloud Logging, Cloud Audit Logs, BigQuery INFORMATION_SCHEMA, Cloud Monitoring, Secret Manager, and Cloud Build/Deploy.

Model options should be evaluated against data residency, private networking, cost, latency, SQL quality, and procurement policy. Prefer a bank-controlled Vertex AI deployment first; allow a self-hosted/open-weight model only where its operational and quality trade-offs are justified.

## Auditability, metrics, and cost controls

Log the user identity, request, retrieved knowledge versions, policy decisions, generated/validated SQL, data models accessed, query job ID, result summary, model/version, latency, cost, and response. Make a human-readable explanation available to users and a complete immutable audit record available to risk and operations.

Track answer acceptance, grounded/verified-answer rate, SQL validation pass rate, policy-block rate, escalation rate, freshness, metric-definition conflicts, latency, BigQuery bytes scanned, model-token spend, and analyst hours saved. Establish evaluation sets with representative banking questions and expected SQL/results before broad rollout.

Control cost through semantic views, partitioning/clustering, mandatory filters, cached verified answers where appropriate, dry-run budgets, query/model rate limits, response/result caps, and usage dashboards with team budgets.

## MVP and roadmap

**MVP (one migration domain):** read-only chat; 10--20 approved migration metrics; curated BigQuery views; glossary and 20--50 verified queries; aggregate-only answers; SSO/IAM; SQL validation; audit logs; simple tables/charts; analyst escalation.

**Phase 2:** richer semantic models, multi-turn context, saved/shareable insights, anomaly and trend tools, automated data-quality signals, and a steward workflow to approve definitions and verified queries.

**Phase 3:** additional domains, controlled cross-domain analytics, proactive insights/alerts, assisted dashboard generation, and continuous evaluation and policy tuning.

## Key design principles

1. Governed data access is enforced in services and the warehouse, never entrusted solely to the LLM.
2. Curated semantic models and clear business definitions matter more than clever prompting.
3. Return evidence: metric definition, data freshness, source model, and query explanation.
4. Default to aggregates and least privilege; make sensitive detail an explicit exception.
5. Treat verified queries and evaluation datasets as product assets.
6. Begin narrow, measure trust and value, then expand by governed domain.
