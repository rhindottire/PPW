"""Script to generate the official Machine Learning Final Defense Presentation Slides (.pptx and .pdf).

Adhering strictly to UTM Computer Science Student Presentation Guidelines:
- Aspect Ratio: 16:9 Widescreen (13.333 x 7.5 inches)
- Palette: Obsidian Dark (#0F172A), Slate (#1E293B, #334155), Pure White (#F8FAFC, #FFFFFF), Accent Indigo
- 12 Comprehensive Slides with Speaker Notes on each slide
- Embeds real experimental plots from resource/ML/report/figures/
- Converts to PDF and renders PNG previews in resource/ML/report/previews/
"""

import os
from typing import Any

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt


def create_report_presentation(output_pptx: str) -> None:
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
        slide: Any, title_text: str, badge_text: str = "SIDANG AKHIR MACHINE LEARNING"
    ) -> None:
        badge = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(0.8),
            Inches(0.45),
            Inches(3.4),
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
        tf_t.margin_left = tf_t.margin_top = tf_t.margin_right = tf_t.margin_bottom = (
            Inches(0)
        )
        p_t = tf_t.paragraphs[0]
        p_t.text = title_text
        p_t.font.name = "Arial"
        p_t.font.size = Pt(21)
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
        p0.font.size = Pt(36)
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
        Inches(3.8),
        Inches(0.35),
    )
    badge1.fill.solid()
    badge1.fill.fore_color.rgb = C_SURFACE_DARK
    badge1.line.color.rgb = C_BORDER_DARK
    tf_b1 = badge1.text_frame
    tf_b1.margin_top = Inches(0.05)
    pb1 = tf_b1.paragraphs[0]
    pb1.text = "LAPORAN AKHIR PROJECT MACHINE LEARNING"
    pb1.font.name = "Arial"
    pb1.font.size = Pt(9)
    pb1.font.bold = True
    pb1.font.color.rgb = C_TEXT_LIGHT
    pb1.alignment = PP_ALIGN.CENTER

    t_box1 = s1.shapes.add_textbox(
        Inches(0.8), Inches(1.45), Inches(11.733), Inches(2.3)
    )
    tf1 = t_box1.text_frame
    tf1.word_wrap = True
    tf1.margin_left = tf1.margin_top = tf1.margin_right = tf1.margin_bottom = Inches(0)

    p_title1 = tf1.paragraphs[0]
    p_title1.text = "Prediksi Kelulusan & Deteksi Dini Mahasiswa Putus Studi (Dropout)"
    p_title1.font.name = "Arial"
    p_title1.font.size = Pt(30)
    p_title1.font.bold = True
    p_title1.font.color.rgb = C_TEXT_LIGHT
    p_title1.space_after = Pt(8)

    p_sub1 = tf1.add_paragraph()
    p_sub1.text = (
        "Evaluasi Komparatif Decision Tree vs K-Nearest Neighbors pada Data Uji Bebas Leakage "
        "dan Simulasi Sistem Deteksi Dini Mahasiswa Aktif"
    )
    p_sub1.font.name = "Arial"
    p_sub1.font.size = Pt(15)
    p_sub1.font.color.rgb = C_MUTED_LIGHT

    c_auth1 = s1.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(0.8),
        Inches(4.1),
        Inches(5.7),
        Inches(2.6),
    )
    c_auth1.fill.solid()
    c_auth1.fill.fore_color.rgb = C_SURFACE_DARK
    c_auth1.line.color.rgb = C_BORDER_DARK
    c_auth1.line.width = Pt(1.5)
    tf_a1 = c_auth1.text_frame
    tf_a1.word_wrap = True
    tf_a1.margin_left = tf_a1.margin_right = tf_a1.margin_top = tf_a1.margin_bottom = (
        Inches(0.3)
    )

    pa1 = tf_a1.paragraphs[0]
    pa1.text = "TIM MAHASISWA:"
    pa1.font.name = "Arial"
    pa1.font.size = Pt(11)
    pa1.font.bold = True
    pa1.font.color.rgb = C_MUTED_LIGHT
    pa1.space_after = Pt(6)

    pa2 = tf_a1.add_paragraph()
    pa2.text = (
        "1. Achmad Ridho Fa'iz (NIM: 230411100197) — Ketua Kelompok\n"
        "2. [Nama Rekan Kelompok] (NIM: [NIM Rekan Kelompok]) — Anggota Kelompok"
    )
    pa2.font.name = "Arial"
    pa2.font.size = Pt(12.5)
    pa2.font.bold = True
    pa2.font.color.rgb = C_TEXT_LIGHT
    pa2.space_after = Pt(6)

    c_meta1 = s1.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(6.8),
        Inches(4.1),
        Inches(5.7),
        Inches(2.6),
    )
    c_meta1.fill.solid()
    c_meta1.fill.fore_color.rgb = C_SURFACE_DARK
    c_meta1.line.color.rgb = C_BORDER_DARK
    c_meta1.line.width = Pt(1.5)
    tf_m1 = c_meta1.text_frame
    tf_m1.word_wrap = True
    tf_m1.margin_left = tf_m1.margin_right = tf_m1.margin_top = tf_m1.margin_bottom = (
        Inches(0.3)
    )

    pm1 = tf_m1.paragraphs[0]
    pm1.text = "DOSEN PENGAMPU & ALMAMATER:"
    pm1.font.name = "Arial"
    pm1.font.size = Pt(11)
    pm1.font.bold = True
    pm1.font.color.rgb = C_MUTED_LIGHT
    pm1.space_after = Pt(6)

    pm2 = tf_m1.add_paragraph()
    pm2.text = (
        "Dosen Pengampu: Ach. Khozaimi, S.Kom., M.Kom.\n"
        "Program Studi S1 Teknik Informatika | Fakultas Teknik\n"
        "Universitas Trunojoyo Madura (2026)"
    )
    pm2.font.name = "Arial"
    pm2.font.size = Pt(12)
    pm2.font.color.rgb = C_TEXT_LIGHT

    set_notes(
        s1,
        "Selamat pagi Bapak Dosen Penguji dan rekan-rekan sekalian. Hari ini kami mempresentasikan laporan akhir komputasi Machine Learning: "
        "Prediksi Keberhasilan Akademik dan Deteksi Dini Risiko Putus Studi Mahasiswa. Kami telah mengeksekusi pipeline CRISP-DM lengkap, "
        "membandingkan Decision Tree vs KNN pada data uji independen bebas data leakage, serta menguji sistem peringatan dini pada 794 data mahasiswa aktif.",
    )

    # ==================== SLIDE 2: URGENSI MASALAH KAMPUS ====================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s2, C_BG_PAGE)
    add_top_nav(
        s2,
        "Urgensi Masalah: Atrisi Mahasiswa & Krisis Pendidikan Tinggi",
        "URGENSI BISNIS",
    )

    add_metric_callout(
        s2,
        0.8,
        1.9,
        3.64,
        1.5,
        "Atrisi Bertahap",
        "Bukan Kejadian Mendadak",
        "Gejala atrisi telah terekam sejak semester 1 lewat nilai dan tunggakan.",
    )
    add_metric_callout(
        s2,
        4.84,
        1.9,
        3.64,
        1.5,
        "Data Pasif",
        "Belum Dimanfaatkan",
        "Data historis BAAK acap kali hanya berakhir sebagai arsip administratif.",
    )
    add_metric_callout(
        s2,
        8.88,
        1.9,
        3.64,
        1.5,
        "Proaktif",
        "Sistem Peringatan Dini",
        "Machine Learning mengubah respons kampus dari reaktif menjadi tindakan preventif.",
        dark_theme=True,
    )

    c_urg = s2.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(0.8),
        Inches(3.65),
        Inches(11.733),
        Inches(3.2),
    )
    c_urg.fill.solid()
    c_urg.fill.fore_color.rgb = C_CARD_BG
    c_urg.line.color.rgb = C_BORDER
    c_urg.line.width = Pt(1.5)
    tf_u = c_urg.text_frame
    tf_u.word_wrap = True
    tf_u.margin_left = tf_u.margin_right = tf_u.margin_top = tf_u.margin_bottom = (
        Inches(0.3)
    )

    pu_h = tf_u.paragraphs[0]
    pu_h.text = "TIGA DAMPAK KRITIS KEGAGALAN STUDI BAGI PERGURUAN TINGGI:"
    pu_h.font.name = "Arial"
    pu_h.font.size = Pt(13)
    pu_h.font.bold = True
    pu_h.font.color.rgb = C_INK
    pu_h.space_after = Pt(10)

    u_points = [
        (
            "1. Kerugian Finansial Institusional: ",
            "Kehilangan pendapatan SPP berkelanjutan secara signifikan selama sisa masa kurikulum.",
        ),
        (
            "2. Degradasi Reputasi & Akreditasi: ",
            "Tingginya rasio dropout menurunkan skor efisiensi edukasi pada evaluasi akreditasi LAM-INFOKOM/BAN-PT.",
        ),
        (
            "3. Hilangnya Masa Depan Mahasiswa: ",
            "Kegagalan studi menimbulkan beban psikososial berat bagi mahasiswa dan orang tua yang dapat dicegah jika terdeteksi lebih awal.",
        ),
    ]
    for h_txt, b_txt in u_points:
        p_pt = tf_u.add_paragraph()
        r_h = p_pt.add_run()
        r_h.text = h_txt
        r_h.font.name = "Arial"
        r_h.font.size = Pt(12.5)
        r_h.font.bold = True
        r_h.font.color.rgb = C_INK
        r_b = p_pt.add_run()
        r_b.text = b_txt
        r_b.font.name = "Arial"
        r_b.font.size = Pt(12)
        r_b.font.color.rgb = C_BODY
        p_pt.space_after = Pt(8)

    set_notes(
        s2,
        "Putus studi bukan peristiwa mendadak. Indikasi seperti tunggakan SPP dan SKS yang tidak lulus sudah tampak di tahun pertama. "
        "Dengan Machine Learning, kampus dapat melakukan intervensi sebelum mahasiswa terlanjur dijatuhi sanksi DO.",
    )

    # ==================== SLIDE 3: FORMULASI MASALAH ====================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s3, C_BG_PAGE)
    add_top_nav(
        s3, "Formulasi Masalah: Klasifikasi Biner vs Regresi", "LANDASAN METODE"
    )

    c_f1 = s3.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.9), Inches(5.66), Inches(5.0)
    )
    c_f1.fill.solid()
    c_f1.fill.fore_color.rgb = C_CARD_BG
    c_f1.line.color.rgb = C_BORDER
    c_f1.line.width = Pt(1.5)
    tf_f1 = c_f1.text_frame
    tf_f1.word_wrap = True
    tf_f1.margin_left = tf_f1.margin_right = tf_f1.margin_top = tf_f1.margin_bottom = (
        Inches(0.35)
    )

    pf1_h = tf_f1.paragraphs[0]
    pf1_h.text = "MENGAPA KLASIFIKASI, BUKAN REGRESI?"
    pf1_h.font.name = "Arial"
    pf1_h.font.size = Pt(13)
    pf1_h.font.bold = True
    pf1_h.font.color.rgb = C_SLATE
    pf1_h.space_after = Pt(12)

    f1_list = [
        (
            "• Tidak Ada Makna Fisik Nilai Kontinu:\n",
            "Status mahasiswa adalah label kualitatif diskrit ('Graduate' vs 'Dropout'). Tidak ada interpretasi logis bagi angka riil seperti 'mahasiswa lulus 0,73' atau 'mahasiswa DO 1,45'.",
        ),
        (
            "• Batas Keputusan Tegas (Decision Boundary):\n",
            "Kampus memerlukan klasifikasi tegas untuk memicu SOP intervensi (seperti restrukturisasi cicilan SPP atau konseling dosen wali).",
        ),
        (
            "• Pelanggaran Probabilitas Regresi Linear:\n",
            "Regresi pada target biner menghasilkan nilai di luar rentang valid (<0 atau >1) serta melanggar asumsi homoskedastisitas residual.",
        ),
    ]
    for h_txt, b_txt in f1_list:
        p = tf_f1.add_paragraph()
        r_h = p.add_run()
        r_h.text = h_txt
        r_h.font.name = "Arial"
        r_h.font.size = Pt(12.5)
        r_h.font.bold = True
        r_h.font.color.rgb = C_INK
        r_b = p.add_run()
        r_b.text = b_txt
        r_b.font.name = "Arial"
        r_b.font.size = Pt(11.5)
        r_b.font.color.rgb = C_BODY
        p.space_after = Pt(10)

    c_f2 = s3.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(6.86),
        Inches(1.9),
        Inches(5.66),
        Inches(5.0),
    )
    c_f2.fill.solid()
    c_f2.fill.fore_color.rgb = C_SURFACE_DARK
    c_f2.line.color.rgb = C_BORDER_DARK
    c_f2.line.width = Pt(1.5)
    tf_f2 = c_f2.text_frame
    tf_f2.word_wrap = True
    tf_f2.margin_left = tf_f2.margin_right = tf_f2.margin_top = tf_f2.margin_bottom = (
        Inches(0.35)
    )

    pf2_h = tf_f2.paragraphs[0]
    pf2_h.text = "STRATEGI POPULASI DATASET (3.630 DATA DEFINITIF)"
    pf2_h.font.name = "Arial"
    pf2_h.font.size = Pt(13)
    pf2_h.font.bold = True
    pf2_h.font.color.rgb = C_MUTED_LIGHT
    pf2_h.space_after = Pt(12)

    f2_list = [
        (
            "• 3.630 Baris Data Biner Definitif:\n",
            "Terdiri dari 2.209 Graduate (60,85%) dan 1.421 Dropout (39,15%). Digunakan murni untuk pelatihan, validasi, dan pengujian model.",
        ),
        (
            "• Isolasi 794 Data Mahasiswa Aktif (Enrolled):\n",
            "Berdasarkan paper rujukan Martins et al. (2021), status Enrolled masih berproses dan belum tamat. Memasukkannya ke data latih menimbulkan label noise yang menurunkan akurasi menjadi ~77%.",
        ),
        (
            "• Kolam Simulasi Deployment:\n",
            "794 data Enrolled dialokasikan khusus sebagai data simulasi inferensi intervensi deteksi dini mahasiswa aktif.",
        ),
    ]
    for h_txt, b_txt in f2_list:
        p = tf_f2.add_paragraph()
        r_h = p.add_run()
        r_h.text = h_txt
        r_h.font.name = "Arial"
        r_h.font.size = Pt(12.5)
        r_h.font.bold = True
        r_h.font.color.rgb = C_TEXT_LIGHT
        r_b = p.add_run()
        r_b.text = b_txt
        r_b.font.name = "Arial"
        r_b.font.size = Pt(11.5)
        r_b.font.color.rgb = C_MUTED_LIGHT
        p.space_after = Pt(10)

    set_notes(
        s3,
        "Di slide ini kami menegaskan justifikasi klasifikasi vs regresi: tidak ada interpretasi fisik 'lulus 0,73' atau 'DO 1,45'. "
        "Kampus butuh batas keputusan tegas. Kami menyaring 3.630 sampel definitif dan menyisihkan 794 sampel Enrolled untuk kolam simulasi intervensi.",
    )

    # ==================== SLIDE 4: PREPROCESSING & PARTISI 3-ARAH ====================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s4, C_BG_PAGE)
    add_top_nav(
        s4,
        "Metodologi: Dual Preprocessing Pipeline & Partisi 3-Arah",
        "PIPELINE DESAIN",
    )

    c_pl1 = s4.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.9), Inches(5.66), Inches(3.2)
    )
    c_pl1.fill.solid()
    c_pl1.fill.fore_color.rgb = C_CARD_BG
    c_pl1.line.color.rgb = C_BORDER
    c_pl1.line.width = Pt(1.5)
    tf_pl1 = c_pl1.text_frame
    tf_pl1.word_wrap = True
    tf_pl1.margin_left = tf_pl1.margin_right = tf_pl1.margin_top = (
        tf_pl1.margin_bottom
    ) = Inches(0.3)
    p_pl1_h = tf_pl1.paragraphs[0]
    p_pl1_h.text = "PIPELINE 1 | DECISION TREE (SKALA ASLI)"
    p_pl1_h.font.bold = True
    p_pl1_h.font.size = Pt(12)
    p_pl1_h.font.color.rgb = C_INK
    p_pl1_h.space_after = Pt(6)
    p_pl1_b = tf_pl1.add_paragraph()
    p_pl1_b.text = (
        "• Data Dibiarkan Unscaled (Skala Asli): Pohon CART kebal terhadap skala karena bekerja berdasarkan ranking nilai.\n"
        "• Aturan IF-THEN Nyata: Menghasilkan batas konkret (misal: 'SKS Lulus Sem 2 <= 3.0' bukan angka z-score).\n"
        "• Cost-Sensitive Learning: Mengaktifkan class_weight='balanced' untuk menghukum kesalahan tebak kelas Dropout secara proporsional."
    )
    p_pl1_b.font.size = Pt(11)
    p_pl1_b.font.color.rgb = C_BODY

    c_pl2 = s4.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(6.86),
        Inches(1.9),
        Inches(5.66),
        Inches(3.2),
    )
    c_pl2.fill.solid()
    c_pl2.fill.fore_color.rgb = C_CARD_BG
    c_pl2.line.color.rgb = C_BORDER
    c_pl2.line.width = Pt(1.5)
    tf_pl2 = c_pl2.text_frame
    tf_pl2.word_wrap = True
    tf_pl2.margin_left = tf_pl2.margin_right = tf_pl2.margin_top = (
        tf_pl2.margin_bottom
    ) = Inches(0.3)
    p_pl2_h = tf_pl2.paragraphs[0]
    p_pl2_h.text = "PIPELINE 2 | KNN (STANDARDSCALER PIPELINE)"
    p_pl2_h.font.bold = True
    p_pl2_h.font.size = Pt(12)
    p_pl2_h.font.color.rgb = C_INK
    p_pl2_h.space_after = Pt(6)
    p_pl2_b = tf_pl2.add_paragraph()
    p_pl2_b.text = (
        "• Wajib StandardScaler (Mean 0, Std 1): Jarak Euclidean mensyaratkan standarisasi agar fitur bernilai besar tidak mendominasi.\n"
        "• Netralisasi Kode Jurusan Nominal: Mencegah KNN menghitung jarak fiktif antar-kode jurusan.\n"
        "• Distance-Weighted Neighbors: Memberikan bobot lebih besar pada tetangga yang lebih dekat (weights='distance')."
    )
    p_pl2_b.font.size = Pt(11)
    p_pl2_b.font.color.rgb = C_BODY

    c_s4b = s4.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(0.8),
        Inches(5.3),
        Inches(11.733),
        Inches(1.7),
    )
    c_s4b.fill.solid()
    c_s4b.fill.fore_color.rgb = C_SURFACE_DARK
    c_s4b.line.color.rgb = C_BORDER_DARK
    c_s4b.line.width = Pt(1.5)
    tf_s4b = c_s4b.text_frame
    tf_s4b.word_wrap = True
    tf_s4b.margin_left = tf_s4b.margin_right = tf_s4b.margin_top = (
        tf_s4b.margin_bottom
    ) = Inches(0.25)
    ps4_h = tf_s4b.paragraphs[0]
    ps4_h.text = "PARTISI 3-ARAH BERSTRATA (ANTI-LEAKAGE DESIGN):"
    ps4_h.font.bold = True
    ps4_h.font.size = Pt(11.5)
    ps4_h.font.color.rgb = C_MUTED_LIGHT
    ps4_h.space_after = Pt(4)
    ps4_b = tf_s4b.add_paragraph()
    ps4_b.text = (
        "1. Train Set (70% / 2.541 baris): Pembentukan struktur model  →  "
        "2. Validation Set (15% / 544 baris): Khusus Hyperparameter Tuning  →  "
        "3. Test Set (15% / 545 baris): Uji murni satu kali di akhir  →  "
        "4. Enrolled Pool (794 baris): Simulasi Deployment."
    )
    ps4_b.font.bold = True
    ps4_b.font.size = Pt(12)
    ps4_b.font.color.rgb = C_TEXT_LIGHT

    set_notes(
        s4,
        "Untuk keadilan ilmiah, kami menggunakan Dual Pipeline: Decision Tree memakai skala asli agar menghasilkan aturan IF-THEN konkret, "
        "sedangkan KNN wajib distandarisasi StandardScaler. Partisi 3-arah 70:15:15 menjamin data uji tidak pernah bocor ke proses tuning.",
    )

    # ==================== SLIDE 5: HYPERPARAMETER TUNING ====================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s5, C_BG_PAGE)
    add_top_nav(
        s5,
        "Hyperparameter Tuning: Optimasi Model pada Data Validasi",
        "TUNING PARAMETER",
    )

    fig_tree = "resource/ML/report/figures/tree_tuning.png"
    if os.path.exists(fig_tree):
        frame1 = s5.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(0.8),
            Inches(1.9),
            Inches(5.66),
            Inches(4.9),
        )
        frame1.fill.solid()
        frame1.fill.fore_color.rgb = C_CARD_BG
        frame1.line.color.rgb = C_BORDER
        s5.shapes.add_picture(fig_tree, Inches(0.95), Inches(2.05), width=Inches(5.36))

        c_dt_desc = s5.shapes.add_textbox(
            Inches(0.95), Inches(5.35), Inches(5.36), Inches(1.3)
        )
        tf_dd = c_dt_desc.text_frame
        tf_dd.word_wrap = True
        pdd = tf_dd.paragraphs[0]
        pdd.text = "Decision Tree: Titik Optimal max_depth = 5\nMencegah overfitting (saat depth > 6 varians naik). Menghasilkan Recall Dropout ~83% dan F1-Score ~80% pada data validasi."
        pdd.font.size = Pt(11)
        pdd.font.color.rgb = C_BODY

    fig_knn = "resource/ML/report/figures/knn_tuning.png"
    if os.path.exists(fig_knn):
        frame2 = s5.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(6.86),
            Inches(1.9),
            Inches(5.66),
            Inches(4.9),
        )
        frame2.fill.solid()
        frame2.fill.fore_color.rgb = C_CARD_BG
        frame2.line.color.rgb = C_BORDER
        s5.shapes.add_picture(fig_knn, Inches(7.01), Inches(2.05), width=Inches(5.36))

        c_knn_desc = s5.shapes.add_textbox(
            Inches(7.01), Inches(5.35), Inches(5.36), Inches(1.3)
        )
        tf_kd = c_knn_desc.text_frame
        tf_kd.word_wrap = True
        pkd = tf_kd.paragraphs[0]
        pkd.text = "KNN (Scaled): Titik Optimal K = 11\nK kecil rentan noise data; K > 15 menghaluskan batas kelas secara berlebihan. K = 11 menghasilkan F1-score puncak ~78%."
        pkd.font.size = Pt(11)
        pkd.font.color.rgb = C_BODY

    set_notes(
        s5,
        "Pada data validasi, kami menemukan bahwa kedalaman pohon optimal Decision Tree adalah max_depth = 5. Kedalaman di atas 6 mengalami overfitting. "
        "Pada KNN, nilai tetangga optimal adalah K = 11. Konfigurasi ini terkunci sebelum masuk ke data uji murni.",
    )

    # ==================== SLIDE 6: EVALUASI KOMPARATIF TEST SET ====================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s6, C_BG_PAGE)
    add_top_nav(
        s6,
        "Evaluasi Komparatif: Kinerja pada Data Uji Murni (545 Sampel)",
        "HASIL EKSPERIMEN",
    )

    add_metric_callout(
        s6,
        0.8,
        1.9,
        2.7,
        1.5,
        "91,56%",
        "Akurasi Decision Tree",
        "Unggul +2,57% dari KNN (88,99%).",
    )
    add_metric_callout(
        s6,
        3.8,
        1.9,
        2.7,
        1.5,
        "87,32%",
        "Recall Dropout (DT)",
        "Unggul mutlak +12,67% (Kunci keselamatan).",
        dark_theme=True,
    )
    add_metric_callout(
        s6,
        6.8,
        1.9,
        2.7,
        1.5,
        "89,00%",
        "F1-Score (DT)",
        "Keseimbangan presisi & sensitivitas.",
    )
    add_metric_callout(
        s6,
        9.8,
        1.9,
        2.73,
        1.5,
        "0,9458",
        "ROC-AUC Score (DT)",
        "Kapabilitas diskriminasi probabilitas.",
    )

    c_tbl = s6.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(0.8),
        Inches(3.65),
        Inches(11.733),
        Inches(3.2),
    )
    c_tbl.fill.solid()
    c_tbl.fill.fore_color.rgb = C_CARD_BG
    c_tbl.line.color.rgb = C_BORDER
    c_tbl.line.width = Pt(1.5)
    tf_tb = c_tbl.text_frame
    tf_tb.word_wrap = True
    tf_tb.margin_left = tf_tb.margin_right = tf_tb.margin_top = tf_tb.margin_bottom = (
        Inches(0.3)
    )

    ptb_h = tf_tb.paragraphs[0]
    ptb_h.text = "RINGKASAN METRIK EVALUASI KOMPARATIF HEAD-TO-HEAD:"
    ptb_h.font.name = "Arial"
    ptb_h.font.size = Pt(12)
    ptb_h.font.bold = True
    ptb_h.font.color.rgb = C_INK
    ptb_h.space_after = Pt(8)

    tb_rows = [
        (
            "• Akurasi Keseluruhan: ",
            "Decision Tree 91,56%  vs  KNN 88,99% (Pemenang: Decision Tree)",
        ),
        (
            "• Precision Kelas Dropout: ",
            "Decision Tree 90,73%  vs  KNN 96,36% (Pemenang: KNN menghasilkan False Positive lebih sedikit)",
        ),
        (
            "• Recall Kelas Dropout (Metrik Kunci): ",
            "Decision Tree 87,32%  vs  KNN 74,65% (Pemenang Mutlak: Decision Tree menjaring 186 dari 213 mahasiswa DO)",
        ),
        (
            "• F1-Score (Harmonic Mean): ",
            "Decision Tree 89,00%  vs  KNN 84,13% (Pemenang: Decision Tree lebih stabil dan seimbang)",
        ),
        (
            "• Area Under Curve (ROC-AUC): ",
            "Decision Tree 0,9458  vs  KNN 0,9304 (Pemenang: Decision Tree memiliki pemisahan probabilitas lebih tajam)",
        ),
    ]
    for h_txt, b_txt in tb_rows:
        p = tf_tb.add_paragraph()
        r_h = p.add_run()
        r_h.text = h_txt
        r_h.font.bold = True
        r_h.font.size = Pt(11.5)
        r_h.font.color.rgb = C_INK
        r_b = p.add_run()
        r_b.text = b_txt
        r_b.font.size = Pt(11.5)
        r_b.font.color.rgb = C_BODY
        p.space_after = Pt(4)

    set_notes(
        s6,
        "Pada data uji murni 545 baris, Decision Tree mengalahkan KNN di hampir seluruh metrik: Akurasi 91,56% vs 88,99%, "
        "F1-Score 89% vs 84,1%, dan terutama Recall Dropout 87,32% vs 74,65%. Decision Tree menang mutlak.",
    )

    # ==================== SLIDE 7: CONFUSION MATRIX & RECALL ====================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s7, C_BG_PAGE)
    add_top_nav(
        s7,
        "Analisis Matriks Kebingungan: Mengapa Recall Kritis Bagi Kampus",
        "CONFUSION MATRIX",
    )

    fig_cm = "resource/ML/report/figures/confusion_matrices.png"
    if os.path.exists(fig_cm):
        frame_cm = s7.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(0.8),
            Inches(1.9),
            Inches(7.5),
            Inches(4.9),
        )
        frame_cm.fill.solid()
        frame_cm.fill.fore_color.rgb = C_CARD_BG
        frame_cm.line.color.rgb = C_BORDER
        s7.shapes.add_picture(fig_cm, Inches(0.95), Inches(2.05), width=Inches(7.2))

    c_cm_t = s7.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(8.55),
        Inches(1.9),
        Inches(3.98),
        Inches(4.9),
    )
    c_cm_t.fill.solid()
    c_cm_t.fill.fore_color.rgb = C_SURFACE_DARK
    c_cm_t.line.color.rgb = C_BORDER_DARK
    tf_cmt = c_cm_t.text_frame
    tf_cmt.word_wrap = True
    tf_cmt.margin_left = tf_cmt.margin_right = tf_cmt.margin_top = (
        tf_cmt.margin_bottom
    ) = Inches(0.3)

    pcm_h = tf_cmt.paragraphs[0]
    pcm_h.text = "BAHAYA FATAL FALSE NEGATIVE"
    pcm_h.font.bold = True
    pcm_h.font.size = Pt(13)
    pcm_h.font.color.rgb = C_TEXT_LIGHT
    pcm_h.space_after = Pt(10)

    pcm_b = tf_cmt.add_paragraph()
    pcm_b.text = (
        "Dari 213 mahasiswa DO aktual:\n\n"
        "• Decision Tree:\n"
        "  - True Positive: 186 mhs\n"
        "  - False Negative: HANYA 27 mhs luput\n\n"
        "• K-Nearest Neighbors:\n"
        "  - True Positive: 159 mhs\n"
        "  - False Negative: 54 MHS LUPUT!\n\n"
        "Konsekuensi Nyata:\n"
        "KNN meluputkan 54 mahasiswa berisiko (dua kali lipat lebih banyak). Mahasiswa ini tidak akan dipanggil konseling dan berujung putus studi."
    )
    pcm_b.font.size = Pt(11)
    pcm_b.font.color.rgb = C_MUTED_LIGHT

    set_notes(
        s7,
        "Confusion matrix memperlihatkan alasan utama kemenangan Decision Tree: dari 213 mahasiswa DO di data uji, Decision Tree hanya meluputkan 27 mahasiswa, "
        "sedangkan KNN meluputkan 54 mahasiswa. Bagi kampus, kehilangan 54 mahasiswa tanpa intervensi adalah kerugian institusional yang sangat besar.",
    )

    # ==================== SLIDE 8: ROC-AUC & FEATURE IMPORTANCE ====================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s8, C_BG_PAGE)
    add_top_nav(
        s8, "Kurva ROC-AUC & Transparansi Aturan (White-Box Tree)", "TRANSPARANSI MODEL"
    )

    fig_roc = "resource/ML/report/figures/roc_curve.png"
    if os.path.exists(fig_roc):
        frame_roc = s8.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(0.8),
            Inches(1.9),
            Inches(5.66),
            Inches(4.9),
        )
        frame_roc.fill.solid()
        frame_roc.fill.fore_color.rgb = C_CARD_BG
        frame_roc.line.color.rgb = C_BORDER
        s8.shapes.add_picture(fig_roc, Inches(0.95), Inches(2.05), width=Inches(5.36))

    fig_fi = "resource/ML/report/figures/feature_importance.png"
    if os.path.exists(fig_fi):
        frame_fi = s8.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(6.86),
            Inches(1.9),
            Inches(5.66),
            Inches(4.9),
        )
        frame_fi.fill.solid()
        frame_fi.fill.fore_color.rgb = C_CARD_BG
        frame_fi.line.color.rgb = C_BORDER
        s8.shapes.add_picture(fig_fi, Inches(7.01), Inches(2.05), width=Inches(5.36))

    set_notes(
        s8,
        "Kurva ROC-AUC membuktikan Decision Tree mencapai AUC 0,9458. Keunggulan terbesarnya adalah White-Box Feature Importance: "
        "faktor penentu utama adalah kelulusan SKS semester 2 & 1, tunggakan SPP, dan fitur rasio kelulusan tahun pertama yang kita rekayasa.",
    )

    # ==================== SLIDE 9: SIMULASI DEPLOYMENT 794 ENROLLED ====================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s9, C_BG_PAGE)
    add_top_nav(
        s9,
        "Simulasi Deployment: Peringatan Dini pada 794 Mahasiswa Aktif",
        "SIMULASI DEPLOYMENT",
    )

    fig_sim = "resource/ML/report/figures/risk_segmentation.png"
    if os.path.exists(fig_sim):
        frame_sim = s9.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(0.8),
            Inches(1.9),
            Inches(6.8),
            Inches(4.9),
        )
        frame_sim.fill.solid()
        frame_sim.fill.fore_color.rgb = C_CARD_BG
        frame_sim.line.color.rgb = C_BORDER
        s9.shapes.add_picture(fig_sim, Inches(0.95), Inches(2.05), width=Inches(6.5))

    c_sim_t = s9.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(7.85),
        Inches(1.9),
        Inches(4.68),
        Inches(4.9),
    )
    c_sim_t.fill.solid()
    c_sim_t.fill.fore_color.rgb = C_SURFACE_DARK
    c_sim_t.line.color.rgb = C_BORDER_DARK
    tf_simt = c_sim_t.text_frame
    tf_simt.word_wrap = True
    tf_simt.margin_left = tf_simt.margin_right = tf_simt.margin_top = (
        tf_simt.margin_bottom
    ) = Inches(0.3)

    psimt_h = tf_simt.paragraphs[0]
    psimt_h.text = "HASIL TRIAGE RISIKO MAHASISWA AKTIF:"
    psimt_h.font.bold = True
    psimt_h.font.size = Pt(12.5)
    psimt_h.font.color.rgb = C_TEXT_LIGHT
    psimt_h.space_after = Pt(10)

    sim_list = [
        (
            "• Zona Merah (Risiko Tinggi):\n",
            "362 Mahasiswa (45,59%)\nProbabilitas DO >= 70%. Memerlukan panggilan darurat BAAK dan restrukturisasi cicilan SPP.",
        ),
        (
            "• Zona Oranye (Risiko Sedang):\n",
            "142 Mahasiswa (17,88%)\nProbabilitas DO 40-69%. Memerlukan pemantauan berkala dosen wali dan asistensi SKS.",
        ),
        (
            "• Zona Hijau (Jalur Reguler Aman):\n",
            "290 Mahasiswa (36,52%)\nProbabilitas DO < 40%. Mahasiswa berada pada lintasan aman menuju kelulusan.",
        ),
    ]
    for h_txt, b_txt in sim_list:
        p = tf_simt.add_paragraph()
        r_h = p.add_run()
        r_h.text = h_txt
        r_h.font.bold = True
        r_h.font.size = Pt(11.5)
        r_h.font.color.rgb = C_TEXT_LIGHT
        r_b = p.add_run()
        r_b.text = b_txt
        r_b.font.size = Pt(11)
        r_b.font.color.rgb = C_MUTED_LIGHT
        p.space_after = Pt(8)

    set_notes(
        s9,
        "Pada tahap simulasi deployment, kami mengumpankan 794 data mahasiswa aktif ke model Decision Tree terbaik. Hasilnya: sistem menemukan "
        "362 mahasiswa (45,6%) berada di zona merah risiko tinggi yang memerlukan intervensi pembiayaan dan konseling segera.",
    )

    # ==================== SLIDE 10: REKOMENDASI MANAJERIAL ====================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s10, C_BG_PAGE)
    add_top_nav(
        s10, "Rekomendasi Kebijakan Manajerial & SOP Kampus", "REKOMENDASI MANAJERIAL"
    )

    cards_data = [
        (
            "01",
            "SOP Finansial Cepat Tanggap",
            "Restrukturisasi Cicilan SPP",
            "Mengingat tunggakan SPP memicu DO hingga 86,6%, kampus wajib membuka skema cicilan darurat bagi 362 mahasiswa zona merah sebelum registrasi ditutup permanen.",
        ),
        (
            "02",
            "Pendampingan Jalur M23",
            "Fleksibilitas Mahasiswa Dewasa",
            "Mahasiswa pendaftaran usia dewasa (>25 tahun) menghadapi konflik beban kerja. Kampus perlu menyediakan konsultasi malam dan mentoring adaptasi belajar.",
        ),
        (
            "03",
            "Dashboard Monitoring SIAKAD",
            "Peringatan Dini Real-Time",
            "Mengintegrasikan model Decision Tree ke SIAKAD kampus agar dosen wali menerima risk alert otomatis jika mahasiswa gagal lulus >50% SKS di semester 1.",
        ),
    ]
    for idx, (num_str, title, subtitle, desc) in enumerate(cards_data):
        c = s10.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(0.8 + idx * 4.0),
            Inches(1.9),
            Inches(3.733),
            Inches(5.0),
        )
        c.fill.solid()
        c.fill.fore_color.rgb = C_CARD_BG
        c.line.color.rgb = C_BORDER
        c.line.width = Pt(1.5)
        tf_c = c.text_frame
        tf_c.word_wrap = True
        tf_c.margin_left = tf_c.margin_right = tf_c.margin_top = tf_c.margin_bottom = (
            Inches(0.3)
        )

        p0 = tf_c.paragraphs[0]
        p0.text = num_str
        p0.font.name = "Arial Black"
        p0.font.size = Pt(28)
        p0.font.bold = True
        p0.font.color.rgb = C_INK
        p0.space_after = Pt(2)

        p1 = tf_c.add_paragraph()
        p1.text = title
        p1.font.bold = True
        p1.font.size = Pt(13)
        p1.font.color.rgb = C_INK
        p1.space_after = Pt(2)

        p_sub = tf_c.add_paragraph()
        p_sub.text = subtitle
        p_sub.font.bold = True
        p_sub.font.size = Pt(11)
        p_sub.font.color.rgb = C_SLATE
        p_sub.space_after = Pt(8)

        p2 = tf_c.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(11.5)
        p2.font.color.rgb = C_BODY

    set_notes(
        s10,
        "Kami merumuskan 3 rekomendasi konkret bagi pimpinan kampus: restrukturisasi SPP darurat untuk 362 mahasiswa zona merah, "
        "program pendampingan khusus mahasiswa dewasa pekerja jalur M23, dan integrasi dashboard peringatan dini ke SIAKAD.",
    )

    # ==================== SLIDE 11: KESIMPULAN AKHIR ====================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s11, C_BG_PAGE)
    add_top_nav(
        s11, "Kesimpulan Proyek: Kemenangan Mutlak Decision Tree", "KESIMPULAN AKHIR"
    )

    add_metric_callout(
        s11,
        0.8,
        1.9,
        3.64,
        1.5,
        "Decision Tree",
        "Pemenang Mutlak",
        "Unggul di Akurasi (91,6%), F1-Score (89,0%), dan Recall (87,3%).",
        dark_theme=True,
    )
    add_metric_callout(
        s11,
        4.84,
        1.9,
        3.64,
        1.5,
        "Recall 87,3%",
        "Menekan False Negative",
        "Hanya 27 DO luput berbanding 54 pada KNN (Penyelamat atrisi).",
    )
    add_metric_callout(
        s11,
        8.88,
        1.9,
        3.64,
        1.5,
        "White-Box",
        "Transparansi Aturan",
        "Aturan IF-THEN mudah diaudit langsung oleh dosen wali tanpa coding.",
    )

    c_con = s11.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(0.8),
        Inches(3.65),
        Inches(11.733),
        Inches(3.2),
    )
    c_con.fill.solid()
    c_con.fill.fore_color.rgb = C_CARD_BG
    c_con.line.color.rgb = C_BORDER
    c_con.line.width = Pt(1.5)
    tf_co = c_con.text_frame
    tf_co.word_wrap = True
    tf_co.margin_left = tf_co.margin_right = tf_co.margin_top = tf_co.margin_bottom = (
        Inches(0.3)
    )

    pco_h = tf_co.paragraphs[0]
    pco_h.text = "TIGA KONTRIBUSI UTAMA PROYEK AKHIR MACHINE LEARNING INI:"
    pco_h.font.bold = True
    pco_h.font.size = Pt(13)
    pco_h.font.color.rgb = C_INK
    pco_h.space_after = Pt(8)

    con_points = [
        (
            "1. Keberhasilan Metodologi Bebas Data Leakage: ",
            "Pemisahan sampel definitif 3.630, rekayasa 4 fitur rasio SKS, dan partisi 3-arah 70:15:15 membuktikan integritas validasi ilmiah.",
        ),
        (
            "2. Pembuktian Empiris Superioritas Decision Tree: ",
            "Decision Tree membuktikan diri sebagai model terbaik untuk sistem peringatan dini kampus karena mengoptimalkan Recall kelas Dropout tanpa manipulasi sintetis SMOTE.",
        ),
        (
            "3. Manfaat Nyata Operasional Kampus: ",
            "Simulasi pada 794 mahasiswa aktif membuktikan kesiapan model untuk dideploy langsung ke lingkungan SIAKAD perguruan tinggi.",
        ),
    ]
    for h_txt, b_txt in con_points:
        p = tf_co.add_paragraph()
        r_h = p.add_run()
        r_h.text = h_txt
        r_h.font.bold = True
        r_h.font.size = Pt(12)
        r_h.font.color.rgb = C_INK
        r_b = p.add_run()
        r_b.text = b_txt
        r_b.font.size = Pt(11.5)
        r_b.font.color.rgb = C_BODY
        p.space_after = Pt(6)

    set_notes(
        s11,
        "Kesimpulan akhir kami: Decision Tree adalah pemenang mutlak karena unggul di seluruh metrik kritis dan bersifat White-Box. "
        "Model ini siap diintegrasikan sebagai sistem deteksi dini nyata di kampus.",
    )

    # ==================== SLIDE 12: CLOSING HERO (DARK) ====================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s12, C_OBSIDIAN)

    badge12 = s12.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(0.8),
        Inches(1.5),
        Inches(2.8),
        Inches(0.35),
    )
    badge12.fill.solid()
    badge12.fill.fore_color.rgb = C_SURFACE_DARK
    badge12.line.color.rgb = C_BORDER_DARK
    tf_b12 = badge12.text_frame
    tf_b12.margin_top = Inches(0.05)
    pb12 = tf_b12.paragraphs[0]
    pb12.text = "SESI AKHIR SIDANG PROJECT"
    pb12.font.name = "Arial"
    pb12.font.size = Pt(9)
    pb12.font.bold = True
    pb12.font.color.rgb = C_TEXT_LIGHT
    pb12.alignment = PP_ALIGN.CENTER

    t_box12 = s12.shapes.add_textbox(
        Inches(0.8), Inches(2.1), Inches(11.733), Inches(2.2)
    )
    tf12 = t_box12.text_frame
    tf12.word_wrap = True
    p12 = tf12.paragraphs[0]
    p12.text = "Terima Kasih.\nSesi Tanya & Jawab (Q&A)"
    p12.font.name = "Arial"
    p12.font.size = Pt(36)
    p12.font.bold = True
    p12.font.color.rgb = C_TEXT_LIGHT
    p12.space_after = Pt(12)

    p12_sub = tf12.add_paragraph()
    p12_sub.text = (
        "Project Akhir Machine Learning: Prediksi Keberhasilan Akademik Mahasiswa\n"
        "Teknik Informatika, Fakultas Teknik, Universitas Trunojoyo Madura (2026)\n\n"
        "Ketua Kelompok: Achmad Ridho Fa'iz (NIM: 230411100197)  |  Dosen Pengampu: Ach. Khozaimi, S.Kom., M.Kom."
    )
    p12_sub.font.name = "Arial"
    p12_sub.font.size = Pt(13)
    p12_sub.font.color.rgb = C_MUTED_LIGHT

    set_notes(
        s12,
        "Demikian pemaparan hasil akhir komputasi dan implementasi proyek Machine Learning kami. "
        "Kami menyambut baik kritik, saran, masukan, dan pertanyaan dari Bapak Dosen Penguji serta rekan-rekan mahasiswa. Terima kasih.",
    )

    prs.save(output_pptx)
    print(f"Final presentation PPTX successfully created at: {output_pptx}")


def generate_and_convert_presentation(
    output_pptx: str, output_pdf: str, preview_dir: str
) -> None:
    os.makedirs(os.path.dirname(output_pptx), exist_ok=True)
    os.makedirs(preview_dir, exist_ok=True)

    create_report_presentation(output_pptx)

    # Convert to PDF
    cmd_pdf = (
        f"libreoffice -env:UserInstallation=file:///tmp/libreoffice_conv "
        f"--headless --convert-to pdf {output_pptx} --outdir {os.path.dirname(output_pptx)}"
    )
    os.system(cmd_pdf)

    # Render PNG previews
    cmd_ppm = f"pdftoppm -png -r 120 {output_pdf} {os.path.join(preview_dir, 'slide')}"
    os.system(cmd_ppm)
    print(f"Presentation PDF and preview PNGs successfully generated in: {preview_dir}")


if __name__ == "__main__":
    out_pptx = "resource/ML/report/Presentasi-Sidang-ML-230411100197.pptx"
    out_pdf = "resource/ML/report/Presentasi-Sidang-ML-230411100197.pdf"
    prev_dir = "resource/ML/report/previews"
    generate_and_convert_presentation(out_pptx, out_pdf, prev_dir)
