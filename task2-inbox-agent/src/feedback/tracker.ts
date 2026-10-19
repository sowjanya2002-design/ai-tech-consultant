import { EmailCategory, ReviewAction } from "../email/types.js";

export interface AutonomyStatus {
  category: EmailCategory;
  consecutiveUnedited: number;
  eligibleForAutonomy: boolean;
}

export class FeedbackTracker {
  private streaks: Map<EmailCategory, number> = new Map();
  private auditLog: ReviewAction[] = [];

  recordReview(review: ReviewAction): AutonomyStatus {
    this.auditLog.push(review);
    const category = review.category;
    const current = this.streaks.get(category) || 0;

    // Must be approved AND exact match (no reviewer edits)
    const isUnedited =
      review.action === "approved" &&
      review.originalDraft.trim() === review.finalSentText.trim();

    if (isUnedited) {
      const nextCount = current + 1;
      this.streaks.set(category, nextCount);
      return {
        category,
        consecutiveUnedited: nextCount,
        eligibleForAutonomy: nextCount >= 20,
      };
    } else {
      // Reset streak upon human edit or rejection
      this.streaks.set(category, 0);
      return {
        category,
        consecutiveUnedited: 0,
        eligibleForAutonomy: false,
      };
    }
  }

  getStreak(category: EmailCategory): number {
    return this.streaks.get(category) || 0;
  }

  getAuditLog(): ReviewAction[] {
    return this.auditLog;
  }
}
