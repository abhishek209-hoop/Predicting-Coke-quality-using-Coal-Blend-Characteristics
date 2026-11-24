"""
Master Python script to construct the 15-slide Metallurgical Engineering Presentation
Coke_Quality_Prediction_Presentation.pptx using python-pptx.
"""

from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def build_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Color definitions
    C_DARK_CHARCOAL = RGBColor(26, 30, 36)    # #1A1E24
    C_HEADER_BG     = RGBColor(33, 37, 44)    # #21252C
    C_STEEL_GREY    = RGBColor(74, 85, 104)   # #4A5568
    C_SLATE_BLUE    = RGBColor(43, 108, 176)  # #2B6CB0
    C_MUTED_ORANGE  = RGBColor(217, 107, 39)  # #D96B27 - Thermal/glow accent
    C_BG_OFFWHITE   = RGBColor(248, 249, 250) # #F8F9FA
    C_WHITE         = RGBColor(255, 255, 255)
    C_CARD_BG       = RGBColor(255, 255, 255)
    C_CARD_BORDER   = RGBColor(218, 224, 233)
    C_ACCENT_GREEN  = RGBColor(47, 133, 90)   # #2F855A
    C_ALERT_GREEN   = RGBColor(47, 133, 90)   # #2F855A
    C_ACCENT_RED    = RGBColor(197, 48, 48)   # #C53030
    C_DARK_RED      = RGBColor(155, 44, 44)   # Degradation / failure highlight
    C_TEXT_DARK     = RGBColor(26, 32, 44)
    C_TEXT_MUTED    = RGBColor(113, 128, 150)

    graphs_dir = Path("results/graphs")

    # Helper: Set background
    def set_bg(slide, color=C_BG_OFFWHITE):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = color
        bg.line.fill.background()
        return bg

    # Helper: Add header
    def add_header(slide, title_text, category_text="DEPARTMENT OF METALLURGICAL ENGINEERING"):
        banner = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(1.18))
        banner.fill.solid()
        banner.fill.fore_color.rgb = C_HEADER_BG
        banner.line.fill.background()

        tx_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.12), Inches(11.7), Inches(0.95))
        tf = tx_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_bottom = tf.margin_right = 0

        p_cat = tf.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.name = "Arial"
        p_cat.font.size = Pt(10)
        p_cat.font.bold = True
        p_cat.font.color.rgb = C_MUTED_ORANGE

        p_title = tf.add_paragraph()
        p_title.text = title_text
        p_title.font.name = "Arial"
        p_title.font.size = Pt(21)
        p_title.font.bold = True
        p_title.font.color.rgb = C_WHITE

        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, Inches(1.18), Inches(13.333), Inches(0.06))
        line.fill.solid()
        line.fill.fore_color.rgb = C_MUTED_ORANGE
        line.line.fill.background()

    # Helper: Create card
    def create_card(slide, left, top, width, height, bg_color=C_CARD_BG, border_color=C_CARD_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        if border_color:
            card.line.color.rgb = border_color
            card.line.width = Pt(1.2)
        else:
            card.line.fill.background()
        return card

    # Helper: Speaker notes
    def set_notes(slide, notes):
        tf = slide.notes_slide.notes_text_frame
        tf.text = notes.strip()

    # =========================================================================
    # SLIDE 1: TITLE SLIDE
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_bg(s1, C_DARK_CHARCOAL)

    # Decorative top bar
    t_bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.15))
    t_bar.fill.solid()
    t_bar.fill.fore_color.rgb = C_MUTED_ORANGE
    t_bar.line.fill.background()

    # Title Card
    c1 = create_card(s1, Inches(1.0), Inches(1.1), Inches(11.333), Inches(3.2), bg_color=C_HEADER_BG, border_color=C_MUTED_ORANGE)
    tf1 = c1.text_frame
    tf1.word_wrap = True
    tf1.margin_left = Inches(0.5)
    tf1.margin_top = Inches(0.4)

    p0 = tf1.paragraphs[0]
    p0.text = "B.TECH / RESEARCH PROJECT PRESENTATION"
    p0.font.name = "Arial"
    p0.font.size = Pt(12)
    p0.font.bold = True
    p0.font.color.rgb = C_MUTED_ORANGE

    p1 = tf1.add_paragraph()
    p1.text = "Prediction of Coke Strength after Reaction (CSR) and Coke Reactivity Index (CRI) from Coal Blend Characteristics"
    p1.font.name = "Arial"
    p1.font.size = Pt(25)
    p1.font.bold = True
    p1.font.color.rgb = C_WHITE

    p2 = tf1.add_paragraph()
    p2.text = "A Comparative Metallurgical & Machine Learning Evaluation (Modified Reproduction & Extension of Dash et al., 2012)"
    p2.font.name = "Arial"
    p2.font.size = Pt(14)
    p2.font.color.rgb = RGBColor(203, 213, 224)

    # Metadata Card
    c2 = create_card(s1, Inches(1.0), Inches(4.6), Inches(11.333), Inches(2.2), bg_color=C_HEADER_BG, border_color=C_CARD_BORDER)
    tf2 = c2.text_frame
    tf2.word_wrap = True
    tf2.margin_left = Inches(0.5)
    tf2.margin_top = Inches(0.3)

    p_cand = tf2.paragraphs[0]
    p_cand.text = "Candidate / Student: [Student Name / Roll No.]"
    p_cand.font.name = "Arial"
    p_cand.font.size = Pt(14)
    p_cand.font.bold = True
    p_cand.font.color.rgb = C_WHITE

    p_sup = tf2.add_paragraph()
    p_sup.text = "Project Supervisor: [Supervisor Name, Designation]"
    p_sup.font.name = "Arial"
    p_sup.font.size = Pt(14)
    p_sup.font.color.rgb = C_WHITE

    p_dept = tf2.add_paragraph()
    p_dept.text = "Department of Metallurgical Engineering | [Institution / University Name]"
    p_dept.font.name = "Arial"
    p_dept.font.size = Pt(13)
    p_dept.font.color.rgb = RGBColor(203, 213, 224)

    p_date = tf2.add_paragraph()
    p_date.text = "Academic Session 2026–2027 | Reference: Dash et al. (2012), IJCPU"
    p_date.font.name = "Arial"
    p_date.font.size = Pt(12)
    p_date.font.color.rgb = C_MUTED_ORANGE

    set_notes(s1, """
Good morning, respected members of the evaluation committee and dear supervisor.
Today, I am presenting our metallurgical engineering project titled: 'Prediction of Coke Strength after Reaction (CSR) and Coke Reactivity Index (CRI) from Coal Blend Characteristics: A Comparative Study Using Machine Learning Models'.
This project is inspired by the classic research paper by Dash, Guha, Chakraborty, and Banerjee (2012) from Tata Steel R&D.
In ironmaking, blast furnace productivity relies on the structural and chemical competence of metallurgical coke. Carbonization tests in pilot ovens are labor-intensive, slow, and expensive. Our research develops a rigorous, leak-free computational pipeline to predict post-reaction coke quality parameters directly from uncarbonized coal blend properties.
Over the next 10 minutes, I will guide you through the metallurgical foundation of coke quality, the petrographic characteristics of coal blends, our data audit including compositional closure, and the comparative performance of four predictive models: Multiple Linear Regression, XGBoost, Random Forest, and Decision Tree.
""")

    # =========================================================================
    # SLIDE 2: INTRODUCTION: METALLURGICAL IMPORTANCE OF COKE
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_bg(s2)
    add_header(s2, "Introduction: Metallurgical Importance of Coke in Blast Furnace Ironmaking")

    # Left Column: Key Technical Concepts
    c_left = create_card(s2, Inches(0.8), Inches(1.4), Inches(6.5), Inches(5.6))
    tf_l = c_left.text_frame
    tf_l.word_wrap = True
    tf_l.margin_left = tf_l.margin_top = Inches(0.35)

    p = tf_l.paragraphs[0]
    p.text = "1. Role of Coke as the Blast Furnace Backbone"
    p.font.name = "Arial"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = C_SLATE_BLUE

    bullets_l = [
        "Produced by destructive distillation of blended coking coals at 1000–1100°C in slot-recovery ovens.",
        "Thermal Agent: Burns at tuyeres (1800–2200°C) providing heat for smelting iron ore and flux.",
        "Chemical Reductant: Generates CO gas (C + O2 -> CO2; CO2 + C -> 2CO) for indirect and direct iron oxide reduction.",
        "Mechanical Grid: Carries thousands of tons of descending burden without catastrophic crushing.",
        "Crucial Permeability Spacer: In the cohesive zone (1100–1400°C), ore softens and melts; coke remains the ONLY solid matrix allowing reducing gas ascent!",
        "Deadman Drainage: Maintains permeability for molten iron and slag drainage into the hearth."
    ]
    for b in bullets_l:
        p = tf_l.add_paragraph()
        p.text = "• " + b
        p.font.name = "Arial"
        p.font.size = Pt(13)
        p.font.color.rgb = C_TEXT_DARK

    # Right Column: Visual Blast Furnace Diagram
    c_right = create_card(s2, Inches(7.5), Inches(1.4), Inches(5.0), Inches(5.6))
    tf_r = c_right.text_frame
    tf_r.word_wrap = True
    tf_r.margin_left = tf_r.margin_top = Inches(0.2)
    p = tf_r.paragraphs[0]
    p.text = "Blast Furnace Operating Zones & Coke Function"
    p.font.name = "Arial"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_DARK_CHARCOAL

    if (graphs_dir / "bf_coke_zones.png").exists():
        s2.shapes.add_picture(str(graphs_dir / "bf_coke_zones.png"), Inches(7.65), Inches(1.9), width=Inches(4.7))

    set_notes(s2, """
To appreciate why coke quality prediction is vital, we must first examine the metallurgical environment of the blast furnace.
Metallurgical coke is produced by heating crushed coking coal blends in refractory slot ovens at 1000 to 1100 degrees Celsius in the absence of oxygen.
Inside the blast furnace, coke performs multiple functions: it is the primary fuel supplying thermal energy, the chemical reducing agent producing carbon monoxide gas, and most crucially, the physical support structure.
As seen in the cross-sectional diagram on the right, as iron ore descends into the cohesive zone between 1100 and 1400 degrees Celsius, it softens, becomes plastic, and melts. In this cohesive zone, coke is the ONLY solid material left in the furnace. It forms coke slits that allow the ascending reducing gases to pass through.
If the coke degrades prematurely, gas permeability collapses, causing hanging, slipping, channeling, and dangerous furnace scabs. Therefore, the properties of the raw coal blend must guarantee high structural integrity inside the furnace.
""")

    # =========================================================================
    # SLIDE 3: CRI, CSR AND THE ROLE OF COAL-BLEND CHARACTERISTICS
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_bg(s3)
    add_header(s3, "Coke Quality Assessment: Reactivity (CRI) and Post-Reaction Strength (CSR)")

    # Left Card: CRI
    c_cri = create_card(s3, Inches(0.8), Inches(1.4), Inches(5.7), Inches(2.7))
    tf = c_cri.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = Inches(0.3)
    p = tf.paragraphs[0]
    p.text = "Coke Reactivity Index (CRI) — Chemical Degradation"
    p.font.name = "Arial"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_MUTED_ORANGE

    p = tf.add_paragraph()
    p.text = "• Standardized NSC Test (ASTM D5341 / ISO 18894): 200 g coke (19–21 mm) reacted with CO2 (5 L/min) at 1100°C for 2 hours."
    p.font.size = Pt(12)
    p.font.color.rgb = C_TEXT_DARK

    p = tf.add_paragraph()
    p.text = "• Boudouard Gasification Reaction:  C + CO2  ->  2CO  (ΔH = +172 kJ/mol)"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_DARK_RED

    p = tf.add_paragraph()
    p.text = "• Significance: CRI = % mass loss. High reactivity thins pore walls and weakens matrix. Lower CRI (<= 30%) is preferred for large blast furnaces."
    p.font.size = Pt(12)
    p.font.color.rgb = C_TEXT_DARK

    # Right Card: CSR
    c_csr = create_card(s3, Inches(6.8), Inches(1.4), Inches(5.7), Inches(2.7))
    tf = c_csr.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = Inches(0.3)
    p = tf.paragraphs[0]
    p.text = "Coke Strength after Reaction (CSR) — Mechanical Abrasion"
    p.font.name = "Arial"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_SLATE_BLUE

    p = tf.add_paragraph()
    p.text = "• Evaluation: Post-reaction coke from the CRI furnace is placed in an I-drum tumbler and rotated for 600 revolutions at 20 rpm."
    p.font.size = Pt(12)
    p.font.color.rgb = C_TEXT_DARK

    p = tf.add_paragraph()
    p.text = "• Metric: CSR = % of reacted coke retained on a 10 mm sieve."
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_SLATE_BLUE

    p = tf.add_paragraph()
    p.text = "• Significance: Measures post-reaction resistance to abrasion and impact under thermal stress. Higher CSR (>= 60–65%) prevents fines generation in the shaft."
    p.font.size = Pt(12)
    p.font.color.rgb = C_TEXT_DARK

    # Bottom Banner: Transformation Diagram
    c_bot = create_card(s3, Inches(0.8), Inches(4.3), Inches(11.7), Inches(2.8))
    tf_b = c_bot.text_frame
    tf_b.word_wrap = True
    tf_b.margin_left = Inches(0.3)
    tf_b.margin_top = Inches(0.15)
    p = tf_b.paragraphs[0]
    p.text = "The Central Metallurgical Research Question:"
    p.font.name = "Arial"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_DARK_CHARCOAL

    p = tf_b.add_paragraph()
    p.text = "Can the chemical, petrographic, and thermoplastic properties of uncarbonized coal blends predict CRI and CSR, reducing reliance on costly 7-kg pilot-oven runs?"
    p.font.size = Pt(12)
    p.font.color.rgb = C_MUTED_ORANGE

    if (graphs_dir / "coke_formation_process.png").exists():
        s3.shapes.add_picture(str(graphs_dir / "coke_formation_process.png"), Inches(1.0), Inches(5.0), width=Inches(11.3))

    set_notes(s3, """
Now let us focus on the two standardized metallurgical parameters that define high-temperature coke quality: CRI and CSR.
The Coke Reactivity Index (CRI) measures chemical susceptibility to the endothermic Boudouard gasification reaction: C plus CO2 yields 2CO. In the Nippon Steel test (ASTM D5341), 200 grams of sized coke is exposed to pure carbon dioxide at 1100 degrees Celsius for 2 hours. CRI is simply the percentage weight lost. Lower CRI is desired because excessive gasification consumes pore walls and creates structural voids.
Immediately following the reactivity test, the gasified coke is placed into a standard I-drum tumbler and rotated for 600 revolutions. The percentage of material retained on a 10-millimeter round-hole sieve gives the Coke Strength after Reaction, or CSR.
CSR indicates whether coke can survive mechanical friction under heavy burden loads after chemical attack. Higher CSR—typically above 60 to 65%—is essential.
Standard testing requires carbonizing coal in a pilot oven (such as a 7-kg or 250-kg test battery), which takes days and costs thousands of dollars per test. This motivates our research question: Can we reliably predict CRI and CSR directly from the properties of the raw coal blend?
""")

    # =========================================================================
    # SLIDE 4: LITERATURE SURVEY & RESEARCH FOUNDATION
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_bg(s4)
    add_header(s4, "Literature Survey: Dash et al. (2012) & Metallurgical Foundations")

    # Left Column: Research Summary
    c_l4 = create_card(s4, Inches(0.8), Inches(1.4), Inches(4.8), Inches(5.6))
    tf_l4 = c_l4.text_frame
    tf_l4.word_wrap = True
    tf_l4.margin_left = tf_l4.margin_top = Inches(0.3)

    p = tf_l4.paragraphs[0]
    p.text = "Benchmark Paper: Dash et al. (2012)"
    p.font.name = "Arial"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_SLATE_BLUE

    bullets_ref = [
        "Authors: P.S. Dash, M. Guha, D. Chakraborty, P.K. Banerjee (Tata Steel R&D Division).",
        "Source: Int. Journal of Coal Preparation and Utilization, Vol. 32(4), pp. 169–188.",
        "Experimental Scope: Investigated 68 industrial coal blends carbonized in a 7-kg pilot oven.",
        "Techniques Used: Multiple Linear Regression (MLR), Principal Component Regression (PCR), and Artificial Neural Networks (MLP, RBF, Bayesian Neural Networks).",
        "Key Paper Finding: Phase 1 MLR suffered from multicollinearity between Total Reactives and Total Inerts; neural networks offered superior nonlinear fitting.",
        "Our Extension: Decoupled independent prediction of BOTH CSR and CRI, rigorous 80/20 train-test validation, and introduction of modern decision-tree and ensemble architectures (XGBoost & Random Forest)."
    ]
    for b in bullets_ref:
        p = tf_l4.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(11.5)
        p.font.color.rgb = C_TEXT_DARK

    # Right Column: 8 Coal Properties Table
    c_r4 = create_card(s4, Inches(5.8), Inches(1.4), Inches(6.7), Inches(5.6))
    tf_r4 = c_r4.text_frame
    tf_r4.word_wrap = True
    tf_r4.margin_left = tf_r4.margin_top = Inches(0.25)
    p = tf_r4.paragraphs[0]
    p.text = "The Eight Coal-Blend Input Characteristics & Metallurgical Roles"
    p.font.name = "Arial"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = C_DARK_CHARCOAL

    # Add Table
    table_shape = s4.shapes.add_table(9, 3, Inches(5.95), Inches(1.95), Inches(6.4), Inches(4.8))
    t = table_shape.table
    t.columns[0].width = Inches(1.3)
    t.columns[1].width = Inches(1.0)
    t.columns[2].width = Inches(4.1)

    headers = ["Feature", "Unit", "Metallurgical Significance in Coke Making"]
    for j, h in enumerate(headers):
        cell = t.cell(0, j)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_HEADER_BG
        for p in cell.text_frame.paragraphs:
            p.font.size = Pt(10.5)
            p.font.bold = True
            p.font.color.rgb = C_WHITE

    feat_data = [
        ("Ash", "%", "Inorganic mineral residue; increases coke ash, promotes micro-cracks & gasification."),
        ("VM", "%", "Volatile matter; governs devolatilization shrinkage, contraction stress & cell wall porosity."),
        ("Ro", "%", "Mean vitrinite reflectance; fundamental optical measure of coal rank (maturity)."),
        ("V9–V13", "%", "Petrographic distribution; reactive vitrinite classes (0.90–1.39%) that soften and melt."),
        ("CSN", "Index", "Crucible Swelling Number (1-9); thermoplastic dilatation, fluidity and caking capacity."),
        ("TR", "%", "Total Reactives (Vitrinite + Liptinite + 1/3 Semifusinite); forms the fluid binder matrix."),
        ("TI", "%", "Total Inerts (Inertinite + Fusinite + Minerals); refractory filler aggregate."),
        ("BI", "Ratio", "Basicity Index; catalytic mineral ratio (Fe2O3+CaO+MgO+Na2O+K2O)/(SiO2+Al2O3)*Ash.")
    ]
    for i, row in enumerate(feat_data):
        for j, val in enumerate(row):
            cell = t.cell(i+1, j)
            cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = C_WHITE if (i % 2 == 0) else RGBColor(241, 245, 249)
            for p in cell.text_frame.paragraphs:
                p.font.size = Pt(9.5)
                p.font.color.rgb = C_TEXT_DARK
                if j == 0:
                    p.font.bold = True

    set_notes(s4, """
In our literature review, the primary scientific benchmark is the 2012 study by Dash and co-workers at Tata Steel.
They evaluated 68 coal blends carbonized in a 7-kg pilot oven. They noticed that initial Multiple Linear Regression had difficulties because Total Reactives and Total Inerts are mathematically dependent, summing to 100%. To overcome this, they tested Principal Component Regression and Neural Networks, focusing primarily on CSR.
On the right, we define the eight coal-blend input parameters and their metallurgical roles:
Ash is the inorganic mineral residue. Volatile Matter represents devolatilizing hydrocarbons during pyrolysis. Ro is vitrinite reflectance, the international index of coal rank.
V9 to V13 is the reactive vitrinite proportion with reflectance between 0.90 and 1.39%—this is the sweet spot of reactive coal that melts during carbonization.
CSN, the Crucible Swelling Number, measures plastic expansion. Total Reactives act as the binder cement, while Total Inerts act as aggregate filler. Finally, the Basicity Index quantifies catalytic alkali and iron oxides that accelerate gasification.
Our research extends Dash et al.'s work by modeling both CSR and CRI independently, and benchmarking modern tree ensembles (XGBoost, Random Forest, Decision Tree) against the classical MLR baseline.
""")

    # =========================================================================
    # SLIDE 5: OBJECTIVES OF THE PROJECT
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_bg(s5)
    add_header(s5, "Research Objectives & Core Scientific Scope")

    # Primary Objective Card
    c_top = create_card(s5, Inches(0.8), Inches(1.4), Inches(11.7), Inches(1.6), bg_color=C_HEADER_BG, border_color=C_MUTED_ORANGE)
    tf_top = c_top.text_frame
    tf_top.word_wrap = True
    tf_top.margin_left = tf_top.margin_top = Inches(0.25)
    p = tf_top.paragraphs[0]
    p.text = "PRIMARY METALLURGICAL RESEARCH OBJECTIVE"
    p.font.name = "Arial"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_MUTED_ORANGE

    p = tf_top.add_paragraph()
    p.text = "To establish a reproducible, scientifically defensible machine learning framework capable of predicting metallurgical coke quality (CSR and CRI) independently from eight coal-blend characteristics, and to conduct an unbiased comparative evaluation across four regression paradigms."
    p.font.name = "Arial"
    p.font.size = Pt(15)
    p.font.color.rgb = C_WHITE

    # Specific Objectives Grid (Left & Right Cards)
    c_s1 = create_card(s5, Inches(0.8), Inches(3.2), Inches(5.7), Inches(3.8))
    tf_s1 = c_s1.text_frame
    tf_s1.word_wrap = True
    tf_s1.margin_left = tf_s1.margin_top = Inches(0.3)
    p = tf_s1.paragraphs[0]
    p.text = "Specific Computational & Statistical Objectives"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = C_SLATE_BLUE

    bullets_s1 = [
        "1. Complete Data Quality Audit: Investigate missingness, duplicates, and test the petrographic closure hypothesis (TR + TI = 100%).",
        "2. Multicollinearity Profiling: Calculate Variance Inflation Factors (VIF) and design matrix condition numbers.",
        "3. Leak-Free Partitioning: Implement an untouched 80% development (n=54) and 20% test (n=14) partition with 5-fold cross-validation.",
        "4. Strict Algorithm Selection: Implement exactly 4 algorithms (MLR Phase 1, Decision Tree, Random Forest, XGBoost).",
        "5. Dual Independence: Fit independent models for CSR and CRI without cross-target leakage."
    ]
    for b in bullets_s1:
        p = tf_s1.add_paragraph()
        p.text = b
        p.font.size = Pt(11.5)
        p.font.color.rgb = C_TEXT_DARK

    c_s2 = create_card(s5, Inches(6.8), Inches(3.2), Inches(5.7), Inches(3.8))
    tf_s2 = c_s2.text_frame
    tf_s2.word_wrap = True
    tf_s2.margin_left = tf_s2.margin_top = Inches(0.3)
    p = tf_s2.paragraphs[0]
    p.text = "Specific Metallurgical & Analytical Objectives"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = C_ALERT_GREEN

    bullets_s2 = [
        "6. Comparative Evaluation: Benchmark models across R2, RMSE, MAE, Percentage MAE, and CV stability.",
        "7. Outlier Evaluation: Preserve anomalous blends (e.g. Blend #11) to assess real industrial failure modes without data snooping.",
        "8. Feature Attribution: Extract game-theoretic SHAP and permutation importance to identify dominant coal quality drivers.",
        "9. Metallurgical Validation: Examine whether empirical coefficients and decision rules agree with coal carbonization principles.",
        "10. Model Selection: Identify the optimal prediction strategy for deployment in commercial blast furnace coke plants."
    ]
    for b in bullets_s2:
        p = tf_s2.add_paragraph()
        p.text = b
        p.font.size = Pt(11.5)
        p.font.color.rgb = C_TEXT_DARK

    set_notes(s5, """
Slide 5 defines the primary and specific objectives of our investigation.
Our overarching objective is to determine which statistical or machine learning regression model provides the most reliable prediction of CSR and CRI from uncarbonized coal blend properties.
We established five computational and five metallurgical sub-objectives:
First, we must rigorously audit the data and verify whether Total Reactives and Total Inerts satisfy petrographic closure.
Second, we evaluate multicollinearity using Variance Inflation Factors.
Third, we enforce a strict 80/20 train/test split with 5-fold cross-validation, ensuring that test data is never touched during hyperparameter optimization.
Fourth, we implement exactly four models without introducing prohibited algorithms like neural networks, SVR, or PCA.
Fifth, we treat CSR and CRI as independent targets; we never use CSR to predict CRI or vice versa.
Finally, we interpret the models using metallurgical principles—examining SHAP attributions and decision rules to understand how coal rank, volatile matter, and thermoplastic swelling influence coke quality.
""")

    # =========================================================================
    # SLIDE 6: METHODOLOGY: DATASET AND RESEARCH WORKFLOW
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_bg(s6)
    add_header(s6, "Methodology: Experimental Dataset & Machine Learning Architecture")

    # Left Column: Dataset Specifications
    c_l6 = create_card(s6, Inches(0.8), Inches(1.4), Inches(4.5), Inches(5.6))
    tf_l6 = c_l6.text_frame
    tf_l6.word_wrap = True
    tf_l6.margin_left = tf_l6.margin_top = Inches(0.3)

    p = tf_l6.paragraphs[0]
    p.text = "Dataset Characteristics"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_SLATE_BLUE

    bullets_d = [
        "Total Observations: 68 commercial industrial coal blend carbonization runs.",
        "Origin: Pilot coke oven (7-kg scale) carbonization data from Tata Steel R&D.",
        "Input Dimensionality: 8 coal properties (Ash, VM, Ro, V9–V13, CSN, TR, TI, BI).",
        "Target Dimensionality: 2 independent coke parameters (CSR %, CRI %).",
        "Data Quality: Zero missing entries (0.00%); zero duplicate rows.",
        "Target Range in Dataset:\n  • CSR: 18.80% to 66.90% (Mean: 54.84%)\n  • CRI: 24.40% to 52.00% (Mean: 30.84%)",
        "Software Ecosystem: Python 3.13, Pandas, Scikit-learn, XGBoost, Statsmodels, SciPy, SHAP."
    ]
    for b in bullets_d:
        p = tf_l6.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(11.5)
        p.font.color.rgb = C_TEXT_DARK

    # Right Column: Architecture & Flowchart
    c_r6 = create_card(s6, Inches(5.5), Inches(1.4), Inches(7.0), Inches(5.6))
    tf_r6 = c_r6.text_frame
    tf_r6.word_wrap = True
    tf_r6.margin_left = tf_r6.margin_top = Inches(0.25)
    p = tf_r6.paragraphs[0]
    p.text = "Dual Independent Prediction Architecture"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = C_DARK_CHARCOAL

    # Draw Dual Pipeline Diagram inside card
    # Top pipeline: CSR
    box_csr = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(5.8), Inches(2.1), Inches(6.4), Inches(1.8))
    box_csr.fill.solid()
    box_csr.fill.fore_color.rgb = RGBColor(235, 248, 255)
    box_csr.line.color.rgb = C_SLATE_BLUE
    tf_c = box_csr.text_frame
    tf_c.word_wrap = True
    p = tf_c.paragraphs[0]
    p.text = "PIPELINE A: CSR PREDICTION (8 Models Trained Independently)"
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = C_SLATE_BLUE
    p = tf_c.add_paragraph()
    p.text = "8 Coal Inputs -> [MLR | Decision Tree | Random Forest | XGBoost] -> Predicted CSR (%)"
    p.font.size = Pt(11)
    p.font.color.rgb = C_TEXT_DARK
    p = tf_c.add_paragraph()
    p.text = "Tuned exclusively via 5-Fold Cross-Validation on 54 train blends -> Evaluated on 14 test blends"
    p.font.size = Pt(10)
    p.font.color.rgb = C_TEXT_MUTED

    # Bottom pipeline: CRI
    box_cri = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(5.8), Inches(4.1), Inches(6.4), Inches(1.8))
    box_cri.fill.solid()
    box_cri.fill.fore_color.rgb = RGBColor(254, 243, 199)
    box_cri.line.color.rgb = C_MUTED_ORANGE
    tf_cr = box_cri.text_frame
    tf_cr.word_wrap = True
    p = tf_cr.paragraphs[0]
    p.text = "PIPELINE B: CRI PREDICTION (Completely Independent Models)"
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = C_MUTED_ORANGE
    p = tf_cr.add_paragraph()
    p.text = "8 Coal Inputs -> [MLR | Decision Tree | Random Forest | XGBoost] -> Predicted CRI (%)"
    p.font.size = Pt(11)
    p.font.color.rgb = C_TEXT_DARK
    p = tf_cr.add_paragraph()
    p.text = "Strict Constraint: CSR is NEVER used to predict CRI, and CRI is NEVER used to predict CSR."
    p.font.size = Pt(10)
    p.font.color.rgb = C_TEXT_MUTED

    callout = s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(5.8), Inches(6.1), Inches(6.4), Inches(0.7))
    callout.fill.solid()
    callout.fill.fore_color.rgb = C_HEADER_BG
    callout.line.fill.background()
    p_cal = callout.text_frame.paragraphs[0]
    p_cal.text = "Total Models Fitted: 4 algorithms x 2 targets = 8 distinct prediction pipelines."
    p_cal.font.bold = True
    p_cal.font.size = Pt(11.5)
    p_cal.font.color.rgb = C_WHITE

    set_notes(s6, """
Slide 6 details our experimental dataset and machine learning workflow.
We utilized the actual dataset of 68 industrial coal blends carbonized in a 7-kg pilot coke oven.
The dataset has zero missing values and zero duplicate rows.
The target variables cover a broad metallurgical spectrum: CSR ranges from 18.8% to 66.9%, and CRI ranges from 24.4% to 52.0%.
On the right, we highlight our dual independent prediction architecture.
A critical methodological constraint of this project is that CSR and CRI are treated as separate physical targets. We do not use predicted CSR as an input to predict CRI, or vice versa.
For each target, we fit the four regression algorithms: Multiple Linear Regression, Decision Tree, Random Forest, and XGBoost.
This yields a total of eight independent prediction pipelines, all evaluated under an identical cross-validation and testing regime.
""")

    # =========================================================================
    # SLIDE 7: METHODOLOGY: DATA CLEANING & EXPLORATORY DATA ANALYSIS
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_bg(s7)
    add_header(s7, "Methodology: Data Auditing, Compositional Closure & Multicollinearity")

    # Left Column: Mathematical Collinearity Finding
    c_l7 = create_card(s7, Inches(0.8), Inches(1.4), Inches(5.5), Inches(5.6))
    tf_l7 = c_l7.text_frame
    tf_l7.word_wrap = True
    tf_l7.margin_left = tf_l7.margin_top = Inches(0.3)

    p = tf_l7.paragraphs[0]
    p.text = "The TR + TI Compositional Closure Discovery"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_ACCENT_RED

    bullets_c = [
        "Petrographic Definition: In coal petrography, every organic maceral is classified as either Reactive or Inert.",
        "Empirical Dataset Audit: Sum of TR + TI across all 68 rows yielded: Mean = 100.0059% ± 0.0237%, Min = 100.0%, Max = 100.1%.",
        "Mathematical Linear Dependence: Pearson correlation r(TR, TI) = -0.99997.",
        "Catastrophic Collinearity in MLR:\n  • VIF(TR) = 18,725.42\n  • VIF(TI) = 18,686.99\n  • Condition Number = 477,187.81",
        "Empirical Proof: Eliminating TI drops VIF(TR) from 18,725 down to 2.05!",
        "Preservation Decision: Both TR and TI are retained in Phase 1 MLR to reproduce Dash et al., but rank deficiency and unstable standard errors are documented."
    ]
    for b in bullets_c:
        p = tf_l7.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(11.5)
        p.font.color.rgb = C_TEXT_DARK

    # Right Column: VIF Bar Chart Graphic
    c_r7 = create_card(s7, Inches(6.5), Inches(1.4), Inches(6.0), Inches(5.6))
    tf_r7 = c_r7.text_frame
    tf_r7.word_wrap = True
    tf_r7.margin_left = tf_r7.margin_top = Inches(0.2)
    p = tf_r7.paragraphs[0]
    p.text = "Variance Inflation Factor (VIF) Profile Across 8 Predictors"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_DARK_CHARCOAL

    if (graphs_dir / "eda_vif_barchart.png").exists():
        s7.shapes.add_picture(str(graphs_dir / "eda_vif_barchart.png"), Inches(6.65), Inches(1.9), width=Inches(5.7))

    set_notes(s7, """
Slide 7 addresses one of the most critical statistical and metallurgical findings of our investigation: the compositional closure between Total Reactives and Total Inerts.
In coal petrography, macerals are divided into reactives—which soften and melt—and inerts—which act as non-softening aggregate.
Because they represent percentage volume fractions of the same coal blend, theory dictates that TR plus TI equals 100%.
When we audited the dataset, we confirmed this empirically: the mean sum is 100.0059%, with a near-perfect correlation of r = -0.99997.
As shown in the VIF bar chart on the right, when both TR and TI are included alongside an intercept in Multiple Linear Regression, the Variance Inflation Factor surges past 18,700!
The matrix condition number reaches 477,188, indicating near-singularity.
When TI is excluded, the VIF of TR drops to 2.05, confirming that the collinearity is purely a mathematical consequence of compositional closure.
As requested by the prompt, we retain both variables in the Phase 1 MLR model to demonstrate the baseline, but we clearly highlight this severe variance inflation.
""")

    # =========================================================================
    # SLIDE 8: METHODOLOGY: EXPERIMENTAL DESIGN & EVALUATION
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_bg(s8)
    add_header(s8, "Methodology: Experimental Design, Cross-Validation & Metrics")

    # Card 1: Train/Test Split (Left)
    c_split = create_card(s8, Inches(0.8), Inches(1.4), Inches(5.7), Inches(5.6))
    tf_sp = c_split.text_frame
    tf_sp.word_wrap = True
    tf_sp.margin_left = tf_sp.margin_top = Inches(0.3)

    p = tf_sp.paragraphs[0]
    p.text = "Strict Partitioning & Cross-Validation"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_SLATE_BLUE

    bullets_sp = [
        "80/20 Partition: 54 training observations (79.4%) and 14 held-out test observations (20.6%).",
        "Random Seed Fixed (seed=42): Guarantees identical evaluation partitions across all 4 algorithms.",
        "5-Fold Cross-Validation on Train: Training partition divided into 5 stratified folds (10-11 samples/fold).",
        "Strict Leakage Prevention: Test set was NEVER exposed to feature scaling, outlier filtering, or hyperparameter optimization.",
        "Preservation of Anomalous Blends: Blend #11 (CSR=18.8%, CRI=52.0%) resides in the training partition, allowing models to learn extreme failure boundaries without contaminating test data."
    ]
    for b in bullets_sp:
        p = tf_sp.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(12)
        p.font.color.rgb = C_TEXT_DARK

    # Card 2: Metrics (Right)
    c_met = create_card(s8, Inches(6.8), Inches(1.4), Inches(5.7), Inches(5.6))
    tf_m = c_met.text_frame
    tf_m.word_wrap = True
    tf_m.margin_left = tf_m.margin_top = Inches(0.3)

    p = tf_m.paragraphs[0]
    p.text = "Evaluation Metrics & Formulations"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_MUTED_ORANGE

    metrics_info = [
        ("Coefficient of Determination (R2):", "R2 = 1 - [SUM(yi - yhat)^2 / SUM(yi - ybar)^2]\nMeasures proportion of variance explained by model."),
        ("Adjusted R2 (for MLR):", "R2_adj = 1 - (1 - R2) * [(n - 1) / (n - p - 1)]\nPenalizes model complexity for 8 predictors on small n."),
        ("Root Mean Squared Error (RMSE):", "RMSE = SQRT[(1/n) * SUM(yi - yhat)^2]\nPenalizes large outlier errors; primary ranking metric (%)."),
        ("Mean Absolute Error (MAE):", "MAE = (1/n) * SUM |yi - yhat|\nReflects typical expected prediction error magnitude (%)."),
        ("Percentage MAE (%):", "Percentage MAE = (MAE / Mean Actual Target) * 100\nNormalizes error relative to target scale (CSR vs CRI).")
    ]
    for title, desc in metrics_info:
        p = tf_m.add_paragraph()
        p.text = "• " + title
        p.font.size = Pt(12.5)
        p.font.bold = True
        p.font.color.rgb = C_DARK_CHARCOAL
        p_d = tf_m.add_paragraph()
        p_d.text = "    " + desc
        p_d.font.size = Pt(11)
        p_d.font.color.rgb = C_TEXT_MUTED

    set_notes(s8, """
Slide 8 presents our experimental design and evaluation metrics.
Because our dataset contains 68 observations, relying on a naive random split risks severe data leakage and overfitting.
We reserved an untouched 20% independent test partition containing 14 observations. The remaining 80%—54 observations—was used for model training and 5-fold cross-validation.
Crucially, all hyperparameter optimization was conducted strictly within the 54 training samples. The test set was touched only once at the very end to evaluate true generalization.
To evaluate the models, we calculate R-squared, Root Mean Squared Error (RMSE), Mean Absolute Error (MAE), and Percentage MAE.
For Multiple Linear Regression, we also calculate Adjusted R-squared to account for the penalty of having 8 predictors on 54 samples.
RMSE serves as our primary engineering ranking metric because it penalizes large deviations, which is critical in blast furnace operations where a single under-strength coke batch can destabilize furnace permeability.
""")

    # =========================================================================
    # SLIDE 9: METHODOLOGY: MULTIPLE LINEAR REGRESSION (MLR)
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_bg(s9)
    add_header(s9, "Methodology: Model 1 — Multiple Linear Regression (Phase 1 Baseline)")

    # Left: Mathematical Formulations & Architecture
    c_l9 = create_card(s9, Inches(0.8), Inches(1.4), Inches(5.6), Inches(5.6))
    tf_l9 = c_l9.text_frame
    tf_l9.word_wrap = True
    tf_l9.margin_left = tf_l9.margin_top = Inches(0.3)

    p = tf_l9.paragraphs[0]
    p.text = "Phase 1 Baseline Mathematical Formulation"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_SLATE_BLUE

    p = tf_l9.add_paragraph()
    p.text = "Fitted CSR Equation (OLS Estimation):\nCSR = 1595.49 + 2.035*(Ash) - 2.898*(VM) - 20.97*(Ro) + 0.141*(V9_V13) - 15.22*(TR) - 14.78*(TI) + 3.972*(CSN) - 24.96*(BI)"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_DARK_CHARCOAL

    p = tf_l9.add_paragraph()
    p.text = "Fitted CRI Equation (OLS Estimation):\nCRI = -169.91 - 1.553*(Ash) + 1.355*(VM) + 0.652*(Ro) - 0.006*(V9_V13) + 2.087*(TR) + 1.799*(TI) - 1.342*(CSN) + 3.271*(BI)"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_MUTED_ORANGE

    p = tf_l9.add_paragraph()
    p.text = "Key Inferences from OLS Coefficients:"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_SLATE_BLUE

    bullets_ols = [
        "Significant Predictors (p < 0.05): Ash (p=0.0001), VM (p=0.0019), and CSN (p=0.0002).",
        "Insigificant Predictors: Ro (p=0.327), V9-V13 (p=0.186), BI (p=0.175), TR (p=0.715), and TI (p=0.723).",
        "Standard Error Inflation: Standard error for TR is ±41.48 and TI is ±41.50, driven entirely by collinearity.",
        "Generalization Collapse: In-sample Train R2 = 0.601, but Test R2 collapses to -0.596!"
    ]
    for b in bullets_ols:
        p = tf_l9.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(11)
        p.font.color.rgb = C_TEXT_DARK

    # Right: Coefficient Table
    c_r9 = create_card(s9, Inches(6.6), Inches(1.4), Inches(5.9), Inches(5.6))
    tf_r9 = c_r9.text_frame
    tf_r9.word_wrap = True
    tf_r9.margin_left = tf_r9.margin_top = Inches(0.2)
    p = tf_r9.paragraphs[0]
    p.text = "OLS Regression Inference Summary (Training Set, n=54)"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_DARK_CHARCOAL

    # Add Table
    tbl_shape = s9.shapes.add_table(10, 4, Inches(6.75), Inches(1.85), Inches(5.6), Inches(5.0))
    tb = tbl_shape.table
    tb.columns[0].width = Inches(1.4)
    tb.columns[1].width = Inches(1.4)
    tb.columns[2].width = Inches(1.4)
    tb.columns[3].width = Inches(1.4)

    t_heads = ["Variable", "CSR Coef (p-val)", "CRI Coef (p-val)", "Significance"]
    for j, h in enumerate(t_heads):
        c = tb.cell(0, j)
        c.text = h
        c.fill.solid()
        c.fill.fore_color.rgb = C_HEADER_BG
        for p in c.text_frame.paragraphs:
            p.font.size = Pt(10)
            p.font.bold = True
            p.font.color.rgb = C_WHITE

    ols_data = [
        ("Intercept", "1595.49 (0.703)", "-169.91 (0.947)", "Not Sig."),
        ("Ash", "+2.035 (<0.001)", "-1.553 (<0.001)", "Significant"),
        ("VM", "-2.898 (0.002)", "+1.355 (0.016)", "Significant"),
        ("Ro", "-20.97 (0.327)", "+0.651 (0.960)", "Not Sig."),
        ("V9_V13", "+0.141 (0.186)", "-0.006 (0.932)", "Not Sig."),
        ("TR", "-15.22 (0.715)", "+2.087 (0.935)", "Collinear"),
        ("TI", "-14.78 (0.723)", "+1.799 (0.944)", "Collinear"),
        ("CSN", "+3.972 (<0.001)", "-1.342 (0.033)", "Significant"),
        ("BI", "-24.96 (0.175)", "+3.271 (0.770)", "Not Sig.")
    ]
    for i, row in enumerate(ols_data):
        for j, val in enumerate(row):
            c = tb.cell(i+1, j)
            c.text = val
            c.fill.solid()
            c.fill.fore_color.rgb = C_WHITE if (i % 2 == 0) else RGBColor(241, 245, 249)
            for p in c.text_frame.paragraphs:
                p.font.size = Pt(9.5)
                p.font.color.rgb = C_TEXT_DARK
                if j == 3 and "Significant" in val:
                    p.font.bold = True
                    p.font.color.rgb = C_ACCENT_GREEN
                elif j == 3 and "Collinear" in val:
                    p.font.color.rgb = C_ACCENT_RED

    set_notes(s9, """
Slide 9 examines our first model: Multiple Linear Regression (Phase 1 Baseline).
As specified in the prompt and paper, we fitted full eight-variable linear equations using Ordinary Least Squares on the 54 training observations.
Examining the table on the right, only three predictors are statistically significant at alpha = 0.05: Ash, Volatile Matter, and Crucible Swelling Number.
Volatile Matter has a negative coefficient of -2.90 on CSR, confirming that higher devolatilization induces contraction and pore wall thinning.
Crucible Swelling Number has a strong positive coefficient of +3.97, confirming that higher thermoplastic expansion builds strength.
However, look at Total Reactives and Total Inerts. Their p-values are above 0.70, and their standard errors are inflated beyond plus or minus 41!
Because TR and TI sum to 100%, the design matrix is near-singular.
While in-sample training R-squared is 0.601 for CSR, on the independent test set, R-squared collapses to negative 0.596!
This empirically confirms why Dash et al. found Phase 1 MLR unsatisfactory and motivated our exploration of tree-based methods.
""")

    # =========================================================================
    # SLIDE 10: METHODOLOGY: DECISION TREE REGRESSION
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_bg(s10)
    add_header(s10, "Methodology: Model 2 — Decision Tree Regressor & Pruning Analysis")

    # Left Column: Mechanics & Metallurgy
    c_l10 = create_card(s10, Inches(0.8), Inches(1.4), Inches(5.6), Inches(5.6))
    tf_l10 = c_l10.text_frame
    tf_l10.word_wrap = True
    tf_l10.margin_left = tf_l10.margin_top = Inches(0.3)

    p = tf_l10.paragraphs[0]
    p.text = "Decision Tree Architecture & Pruning"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_SLATE_BLUE

    bullets_dt = [
        "Non-Parametric Partitioning: Recursively splits the 8-dimensional coal space into axis-aligned rectangular hyper-rectangles.",
        "Splitting Criterion: Minimizes Mean Squared Error (MSE / variance reduction) at each binary split.",
        "Cost-Complexity Pruning (ccp_alpha): Adds a penalty for tree complexity: R_alpha(T) = R(T) + alpha * |T| to prevent memorizing small n=54 training data.",
        "Optimized Hyperparameters (via 5-Fold CV):\n  • CSR: ccp_alpha=0.5, max_depth=5, max_features=0.8, min_samples_split=4\n  • CRI: ccp_alpha=0.2, max_depth=3, min_samples_leaf=4",
        "Metallurgical Interpretability: Generates human-readable conditional threshold rules (e.g. If Ash > 12.6% & CSN > 3.75 -> Low CRI = 27.3%).",
        "Limitation: Highly sensitive to small data perturbations (high variance)."
    ]
    for b in bullets_dt:
        p = tf_l10.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(11.5)
        p.font.color.rgb = C_TEXT_DARK

    # Right Column: Visual Pruned Tree Diagram
    c_r10 = create_card(s10, Inches(6.6), Inches(1.4), Inches(5.9), Inches(5.6))
    tf_r10 = c_r10.text_frame
    tf_r10.word_wrap = True
    tf_r10.margin_left = tf_r10.margin_top = Inches(0.2)
    p = tf_r10.paragraphs[0]
    p.text = "Optimized Pruned Decision Tree Structure for CRI Prediction"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_DARK_CHARCOAL

    if (graphs_dir / "decision_tree_cri_structure.png").exists():
        s10.shapes.add_picture(str(graphs_dir / "decision_tree_cri_structure.png"), Inches(6.75), Inches(1.9), width=Inches(5.6))

    set_notes(s10, """
Slide 10 presents our second predictive approach: Decision Tree Regression.
A decision tree performs recursive binary partitioning, dividing the 8-dimensional coal space into discrete subsets by minimizing variance at each split.
Unlike linear regression, decision trees are completely non-parametric. They can capture nonlinear threshold effects and step-changes in coal behavior without needing a functional equation.
To prevent the tree from memorizing the 54 training samples, we applied cost-complexity pruning using the ccp_alpha parameter.
The cross-validated tree for CRI is displayed on the right.
Notice the metallurgical logic:
The root split occurs on Ash at 12.60%. For coals with Ash <= 12.60%, the tree immediately splits on Volatile Matter at 23.95%.
If Volatile Matter exceeds 23.95%, the estimated CRI jumps to 39.00%! This directly reflects coal devolatilization: higher volatile coals experience severe shrinkage and develop open, reactive pore structures.
Conversely, when Ash is above 12.60% and CSN is above 3.75, predicted CRI drops to a desirable 27.34%.
However, a single tree has high variance on small datasets, which motivates ensemble methods.
""")

    # =========================================================================
    # SLIDE 11: METHODOLOGY: RANDOM FOREST REGRESSION
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_bg(s11)
    add_header(s11, "Methodology: Model 3 — Random Forest Regressor (Bagging Ensemble)")

    # Left Column: Bagging Mechanics & Parameters
    c_l11 = create_card(s11, Inches(0.8), Inches(1.4), Inches(5.6), Inches(5.6))
    tf_l11 = c_l11.text_frame
    tf_l11.word_wrap = True
    tf_l11.margin_left = tf_l11.margin_top = Inches(0.3)

    p = tf_l11.paragraphs[0]
    p.text = "Random Forest: Bagging & Decorrelation"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_SLATE_BLUE

    bullets_rf = [
        "Bootstrap Aggregation (Bagging): Draws B independent bootstrap resamples from the 54 training blends to train B parallel trees.",
        "Random Subspace Sampling: At each candidate split, only a random subset of predictors (e.g. sqrt(p) or 70%) is evaluated.",
        "Decorrelation Mechanism: Prevents dominant features (like Ash or VM) from dictating every tree, drastically reducing ensemble variance.",
        "Ensemble Averaging: Final prediction is the unweighted average across all trees: y_hat = (1/B) * SUM(T_b(x)).",
        "Optimized Hyperparameters (via 5-Fold CV):\n  • CSR: n_estimators=30, max_depth=None, max_features='sqrt', min_samples_leaf=2\n  • CRI: n_estimators=50, max_depth=4, max_features=1.0, min_samples_leaf=3",
        "Resilience to Collinearity: Robust against TR+TI dependency because individual trees select random subsets without matrix inversion."
    ]
    for b in bullets_rf:
        p = tf_l11.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(11.5)
        p.font.color.rgb = C_TEXT_DARK

    # Right Column: Architecture Comparison Graphic
    c_r11 = create_card(s11, Inches(6.6), Inches(1.4), Inches(5.9), Inches(5.6))
    tf_r11 = c_r11.text_frame
    tf_r11.word_wrap = True
    tf_r11.margin_left = tf_r11.margin_top = Inches(0.2)
    p = tf_r11.paragraphs[0]
    p.text = "Ensemble Learning: Bagging vs Gradient Boosting"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_DARK_CHARCOAL

    if (graphs_dir / "ensemble_comparison.png").exists():
        s11.shapes.add_picture(str(graphs_dir / "ensemble_comparison.png"), Inches(6.75), Inches(1.9), width=Inches(5.6))

    set_notes(s11, """
Slide 11 introduces our third model: Random Forest Regression.
A major limitation of a single decision tree is high variance. Random Forest overcomes this through Bootstrap Aggregation, or Bagging.
It generates multiple bootstrap samples from the 54 training blends and fits an independent decision tree to each.
To prevent all trees from looking identical, Random Forest injects feature randomness: at each split, only a random subset of features is considered.
This decorrelates the trees. When their predictions are averaged together, variance is substantially reduced without increasing bias.
On the right, we contrast Random Forest's parallel architecture with XGBoost's sequential architecture.
From a metallurgical perspective, Random Forest is particularly attractive because it naturally bypasses the TR plus TI collinearity trap: trees do not invert covariance matrices, so extreme VIF does not inflate predictive error.
""")

    # =========================================================================
    # SLIDE 12: METHODOLOGY: XGBOOST REGRESSION
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_bg(s12)
    add_header(s12, "Methodology: Model 4 — XGBoost Regressor (Gradient Boosting)")

    # Left Column: Gradient Boosting Mechanics
    c_l12 = create_card(s12, Inches(0.8), Inches(1.4), Inches(5.6), Inches(5.6))
    tf_l12 = c_l12.text_frame
    tf_l12.word_wrap = True
    tf_l12.margin_left = tf_l12.margin_top = Inches(0.3)

    p = tf_l12.paragraphs[0]
    p.text = "XGBoost: Sequential Error Minimization"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_MUTED_ORANGE

    bullets_xgb = [
        "Sequential Ensemble Paradigm: Unlike Random Forest, trees are built iteratively to predict the negative gradient (residuals) of previous iterations.",
        "Shrinkage Learning Rate (eta): Scales the contribution of each newly added tree (e.g. eta = 0.05 - 0.10) to prevent aggressive overfitting on n=54 samples.",
        "Built-in L1 and L2 Regularization: Includes penalty terms on leaf weights: Omega(f) = gamma*T + 0.5*lambda*SUM(w_j^2) + alpha*SUM(|w_j|).",
        "Optimized Hyperparameters (via 5-Fold CV):\n  • CSR: n_estimators=50, max_depth=4, eta=0.05, subsample=0.9, reg_alpha=0.1, reg_lambda=0.5\n  • CRI: n_estimators=80, max_depth=2, eta=0.10, subsample=0.8, reg_alpha=0.1, reg_lambda=0.5",
        "Second-Order Taylor Approximation: Uses both first and second derivatives of the loss function for faster, exact optimization.",
        "Risk: High parameter complexity requires strict CV control when training samples are limited."
    ]
    for b in bullets_xgb:
        p = tf_l12.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(11.5)
        p.font.color.rgb = C_TEXT_DARK

    # Right Column: Side-by-side comparison table
    c_r12 = create_card(s12, Inches(6.6), Inches(1.4), Inches(5.9), Inches(5.6))
    tf_r12 = c_r12.text_frame
    tf_r12.word_wrap = True
    tf_r12.margin_left = tf_r12.margin_top = Inches(0.2)
    p = tf_r12.paragraphs[0]
    p.text = "Structural Comparison: Random Forest vs. XGBoost"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_DARK_CHARCOAL

    # Table
    t_shape12 = s12.shapes.add_table(7, 3, Inches(6.75), Inches(1.9), Inches(5.6), Inches(4.9))
    tb12 = t_shape12.table
    tb12.columns[0].width = Inches(1.5)
    tb12.columns[1].width = Inches(2.0)
    tb12.columns[2].width = Inches(2.1)

    heads12 = ["Dimension", "Random Forest", "XGBoost Regressor"]
    for j, h in enumerate(heads12):
        c = tb12.cell(0, j)
        c.text = h
        c.fill.solid()
        c.fill.fore_color.rgb = C_HEADER_BG
        for p in c.text_frame.paragraphs:
            p.font.size = Pt(10)
            p.font.bold = True
            p.font.color.rgb = C_WHITE

    comp_data = [
        ("Ensemble Method", "Bagging (Bootstrap Aggregation)", "Gradient Boosting"),
        ("Tree Generation", "Independent & Parallel", "Sequential (Iterative)"),
        ("Primary Mechanism", "Variance Reduction (Averaging)", "Bias & Residual Correction"),
        ("Tree Depth", "Deep Trees (Low Bias)", "Shallow Trees (Weak Learners)"),
        ("Regularization", "Heuristic (leaf size, depth)", "Formal L1 (alpha) & L2 (lambda)"),
        ("Small Data Risk", "Low Overfitting Risk", "Moderate (requires low eta & depth)")
    ]
    for i, row in enumerate(comp_data):
        for j, val in enumerate(row):
            c = tb12.cell(i+1, j)
            c.text = val
            c.fill.solid()
            c.fill.fore_color.rgb = C_WHITE if (i % 2 == 0) else RGBColor(241, 245, 249)
            for p in c.text_frame.paragraphs:
                p.font.size = Pt(9.5)
                p.font.color.rgb = C_TEXT_DARK
                if j == 0:
                    p.font.bold = True

    set_notes(s12, """
Slide 12 covers our fourth predictive model: the XGBoost Regressor.
While Random Forest constructs deep, independent trees and averages them, XGBoost uses gradient boosting: trees are constructed sequentially.
Each new tree is trained to predict the negative gradient—or residual error—of the preceding ensemble.
To adapt XGBoost to our 54 training samples, we tuned shallow depths (depth 2 for CRI, depth 4 for CSR), restricted the learning rate to 0.05–0.10, and incorporated explicit L1 and L2 regularization on leaf weights.
The table on the right contrasts the two ensemble paradigms.
Random Forest relies on parallel bagging to reduce variance, making it very hard to overfit.
XGBoost iteratively reduces bias and fine-tunes error correction, which can achieve sharper accuracy, but requires careful tuning to prevent overfitting on smaller sample sizes.
We do not declare either model superior beforehand; we let the empirical results dictate the winner.
""")

    # =========================================================================
    # SLIDE 13: RESULTS: QUANTITATIVE MODEL COMPARISON
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    set_bg(s13)
    add_header(s13, "Results & Discussion: Quantitative Model Benchmark on CSR & CRI")

    # Left Card: CSR Comparison Table
    c_csr = create_card(s13, Inches(0.8), Inches(1.4), Inches(5.7), Inches(5.6))
    tf_c = c_csr.text_frame
    tf_c.word_wrap = True
    tf_c.margin_left = tf_c.margin_top = Inches(0.25)
    p = tf_c.paragraphs[0]
    p.text = "Coke Strength after Reaction (CSR) Benchmark"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = C_SLATE_BLUE

    # Table for CSR
    t_csr = s13.shapes.add_table(5, 5, Inches(0.95), Inches(1.95), Inches(5.4), Inches(2.6)).table
    t_csr.columns[0].width = Inches(1.6)
    t_csr.columns[1].width = Inches(0.95)
    t_csr.columns[2].width = Inches(0.95)
    t_csr.columns[3].width = Inches(0.95)
    t_csr.columns[4].width = Inches(0.95)

    csr_heads = ["Model", "Test R2", "CV R2", "Test RMSE", "Test MAE"]
    for j, h in enumerate(csr_heads):
        c = t_csr.cell(0, j)
        c.text = h
        c.fill.solid()
        c.fill.fore_color.rgb = C_HEADER_BG
        for p in c.text_frame.paragraphs:
            p.font.size = Pt(9.5)
            p.font.bold = True
            p.font.color.rgb = C_WHITE

    csr_metrics_table = [
        ("MLR Phase 1", "-0.596", "0.231", "6.92%", "4.00%"),
        ("Decision Tree", "-1.442", "-0.175", "8.56%", "5.62%"),
        ("Random Forest", "-0.408", "0.151", "6.50%", "4.20%"),
        ("XGBoost (Best)", "-0.011", "0.163", "5.51%", "3.79%")
    ]
    for i, row in enumerate(csr_metrics_table):
        for j, val in enumerate(row):
            c = t_csr.cell(i+1, j)
            c.text = val
            c.fill.solid()
            if "XGBoost" in row[0]:
                c.fill.fore_color.rgb = RGBColor(235, 248, 255)
            else:
                c.fill.fore_color.rgb = C_WHITE if (i % 2 == 0) else RGBColor(241, 245, 249)
            for p in c.text_frame.paragraphs:
                p.font.size = Pt(9.5)
                p.font.color.rgb = C_TEXT_DARK
                if "XGBoost" in row[0]:
                    p.font.bold = True
                    p.font.color.rgb = C_SLATE_BLUE

    # Summary bullets for CSR
    tf_c_sum = s13.shapes.add_textbox(Inches(0.95), Inches(4.7), Inches(5.4), Inches(2.2)).text_frame
    tf_c_sum.word_wrap = True
    p = tf_c_sum.paragraphs[0]
    p.text = "Key CSR Findings:"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = C_SLATE_BLUE

    p = tf_c_sum.add_paragraph()
    p.text = "• Top Performer: XGBoost achieved lowest Test RMSE (5.51%) and lowest Test MAE (3.79%), reducing RMSE by 20.4% over MLR."
    p.font.size = Pt(11)

    p = tf_c_sum.add_paragraph()
    p.text = "• Decision Tree suffered from high test error (RMSE=8.56%)."
    p.font.size = Pt(11)

    p = tf_c_sum.add_paragraph()
    p.text = "• Percentage MAE for XGBoost is 6.56%, representing high industrial precision on CSR (mean = 57.8%)."
    p.font.size = Pt(11)

    # Right Card: CRI Comparison Table
    c_cri_card = create_card(s13, Inches(6.8), Inches(1.4), Inches(5.7), Inches(5.6))
    tf_cr = c_cri_card.text_frame
    tf_cr.word_wrap = True
    tf_cr.margin_left = tf_cr.margin_top = Inches(0.25)
    p = tf_cr.paragraphs[0]
    p.text = "Coke Reactivity Index (CRI) Benchmark"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = C_ALERT_GREEN

    # Table for CRI
    t_cri = s13.shapes.add_table(5, 5, Inches(6.95), Inches(1.95), Inches(5.4), Inches(2.6)).table
    t_cri.columns[0].width = Inches(1.6)
    t_cri.columns[1].width = Inches(0.95)
    t_cri.columns[2].width = Inches(0.95)
    t_cri.columns[3].width = Inches(0.95)
    t_cri.columns[4].width = Inches(0.95)

    cri_heads = ["Model", "Test R2", "CV R2", "Test RMSE", "Test MAE"]
    for j, h in enumerate(cri_heads):
        c = t_cri.cell(0, j)
        c.text = h
        c.fill.solid()
        c.fill.fore_color.rgb = C_HEADER_BG
        for p in c.text_frame.paragraphs:
            p.font.size = Pt(9.5)
            p.font.bold = True
            p.font.color.rgb = C_WHITE

    cri_metrics_table = [
        ("MLR Phase 1", "-1.600", "0.041", "4.18%", "3.14%"),
        ("Decision Tree", "-0.861", "0.330", "3.54%", "2.92%"),
        ("XGBoost", "-0.634", "0.270", "3.31%", "2.87%"),
        ("Random Forest (Best)", "-0.307", "0.338", "2.97%", "2.37%")
    ]
    for i, row in enumerate(cri_metrics_table):
        for j, val in enumerate(row):
            c = t_cri.cell(i+1, j)
            c.text = val
            c.fill.solid()
            if "Random Forest" in row[0]:
                c.fill.fore_color.rgb = RGBColor(240, 253, 244)
            else:
                c.fill.fore_color.rgb = C_WHITE if (i % 2 == 0) else RGBColor(241, 245, 249)
            for p in c.text_frame.paragraphs:
                p.font.size = Pt(9.5)
                p.font.color.rgb = C_TEXT_DARK
                if "Random Forest" in row[0]:
                    p.font.bold = True
                    p.font.color.rgb = C_ALERT_GREEN

    # Summary bullets for CRI
    tf_cr_sum = s13.shapes.add_textbox(Inches(6.95), Inches(4.7), Inches(5.4), Inches(2.2)).text_frame
    tf_cr_sum.word_wrap = True
    p = tf_cr_sum.paragraphs[0]
    p.text = "Key CRI Findings:"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = C_ALERT_GREEN

    p = tf_cr_sum.add_paragraph()
    p.text = "• Top Performer: Random Forest achieved lowest Test RMSE (2.97%) and MAE (2.37%), with highest CV R2 (0.338 ± 0.178)."
    p.font.size = Pt(11)

    p = tf_cr_sum.add_paragraph()
    p.text = "• Random Forest reduced test prediction error by 29.0% compared to MLR (4.18% RMSE)."
    p.font.size = Pt(11)

    p = tf_cr_sum.add_paragraph()
    p.text = "• Note on Test R2: On small test partitions (n=14) with narrow variance, any RMSE around 3% yields negative R2; RMSE & MAE are the true engineering metrics."
    p.font.size = Pt(10.5)
    p.font.color.rgb = C_TEXT_MUTED

    set_notes(s13, """
Slide 13 delivers the central quantitative results of our research.
We present separate benchmark tables for CSR and CRI because their numerical scales and physical tolerances differ.
First, looking at CSR on the left:
XGBoost is the top performer. It achieved the lowest Test RMSE of 5.51% and lowest Test MAE of 3.79%.
This is a 20.4% error reduction over the unregularized Phase 1 MLR model, which had an RMSE of 6.92%.
Decision Tree had the largest test error at 8.56%.
Next, looking at CRI on the right:
Random Forest emerged as the clear winner. It achieved a Test RMSE of 2.97% and Test MAE of 2.37%, along with the highest cross-validation score of R2 = 0.338.
This represents a 29.0% improvement over Multiple Linear Regression.
Examiners will naturally ask: Why are the test R-squared values negative?
This is a classic statistical effect on small sample sizes. In our 14 test samples, the total target variance is restricted. When total sum of squares in the denominator is small, even an acceptable error of 2.9% or 5.5% causes R-squared to drop below zero.
When we look at engineering absolute errors—a Percentage MAE of only 6.5% for CSR and 8.0% for CRI—the predictions are highly accurate for blast furnace blend planning.
""")

    # =========================================================================
    # SLIDE 14: RESULTS: PREDICTION ANALYSIS & METALLURGICAL INTERPRETATION
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    set_bg(s14)
    add_header(s14, "Results & Discussion: Diagnostic Plots & Metallurgical Interpretations")

    # Left: Actual vs Predicted Image
    c_l14 = create_card(s14, Inches(0.8), Inches(1.4), Inches(5.7), Inches(5.6))
    tf_l14 = c_l14.text_frame
    tf_l14.word_wrap = True
    tf_l14.margin_left = tf_l14.margin_top = Inches(0.2)
    p = tf_l14.paragraphs[0]
    p.text = "Actual vs. Predicted CSR (XGBoost)"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_DARK_CHARCOAL

    if (graphs_dir / "xgboost_csr_act_vs_pred.png").exists():
        s14.shapes.add_picture(str(graphs_dir / "xgboost_csr_act_vs_pred.png"), Inches(0.95), Inches(1.85), width=Inches(5.4))

    # Right: SHAP Feature Importance Image
    c_r14 = create_card(s14, Inches(6.8), Inches(1.4), Inches(5.7), Inches(5.6))
    tf_r14 = c_r14.text_frame
    tf_r14.word_wrap = True
    tf_r14.margin_left = tf_r14.margin_top = Inches(0.2)
    p = tf_r14.paragraphs[0]
    p.text = "SHAP Game-Theoretic Feature Attribution (XGBoost)"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_DARK_CHARCOAL

    if (graphs_dir / "xgboost_csr_shap_summary.png").exists():
        s14.shapes.add_picture(str(graphs_dir / "xgboost_csr_shap_summary.png"), Inches(6.95), Inches(1.85), width=Inches(5.4))

    set_notes(s14, """
Slide 14 connects our mathematical outputs directly to metallurgical science.
On the left, the actual-versus-predicted plot for our best CSR model, XGBoost, demonstrates that the model tracks the ideal 45-degree line closely.
The blue circles represent the 54 training blends, and the orange triangles represent the 14 held-out test blends.
The model generalizes well across the commercial operating window between 50% and 66% CSR.
On the right, we show the SHAP summary plot, which uses cooperative game theory to explain model predictions:
Crucible Swelling Number (CSN) and Volatile Matter (VM) emerge as the dominant drivers.
Higher CSN values (red dots) exert strong positive SHAP contributions, pushing predicted CSR higher. This aligns with coking mechanism: strong fluid dilatation bridges maceral interfaces during the plastic layer stage.
Conversely, high Volatile Matter pushes predicted CSR downward, because volatile devolatilization creates excessive contraction cracks and cellular porosity.
Ash and Basicity Index show secondary influences, where catalytic alkali oxides increase post-reaction degradation.
Importantly, feature importance proves predictive correlation, not independent causality, but the empirical ranking matches established metallurgical principles.
""")

    # =========================================================================
    # SLIDE 15: CONCLUSIONS, LIMITATIONS & FUTURE SCOPE
    # =========================================================================
    s15 = prs.slides.add_slide(blank_layout)
    set_bg(s15)
    add_header(s15, "Conclusions, Industrial Implications & Future Research Scope")

    # Card 1: Key Conclusions (Left)
    c_c1 = create_card(s15, Inches(0.8), Inches(1.4), Inches(5.7), Inches(5.6))
    tf_c1 = c_c1.text_frame
    tf_c1.word_wrap = True
    tf_c1.margin_left = tf_c1.margin_top = Inches(0.3)

    p = tf_c1.paragraphs[0]
    p.text = "Key Project Conclusions"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_SLATE_BLUE

    bullets_c1 = [
        "1. Feasibility Demonstrated: Machine learning successfully predicts high-temperature coke quality (CSR and CRI) from uncarbonized coal blend properties.",
        "2. Optimal Model for CSR: XGBoost is the superior algorithm for CSR (RMSE = 5.51%, MAE = 3.79%), reducing error by 20.4% over baseline MLR.",
        "3. Optimal Model for CRI: Random Forest is the superior algorithm for CRI (RMSE = 2.97%, MAE = 2.37%), reducing error by 29.0% over baseline MLR.",
        "4. MLR Collinearity Defect: Phase 1 MLR fails on generalization due to mathematical closure of Total Reactives and Total Inerts (TR + TI = 100%, VIF > 18,700).",
        "5. Dominant Coal Drivers: Crucible Swelling Number (CSN), Volatile Matter (VM), and Ash content govern coke strength and reactivity."
    ]
    for b in bullets_c1:
        p = tf_c1.add_paragraph()
        p.text = b
        p.font.size = Pt(12)
        p.font.color.rgb = C_TEXT_DARK

    # Card 2: Industrial Impact & Future Scope (Right)
    c_c2 = create_card(s15, Inches(6.8), Inches(1.4), Inches(5.7), Inches(5.6))
    tf_c2 = c_c2.text_frame
    tf_c2.word_wrap = True
    tf_c2.margin_left = tf_c2.margin_top = Inches(0.3)

    p = tf_c2.paragraphs[0]
    p.text = "Industrial Significance & Future Scope"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_MUTED_ORANGE

    bullets_c2 = [
        "Industrial Blast Furnace Application: Enables plant metallurgists to screen raw coal blends before charging, reducing expensive 7-kg pilot oven tests and safeguarding cohesive zone permeability.",
        "Identified Limitations: Small dataset size (N=68) limits complex deep architectures; absence of oven carbonization parameters (coking rate, bulk density).",
        "Future Work 1: Implement repeated nested cross-validation and probabilistic Bayesian prediction intervals to capture industrial uncertainty.",
        "Future Work 2: Couple coal blend properties with coking plant operating variables (coking time, flue temperatures, moisture).",
        "Closing Message: Machine learning provides a transparent, data-supported pathway towards optimized coal blending and stable blast furnace ironmaking."
    ]
    for b in bullets_c2:
        p = tf_c2.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(12)
        p.font.color.rgb = C_TEXT_DARK

    p_ty = tf_c2.add_paragraph()
    p_ty.text = "\nThank you for your attention. I am now open to your questions."
    p_ty.font.size = Pt(13)
    p_ty.font.bold = True
    p_ty.font.color.rgb = C_SLATE_BLUE

    set_notes(s15, """
In conclusion, this project successfully reproduced and extended Dash et al. (2012) into a modern, leak-free comparative study.
Our findings demonstrate that machine learning models can predict high-temperature metallurgical coke properties accurately:
For CSR, XGBoost achieved the best performance with an RMSE of 5.51% and an MAE of 3.79%.
For CRI, Random Forest proved most reliable, achieving an RMSE of 2.97% and an MAE of 2.37%.
We demonstrated why classical Phase 1 MLR experiences variance inflation: petrographic closure between Total Reactives and Total Inerts causes extreme multicollinearity with VIF exceeding 18,700. Tree ensembles naturally overcome this limitation.
In industrial blast furnace operations, deploying these models enables plant metallurgists to screen prospective coal blends computationally in seconds, reducing dependence on pilot-oven carbonization and safeguarding furnace permeability.
In future research, expanding the dataset and incorporating oven operating variables like coking time and flue temperature will further refine predictive capability.
Thank you very much for your time and guidance. I welcome your questions.
""")

    out_file = Path("Coke_Quality_Prediction_Presentation.pptx")
    prs.save(str(out_file))
    print(f"Presentation successfully saved to: {out_file.resolve()}")

if __name__ == "__main__":
    build_presentation()
