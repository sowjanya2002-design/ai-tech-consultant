import Anthropic from "@anthropic-ai/sdk";
import { InboundEmail, ClassificationResult, DraftResult, EmailCategory } from "../email/types.js";
import { KnowledgeBrainClient } from "../knowledge-client/client.js";

const HIGH_RISK_CATEGORIES: EmailCategory[] = ["refund_cancellation", "complaint"];

export class InboxPipeline {
  private anthropic: Anthropic;
  private kbClient: KnowledgeBrainClient;

  constructor() {
    this.anthropic = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });
    this.kbClient = new KnowledgeBrainClient();
  }

  async classify(email: InboundEmail): Promise<ClassificationResult> {
    const prompt = `Classify this inbound customer support email.
Categories:
- how_to: How-to questions about platform features
- troubleshooting: Error reports, broken features, bugs
- project_request: Custom development or feature additions
- refund_cancellation: Billing disputes, cancellations, refunds
- complaint: Frustration, threats to leave, escalation
- quote_request: Pricing or estimation requests
- follow_up: Checking status of past requests
- other: General inquiries

Reply strictly in JSON format:
{
  "category": "how_to",
  "intent": "Short one-sentence summary of what the user wants",
  "searchQuery": "Keyword query to look up product knowledge",
  "risk": "low" | "medium" | "high"
}`;

    const res = await this.anthropic.messages.create({
      model: "claude-3-5-sonnet-20241022",
      max_tokens: 300,
      system: prompt,
      messages: [{ role: "user", content: `Subject: ${email.subject}\n\nBody: ${email.body}` }],
    });

    const text = res.content[0].type === "text" ? res.content[0].text : "{}";
    try {
      const parsed = JSON.parse(text.replace(/```json|```/g, "").trim());
      const isHighRisk = HIGH_RISK_CATEGORIES.includes(parsed.category) || parsed.risk === "high";
      return {
        category: parsed.category || "other",
        intent: parsed.intent || "",
        searchQuery: parsed.searchQuery || email.subject,
        risk: isHighRisk ? "high" : (parsed.risk || "medium"),
        needsHumanReview: isHighRisk,
      };
    } catch {
      return {
        category: "other",
        intent: "Unknown intent",
        searchQuery: email.subject,
        risk: "medium",
        needsHumanReview: true,
      };
    }
  }

  async processEmail(email: InboundEmail, pastFeedback: string = ""): Promise<DraftResult> {
    const classification = await this.classify(email);
    const kb = await this.kbClient.ask(classification.searchQuery);

    const systemPrompt = `You are a polite, helpful AI Tech Consultant support agent.
Guidelines:
1. Ground answers strictly in the provided Knowledge Base facts.
2. Never promise refunds, discounts, SLA deadlines, or customized prices.
3. If information is missing or unverified, state that a specialist will review.
4. Sign off as "Support Team".
${pastFeedback ? `Incorporate this reviewer feedback: ${pastFeedback}` : ""}`;

    const userPrompt = `Inbound Customer Email:
From: ${email.sender}
Subject: ${email.subject}
Message: ${email.body}

Retrieved Knowledge Base Answer (${kb.status}):
${kb.answer}

Sources:
${JSON.stringify(kb.sources)}`;

    const res = await this.anthropic.messages.create({
      model: "claude-3-5-sonnet-20241022",
      max_tokens: 600,
      system: systemPrompt,
      messages: [{ role: "user", content: userPrompt }],
    });

    const draftText = res.content[0].type === "text" ? res.content[0].text : "";
    const needsHumanReview = classification.needsHumanReview || kb.status !== "answered";

    return {
      emailId: email.id,
      classification,
      draftText,
      sources: kb.sources,
      needsHumanReview,
      generatedAt: new Date().toISOString(),
    };
  }
}
