from pathlib import Path
import fitz

out = Path(__file__).parent
pdf = fitz.open()
W, H, M = 612, 792, 42

def wrap(text, font, size, width):
    words=text.split(); lines=[]; cur=""
    for word in words:
        test=(cur+" "+word).strip()
        if fitz.get_text_length(test,fontname=font,fontsize=size)<=width: cur=test
        else:
            if cur: lines.append(cur)
            cur=word
    if cur: lines.append(cur)
    return lines

def side(title, sections, side_label):
    page=pdf.new_page(width=W,height=H); y=40
    page.insert_text((M,y),title,fontname="hebo",fontsize=19,color=(.08,.28,.4)); y+=23
    page.insert_text((M,y),side_label,fontname="helv",fontsize=8.5,color=(.35,.39,.43)); y+=17
    for head, paras in sections:
        y+=5
        if y>H-70: raise ValueError(f"Content overflow before {head}: {y}")
        page.insert_text((M,y),head,fontname="hebo",fontsize=12.5,color=(.08,.28,.4)); y+=17
        for txt in paras:
            size=9.5; leading=12.3
            lines=wrap(txt,"helv",size,W-2*M)
            if y+leading*len(lines)>H-35: raise ValueError(f"Content overflow: {head}")
            for line in lines:
                page.insert_text((M,y),line,fontname="helv",fontsize=size,color=(.12,.17,.23)); y+=leading
            y+=3
    return page

side("STAT 110 | EXAM SHEET",[
 ("FRONT · Conditional probability & two-way tables",[
  "Draft for studying. Confirm instructor rules for permitted content, paper size, and printing before bringing this sheet into the exam."]),
 ("Conditional probability · T1",[
  "P(A | B): probability of A among cases in B. Compute: count in both A and B ÷ count in B.",
  "Denominator = reference group B, not the whole sample. Decide which group the question restricts you to before dividing.",
  "Order matters: P(A | B) and P(B | A) usually differ because their reference groups differ. Assumes equally weighted cases and a non-empty reference group. (Notes §1.1–1.4)",
  "Example: 10 of 25 commuters cycle → 10 ÷ 25 = 40.0% of commuters. (Practice A Q1/key)"]),
 ("Two-way tables · T2",[
  "Row % = cell ÷ row total: share of that row group in the cell.",
  "Column % = cell ÷ column total: share of that column group in the cell.",
  "Same decision as conditional probability: the chosen reference group determines the denominator.",
  "Check: row percentages sum to 100% within each row; column percentages sum to 100% within each column. Different columns’ percentages across a row need not sum to 100%. (Notes §2.1–2.3)",
  "Example: cell 8, row total 20, column total 16 → 40.0% of row group; 50.0% of column group."]),
 ("Fast denominator check",[
  "Say the reference group in words first. Circle its total. Divide the cell/joint count by that total.",
  "Your saved T2 attempt used a row total for a column percentage: for a column %, use the column total."]),
],"SIDE 1 OF 2 · Print as one sheet, front and back")

side("STAT 110 | EXAM SHEET",[
 ("BACK · Grouped summaries, reporting & scope",[
  "Draft for studying. Confirm instructor rules for permitted content, paper size, and printing before bringing this sheet into the exam."]),
 ("Grouped summaries · T4",[
  "Split cases by a categorical variable; compute one summary (e.g., mean or count) per non-empty group.",
  "Output rows = number of non-empty groups, not number of original cases.",
  "Compare like with like: mean to mean or total to total; do not compare a group mean with a group total. (Notes §3.1–3.3)",
  "Example: means for 4 course sections → 4 rows. (2025 Midterm 1 Q3; historical example)"]),
 ("Reporting rule · applies to every proportion",[
  "Report as a percentage rounded to one decimal place, and name the reference group in words.",
  "Write “40.0% of commuters,” not “0.4,” “40%,” or “2/5.” The outline says omitting the reference group loses one point. (Outline)"]),
 ("Bayes’ rule · T3 source needed",[
  "Listed in the outline as in scope and lecture-covered, but no explanation or worked example appears in supplied notes. Add only your instructor’s approved rule/example here; don’t rely on this sheet as a complete Bayes’ reference."]),
 ("Scope reminder",[
  "Supplied outline is labeled Midterm 1, while the course profile calls the final cumulative. It confirms T1–T4 for that midterm, not the complete final scope.",
  "Hypothesis testing is excluded from that Midterm 1 outline; its appearance on the 2025 past paper does not establish final coverage.",
  "Source map: outline; lecture notes §§1–3; Practice A Q1–Q4/key; 2025 Midterm 1 Q2–Q3; learning record (T2 denominator error; T1 recheck due). Final topics, sheet allowance, and formatting remain unconfirmed."]),
],"SIDE 2 OF 2 · Reverse side")

pdf.set_metadata({"title":"STAT 110 Exam Sheet — Study Draft", "author":"Prepared from supplied course materials"})
pdf.save(out/"STAT110_exam_sheet_draft.pdf",garbage=4,deflate=True)
