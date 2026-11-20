from pathlib import Path
import fitz

out = Path(__file__).parent
pdf = fitz.open()
page = pdf.new_page(width=612, height=792)
margin = 48
y = 54

def wrap(text, font, size, width):
    words = text.split()
    lines, current = [], ""
    for word in words:
        test = f"{current} {word}".strip()
        if fitz.get_text_length(test, fontname=font, fontsize=size) <= width:
            current = test
        else:
            if current: lines.append(current)
            current = word
    if current: lines.append(current)
    return lines

def ensure(needed=30):
    global page, y
    if y + needed > 744:
        page = pdf.new_page(width=612, height=792)
        y = 54

def para(text, size=10.2, color=(0.12,0.17,0.23), font="helv", indent=0, gap=5, leading=None):
    global y
    leading = leading or size * 1.35
    lines = wrap(text, font, size, 516-indent)
    ensure(leading*len(lines)+gap)
    for line in lines:
        page.insert_text((margin+indent, y), line, fontname=font, fontsize=size, color=color)
        y += leading
    y += gap

def heading(text, level=2):
    global y
    size = 17 if level == 1 else 12.5
    ensure(size+16)
    y += 7
    page.insert_text((margin,y), text, fontname="hebo", fontsize=size, color=(0.08,0.28,0.40))
    y += size+7

def bullet(text):
    para("•  " + text, indent=8, gap=3)

heading("STAT 110 | Final Study Guide", 1)
para("Course-based starter · Prepared from the supplied outline, lecture notes, practice set, key, past paper, and learning record.", size=9, color=(0.35,0.39,0.43))
para("Scope note: the available outline is labeled Midterm 1, although the course profile names a cumulative final. This guide covers the four topics confirmed in that outline; it cannot establish the full final scope. Bayes’ rule is listed as covered, but its teaching notes were not supplied.", size=10.2, color=(0.53,0.20,0.12), gap=6)

heading("1. Conditional probability · T1")
para("Meaning: P(A | B) asks what share of group B also belongs to A. B is the reference group, so its count is the denominator.")
para("Compute: count in both A and B ÷ count in B. State the result as a percentage to one decimal place and name the reference group.", size=10.2)
para("Example (Practice A Q1; key): 10 commuters cycle out of 25 commuters. 10 ÷ 25 = 40.0% of commuters.", size=10.2)
bullet("Order matters: P(A | B) and P(B | A) generally use different reference groups and can differ.")
bullet("Check before dividing: identify the group named after “among/of” or otherwise restricted by the question; use that group’s total.")
bullet("Course condition: cases are equally weighted and the reference group is non-empty. (Notes §1.4)")
para("Personal recheck: this topic is marked Demonstrated in your record, with a recheck due before the exam. Retrieval cue: say “among B” first, then point to B’s count before calculating.", size=9.5, color=(0.18,0.34,0.30))

heading("2. Two-way tables · T2")
para("A two-way table counts cases classified by two categorical variables, with row totals and column totals. A cell is the intersection of one row category and one column category. (Notes §2.1)")
bullet("Row percentage = cell count ÷ that row’s total. It answers what share of the row group is in the cell.")
bullet("Column percentage = cell count ÷ that column’s total. It answers what share of the column group is in the cell.")
bullet("Sanity check: row percentages add to 100% within each row; column percentages add to 100% within each column. (Notes §2.3)")
para("Personal target: your recorded attempt chose a row total for a column percentage. Corrective rule: name the reference group first; for a column percentage, divide by the column total. Percentages across a row of column percentages need not add to 100%.", size=9.8, color=(0.18,0.34,0.30))
para("Mini-check: if a cell is 8, its row total is 20, and its column total is 16, the row percentage is 40.0% of that row group; the column percentage is 50.0% of that column group. (Direct example from Notes §2.2.)", size=9.8)

heading("3. Grouped summaries · T4")
para("A grouped summary splits cases by a categorical variable and computes one summary value (such as a mean or count) for each non-empty group. (Notes §3.1)")
bullet("Output has one row per non-empty group, not one row per original case. (Notes §3.2)")
bullet("Compare like with like: group mean with group mean, or group total with group total. Do not compare a mean with a total. (Notes §3.3)")
para("Past-paper example (2025 Midterm 1 Q3): means for 4 sections produce 4 rows, because there are four groups. This is a historical example, not evidence of final format.", size=9.8)

if y > 650:
    page = pdf.new_page(width=612, height=792)
    y = 54
heading("4. Bayes’ rule · T3 — source gap")
para("The outline lists Bayes’ rule as in scope and says it was covered in lecture, but the supplied notes contain no explanation or worked example. This guide does not invent a formula or procedure. Add the lecture notes or an instructor example here, then practice identifying the relevant events, probabilities, and conditions from that source.", size=10.2, color=(0.53,0.20,0.12))

heading("5. Reporting checklist")
for item in [
    "Convert every proportion to a percentage rounded to one decimal place.",
    "Name the reference group in words: for example, “40.0% of commuters.” The outline says an answer without the group loses one point.",
    "For conditional probabilities and table percentages, verify the denominator is the reference-group total.",
    "For grouped summaries, report one result per non-empty group and compare the same kind of summary.",
]: bullet(item)

heading("6. Scope and source map")
para("Confirmed in the supplied Midterm 1 outline: T1 conditional probability (Notes §1; Practice A Q1–Q4), T2 two-way table row and column percentages (Notes §2), T3 Bayes’ rule (outline only; explanation source missing), and T4 grouped summaries (Notes §3). Hypothesis testing is explicitly excluded from that Midterm 1 outline; the 2025 past-paper Q2 is historical and does not confirm it for this final.", size=9.4)
para("Unconfirmed for the cumulative final: whether these topics exhaust the exam scope, any Midterm 2 or later topics, final question formats/scoring, and reference-sheet rules. Ask for the final review sheet or later-unit notes to complete coverage.", size=9.4)
para("Sources: materials/outline.md; materials/notes.md §§1–3; materials/practice.md Q1–Q4 and practice-key.md; materials/midterm-2025.md Q2–Q3; learning-record.md. Topic status and personalization follow the supplied learning record; no new attempt was assessed for this guide.", size=8.7, color=(0.35,0.39,0.43), gap=2)

pdf.set_metadata({"title":"STAT 110 Final Study Guide", "author":"Study guide from supplied course materials"})
pdf.save(out / "STAT110_final_study_guide.pdf", garbage=4, deflate=True)
