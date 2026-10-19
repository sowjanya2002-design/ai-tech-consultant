import { describe, it, expect } from "vitest";
import { FeedbackTracker } from "../src/feedback/tracker.js";

describe("FeedbackTracker - 20 Unedited Consecutive Rule", () => {
  it("increments count when draft is approved without edits", () => {
    const tracker = new FeedbackTracker();
    const result = tracker.recordReview({
      emailId: "1",
      category: "how_to",
      action: "approved",
      originalDraft: "Hello, visit Settings to change your logo.",
      finalSentText: "Hello, visit Settings to change your logo.",
    });

    expect(result.consecutiveUnedited).toBe(1);
    expect(result.eligibleForAutonomy).toBe(false);
  });

  it("resets streak to 0 when draft is edited", () => {
    const tracker = new FeedbackTracker();
    tracker.recordReview({
      emailId: "1",
      category: "how_to",
      action: "approved",
      originalDraft: "Draft text",
      finalSentText: "Draft text",
    });

    const editedResult = tracker.recordReview({
      emailId: "2",
      category: "how_to",
      action: "edited",
      originalDraft: "Draft text",
      finalSentText: "Edited draft text",
    });

    expect(editedResult.consecutiveUnedited).toBe(0);
  });

  it("becomes eligible for autonomy after 20 consecutive unedited drafts", () => {
    const tracker = new FeedbackTracker();
    for (let i = 1; i <= 19; i++) {
      tracker.recordReview({
        emailId: `${i}`,
        category: "how_to",
        action: "approved",
        originalDraft: "Same approved draft",
        finalSentText: "Same approved draft",
      });
    }
    const finalResult = tracker.recordReview({
      emailId: "20",
      category: "how_to",
      action: "approved",
      originalDraft: "Same approved draft",
      finalSentText: "Same approved draft",
    });

    expect(finalResult.consecutiveUnedited).toBe(20);
    expect(finalResult.eligibleForAutonomy).toBe(true);
  });
});
