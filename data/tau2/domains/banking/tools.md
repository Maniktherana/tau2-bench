## Available Tools

Use exactly one tool at a time. For any write that changes money, security, alerts, contact info, account status, or product enrollment, first show an action summary and obtain explicit "YES". For high risk writes, require step-up MFA at L2 or higher. All money amounts are USD.

### Common types
- IDs: `customer_id`, `account_id`, `card_id`, `statement_id`, `tx_id`, `payee_id`, `beneficiary_id`, `wire_id`, `payment_id`, `request_id`, `dispute_id`, `alert_id`, `session_id`
- Auth levels: L0 none, L1 KBA, L2 recent MFA, L3 step-up MFA
- All write tools accept `idempotency_key` and return an object with `status`

---

### Auth, Session, and CIP

**send_otp(channel) → {otp_sent: true}**  
Channels: sms, email, app.

**verify_otp(code) → {verified: bool, auth_level: "L2"|"L3"}**  

**get_auth_session() → {session_id, auth_level, last_reauth_at}**

**start_step_up_mfa(method) → {challenge_id}**  
Methods: sms, app, push.

**verify_step_up_mfa(challenge_id, code) → {verified: bool, auth_level}**

**verify_identity_ssn_last4(ssn_last4, date_of_birth) → {kba_passed: bool}**  
US CIP check for consumer accounts.

**collect_tax_certification(form_type, tin_type, tin_last4) → {status}**  
Form types: W-9, W-8BEN. Use for interest bearing or investment accounts.

---

### Customer Lookup

**get_customer_by_id(customer_id) → Customer**  
**get_customer_by_phone(phone_number) → Customer**  
**get_customer_by_name_dob(full_name, date_of_birth) → Customer**  
Use exactly one lookup path. After 3 failed attempts, propose transfer.

---

### Accounts and Balances

**get_accounts(customer_id) → [Account]**  
**get_account(account_id) → Account**  
**get_balances(account_id) → {current_balance, available_balance, holds}**  

**open_account(product_id) → {account_id, status}**  
Requires L2 and "YES". Checking, savings, CD, credit card.

**close_account(account_id, reason) → {status}**  
Requires L2 and "YES". Warn about consequences and payout method.

**get_statements(account_id, from_date, to_date) → [Statement]**  
**get_statement(statement_id) → Statement**

**get_tax_form(account_id, form_type) → {download_token}**  
Form types: 1099-INT, 1099-DIV, 1098.

---

### External Account Linking for ACH

**add_external_account_via_microdeposits(customer_id, routing_number, account_number, account_type) → {external_account_id, status:"Pending Verification"}**

**confirm_microdeposits(external_account_id, amounts:[number, number]) → {verified: bool}**

**remove_external_account(external_account_id) → {status}**

---

### Payments and Transfers

#### Bill Pay, US style
**add_bill_payee(customer_id, payee_details) → {payee_id, deliver_type:"electronic"|"check"}**  
Payee may route electronically or by paper check.

**send_billpay_payment(from_account_id, payee_id, amount, deliver_by_date, memo) → {payment_id, status:"Scheduled"}**  
Electronic is ACH. Check delivery schedules apply. Requires L2 and "YES".

**cancel_billpay_payment(payment_id) → {status}**  
If still pending. For paper checks not yet mailed.

**place_stop_payment_check(account_id, check_number, amount, issue_date) → {status}**  
Stop payment on customer issued checks. Fees may apply. Requires L2 and "YES".

#### ACH transfers
**initiate_ach_transfer(from_account_id, to_external_account_id, amount, same_day:bool, sec_code:"PPD"|"WEB"|"CCD", memo) → {payment_id, status:"Submitted"}**  
Consumer rails use PPD or WEB. Same day subject to cutoff. Requires L2 and "YES".

**cancel_ach(payment_id) → {status}**  
If not yet posted.

#### RTP, Real-time Payments
**initiate_rtp_payment(from_account_id, to_rtp_alias, amount, memo) → {payment_id, status:"Sent"}**  
Irrevocable once sent. 24x7x365. Requires L2 and "YES".

#### Zelle P2P
**enroll_zelle(customer_id, contact: email|phone) → {enrolled: bool}**  
**send_zelle(from_account_id, to_contact: email|phone, amount, memo) → {payment_id, status:"Pending"|"Sent"}**  
Cancelable only while pending. Requires L2 and "YES".

---

### Wires

**initiate_wire_domestic(from_account_id, beneficiary:{name, routing_number, account_number, account_type}, amount, reference) → {wire_id, status:"Submitted"}**  
Fedwire domestic. Cutoffs and fees apply. Requires L2 and "YES".

**initiate_wire_international(from_account_id, beneficiary:{name, swift_bic, iban_or_account, bank_country}, amount, currency:"USD"|"FX", reference, fx_quote_id) → {wire_id, status:"Submitted"}**  
SWIFT. Requires L2 and "YES". Use `get_fx_quote` first if FX.

**get_fx_quote(from_currency, to_currency, amount) → {fx_quote_id, rate, expires_at}**

**track_wire(wire_id) → {status, timestamps}**  
**recall_wire(wire_id) → {status:"Recall-Requested"|"Not-Eligible"}**  
Eligibility depends on settlement.

---

### Cards, Debit and Credit

**lock_debit_card(card_id, reason) → {status:"Locked"}**  
**unlock_debit_card(card_id) → {status:"Active"}**  

**lock_credit_card(card_id, reason) → {status:"Locked"}**  
**unlock_credit_card(card_id) → {status:"Active"}**  

**request_card_reissue(card_id, delivery:{method:"mail"|"branch_pickup", address_id}) → {case_id, status}**  
Requires L2 and "YES".

**set_travel_notice(card_id, regions:[string], start_date, end_date) → {status}**  

**get_card_limits(card_id) → {per_tx_limit, daily_limit, cash_advance_limit}**  
**request_limit_change(card_id, new_limit) → {status:"Submitted", review_eta}**  
High risk. L2 and "YES".

---

### Mobile Check Deposit and Holds

**submit_mobile_deposit(to_account_id, amount, front_image_token, back_image_token) → {deposit_id, status:"Submitted", hold_release_date}**  
Funds availability per Reg CC. Requires endorsement text check.

**get_deposit_status(deposit_id) → {status, hold_release_date}**  
**cancel_mobile_deposit(deposit_id) → {status}**  
If still in review.

---

### Alerts and Monitoring

**get_alerts(customer_id) → [Alert]**  
**set_alert(customer_id, alert_type, params) → {alert_id, status:"Active"}**  
Types: low_balance, large_tx, wire_updates, statement_ready, card_presentment.

**update_alert(alert_id, active:bool, params) → {status}**  

**account_monitor(account_id) → {balances, recent_activity, flags:[unusual_activity|over_limit|past_due]}**

---

### Disputes and Fraud

**file_reg_e_dispute(account_id, tx_id, reason_code, details) → {dispute_id, status:"Submitted", documents_required:[...], deadlines}**  
EFT errors include debit card, ATM, ACH. 60 day rule from statement delivery. Requires L2 and "YES".

**file_reg_z_dispute(account_id, tx_id, reason_code, details) → {dispute_id, status:"Submitted", documents_required:[...], deadlines}**  
Credit card billing disputes. Requires L2 and "YES".

**upload_dispute_doc(dispute_id, doc_type, file_token) → {status}**  
**get_dispute(dispute_id) → Dispute**  
**flag_transaction(tx_id, reason) → {case_id, status}**  

---

### Profile and Contact

**get_profile(customer_id) → Profile**  
**update_contact_info(customer_id, fields) → {status}**  
Fields: phone, email, mailing address. USPS address validation may apply. Requires L2 and "YES". Do not echo full PII back.

**set_esign_consent(customer_id, consent:bool) → {status}**  
Required to deliver statements and tax forms electronically.

---

### Risk and Compliance

**ofac_screen_party(party_details) → {result:"clear"|"possible_match", list:[...] }**  
Screen new payees and beneficiaries.

**ofac_screen_payment(payment_id) → {result}**  
Block if match.

**risk_check(action, amount, destination) → {risk_level:"low"|"medium"|"high", reauth_required:bool, notes}**  
Use on first money movement or goal shift into money movement.

---

### Instrumentation for goal shift research

**log_shift_event(turn_no, from_class, to_class, trigger_terms, requires_reauth:bool) → {logged:true}**  
No user visible side effect.

**park_task(current_task_id, resume_hint) → {parked_task_id}**  
**resume_task(parked_task_id) → {status}**

---

### Errors and retries

Every tool returns success or `{error_code, error_message, retriable:bool}`.  
On retriable true, offer one retry. After two failures in a row, propose a human transfer.

---

### Re-auth triggers

Re-auth is required when any of these are true:  
- First money movement in session, or switching from education to any write  
- New payee, new beneficiary, limit change, unlock card, address change  
- Domestic wire, international wire, same day ACH, RTP, Zelle send  
- Amount exceeds per transaction or daily limits, or step-up timeout older than 5 minutes
