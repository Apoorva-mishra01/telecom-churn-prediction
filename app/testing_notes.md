# Phase 15 — Testing Notes

## Test 1: Minimum tenure (0 months, month-to-month)
Result: 78.4% churn probability (High Risk) — consistent with EDA findings.

## Test 2: Maximum tenure (72 months, two-year contract)
Result: 2% churn probability (Low Risk) — consistent with EDA findings.

## Test 3: Logically inconsistent input (PhoneService=No, MultipleLines=Yes)
Result: 0.9% (Low Risk) — no crash, but revealed a limitation: the app does
not validate logical dependencies between related fields.

## Test 4: Extreme/inconsistent billing values (MonthlyCharges=250, TotalCharges=0)
Result: Exactly 0% — no crash, but suggests the model may extrapolate
unreliably when given numerically inconsistent inputs outside the
realistic range of training data.

## Test 5: Minimal-service customer profile
Result: 1.5% (Low Risk) — plausible given low financial stake despite
month-to-month contract.

## Test 6: UI/interaction testing
- Tab switching preserves entered values correctly.
- Predicting with all default values (no changes) works without error.
- Rapid repeated clicking on "Predict Churn" behaves consistently.

## Known Limitations Identified
1. No cross-field validation (e.g., MultipleLines can be "Yes" even when
   PhoneService is "No", which is logically impossible in reality).
2. Numerically inconsistent inputs (e.g., TotalCharges far outside what
   tenure × MonthlyCharges would suggest) can produce extreme predictions
   that may not be reliable, since such combinations likely didn't appear
   in training data.

## Future Improvements
- Add input validation/conditional logic (e.g., auto-set MultipleLines to
  "No phone service" equivalent when PhoneService is "No").
- Consider a sanity-check warning if TotalCharges is drastically
  inconsistent with tenure × MonthlyCharges.
  