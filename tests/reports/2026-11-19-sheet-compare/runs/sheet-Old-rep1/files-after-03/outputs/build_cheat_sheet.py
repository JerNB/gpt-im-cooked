from pathlib import Path
import fitz

out = Path(__file__).parent
pdf = fitz.open()
W, H, M = 612, 792, 50

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

def side(title, sections, side_label, body_size=12.5, leading=18.5):
    page=pdf.new_page(width=W,height=H); y=40
    page.insert_text((M,y),title,fontname="hebo",fontsize=21,color=(.08,.28,.4)); y+=27
    page.insert_text((M,y),side_label,fontname="helv",fontsize=10,color=(.35,.39,.43)); y+=20
    for head, paras in sections:
        y+=9
        if y>H-70: raise ValueError(f"Content overflow before {head}: {y}")
        page.insert_text((M,y),head,fontname="hebo",fontsize=16 if body_size > 13 else 15,color=(.08,.28,.4)); y+=23
        for txt in paras:
            size=body_size
            lines=wrap(txt,"helv",size,W-2*M)
            if y+leading*len(lines)>H-35: raise ValueError(f"Content overflow: {head} at {y}")
            for line in lines:
                page.insert_text((M,y),line,fontname="helv",fontsize=size,color=(.12,.17,.23)); y+=leading
            y+=6
    return page

side("STAT 110 | EXAM SHEET",[
 ("FRONT · Conditional probability & two-way tables",[
  "Study draft only. Confirm instructor rules for allowed content, paper size, and printing before the exam."]),
 ("One worked example · T1 conditional probability + T2 table percentages",[
  "A cell count is 8. Its row total is 20 and its column total is 16. (Counts already used in this sheet.)",
  "Row percentage: 8 ÷ 20 = 40.0% of that row group.",
  "Column percentage: 8 ÷ 16 = 50.0% of that column group.",
  "Read as a conditional probability: the percentage depends on which group is the reference group. The reference group supplies the denominator. (Notes §§1.2, 2.2)",
  "Reporting style: percentage to one decimal place + reference group in words. Your saved T2 attempt used a row total for a column percentage; this example shows the denominator change."]),
],"SIDE 1 OF 2 · Print as one sheet, front and back",body_size=15,leading=22)

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
],"SIDE 2 OF 2 · Reverse side",body_size=12.5,leading=18.5)

pdf.set_metadata({"title":"STAT 110 Exam Sheet — Study Draft", "author":"Prepared from supplied course materials"})
pdf.save(out/"STAT110_exam_sheet_draft.pdf",garbage=4,deflate=True)
