export type EmailCategory =
  | "how_to"
  | "troubleshooting"
  | "project_request"
  | "refund_cancellation"
  | "complaint"
  | "quote_request"
  | "follow_up"
  | "other";

export type RiskLevel = "low" | "medium" | "high";

export interface InboundEmail {
  id: string;
  sender: string;
  subject: string;
  body: string;
  expectedCategory?: EmailCategory;
  expectedRisk?: RiskLevel;
}

export interface ClassificationResult {
  category: EmailCategory;
  intent: string;
  searchQuery: string;
  risk: RiskLevel;
  needsHumanReview: boolean;
}

export interface KnowledgeResponse {
  answer: string;
  status: "answered" | "escalate_to_human";
  confidence: "high" | "low";
  sources: { title: string; url: string }[];
  escalationReason?: string;
}

export interface DraftResult {
  emailId: string;
  classification: ClassificationResult;
  draftText: string;
  sources: { title: string; url: string }[];
  needsHumanReview: boolean;
  generatedAt: string;
}

export interface ReviewAction {
  emailId: string;
  category: EmailCategory;
  action: "approved" | "edited" | "rejected";
  originalDraft: string;
  finalSentText: string;
  rejectionReason?: string;
}
