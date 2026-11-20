from pathlib import Path
import textwrap
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

root = Path(__file__).resolve().parent
source = (root / 'sta_final_study_guide.md').read_text(encoding='utf-8')
pages = [
    ('STAT 110 FINAL STUDY GUIDE', 'SUPPORTED STARTER • 18 NOV 2026', [
        ('SCOPE NOTE', 'The profile lists a cumulative final on December 8, 2026, but the only supplied outline is labeled “Midterm 1.” This guide covers topics confirmed in that outline; it does not establish the final’s full scope. Ask for the final review sheet or remaining lecture notes to complete it. Bayes’ rule is listed in scope in the outline, but its teaching notes were not supplied. Hypothesis testing is explicitly excluded from the supplied Midterm 1 outline; its status on the final is unconfirmed.'),
        ('1  CONDITIONAL PROBABILITY  (T1)', 'P(A | B) means “the probability of A among cases in B.” The group after the vertical bar is the reference group and supplies the denominator.\n\nMethod: Identify the restricted group B; count cases in both A and B; divide the overlap by the total in B. State a percentage rounded to one decimal place and name B in words. The notes assume equally weighted cases and a nonempty reference group.\n\nExample: 10 of 25 commuters cycle: 10 / 25 = 40.0% of commuters.\n\nFragile distinction: P(cycles | commuter) uses commuters as denominator. P(commuter | cycles) uses cyclists. These generally differ.\n\nBefore dividing, ask “out of which group?” The saved practice attempt chose a row total when a column percentage was requested; choose the denominator from the requested reference group.'),
        ('2  TWO-WAY TABLES  (T2)', 'A two-way table counts cases across two categorical variables. A cell is one combination; row and column totals summarize their respective groups.\n\nROW PERCENTAGE: cell ÷ total of that row.\nCOLUMN PERCENTAGE: cell ÷ total of that column.\n\nRow percentages add to 100% across each row. Column percentages add to 100% down each column. Percentages across a row of column percentages need not add to 100%.\n\nChoose the margin by reading the wording as a conditional probability. The population named after “of,” “among,” or “within” is the reference group and denominator. Example: “what percentage of remote workers are trainees?” divides trainees among remote workers by the remote-worker total. Report “x.x% of remote workers.”'),
    ]),
    ('STAT 110 • STUDY GUIDE', 'SUPPORTED TOPICS & EXAM CHECKS', [
        ('3  GROUPED SUMMARIES  (T4)', 'A grouped summary splits cases by a categorical variable and calculates one summary (such as a mean or count) for each group. The output has one row per nonempty group, not one row per original case.\n\nExample: A mean score for each of four course sections produces four rows, even if there are 120 students. Each row represents a section’s summary, not an individual student.\n\nCompare like with like: mean to mean, count to count. Do not compare a group mean with a group total.'),
        ('4  NAMED BUT UNSUPPORTED: BAYES’ RULE  (T3)', 'The supplied outline says Bayes’ rule was covered in lecture, but teaching notes were not included in the supplied files. This guide does not invent a rule or formula. Add the lecture notes or a course example before relying on a Bayes’ rule explanation for the final.'),
        ('REPORTING RULE & QUICK CHECKLIST', 'The supplied outline requires every proportion as a percentage rounded to one decimal place, with its reference group named: “40.0% of commuters.”\n\n1. What group does the question restrict me to?\n2. Is the denominator that group’s total?\n3. Is this a row or column percentage?\n4. Did I report one decimal place and name the reference group?\n5. For grouped summaries, am I counting nonempty groups and comparing the same summary type?'),
        ('COURSE-BASED REVIEW ROUTE', 'Recheck T1 independently. Spend extra retrieval practice on T2’s denominator choice (the saved record flags this as needing practice). Learn T4 from the supplied notes. Obtain course notes for T3. The final’s full scope and format remain unconfirmed from the available materials.'),
        ('SOURCE LOCATORS', 'Outline: supplied Midterm 1 outline, T1–T4 and reporting rule. Lecture notes: §§1–3. Practice set A and instructor key: T1 examples. Historical Midterm 1 2025: Q3 illustrates grouped-summary row count; historical questions do not establish final coverage. Saved course profile and learning record: final date and learning evidence.'),
    ])
]

out = root / 'sta_final_study_guide.pdf'
with PdfPages(out) as pdf:
    for title, subtitle, blocks in pages:
        fig = plt.figure(figsize=(8.27, 11.69), facecolor='#fbfaf7')
        ax = fig.add_axes([0, 0, 1, 1]); ax.set_axis_off()
        ax.text(.09, .94, title, fontsize=19, fontweight='bold', color='#17324d', va='top')
        ax.text(.09, .905, subtitle, fontsize=9, color='#287c78', va='top', fontweight='bold')
        y = .855
        for heading, body in blocks:
            ax.text(.09, y, heading, fontsize=11, color='#17324d', fontweight='bold', va='top')
            y -= .027
            for para in body.split('\n'):
                if not para:
                    y -= .012
                    continue
                wrapped = textwrap.wrap(para, width=105, break_long_words=False)
                ax.text(.09, y, '\n'.join(wrapped), fontsize=8.2, color='#273746', va='top', linespacing=1.2)
                y -= .017 * len(wrapped) + .008
            y -= .008
        ax.text(.09, .018, 'STAT 110 • Study guide based only on supplied local course files', fontsize=7, color='#73808c')
        pdf.savefig(fig, bbox_inches='tight')
        fig.savefig(root / f'preview-{pages.index((title, subtitle, blocks))+1}.png', dpi=110, facecolor=fig.get_facecolor())
        plt.close(fig)
print(out)
