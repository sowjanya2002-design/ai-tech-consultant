import { KnowledgeResponse } from "../email/types.js";

const KB_URL = process.env.KNOWLEDGE_BRAIN_URL || "http://localhost:8000";

export class KnowledgeBrainClient {
  private baseUrl: string;

  constructor(baseUrl: string = KB_URL) {
    this.baseUrl = baseUrl.replace(/\/$/, "");
  }

  async ask(question: string): Promise<KnowledgeResponse> {
    try {
      const response = await fetch(`${this.baseUrl}/ask`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });

      if (!response.ok) {
        return {
          answer: "Knowledge base returned an error status.",
          status: "escalate_to_human",
          confidence: "low",
          sources: [],
          escalationReason: `Knowledge service HTTP error: ${response.status}`,
        };
      }

      const data = await response.json();
      return {
        answer: data.answer || "No details found.",
        status: data.status === "answered" ? "answered" : "escalate_to_human",
        confidence: data.confidence || "low",
        sources: data.sources || [],
        escalationReason: data.escalation,
      };
    } catch (error: any) {
      return {
        answer: "Knowledge base is currently unreachable.",
        status: "escalate_to_human",
        confidence: "low",
        sources: [],
        escalationReason: `Connection error: ${error.message}`,
      };
    }
  }
}
