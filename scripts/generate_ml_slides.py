"""
Clean, Readable, Student-Authored Presentation Slides (.pptx)
No AI Slop / Buzzwords - Natural Indonesian Computer Science Student Tone.
Aspect Ratio: 16:9 Widescreen (13.333 x 7.5 inches).
High Legibility: 14-16pt Body, 16-18pt Headings, 38-42pt Stats.
Monochrome Minimalist: Obsidian Black, Slate Grey, Pure White.
Upgraded Methodology:
- Binary Classification (Dropout vs Graduate - 3,630 instances)
- 794 Enrolled instances allocated to active student monitoring simulation pool
- 3-Way Splitting (Train 70% : Validation 15% : Test 15%)
- Dual Preprocessing Pipeline (Decision Tree: unscaled, KNN: StandardScaler)
"""

import os
from typing import Any

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt


def create_proposal_presentation(output_path: str) -> None:
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Clean High-Contrast Palette
    C_OBSIDIAN = RGBColor(15, 23, 42)  # #0F172A Dark Ink
    C_SURFACE_DARK = RGBColor(30, 41, 59)  # #1E293B Dark Slate Card
    C_BORDER_DARK = RGBColor(51, 65, 85)  # #334155 Dark Border
    C_TEXT_LIGHT = RGBColor(248, 250, 252)  # #F8FAFC Crisp White
    C_MUTED_LIGHT = RGBColor(148, 163, 184)  # #94A3B8 Soft Slate

    C_BG_PAGE = RGBColor(248, 250, 252)  # Clean Off-White
    C_CARD_BG = RGBColor(255, 255, 255)  # Pure White
    C_BORDER = RGBColor(226, 232, 240)  # Subtle Line
    C_INK = RGBColor(15, 23, 42)  # Pitch Black Text
    C_BODY = RGBColor(51, 65, 85)  # Charcoal Body Text
    C_SLATE = RGBColor(100, 116, 139)  # Secondary Slate

    def set_notes(slide: Any, text: str) -> None:
        notes_slide = slide.notes_slide
        tf = getattr(notes_slide, "notes_text_frame", None)
        if tf is not None:
            tf.text = text

    def set_slide_bg(slide: Any, color: RGBColor) -> None:
        bg = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5)
        )
        bg.fill.solid()
        bg.fill.fore_color.rgb = color
        bg.line.fill.background()

    def add_top_nav(
        slide: Any, title_text: str, badge_text: str = "PROYEK AKHIR MACHINE LEARNING"
    ) -> None:
        badge = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(0.8),
            Inches(0.45),
            Inches(3.2),
            Inches(0.32),
        )
        badge.fill.solid()
        badge.fill.fore_color.rgb = C_INK
        badge.line.fill.background()
        tf_b = badge.text_frame
        tf_b.margin_top = Inches(0.04)
        p_b = tf_b.paragraphs[0]
        p_b.text = badge_text.upper()
        p_b.alignment = PP_ALIGN.CENTER
        p_b.font.name = "Arial"
        p_b.font.size = Pt(9)
        p_b.font.bold = True
        p_b.font.color.rgb = C_TEXT_LIGHT

        t_box = slide.shapes.add_textbox(
            Inches(0.8), Inches(0.85), Inches(11.733), Inches(0.65)
        )
        tf_t = t_box.text_frame
        tf_t.word_wrap = True
        tf_t.margin_left = tf_t.margin_top = tf_t.margin_right = tf_t.margin_bottom = 0
        p_t = tf_t.paragraphs[0]
        p_t.text = title_text
        p_t.font.name = "Arial"
        p_t.font.size = Pt(22)
        p_t.font.bold = True
        p_t.font.color.rgb = C_INK

        rule = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.58), Inches(11.733), Inches(0.02)
        )
        rule.fill.solid()
        rule.fill.fore_color.rgb = C_BORDER
        rule.line.fill.background()

    def add_metric_callout(
        slide: Any,
        left: float,
        top: float,
        width: float,
        height: float,
        big_num: str,
        label: str,
        desc: str,
        dark_theme: bool = False,
    ) -> None:
        card = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(left),
            Inches(top),
            Inches(width),
            Inches(height),
        )
        card.fill.solid()
        card.fill.fore_color.rgb = C_SURFACE_DARK if dark_theme else C_CARD_BG
        card.line.color.rgb = C_BORDER_DARK if dark_theme else C_BORDER
        card.line.width = Pt(1.5)

        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = Inches(0.3)
        tf.margin_top = Inches(0.2)
        tf.margin_bottom = Inches(0.2)

        p0 = tf.paragraphs[0]
        p0.text = big_num
        p0.font.name = "Arial Black"
        p0.font.size = Pt(38)
        p0.font.bold = True
        p0.font.color.rgb = C_TEXT_LIGHT if dark_theme else C_INK
        p0.space_after = Pt(2)

        p1 = tf.add_paragraph()
        p1.text = label
        p1.font.name = "Arial"
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = C_MUTED_LIGHT if dark_theme else C_INK
        p1.space_after = Pt(4)

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.name = "Arial"
        p2.font.size = Pt(11)
        p2.font.color.rgb = C_MUTED_LIGHT if dark_theme else C_SLATE

    # ==================== SLIDE 1: COVER SLIDE (DARK HERO) ====================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s1, C_OBSIDIAN)

    badge1 = s1.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(0.8),
        Inches(0.9),
        Inches(3.6),
        Inches(0.35),
    )
    badge1.fill.solid()
    badge1.fill.fore_color.rgb = C_SURFACE_DARK
    badge1.line.color.rgb = C_BORDER_DARK
    tf_b1 = badge1.text_frame
    tf_b1.margin_top = Inches(0.05)
    pb1 = tf_b1.paragraphs[0]
    pb1.text = "PROPOSAL PROYEK AKHIR MACHINE LEARNING"
    pb1.font.name = "Arial"
    pb1.font.size = Pt(9)
    pb1.font.bold = True
    pb1.font.color.rgb = C_TEXT_LIGHT
    pb1.alignment = PP_ALIGN.CENTER

    t_box1 = s1.shapes.add_textbox(
        Inches(0.8), Inches(1.45), Inches(11.733), Inches(2.2)
    )
    tf1 = t_box1.text_frame
    tf1.word_wrap = True
    p1 = tf1.paragraphs[0]
    p1.text = "Prediksi Kelulusan & Deteksi Dini\nMahasiswa Putus Studi (Dropout)"
    p1.font.name = "Arial Black"
    p1.font.size = Pt(34)
    p1.font.bold = True
    p1.font.color.rgb = C_TEXT_LIGHT
    p1.space_after = Pt(12)

    p1_sub = tf1.add_paragraph()
    p1_sub.text = (
        "Klasifikasi Biner Komparatif: Decision Tree vs K-Nearest Neighbors (KNN)"
    )
    p1_sub.font.name = "Arial"
    p1_sub.font.size = Pt(16)
    p1_sub.font.color.rgb = C_MUTED_LIGHT

    # Two Bottom Cards
    c_team = s1.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.1), Inches(6.8), Inches(2.55)
    )
    c_team.fill.solid()
    c_team.fill.fore_color.rgb = C_SURFACE_DARK
    c_team.line.color.rgb = C_BORDER_DARK
    c_team.line.width = Pt(1)
    tf_tm = c_team.text_frame
    tf_tm.margin_left = tf_tm.margin_right = tf_tm.margin_top = tf_tm.margin_bottom = (
        Inches(0.3)
    )

    pt_h = tf_tm.paragraphs[0]
    pt_h.text = "TIM MAHASISWA:"
    pt_h.font.name = "Arial"
    pt_h.font.size = Pt(11)
    pt_h.font.bold = True
    pt_h.font.color.rgb = C_MUTED_LIGHT
    pt_h.space_after = Pt(8)

    pt_1 = tf_tm.add_paragraph()
    pt_1.text = (
        "1. Achmad Ridho Fa'iz (NIM: 230411100197) — Ketua\n"
        "2. [Nama Anggota 2] (NIM: [NIM Anggota 2])\n"
        "3. [Nama Anggota 3] (NIM: [NIM Anggota 3])\n"
        "4. [Nama Anggota 4] (NIM: [NIM Anggota 4])"
    )
    pt_1.font.name = "Arial"
    pt_1.font.size = Pt(12)
    pt_1.font.color.rgb = C_TEXT_LIGHT

    c_inst = s1.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(7.8),
        Inches(4.1),
        Inches(4.733),
        Inches(2.55),
    )
    c_inst.fill.solid()
    c_inst.fill.fore_color.rgb = C_SURFACE_DARK
    c_inst.line.color.rgb = C_BORDER_DARK
    c_inst.line.width = Pt(1)
    tf_in = c_inst.text_frame
    tf_in.margin_left = tf_in.margin_right = tf_in.margin_top = tf_in.margin_bottom = (
        Inches(0.3)
    )

    pi_h = tf_in.paragraphs[0]
    pi_h.text = "DOSEN PENGAMPU & PROGRAM STUDI:"
    pi_h.font.name = "Arial"
    pi_h.font.size = Pt(11)
    pi_h.font.bold = True
    pi_h.font.color.rgb = C_MUTED_LIGHT
    pi_h.space_after = Pt(8)

    pi_1 = tf_in.add_paragraph()
    pi_1.text = (
        "Dosen Pengampu: Ach. Khozaimi, S.Kom., M.Kom.\n\n"
        "Program Studi S1 Teknik Informatika\n"
        "Fakultas Teknik - Universitas Trunojoyo Madura"
    )
    pi_1.font.name = "Arial"
    pi_1.font.size = Pt(12)
    pi_1.font.color.rgb = C_TEXT_LIGHT

    set_notes(
        s1,
        "Selamat pagi Bapak Dosen dan rekan-rekan sekalian. Hari ini kelompok kami mempresentasikan usulan proyek akhir "
        "Machine Learning: Prediksi Kelulusan dan Deteksi Dini Mahasiswa Putus Studi (Dropout) menggunakan pendekatan komparatif "
        "Decision Tree dan K-Nearest Neighbors.",
    )

    # ==================== SLIDE 2: LATAR BELAKANG ====================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s2, C_BG_PAGE)
    add_top_nav(
        s2, "Latar Belakang: Masalah Nyata Mahasiswa & Kampus", "LATAR BELAKANG"
    )

    c_stmt = s2.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.9), Inches(5.6), Inches(5.0)
    )
    c_stmt.fill.solid()
    c_stmt.fill.fore_color.rgb = C_OBSIDIAN
    c_stmt.line.fill.background()
    tf_s = c_stmt.text_frame
    tf_s.word_wrap = True
    tf_s.margin_left = tf_s.margin_right = tf_s.margin_top = tf_s.margin_bottom = (
        Inches(0.35)
    )

    ps1 = tf_s.paragraphs[0]
    ps1.text = "FAKTA LAPANGAN"
    ps1.font.name = "Arial"
    ps1.font.size = Pt(12)
    ps1.font.bold = True
    ps1.font.color.rgb = C_MUTED_LIGHT
    ps1.space_after = Pt(14)

    ps2 = tf_s.add_paragraph()
    ps2.text = "Mahasiswa putus studi (DO) jarang terjadi secara tiba-tiba."
    ps2.font.name = "Arial"
    ps2.font.size = Pt(22)
    ps2.font.bold = True
    ps2.font.color.rgb = C_TEXT_LIGHT
    ps2.space_after = Pt(14)

    ps3 = tf_s.add_paragraph()
    ps3.text = (
        "• Mahasiswa bermasalah biasanya menunjukkan indikasi awal sejak tahun pertama: nilai anjlok atau menunggak biaya kuliah.\n\n"
        "• Data historis akademik dan pembayaran sudah terekam di sistem kampus, namun belum dimanfaatkan secara prediktif.\n\n"
        "• Proyek ini membangun sistem deteksi dini agar pihak program studi dapat mengidentifikasi mahasiswa yang memerlukan pendampingan sedini mungkin."
    )
    ps3.font.name = "Arial"
    ps3.font.size = Pt(13.5)
    ps3.font.color.rgb = RGBColor(226, 232, 240)

    pts = [
        (
            "1. Dampak bagi Institusi",
            "Tingginya angka DO mempengaruhi akreditasi program studi dan efektivitas perencanaan akademik institusi.",
        ),
        (
            "2. Faktor Multidimensi",
            "Penyebab utama DO saling berkaitan: kondisi finansial keluarga, usia pendaftaran, dan adaptasi beban studi tahun pertama.",
        ),
        (
            "3. Peran Machine Learning",
            "Model klasifikasi mampu mengenali pola risiko sejak semester awal sehingga tindakan pendampingan preventif dapat segera diambil.",
        ),
    ]
    for idx, (head, body) in enumerate(pts):
        c_sub = s2.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(6.6),
            Inches(1.9 + (idx * 1.72)),
            Inches(5.933),
            Inches(1.56),
        )
        c_sub.fill.solid()
        c_sub.fill.fore_color.rgb = C_CARD_BG
        c_sub.line.color.rgb = C_BORDER
        c_sub.line.width = Pt(1.5)
        tf_sub = c_sub.text_frame
        tf_sub.word_wrap = True
        tf_sub.margin_left = tf_sub.margin_right = tf_sub.margin_top = (
            tf_sub.margin_bottom
        ) = Inches(0.25)

        p_sub0 = tf_sub.paragraphs[0]
        p_sub0.text = head
        p_sub0.font.name = "Arial"
        p_sub0.font.size = Pt(14)
        p_sub0.font.bold = True
        p_sub0.font.color.rgb = C_INK
        p_sub0.space_after = Pt(4)

        p_sub1 = tf_sub.add_paragraph()
        p_sub1.text = body
        p_sub1.font.name = "Arial"
        p_sub1.font.size = Pt(12)
        p_sub1.font.color.rgb = C_BODY

    set_notes(
        s2,
        "Pada slide ini kami mengangkat urgensi masalah: putus studi merupakan proses atrisi bertahap yang indikasinya sudah terlihat "
        "sejak semester satu lewat kendala finansial atau performa akademik awal. Data historis tersebut sudah terekam di sistem kampus, "
        "sehingga pemodelan Machine Learning dapat dimanfaatkan untuk memberikan peringatan dini sebelum mahasiswa mengalami kegagalan studi.",
    )

    # ==================== SLIDE 3: RUMUSAN MASALAH & TUJUAN ====================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s3, C_BG_PAGE)
    add_top_nav(s3, "Rumusan Masalah & Tujuan Proyek", "FOKUS KAJIAN")

    c_rm = s3.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.9), Inches(5.66), Inches(5.0)
    )
    c_rm.fill.solid()
    c_rm.fill.fore_color.rgb = C_CARD_BG
    c_rm.line.color.rgb = C_BORDER
    c_rm.line.width = Pt(1.5)
    tf_rm = c_rm.text_frame
    tf_rm.word_wrap = True
    tf_rm.margin_left = tf_rm.margin_right = tf_rm.margin_top = tf_rm.margin_bottom = (
        Inches(0.35)
    )

    prm_h = tf_rm.paragraphs[0]
    prm_h.text = "RUMUSAN MASALAH"
    prm_h.font.name = "Arial"
    prm_h.font.size = Pt(13)
    prm_h.font.bold = True
    prm_h.font.color.rgb = C_SLATE
    prm_h.space_after = Pt(14)

    rm_list = [
        (
            "1. Faktor Determinan Utama",
            "Variabel manakah antara tunggakan SPP, usia mahasiswa, dan performa SKS semester 1 yang paling dominan memicu risiko dropout?",
        ),
        (
            "2. Komparasi Kinerja Model",
            "Bagaimana perbandingan akurasi dan interpretabilitas Decision Tree vs KNN pada data klasifikasi biner 3.630 baris data definitif?",
        ),
        (
            "3. Desain Validasi & Pipeline",
            "Bagaimana pembagian data 3-arah (70:15:15) dan preprocessing khusus (Dual Pipeline) mencegah kebocoran data dan bias model?",
        ),
    ]
    for t_txt, b_txt in rm_list:
        pt = tf_rm.add_paragraph()
        pt.text = t_txt
        pt.font.name = "Arial"
        pt.font.size = Pt(14)
        pt.font.bold = True
        pt.font.color.rgb = C_INK
        pt.space_after = Pt(3)

        pb = tf_rm.add_paragraph()
        pb.text = b_txt
        pb.font.name = "Arial"
        pb.font.size = Pt(12)
        pb.font.color.rgb = C_BODY
        pb.space_after = Pt(12)

    c_tj = s3.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(6.86),
        Inches(1.9),
        Inches(5.66),
        Inches(5.0),
    )
    c_tj.fill.solid()
    c_tj.fill.fore_color.rgb = C_SURFACE_DARK
    c_tj.line.color.rgb = C_BORDER_DARK
    c_tj.line.width = Pt(1.5)
    tf_tj = c_tj.text_frame
    tf_tj.word_wrap = True
    tf_tj.margin_left = tf_tj.margin_right = tf_tj.margin_top = tf_tj.margin_bottom = (
        Inches(0.35)
    )

    ptj_h = tf_tj.paragraphs[0]
    ptj_h.text = "TUJUAN PROYEK"
    ptj_h.font.name = "Arial"
    ptj_h.font.size = Pt(13)
    ptj_h.font.bold = True
    ptj_h.font.color.rgb = C_MUTED_LIGHT
    ptj_h.space_after = Pt(14)

    tj_list = [
        (
            "1. Formulasi Klasifikasi Biner",
            "Menetapkan target diskrit ('Graduate' vs 'Dropout') karena tidak ada makna fisik bagi nilai kontinu seperti 'lulus 0,73' atau 'DO 1,45'. Kampus butuh batas keputusan tegas.",
        ),
        (
            "2. Pengujian Terukur Bebas Leakage",
            "Melatih model pada 70% data latih, validasi 15%, dan uji 15% pada 3.630 data definitif guna membandingkan Decision Tree vs KNN.",
        ),
        (
            "3. Simulasi Mahasiswa Aktif",
            "Menerapkan model terbaik pada 794 data mahasiswa aktif (Enrolled) untuk simulasi deteksi dini dan intervensi preventif dosen wali.",
        ),
    ]
    for t_txt, b_txt in tj_list:
        pt = tf_tj.add_paragraph()
        pt.text = t_txt
        pt.font.name = "Arial"
        pt.font.size = Pt(14)
        pt.font.bold = True
        pt.font.color.rgb = C_TEXT_LIGHT
        pt.space_after = Pt(3)

        pb = tf_tj.add_paragraph()
        pb.text = b_txt
        pb.font.name = "Arial"
        pb.font.size = Pt(12)
        pb.font.color.rgb = C_MUTED_LIGHT
        pb.space_after = Pt(12)

    set_notes(
        s3,
        "Rumusan masalah kami terfokus pada perumusan Supervised Classification dan bukan Regression. "
        "Status mahasiswa adalah label kualitatif diskrit ('Graduate' vs 'Dropout')—tidak ada interpretasi fisik bagi nilai kontinu "
        "seperti 'mahasiswa lulus 0,73' atau 'mahasiswa DO 1,45'. Pihak kampus dan dosen wali memerlukan batas keputusan tegas (decision boundary) untuk memicu SOP intervensi. "
        "Tujuannya adalah membandingkan Decision Tree vs KNN secara adil dengan validasi 3-arah bebas kebocoran data, "
        "serta menghasilkan simulasi deteksi dini bagi 794 mahasiswa aktif.",
    )

    # ==================== SLIDE 4: PROFIL DATASET BINER (3.630 DATA) ====================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s4, C_BG_PAGE)
    add_top_nav(
        s4, "Dataset: Formulasi Klasifikasi Biner (3.630 Mahasiswa)", "DATASET RISET"
    )

    add_metric_callout(
        s4,
        0.8,
        1.9,
        3.64,
        1.6,
        "3.630",
        "Data Riset Utama",
        "Populasi mahasiswa bertarget definitif (Lulus vs DO).",
    )
    add_metric_callout(
        s4,
        4.84,
        1.9,
        3.64,
        1.6,
        "36",
        "Fitur Prediktor",
        "Indikator keuangan SPP, beban SKS, usia, dan sosial-ekonomi.",
    )
    add_metric_callout(
        s4,
        8.88,
        1.9,
        3.64,
        1.6,
        "2 Kelas",
        "Target Biner Definitif",
        "Lulus (60,9% / 2.209) vs Putus Studi (39,1% / 1.421).",
    )

    c_dinfo = s4.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(3.7), Inches(5.6), Inches(3.2)
    )
    c_dinfo.fill.solid()
    c_dinfo.fill.fore_color.rgb = C_CARD_BG
    c_dinfo.line.color.rgb = C_BORDER
    c_dinfo.line.width = Pt(1.5)
    tf_di = c_dinfo.text_frame
    tf_di.word_wrap = True
    tf_di.margin_left = tf_di.margin_right = tf_di.margin_top = tf_di.margin_bottom = (
        Inches(0.25)
    )

    pdi_h = tf_di.paragraphs[0]
    pdi_h.text = "STRATEGI PENYARINGAN KELAS ENROLLED"
    pdi_h.font.name = "Arial"
    pdi_h.font.size = Pt(13)
    pdi_h.font.bold = True
    pdi_h.font.color.rgb = C_INK
    pdi_h.space_after = Pt(8)

    pdi_b = tf_di.add_paragraph()
    pdi_b.text = (
        "• Formulasi Klasifikasi Biner (Bukan Regresi):\n"
        "  Label kualitatif nominal ('Graduate' vs 'Dropout') tidak memiliki makna fisik kontinu seperti 'lulus 0,73' atau 'DO 1,45'. Fokus pada 3.630 data definitif mengoptimalkan batas keputusan (decision boundary).\n\n"
        "• Eliminasi Noise (Paper Martins et al., 2021):\n"
        "  Mahasiswa aktif (Enrolled - 794 data) belum memiliki takdir studi final. Memasukkannya ke data latih menimbulkan ambiguitas label.\n\n"
        "• Kolam Simulasi Deployment:\n"
        "  794 data Enrolled dialokasikan sebagai data uji simulasi pemantauan mahasiswa aktif."
    )
    pdi_b.font.name = "Arial"
    pdi_b.font.size = Pt(11.5)
    pdi_b.font.color.rgb = C_BODY

    if os.path.exists("resource/ML/proposal/figures/target_distribution.png"):
        frame = s4.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(6.6),
            Inches(3.7),
            Inches(5.933),
            Inches(3.2),
        )
        frame.fill.solid()
        frame.fill.fore_color.rgb = C_CARD_BG
        frame.line.color.rgb = C_BORDER
        frame.line.width = Pt(1.5)
        s4.shapes.add_picture(
            "resource/ML/proposal/figures/target_distribution.png",
            Inches(6.8),
            Inches(3.85),
            width=Inches(5.533),
        )

    set_notes(
        s4,
        "Dataset acuan kami dari UCI Repository. Berdasarkan dokumentasi dan paper resmi Martins et al., 794 data mahasiswa yang masih "
        "aktif (Enrolled) kami pisahkan dari data latih karena status studinya belum selesai. Kami fokus pada 3.630 mahasiswa berstatus "
        "pasti (Lulus vs DO), sehingga masalah menjadi klasifikasi biner dan bukan regresi. Status mahasiswa merupakan label nominal kualitatif diskrit "
        "sehingga tidak ada makna fisik bagi nilai kontinu seperti 'lulus 0,73' atau 'DO 1,45'. Batas kelas menjadi bersih, dan potensi akurasi melonjak ke kisaran 88 hingga 92 persen.",
    )

    # ==================== SLIDE 5: TEMUAN EDA - RISIKO FINANSIAL ====================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s5, C_BG_PAGE)
    add_top_nav(
        s5, "Temuan EDA: Pengaruh Besar Biaya Kuliah & Beasiswa", "TEMUAN 1: KEUANGAN"
    )

    add_metric_callout(
        s5,
        0.8,
        1.9,
        5.66,
        1.5,
        "86,6%",
        "Mahasiswa Nunggak SPP Berujung DO",
        "Menunggak pembayaran SPP menjadi indikator risiko paling tajam terhadap kegagalan studi.",
        dark_theme=True,
    )
    add_metric_callout(
        s5,
        6.86,
        1.9,
        5.66,
        1.5,
        "76,2%",
        "Penerima Beasiswa Berhasil Lulus",
        "Bantuan pembiayaan terbukti memberikan bantalan stabilitas yang signifikan terhadap kelulusan.",
    )

    if os.path.exists("resource/ML/proposal/figures/financial_risk.png"):
        f_card1 = s5.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(0.8),
            Inches(3.6),
            Inches(5.66),
            Inches(3.3),
        )
        f_card1.fill.solid()
        f_card1.fill.fore_color.rgb = C_CARD_BG
        f_card1.line.color.rgb = C_BORDER
        f_card1.line.width = Pt(1.5)
        s5.shapes.add_picture(
            "resource/ML/proposal/figures/financial_risk.png",
            Inches(0.95),
            Inches(3.72),
            width=Inches(5.36),
        )

    if os.path.exists("resource/ML/proposal/figures/scholarship_protection.png"):
        f_card2 = s5.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(6.86),
            Inches(3.6),
            Inches(5.66),
            Inches(3.3),
        )
        f_card2.fill.solid()
        f_card2.fill.fore_color.rgb = C_CARD_BG
        f_card2.line.color.rgb = C_BORDER
        f_card2.line.width = Pt(1.5)
        s5.shapes.add_picture(
            "resource/ML/proposal/figures/scholarship_protection.png",
            Inches(7.01),
            Inches(3.72),
            width=Inches(5.36),
        )

    set_notes(
        s5,
        "Temuan eksplorasi data membuktikan bahwa kewajiban finansial merupakan pembeda paling tajam. "
        "Mahasiswa yang menunggak SPP memiliki angka putus studi mencapai 86.6 persen, sedangkan mahasiswa penerima beasiswa "
        "mencatat tingkat kelulusan 76.2 persen. Ini bukti kuantitatif bahwa stabilitas biaya memegang peranan krusial.",
    )

    # ==================== SLIDE 6: TEMUAN EDA - DINAMIKA AKADEMIK & USIA ====================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s6, C_BG_PAGE)
    add_top_nav(
        s6, "Temuan EDA: Nilai Semester Awal & Faktor Usia", "TEMUAN 2: AKADEMIK & USIA"
    )

    add_metric_callout(
        s6,
        0.8,
        1.9,
        5.66,
        1.5,
        "r > 0.85",
        "Korelasi SKS Semester 1 & 2 Sangat Kuat",
        "Kegagalan kelulusan beban SKS di semester 1 mengunci performa rendah pada semester 2.",
    )
    add_metric_callout(
        s6,
        6.86,
        1.9,
        5.66,
        1.5,
        "> 25 Tahun",
        "Kelompok Usia Paling Rawan Putus Studi",
        "Mahasiswa yang mendaftar pada usia dewasa lebih rentan DO akibat konflik peran kerja dan keluarga.",
    )

    if os.path.exists("resource/ML/proposal/figures/academic_correlation.png"):
        f_card1 = s6.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(0.8),
            Inches(3.6),
            Inches(5.66),
            Inches(3.3),
        )
        f_card1.fill.solid()
        f_card1.fill.fore_color.rgb = C_CARD_BG
        f_card1.line.color.rgb = C_BORDER
        f_card1.line.width = Pt(1.5)
        s5_img = s6.shapes.add_picture(
            "resource/ML/proposal/figures/academic_correlation.png",
            Inches(0.95),
            Inches(3.72),
            width=Inches(5.36),
        )
        del s5_img

    if os.path.exists("resource/ML/proposal/figures/age_demographics.png"):
        f_card2 = s6.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(6.86),
            Inches(3.6),
            Inches(5.66),
            Inches(3.3),
        )
        f_card2.fill.solid()
        f_card2.fill.fore_color.rgb = C_CARD_BG
        f_card2.line.color.rgb = C_BORDER
        f_card2.line.width = Pt(1.5)
        s6_img = s6.shapes.add_picture(
            "resource/ML/proposal/figures/age_demographics.png",
            Inches(7.01),
            Inches(3.72),
            width=Inches(5.36),
        )
        del s6_img

    set_notes(
        s6,
        "Di sisi akademik, matriks korelasi menunjukkan korelasi di atas 0.85 antara semester 1 dan semester 2. "
        "Artinya jika mahasiswa gagal di semester 1, mereka sulit mengejar di semester berikutnya jika tanpa intervensi. "
        "Grafik usia juga membuktikan mahasiswa usia dewasa (>25 tahun) memiliki risiko dropout jauh lebih tinggi.",
    )

    # ==================== SLIDE 7: VERSUS CARD & DUAL PIPELINE ====================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s7, C_BG_PAGE)
    add_top_nav(
        s7, "Keadilan Model: Arsitektur Dual Preprocessing Pipeline", "DUAL PIPELINE"
    )

    c_dt = s7.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.9), Inches(5.66), Inches(5.0)
    )
    c_dt.fill.solid()
    c_dt.fill.fore_color.rgb = C_CARD_BG
    c_dt.line.color.rgb = C_INK
    c_dt.line.width = Pt(2)
    tf_dt = c_dt.text_frame
    tf_dt.word_wrap = True
    tf_dt.margin_left = tf_dt.margin_right = tf_dt.margin_top = tf_dt.margin_bottom = (
        Inches(0.3)
    )

    pdt_tag = tf_dt.paragraphs[0]
    pdt_tag.text = "PIPELINE 1 | DECISION TREE"
    pdt_tag.font.name = "Arial"
    pdt_tag.font.size = Pt(10)
    pdt_tag.font.bold = True
    pdt_tag.font.color.rgb = C_SLATE
    pdt_tag.space_after = Pt(4)

    pdt_title = tf_dt.add_paragraph()
    pdt_title.text = "Decision Tree (Skala Asli)"
    pdt_title.font.name = "Arial Black"
    pdt_title.font.size = Pt(22)
    pdt_title.font.bold = True
    pdt_title.font.color.rgb = C_INK
    pdt_title.space_after = Pt(12)

    dt_points = [
        (
            "• Tanpa Penskalaan (Unscaled):",
            "Pohon keputusan kebal terhadap skala fitur karena memotong data berdasarkan urutan/ranking nilai numerik.",
        ),
        (
            "• Interpretabilitas Terjaga:",
            "Diagram pohon menghasilkan aturan batas nyata yang konkret (misal: 'IPK < 12.0 dan SPP = 0' bukan angka z-score).",
        ),
        (
            "• Penanganan Data Campuran:",
            "Mampu mempartisi data kategorikal biner dan kontinu secara simultan melalui kriteria Gini Impurity.",
        ),
        (
            "• Kontrol Kompleksitas:",
            "Kedalaman pohon dibatasi (max_depth 3-6) melalui data validasi agar tidak mengalami overfitting.",
        ),
    ]
    for h, b in dt_points:
        p_p = tf_dt.add_paragraph()
        p_p.text = f"{h} {b}"
        p_p.font.name = "Arial"
        p_p.font.size = Pt(12)
        p_p.font.color.rgb = C_BODY
        p_p.space_after = Pt(8)

    c_knn = s7.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(6.86),
        Inches(1.9),
        Inches(5.66),
        Inches(5.0),
    )
    c_knn.fill.solid()
    c_knn.fill.fore_color.rgb = C_SURFACE_DARK
    c_knn.line.color.rgb = C_BORDER_DARK
    c_knn.line.width = Pt(2)
    tf_kn = c_knn.text_frame
    tf_kn.word_wrap = True
    tf_kn.margin_left = tf_kn.margin_right = tf_kn.margin_top = tf_kn.margin_bottom = (
        Inches(0.3)
    )

    pkn_tag = tf_kn.paragraphs[0]
    pkn_tag.text = "PIPELINE 2 | K-NEAREST NEIGHBORS"
    pkn_tag.font.name = "Arial"
    pkn_tag.font.size = Pt(10)
    pkn_tag.font.bold = True
    pkn_tag.font.color.rgb = C_MUTED_LIGHT
    pkn_tag.space_after = Pt(4)

    pkn_title = tf_kn.add_paragraph()
    pkn_title.text = "KNN (StandardScaler Pipeline)"
    pkn_title.font.name = "Arial Black"
    pkn_title.font.size = Pt(22)
    pkn_title.font.bold = True
    pkn_title.font.color.rgb = C_TEXT_LIGHT
    pkn_title.space_after = Pt(12)

    knn_points = [
        (
            "• Wajib StandardScaler:",
            "Jarak Euclidean mensyaratkan semua fitur memiliki mean 0 dan std 1 agar tidak didominasi fitur berangka besar.",
        ),
        (
            "• Netralisasi ID Nominal:",
            "Kode jurusan nominal (misal 9254 vs 171) dinetralkan agar KNN tidak menghitung jarak kode fiktif yang tidak logis.",
        ),
        (
            "• Estimasi Kemiripan Murni:",
            "Mengklasifikasikan mahasiswa berdasarkan kedekatan jarak profil objektif dari K tetangga terdekat.",
        ),
        (
            "• Tuning K Terukur:",
            "Nilai K (3, 5, 7, 9, 11) dioptimasi secara khusus pada data validasi untuk mencegah underfitting maupun noise.",
        ),
    ]
    for h, b in knn_points:
        p_p = tf_kn.add_paragraph()
        p_p.text = f"{h} {b}"
        p_p.font.name = "Arial"
        p_p.font.size = Pt(12)
        p_p.font.color.rgb = C_MUTED_LIGHT
        p_p.space_after = Pt(8)

    set_notes(
        s7,
        "Untuk menjamin perbandingan yang adil, kami merancang Dual Preprocessing Pipeline. "
        "Decision Tree bekerja maksimal dengan data berskala asli sehingga aturan pohonnya mudah dibaca dosen wali. "
        "Sedangkan KNN wajib menggunakan StandardScaler dan netralisasi kode jurusan agar rumus jarak Euclidean bekerja secara adil dan valid.",
    )

    # ==================== SLIDE 8: 3-WAY SPLIT & PIPELINE CRISP-DM ====================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s8, C_BG_PAGE)
    add_top_nav(
        s8,
        "Strategi Partisi 3-Arah (Train-Validation-Test 70:15:15)",
        "SPLIT & VALIDASI",
    )

    pipeline_steps = [
        (
            "BAGIAN 01",
            "Data Latih (70%)",
            "2.541 Baris Mahasiswa\n\nDigunakan murni untuk melatih pola data dan pembentukan struktur model klasifikasi.",
        ),
        (
            "BAGIAN 02",
            "Data Validasi (15%)",
            "544 Baris Mahasiswa\n\nKhusus untuk Hyperparameter Tuning (mencari K terbaik KNN dan kedalaman max_depth Tree tanpa kebocoran data).",
        ),
        (
            "BAGIAN 03",
            "Data Uji Murni (15%)",
            "545 Baris Mahasiswa\n\nDisimpan rapat dan hanya diuji satu kali di akhir untuk evaluasi performa final yang objektif.",
        ),
        (
            "BAGIAN 04",
            "Kolam Simulasi",
            "794 Data Mahasiswa Aktif\n\nData mahasiswa Enrolled diuji untuk simulasi peringatan dini sistem monitoring kampus.",
        ),
    ]
    for idx, (step_num, title, body) in enumerate(pipeline_steps):
        left_pos = 0.8 + (idx * 2.98)
        card_step = s8.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(left_pos),
            Inches(1.9),
            Inches(2.78),
            Inches(3.4),
        )
        card_step.fill.solid()
        card_step.fill.fore_color.rgb = C_CARD_BG
        card_step.line.color.rgb = C_BORDER
        card_step.line.width = Pt(1.5)
        tf_cs = card_step.text_frame
        tf_cs.word_wrap = True
        tf_cs.margin_left = tf_cs.margin_right = tf_cs.margin_top = (
            tf_cs.margin_bottom
        ) = Inches(0.2)

        p_s0 = tf_cs.paragraphs[0]
        p_s0.text = step_num
        p_s0.font.name = "Arial Black"
        p_s0.font.size = Pt(13)
        p_s0.font.bold = True
        p_s0.font.color.rgb = C_INK
        p_s0.space_after = Pt(4)

        p_s1 = tf_cs.add_paragraph()
        p_s1.text = title
        p_s1.font.name = "Arial"
        p_s1.font.size = Pt(13)
        p_s1.font.bold = True
        p_s1.font.color.rgb = C_SLATE
        p_s1.space_after = Pt(8)

        p_s2 = tf_cs.add_paragraph()
        p_s2.text = body
        p_s2.font.name = "Arial"
        p_s2.font.size = Pt(11)
        p_s2.font.color.rgb = C_BODY

    b_banner = s8.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(0.8),
        Inches(5.5),
        Inches(11.733),
        Inches(1.4),
    )
    b_banner.fill.solid()
    b_banner.fill.fore_color.rgb = C_OBSIDIAN
    b_banner.line.fill.background()
    tf_bb = b_banner.text_frame
    tf_bb.word_wrap = True
    tf_bb.margin_left = tf_bb.margin_right = tf_bb.margin_top = tf_bb.margin_bottom = (
        Inches(0.22)
    )

    pbb_0 = tf_bb.paragraphs[0]
    pbb_0.text = "INTEGRASI SIKLUS PENGERJAAN CRISP-DM:"
    pbb_0.font.name = "Arial"
    pbb_0.font.size = Pt(11)
    pbb_0.font.bold = True
    pbb_0.font.color.rgb = C_MUTED_LIGHT
    pbb_0.space_after = Pt(2)

    pbb_1 = tf_bb.add_paragraph()
    pbb_1.text = (
        "1. Identifikasi Masalah Kampus  →  2. Eksplorasi 3.630 Data Biner  →  3. Dual Preprocessing Pipeline  →  "
        "4. Pelatihan & Validasi (70:15)  →  5. Uji Murni (15%)  →  6. Simulasi 794 Data Mahasiswa Aktif."
    )
    pbb_1.font.name = "Arial"
    pbb_1.font.size = Pt(11.5)
    pbb_1.font.color.rgb = C_TEXT_LIGHT

    set_notes(
        s8,
        "Untuk mencegah kebocoran data, kami menerapkan partisi 3-arah: 70 persen untuk latihan, 15 persen data validasi khusus "
        "untuk mencari nilai K dan kedalaman pohon optimal, serta 15 persen data uji murni untuk evaluasi akhir. "
        "794 data Enrolled disiapkan untuk simulasi monitoring kampus.",
    )

    # ==================== SLIDE 9: RENCANA EVALUASI BINER ====================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s9, C_BG_PAGE)
    add_top_nav(
        s9, "Rencana Evaluasi: Metrik Diagnostik Klasifikasi Biner", "RENCANA EVALUASI"
    )

    eval_cards = [
        (
            "01",
            "Confusion Matrix 2x2",
            "Transparansi Hasil Tebakan",
            (
                "Memetakan secara akurat:\n\n"
                "• True Positive: Mahasiswa DO yang berhasil terdeteksi.\n\n"
                "• False Negative: Mahasiswa DO yang luput terdeteksi.\n\n"
                "• True Negative & False Positive."
            ),
        ),
        (
            "02",
            "Prioritas Recall Dropout",
            "Sensitivitas Deteksi Dini",
            (
                "Fokus utama institusi kampus:\n\n"
                "• Biaya kegagalan terbesar adalah False Negative (mahasiswa DO yang tidak terdeteksi sistem).\n\n"
                "• Oleh karena itu, metrik Recall kelas Dropout menjadi target optimasi utama."
            ),
        ),
        (
            "03",
            "ROC-AUC & Aturan Aksi",
            "Daya Diskriminasi & Kebijakan",
            (
                "Evaluasi performa komprehensif:\n\n"
                "• ROC-AUC mengukur pemisahan kelas di berbagai threshold.\n\n"
                "• Aturan hasil pohon keputusan diekstrak menjadi panduan indikator risiko bagi program studi."
            ),
        ),
    ]
    for idx, (num, title, subtitle, desc) in enumerate(eval_cards):
        left_pos = 0.8 + (idx * 3.98)
        c_eval = s9.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(left_pos),
            Inches(1.9),
            Inches(3.78),
            Inches(5.0),
        )
        c_eval.fill.solid()
        c_eval.fill.fore_color.rgb = C_CARD_BG
        c_eval.line.color.rgb = C_BORDER
        c_eval.line.width = Pt(1.5)
        tf_ev = c_eval.text_frame
        tf_ev.word_wrap = True
        tf_ev.margin_left = tf_ev.margin_right = tf_ev.margin_top = (
            tf_ev.margin_bottom
        ) = Inches(0.25)

        pev_0 = tf_ev.paragraphs[0]
        pev_0.text = num
        pev_0.font.name = "Arial Black"
        pev_0.font.size = Pt(28)
        pev_0.font.bold = True
        pev_0.font.color.rgb = C_INK
        pev_0.space_after = Pt(4)

        pev_1 = tf_ev.add_paragraph()
        pev_1.text = title
        pev_1.font.name = "Arial"
        pev_1.font.size = Pt(14)
        pev_1.font.bold = True
        pev_1.font.color.rgb = C_INK
        pev_1.space_after = Pt(2)

        pev_sub = tf_ev.add_paragraph()
        pev_sub.text = subtitle
        pev_sub.font.name = "Arial"
        pev_sub.font.size = Pt(11)
        pev_sub.font.bold = True
        pev_sub.font.color.rgb = C_SLATE
        pev_sub.space_after = Pt(12)

        pev_2 = tf_ev.add_paragraph()
        pev_2.text = desc
        pev_2.font.name = "Arial"
        pev_2.font.size = Pt(11.5)
        pev_2.font.color.rgb = C_BODY

    set_notes(
        s9,
        "Dalam evaluasi klasifikasi biner, kami memanfaatkan Confusion Matrix 2x2, ROC-AUC, dan prioritas Recall pada kelas Dropout. "
        "Evaluasi ini menjadi penutup proposal sekaligus pintu gerbang eksekusi laporan akhir: mengatasi The Accuracy Trap (60,85%), "
        "menghubungkan temuan outlier usia M23, multikolinearitas SKS, dan isolasi data Enrolled secara bertahap menuju simulasi intervensi mahasiswa aktif.",
    )

    # ==================== SLIDE 10: CLOSING SLIDE (DARK HERO) ====================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s10, C_OBSIDIAN)

    badge10 = s10.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(0.8),
        Inches(1.5),
        Inches(2.4),
        Inches(0.35),
    )
    badge10.fill.solid()
    badge10.fill.fore_color.rgb = C_SURFACE_DARK
    badge10.line.color.rgb = C_BORDER_DARK
    tf_tb10 = badge10.text_frame
    tf_tb10.margin_top = Inches(0.05)
    ptb10 = tf_tb10.paragraphs[0]
    ptb10.text = "SESI AKHIR PRESENTASI"
    ptb10.font.name = "Arial"
    ptb10.font.size = Pt(9)
    ptb10.font.bold = True
    ptb10.font.color.rgb = C_TEXT_LIGHT
    ptb10.alignment = PP_ALIGN.CENTER

    t_box10 = s10.shapes.add_textbox(
        Inches(0.8), Inches(2.1), Inches(11.733), Inches(4.5)
    )
    tf10 = t_box10.text_frame
    tf10.word_wrap = True

    p10_1 = tf10.paragraphs[0]
    p10_1.text = "Terima Kasih.\nSesi Tanya & Jawab (Q&A)"
    p10_1.font.name = "Arial Black"
    p10_1.font.size = Pt(36)
    p10_1.font.bold = True
    p10_1.font.color.rgb = C_TEXT_LIGHT
    p10_1.space_after = Pt(20)

    p10_2 = tf10.add_paragraph()
    p10_2.text = (
        "Proyek Akhir Machine Learning: Prediksi Kelulusan Mahasiswa\n"
        "Teknik Informatika, Fakultas Teknik, Universitas Trunojoyo Madura\n\n"
        "Ketua Kelompok: Achmad Ridho Fa'iz (NIM: 230411100197)  |  Dosen Pengampu: Ach. Khozaimi, S.Kom., M.Kom."
    )
    p10_2.font.name = "Arial"
    p10_2.font.size = Pt(13.5)
    p10_2.font.color.rgb = C_MUTED_LIGHT

    set_notes(
        s10,
        "Sekian pemaparan usulan proyek akhir dari kelompok kami. "
        "Kami menyambut baik masukan, saran, dan pertanyaan dari Bapak Dosen serta rekan-rekan sekalian. Terima kasih.",
    )

    prs.save(output_path)
    print(f"Presentation PPTX successfully created at: {output_path}")


if __name__ == "__main__":
    target_pptx = "resource/ML/proposal/Presentasi-Proposal-ML-230411100197.pptx"
    create_proposal_presentation(target_pptx)
