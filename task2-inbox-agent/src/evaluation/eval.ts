import dotenv from "dotenv";
dotenv.config();

import dataset from "../email/dataset.json" with { type: "json" };
import { InboxPipeline } from "../drafting/pipeline.js";
import { InboundEmail } from "../email/types.js";

async function runEvaluation() {
  console.log("=== Running Task 2 Inbox Agent Evaluation ===");
  const pipeline = new InboxPipeline();

  let correctClassification = 0;
  const emails = dataset as InboundEmail[];

  for (const email of emails) {
    console.log(`\nEvaluating Email: [${email.id}] "${email.subject}"`);
    const result = await pipeline.processEmail(email);

    const matchedCategory = result.classification.category === email.expectedCategory;
    if (matchedCategory) correctClassification++;

    console.log(`- Expected Category: ${email.expectedCategory} | Predicted: ${result.classification.category}`);
    console.log(`- Risk: ${result.classification.risk} | Needs Review: ${result.needsHumanReview}`);
    console.log(`- Citations: ${result.sources.length} sources`);
  }

  const accuracy = ((correctClassification / emails.length) * 100).toFixed(1);
  console.log(`\n===========================================`);
  console.log(`Total Emails: ${emails.length}`);
  console.log(`Classification Accuracy: ${accuracy}%`);
  console.log(`===========================================`);
}

runEvaluation().catch(console.error);
