"""Build an editable presentation from the results in report/main.pdf.

Requires python-pptx. Run with: python3 report/build_main_pptx.py
"""

from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Inches, Pt


OUT = Path(__file__).with_name("main_presentation.pptx")
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]

NAVY = "14223A"
INK = "1B2940"
MUTED = "5C6D82"
TEAL = "078B83"
TEAL_DARK = "066B66"
TEAL_PALE = "E3F3F0"
ORANGE = "F39743"
ORANGE_PALE = "FFF0DD"
RED = "D95655"
WHITE = "FFFFFF"
BG = "F8FAFC"
LINE = "DCE5EC"
BLUE_PALE = "EAF1F8"


def color(hexcode):
    return RGBColor.from_string(hexcode)


def rect(slide, x, y, w, h, fill=WHITE, stroke=None, radius=False, width=1):
    shape = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE,
        Inches(x), Inches(y), Inches(w), Inches(h)
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = color(fill)
    shape.line.fill.background() if stroke is None else None
    if stroke:
        shape.line.color.rgb = color(stroke)
        shape.line.width = Pt(width)
    if radius:
        try:
            shape.adjustments[0] = 0.12
        except Exception:
            pass
    return shape


def line(slide, x1, y1, x2, y2, stroke=LINE, width=1):
    s = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
    s.line.color.rgb = color(stroke)
    s.line.width = Pt(width)
    return s


def text(slide, value, x, y, w, h, size=18, fg=INK, bold=False, align=None,
         valign=MSO_ANCHOR.TOP, margin=0, font="Aptos", spacing=1.08):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.clear()
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(margin)
    tf.margin_top = tf.margin_bottom = Inches(margin)
    tf.vertical_anchor = valign
    for i, part in enumerate(value.split("\n")):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = part
        p.font.name = font
        p.font.size = Pt(size)
        p.font.bold = bold
        p.font.color.rgb = color(fg)
        p.space_after = Pt(3)
        p.line_spacing = spacing
        if align is not None:
            p.alignment = align
    return box


def slide(title, eyebrow, n, subtitle=None):
    s = prs.slides.add_slide(BLANK)
    rect(s, 0, 0, 13.333, 7.5, BG)
    rect(s, 0, 0, 0.12, 7.5, TEAL)
    text(s, eyebrow.upper(), 0.58, 0.35, 9.5, 0.3, 10.5, TEAL_DARK, True)
    text(s, title, 0.58, 0.72, 12.1, 0.62, 28, NAVY, True)
    if subtitle:
        text(s, subtitle, 0.59, 1.38, 12.0, 0.43, 14.2, MUTED)
    line(s, 0.58, 7.12, 12.74, 7.12)
    text(s, "Dependency-preserving evidence packing  •  Big Data course project", 0.59, 7.19, 10.8, 0.19, 9.2, MUTED)
    text(s, f"{n:02d} / 12", 11.7, 7.17, 1.02, 0.23, 9.5, MUTED, align=PP_ALIGN.RIGHT)
    return s


def card(slide_, x, y, w, h, title_, body, accent=TEAL, fill=WHITE, title_size=17, body_size=14.5):
    rect(slide_, x, y, w, h, fill, LINE, True)
    rect(slide_, x, y, 0.06, h, accent)
    text(slide_, title_, x+0.22, y+0.18, w-0.44, 0.43, title_size, NAVY, True)
    text(slide_, body, x+0.22, y+0.7, w-0.44, h-0.83, body_size, MUTED)


def pill(slide_, label, x, y, w, fill=TEAL_PALE, fg=TEAL_DARK, size=12):
    rect(slide_, x, y, w, 0.39, fill, None, True)
    text(slide_, label, x+0.09, y+0.06, w-0.18, 0.24, size, fg, True, PP_ALIGN.CENTER)


# 1. Title
s = prs.slides.add_slide(BLANK)
rect(s, 0, 0, 13.333, 7.5, NAVY)
rect(s, 0, 0, 0.15, 7.5, TEAL)
pill(s, "BIG DATA COURSE PROJECT", 0.72, 0.6, 2.75, TEAL, WHITE, 10.5)
text(s, "Keep the number.\nKeep its meaning.", 0.72, 1.25, 8.1, 2.04, 34, WHITE, True, spacing=1.0)
text(s, "Dependency-preserving evidence packing for numerical question answering over financial reports", 0.75, 3.6, 8.35, 1.05, 20, "D8E8F1")
text(s, "Pushpendra Singh  ·  Badri Bishal Das", 0.75, 6.54, 7.6, 0.35, 14, WHITE, True)
text(s, "Indian Institute of Technology Guwahati", 0.75, 6.91, 7.6, 0.29, 11.5, "AFC4D2")
rect(s, 9.45, 1.18, 3.16, 4.76, "203852", None, True)
text(s, "637", 9.86, 1.63, 2.36, 0.85, 43, WHITE, True, PP_ALIGN.CENTER)
text(s, "payment volume", 9.83, 2.37, 2.41, 0.34, 14, "B6D1DC", align=PP_ALIGN.CENTER)
line(s, 9.85, 2.93, 12.2, 2.93, TEAL, 2)
text(s, "÷ 5.0", 9.86, 3.22, 2.36, 0.66, 30, WHITE, True, PP_ALIGN.CENTER)
text(s, "transactions", 9.83, 3.91, 2.41, 0.34, 14, "B6D1DC", align=PP_ALIGN.CENTER)
rect(s, 9.85, 4.68, 2.34, 0.74, TEAL, None, True)
text(s, "= 127.4", 9.96, 4.82, 2.13, 0.45, 25, WHITE, True, PP_ALIGN.CENTER)

# 2. Problem
s = slide("Why financial QA fails", "The problem", 2, "A number without its table context can be the wrong number.")
rect(s, 0.65, 2.04, 7.15, 3.87, WHITE, LINE, True)
text(s, "American Express", 0.98, 2.38, 3.0, 0.44, 18, NAVY, True)
text(s, "Payment volume (bn)", 1.0, 3.05, 2.26, 0.66, 15, MUTED)
text(s, "Total volume (bn)", 3.28, 3.05, 2.08, 0.66, 15, MUTED)
text(s, "Transactions (bn)", 5.37, 3.05, 2.08, 0.66, 15, MUTED)
rect(s, 0.96, 3.87, 2.08, 1.12, TEAL_PALE, None, True)
text(s, "637", 1.25, 4.08, 1.5, 0.67, 30, TEAL_DARK, True, PP_ALIGN.CENTER)
rect(s, 3.28, 3.87, 2.08, 1.12, ORANGE_PALE, None, True)
text(s, "647", 3.58, 4.08, 1.5, 0.67, 30, NAVY, True, PP_ALIGN.CENTER)
rect(s, 5.52, 3.87, 1.83, 1.12, BLUE_PALE, None, True)
text(s, "5.0", 5.76, 4.08, 1.35, 0.67, 30, NAVY, True, PP_ALIGN.CENTER)
text(s, "Which volume belongs in the answer?", 0.99, 5.25, 6.48, 0.4, 17, NAVY, True)
card(s, 8.14, 2.05, 4.5, 1.72, "Correct calculation", "637 ÷ 5.0 = 127.4", TEAL, TEAL_PALE, 17, 20)
card(s, 8.14, 4.09, 4.5, 1.72, "Wrong but plausible", "647 ÷ 5.0 = 129.4", ORANGE, ORANGE_PALE, 17, 20)

# 3. Question and data
s = slide("One question, six datasets", "Research scope", 3,
          "At the same model and evidence budget, do preserved labels and links improve answers?")
items = [
    ("FinQA", "Report tables + arithmetic programs"),
    ("ConvFinQA", "Ordered follow-up questions"),
    ("TAT-QA", "Table + text, scales and spans"),
    ("TAT-HQA", "Hypothetical financial changes"),
    ("HybridQA", "Linked table cells and passages"),
    ("MultiHiertt", "Nested headers across tables"),
]
for i, (name, desc) in enumerate(items):
    x = 0.65 + (i % 3) * 4.13
    y = 2.08 + (i // 3) * 1.87
    card(s, x, y, 3.85, 1.57, name, desc, TEAL if i < 4 else ORANGE, WHITE, 17, 13.5)
text(s, "HybridQA tests transfer beyond financial reports.", 0.7, 6.18, 11.8, 0.42, 15, MUTED)

# 4. Method
s = slide("Represent evidence as a dependency graph", "Our solution", 4,
          "Facts point to the labels required to interpret them.")
rect(s, 0.65, 2.03, 7.42, 3.92, WHITE, LINE, True)
pill(s, "SHARED ROW LABEL", 2.85, 2.38, 2.87, TEAL_PALE)
text(s, "American Express", 2.7, 2.89, 3.25, 0.44, 19, NAVY, True, PP_ALIGN.CENTER)
for x, number, label in [(1.3, "637", "payment volume"), (3.54, "647", "total volume"), (5.74, "5.0", "transactions")]:
    line(s, x+0.71, 3.38, 4.38, 3.36, LINE, 1.2)
    rect(s, x, 3.7, 1.51, 0.9, TEAL_PALE, None, True)
    text(s, number, x+0.1, 3.9, 1.31, 0.48, 25, TEAL_DARK, True, PP_ALIGN.CENTER)
    text(s, label, x-0.11, 4.79, 1.75, 0.6, 13, MUTED, align=PP_ALIGN.CENTER)
card(s, 8.42, 2.03, 4.23, 1.78, "Bundle rule", "Admit a value with its headers, unit, ancestors and link anchors.", TEAL, WHITE, 17, 14.3)
card(s, 8.42, 4.08, 4.23, 1.87, "Shared-label payoff", "First cell: 18 vs 15 tokens. Four cells: 50 vs 57 tokens.", ORANGE, WHITE, 17, 14.3)
text(s, "Complete bundles only; labels already packed cost nothing extra.", 0.7, 6.22, 11.8, 0.36, 15, MUTED)

# 5. Pipeline
s = slide("Only the packing step changes", "Controlled pipeline", 5,
          "The same candidates and model are used for each evidence selection method.")
stages = [
    ("01", "Read + normalize", "Raw records become facts and dependencies"),
    ("02", "BM25 rank", "Rank candidate cells and passages"),
    ("03", "Pack evidence", "Ordinary / dependency / length-matched"),
    ("04", "Gemini plan", "Copy source numbers into a JSON plan"),
    ("05", "Check + score", "Validate, execute, official scorer"),
]
for i, (num, name, desc) in enumerate(stages):
    x = 0.67+i*2.52
    fill = TEAL_PALE if i == 2 else WHITE
    rect(s, x, 2.28, 2.27, 2.6, fill, TEAL if i == 2 else LINE, True)
    pill(s, num, x+0.2, 2.52, 0.53, TEAL if i == 2 else BLUE_PALE, WHITE if i == 2 else NAVY, 11)
    text(s, name, x+0.19, 3.12, 1.9, 0.43, 16, NAVY, True)
    text(s, desc, x+0.19, 3.68, 1.9, 0.9, 13.5, MUTED)
    if i < 4:
        text(s, "→", x+2.28, 3.3, 0.21, 0.45, 18, TEAL, True, PP_ALIGN.CENTER)
rect(s, 0.69, 5.34, 11.9, 0.92, BLUE_PALE, None, True)
text(s, "Grounding check: every numeric argument must appear in packed evidence or the question.", 0.96, 5.55, 11.3, 0.43, 17, NAVY, True)
text(s, "Gold answers enter only at scoring; future conversation turns stay hidden.", 0.7, 6.49, 11.75, 0.32, 13.8, MUTED)

# 6. Big Data
s = slide("A verified graph at 1.36M-fact scale", "Big Data preparation", 6,
          "Spark creates a partitioned Parquet store and checks the fact links.")
metrics = [("1,360,644", "facts"), ("1,884,748", "dependency edges"), ("0", "unresolved links"), ("4,395", "deduplicated documents")]
for i, (value, label) in enumerate(metrics):
    x = 0.66 + i*3.16
    rect(s, x, 2.16, 2.91, 1.48, WHITE, LINE, True)
    text(s, value, x+0.17, 2.41, 2.57, 0.53, 25, TEAL_DARK, True, PP_ALIGN.CENTER)
    text(s, label, x+0.14, 3.02, 2.63, 0.32, 13.2, MUTED, align=PP_ALIGN.CENTER)
rect(s, 0.66, 4.09, 6.07, 1.73, TEAL_PALE, None, True)
text(s, "Parquet storage", 0.96, 4.35, 5.45, 0.38, 18, NAVY, True)
text(s, "0.18 GB vs 0.95 GB of JSONL  •  5.1× smaller", 0.96, 4.86, 5.45, 0.54, 18, TEAL_DARK, True)
rect(s, 6.96, 4.09, 5.7, 1.73, ORANGE_PALE, None, True)
text(s, "Measured local run", 7.25, 4.35, 5.1, 0.38, 18, NAVY, True)
text(s, "Spark: 37.0 s at 4 cores; Python: 15.8 s", 7.25, 4.86, 5.08, 0.62, 17.5, NAVY, True)
text(s, "The benefit here is a verified columnar data layer, not a speedup on this machine.", 0.7, 6.2, 11.7, 0.51, 15.1, MUTED)

# 7. Comparison
s = slide("Three ways to spend the same budget", "Experiment design", 7,
          "All methods use the same BM25 ranking and the same evidence cap.")
methods = [
    ("Ordinary", "Repeat each fact's immediate structural labels inline.", BLUE_PALE, NAVY),
    ("Dependency", "Add recursive headers, units, hierarchy and links as complete bundles.", TEAL_PALE, TEAL_DARK),
    ("Length-matched", "Spend similar space on source neighbours without graph closure.", ORANGE_PALE, NAVY),
]
for i, (name, desc, fill, fg) in enumerate(methods):
    x = 0.66 + i*4.22
    rect(s, x, 2.15, 3.92, 2.56, fill, None, True)
    text(s, name, x+0.22, 2.48, 3.48, 0.46, 21, fg, True)
    text(s, desc, x+0.22, 3.12, 3.47, 1.14, 16, INK)
rect(s, 0.66, 5.2, 12.0, 1.13, WHITE, LINE, True)
text(s, "Coverage: all 9,268 scorable development questions, 5 budgets, 3 methods", 0.96, 5.43, 11.32, 0.42, 17, NAVY, True)
text(s, "Answer test: Gemini 3.5 Flash-Lite, 50 samples per dataset (45 ConvFinQA turns).", 0.7, 6.48, 11.72, 0.32, 13.7, MUTED)

# 8. Coverage
s = slide("Dependency packing retains more gold evidence", "Full development-set coverage", 8,
          "At the chosen budgets, the gain appears across all six datasets.")
rows = [
    ("FinQA", "96.3", "97.3", "+1.0"),
    ("ConvFinQA", "97.1", "97.4", "+0.3"),
    ("TAT-QA", "90.1", "91.7", "+1.6"),
    ("HybridQA", "72.0", "76.0", "+4.0"),
    ("TAT-HQA", "84.2", "86.9", "+2.7"),
    ("MultiHiertt", "84.9", "88.6", "+3.7"),
]
rect(s, 0.69, 2.13, 8.05, 4.45, WHITE, LINE, True)
for x, label in [(1.0, "Dataset"), (4.38, "Ordinary"), (5.91, "Dependency"), (7.36, "Gain")]:
    text(s, label, x, 2.38, 1.5, 0.35, 13.5, MUTED, True)
line(s, 1.0, 2.85, 8.35, 2.85, LINE)
for i, (name, o, d, gain) in enumerate(rows):
    y = 3.01+i*0.53
    text(s, name, 1.0, y, 2.25, 0.33, 15.5, NAVY, True)
    text(s, o+"%", 4.4, y, 1.12, 0.33, 15, MUTED)
    text(s, d+"%", 5.92, y, 1.12, 0.33, 15, TEAL_DARK, True)
    pill(s, gain+" pp", 7.16, y-0.045, 1.17, TEAL_PALE, TEAL_DARK, 11)
    if i < 5:
        line(s, 1.0, y+0.43, 8.35, y+0.43, "EBF0F3")
card(s, 9.04, 2.13, 3.57, 1.84, "Strongest gain", "HybridQA: +4.0 percentage points", TEAL, TEAL_PALE, 16, 17)
card(s, 9.04, 4.19, 3.57, 2.38, "Where it fades", "At 4,000 tokens the gap closes on four smaller datasets. At 200 tokens, structure can cost more than it saves.", ORANGE, ORANGE_PALE, 16, 14)

# 9. Answer quality
s = slide("Answer gains track better evidence coverage", "Paired answer experiment", 9,
          "Gemini 3.5 Flash-Lite; official execution accuracy for FinQA/ConvFinQA, F1 elsewhere.")
rect(s, 0.66, 2.14, 5.08, 3.98, TEAL_PALE, None, True)
text(s, "TAT-QA", 0.96, 2.49, 4.5, 0.4, 19, TEAL_DARK, True)
text(s, "60.2%  →  71.5%", 0.94, 3.19, 4.5, 0.68, 30, NAVY, True)
text(s, "+11.3 percentage points", 0.96, 4.09, 4.44, 0.43, 20, TEAL_DARK, True)
text(s, "95% paired interval: +4.1 to +19.9", 0.96, 4.79, 4.39, 0.45, 15, MUTED)
text(s, "Only gain whose interval excludes zero.", 0.96, 5.45, 4.39, 0.42, 15.2, NAVY, True)
rect(s, 6.05, 2.14, 6.58, 3.98, WHITE, LINE, True)
text(s, "Other dependency − ordinary differences", 6.37, 2.47, 5.92, 0.39, 17.4, NAVY, True)
diffs = [("FinQA", "+2.0"), ("ConvFinQA", "0.0"), ("HybridQA", "+5.3"), ("TAT-HQA", "+4.0"), ("MultiHiertt", "+9.8")]
for i, (name, diff) in enumerate(diffs):
    y=3.09+i*0.53
    text(s, name, 6.37, y, 3.45, 0.34, 15.1, MUTED)
    text(s, diff+" pp", 10.57, y, 1.63, 0.34, 15.1, TEAL_DARK, True, PP_ALIGN.RIGHT)
    if i < 4:
        line(s, 6.37, y+0.42, 12.25, y+0.42, "EBF0F3")
text(s, "These answer scores use 50 questions per dataset, except 45 ConvFinQA turns.", 0.7, 6.44, 11.66, 0.37, 14.2, MUTED)

# 10. Case study
s = slide("One TAT-QA question shows the mechanism", "Saved-output case study", 10,
          "Question: ratio of inventory reserves to accrued compensation in 2018.")
rect(s, 0.68, 2.18, 5.83, 3.87, ORANGE_PALE, None, True)
pill(s, "ORDINARY  ·  398 / 400 TOKENS", 1.0, 2.47, 3.39, ORANGE, WHITE, 11)
text(s, "355 tokens of shared text", 1.0, 3.13, 4.88, 0.46, 19, NAVY, True)
text(s, "Labels repeated beside each cell", 1.0, 3.82, 4.88, 0.43, 17, INK)
text(s, "Accrued-compensation value 358 is excluded.", 1.0, 4.54, 4.88, 0.77, 18, RED, True)
text(s, "Model abstains.", 1.0, 5.4, 4.84, 0.38, 16, NAVY, True)
rect(s, 6.81, 2.18, 5.83, 3.87, TEAL_PALE, None, True)
pill(s, "DEPENDENCY  ·  400 / 400 TOKENS", 7.13, 2.47, 3.67, TEAL, WHITE, 11)
text(s, "Same 355 tokens of text", 7.13, 3.13, 4.89, 0.46, 19, NAVY, True)
text(s, "Shared labels written once", 7.13, 3.82, 4.87, 0.43, 17, INK)
text(s, "Both 948 and 358 fit with context.", 7.13, 4.54, 4.87, 0.64, 18, TEAL_DARK, True)
text(s, "948 ÷ 358 = 2.65  ✓", 7.13, 5.38, 4.88, 0.4, 19, NAVY, True)
text(s, "This is an illustrative saved question; aggregate results are on the previous slides.", 0.7, 6.42, 11.7, 0.39, 14.1, MUTED)

# 11. Grounded executor
s = slide("Grounding improves traceability, not every score", "Executor follow-up", 11,
          "A separate Gemini 3.1 Flash-Lite experiment compared execution with direct answers.")
card(s, 0.69, 2.17, 3.83, 2.15, "What the executor adds", "The model copies evidence numbers; code validates and computes a bounded decimal result.", TEAL, TEAL_PALE, 17, 15)
card(s, 4.76, 2.17, 3.83, 2.15, "HybridQA", "Direct answering leads by 16.4 points on linked-passage questions.", ORANGE, ORANGE_PALE, 17, 15)
card(s, 8.82, 2.17, 3.83, 2.15, "MultiHiertt", "A reported +22.1 executor gain is sensitive to the scorer's numeric treatment.", ORANGE, ORANGE_PALE, 17, 14.4)
rect(s, 0.69, 4.83, 11.96, 1.1, WHITE, LINE, True)
text(s, "Takeaway: execution gives auditable evidence links, but this study does not show a consistent accuracy gain over direct answers.", 0.98, 5.1, 11.37, 0.55, 18, NAVY, True)

# 12. Conclusion
s = slide("Keep context where the budget is tight", "Conclusion", 12)
rect(s, 0.66, 1.83, 7.54, 3.61, TEAL_PALE, None, True)
text(s, "What the evidence supports", 0.97, 2.14, 6.92, 0.43, 20, TEAL_DARK, True)
text(s, "• Better gold-evidence retention on all six datasets at chosen budgets\n• TAT-QA answer gain: +11.3 points on a 50-question sample\n• Verified 1.36M-fact graph with zero unresolved links", 0.97, 2.78, 6.88, 2.34, 17, NAVY, spacing=1.3)
rect(s, 8.5, 1.83, 4.15, 3.61, WHITE, LINE, True)
text(s, "Limits", 8.81, 2.14, 3.52, 0.43, 20, NAVY, True)
text(s, "• 50-question answer samples\n• Loss at very small budgets\n• Inferred headers may be wrong\n• Development splits only", 8.81, 2.75, 3.45, 2.22, 16.1, MUTED, spacing=1.21)
rect(s, 0.66, 5.83, 11.99, 0.85, NAVY, None, True)
text(s, "Next: larger answer tests, budget-aware closure, and better nested-header inference.", 0.95, 6.05, 11.38, 0.4, 17.2, WHITE, True)


prs.core_properties.title = "Dependency-Preserving Evidence Packing"
prs.core_properties.subject = "Presentation based on report/main.pdf"
prs.core_properties.author = "Pushpendra Singh and Badri Bishal Das"
prs.core_properties.keywords = "FinQA; evidence packing; numerical reasoning; Big Data"
prs.save(OUT)
print(f"Wrote {OUT} ({len(prs.slides)} slides)")
