# User Persona Policy for Goal-Shift Testing

## Purpose
To simulate diverse and realistic customer interactions that stress-test the bot's ability to:
1. Adapt to changes in user goals mid-conversation
2. Coordinate step-by-step instructions for human users
3. Correctly call and sequence API tools (one at a time) while re-confirming when goals change
4. Maintain tone, empathy, and compliance across different personalities, technical skill levels, and motivations

## Personas

### EASY_1
**Personality & Tone:** Polite, detail-oriented, expects step-by-step guidance

**Expertise:** Intermediate banking knowledge; very comfortable with budgeting tools, less so with investment concepts

**Technology Comfort:** Moderate; can follow clear instructions for MFA, online banking, and document uploads

**Goal-Change Pattern:** Occasionally changes goals after receiving a partial answer (e.g., starts with budgeting help, then wants to open a new savings account)

**Motivations:** Wants to organize finances for retirement in 15 years, minimize fees, and maximize interest

**Expected Service Usage:** 2–3 functions in one session (FinanceWise → BankAssist → WealthAdvisor)

**Empathy Requirement:** Medium — expects clear, logical sequencing but not emotional reassurance

**Testing Value:**
- Checks if LLM can preserve structured budgeting advice while pivoting to product recommendation flow mid-conversation
- Tests seamless switching between financial planning education and account setup tool calls

---

### EASY_2
**Personality & Tone:** Friendly but easily distracted, prone to mid-conversation shifts

**Expertise:** Low; struggles with banking terminology

**Technology Comfort:** Low; needs extra coaching for MFA and online forms

**Goal-Change Pattern:** High frequency — starts with a fraud alert, switches to payment reminders, then to credit card reward advice

**Motivations:** Wants immediate issue resolution but also explores unrelated features during chat

**Expected Service Usage:** 4–5 functions in one session (SecureWatch → PaymentAssist → SpendingSmart → SalesStrategy)

**Empathy Requirement:** High — requires reassurance when using security-related features

**Testing Value:**
- Stress-tests LLM's ability to pause and safely abandon one flow for another without leaving unresolved high-risk actions
- Validates correct re-authentication prompts when switching between security-sensitive and non-sensitive actions

---

### MEDIUM_1
**Personality & Tone:** Direct, impatient, expects rapid, accurate responses

**Expertise:** High in business finance; minimal patience for explanations

**Technology Comfort:** High; can complete MFA, API tool flows without coaching

**Goal-Change Pattern:** Moderate — starts with high-value wire tracking, then wants an account structure review for optimization

**Motivations:** Avoids fraud at all costs; wants premium banking efficiency and ROI

**Expected Service Usage:** 2–4 functions in one session (TransactionResolver → AccountGuardian → WealthAdvisor)

**Empathy Requirement:** Low — values speed over empathy

**Testing Value:**
- Ensures LLM prioritizes high-risk, high-value actions without losing state when switching to optimization flows
- Tests compliance with re-confirmation on high-value transactions even for expert users

---

### HARD_1
**Personality & Tone:** Suspicious, often asks for proof or policy references

**Expertise:** Intermediate; understands banking basics but distrusts automation

**Technology Comfort:** Medium; capable but reluctant to use online tools

**Goal-Change Pattern:** Low frequency but major — may abandon a product application if terms seem unclear, switching to fraud education

**Motivations:** Wants full transparency on fees, rates, and security measures

**Expected Service Usage:** 1–2 functions in one session (SalesStrategy → SecurityEducator)

**Empathy Requirement:** High — requires reassurance through policy citations and security explanations

**Testing Value:**
- Verifies bot can handle objection handling and pivot to educational flows without losing credibility
- Validates ability to insert disclaimers and compliance notes dynamically

---

### MEDIUM_2
**Personality & Tone:** Curious, asks many follow-up questions

**Expertise:** Beginner; limited banking knowledge but high willingness to learn

**Technology Comfort:** Moderate; can handle mobile app flows with some instruction

**Goal-Change Pattern:** High frequency — starts with learning about investments, then tries to set up multiple alerts, then explores budgeting tools

**Motivations:** Wants to improve financial literacy while actively using tools to track progress

**Expected Service Usage:** 3–5 functions in one session (InvestmentGuide → AlertAssist → SpendingSmart → FinanceWise)

**Empathy Requirement:** High — needs patient, jargon-free explanations

**Testing Value:**
- Measures LLM's ability to chain educational answers with action flows
- Tests whether bot can maintain state across multiple low-risk but multi-step tool calls

## Common Testing Parameters Across Personas

For each conversation simulation:

### 1. Authentication Flow
Must always occur first, with variations in complexity based on persona comfort

### 2. Tool Call Sequencing
Bot must perform only one tool call at a time, re-confirm before committing actions

### 3. Goal Shift Handling
Bot must:
- Pause current task
- Summarize pending steps
- Offer to resume later or cancel safely

### 4. Tone Adjustment
Adapt empathy, pace, and explanation depth to persona

### 5. Regulatory/Compliance Hooks
Disclaimers, security reminders, and masked data must be included where relevant

### 6. Performance Metrics
Measure:
- Task completion rate despite goal changes
- Latency between user intent change and bot adaptation
- Number of re-authentication prompts handled correctly
- User satisfaction proxy (politeness, clarity scores)