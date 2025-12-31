# Use **Claude Code** to help extract Business Calculation Formulas from **Java EE (JSP + JS)** codebases

What Claude Code can realistically do well for your use case:

## What Claude Code can do (practical)

1. **Codebase discovery & mapping**

   * Scan JSP/JS files and identify where calculations happen (onChange/onClick handlers, inline script blocks, JSP tag outputs, etc.).
   * Build a “calculation inventory” (file → function → inputs → outputs).

2. **Extract formulas into structured artifacts**

   * Convert scattered logic into a clean spec format (e.g., Markdown tables / JSON):

     * `FormulaName`
     * `Inputs (fields)`
     * `Calculation`
     * `Rounding`
     * `Dependencies`
     * `Visibility/conditions`
     * `Error handling`

3. **Refactor + migrate targets**

   * Help translate old UI-driven JS rules into a **microservice calculation module** (e.g., TypeScript/Java service) with deterministic functions.
   * Generate unit tests to lock behavior (important before changing logic).

4. **Run grep/ripgrep, execute scripts, and commit changes**

   * Claude Code can operate “in your terminal” to read/write files, run commands, and manage git commits. 

5. **Use sub-agents for parallel extraction**

   * You can split work by module/screen: one agent scans “LC Amount” pages, another scans “Exchange Rate” pages, etc. 

---

## Recommended workflow (high success rate)

1. **Define scope**

   * Pick 1–2 representative screens first (where formulas are known and critical).

2. **Inventory phase (automated search)**

   * Ask Claude Code to locate:

     * `onChange`, `onClick`, `calculate*`, `recalc*`, `setValue`, `formatCurrency`, etc.
     * JSP expressions that compute values server-side.

3. **Normalize formulas**

   * Output a **“Formula Catalog”** (CSV/JSON/MD) with:

     * formula id, description, inputs, outputs, dependencies, conditions.

4. **Validate against runtime**

   * Run sample transactions to confirm extracted formulas match actual results.

5. **Implement microservice functions + tests**

   * Create pure functions + tests per formula to preserve behavior.

---

## A Claude Code prompt you can use (copy/paste)

> Scan the Java EE codebase (JSP + JS) and identify all business calculation logic.
> Produce a “Formula Catalog” in Markdown and JSON with: formula name, file path, function name, input fields, output fields, conditions, rounding rules, and pseudo-code.
> Prioritize calculation logic tied to UI events (onChange/onClick) and any server-side JSP expressions that compute values.
> Do not change logic yet—only extract and document. After catalog is done, propose a refactoring plan to move these formulas into a microservice-friendly pure function module with unit tests.

This aligns with Claude Code’s strengths in **planning + code navigation + debugging/refactoring**. 

---

## Caveats (so you set expectations correctly)

* If calculations are split across **JSP → JS → Java backend → stored procedures**, Claude can still help, but you’ll need to extract **end-to-end dependencies** (not just JS).
* Some “formulas” are actually **business rules** (validation, visibility, enable/disable) — treat them as a separate catalog to avoid mixing concerns.

If you share a small sample (one JSP + its linked JS + a screenshot of fields), I can show you exactly what the **Formula Catalog** output should look like for your system.
