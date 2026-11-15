"""Script to generate the official Machine Learning Final Report (.docx and .pdf).

Adhering strictly to UTM Academic Writing Governance & Course Assignment Guidelines:
- Paper: A4, Margins: 4-3-3-3 cm (Left 4.0 cm, Top 3.0 cm, Right 3.0 cm, Bottom 3.0 cm)
- Typography: Times New Roman, 12 pt body, 1.5 spacing, justify alignment, 1.0 cm indent
- Formal UTM Elements:
  * Front Matter: Cover page (clean, no printed page num) + Daftar Isi (Page ii) with dot leaders
  * Dynamic Page Numbering: Lower Roman for front matter, Decimal Arabic (1, 2, 3...) for body
  * Team format: 2-person group (Achmad Ridho Fa'iz as Ketua + Rekan Kelompok)
  * Tables with titles on TOP (Tabel 3.1, Tabel 3.2, Tabel 4.1, Tabel 4.2)
  * Figures with captions on BOTTOM (Gambar 4.1 to Gambar 4.6)
  * Strict IEEE style references [1] through [7] with contextual in-text citations
  * 5 Canonical Chapters (BAB I s.d. BAB V) reflecting real computation from Report.ipynb
"""

import os
from typing import Any, cast

from docx import Document
from docx.document import Document as DocObject
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
from docx.shared import Cm, Pt, RGBColor


def set_cell_margins(
    cell: Any, top: int = 80, bottom: int = 80, left: int = 120, right: int = 120
) -> None:
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement("w:tcMar")
    for m, val in [
        ("w:top", top),
        ("w:bottom", bottom),
        ("w:left", left),
        ("w:right", right),
    ]:
        node = OxmlElement(m)
        node.set(qn("w:w"), str(val))
        node.set(qn("w:type"), "dxa")
        tcMar.append(node)
    tcPr.append(tcMar)


def set_cell_shading(cell: Any, color_hex: str) -> None:
    shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading)


def setup_footer_page_number(section: Any) -> None:
    footer = section.footer
    p = footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    r = p.add_run()
    r.font.name = "Times New Roman"
    r.font.size = Pt(10.5)

    fld1 = OxmlElement("w:fldChar")
    fld1.set(qn("w:fldCharType"), "begin")
    ins = OxmlElement("w:instrText")
    ins.set(qn("xml:space"), "preserve")
    ins.text = "PAGE"
    fld2 = OxmlElement("w:fldChar")
    fld2.set(qn("w:fldCharType"), "separate")
    fld3 = OxmlElement("w:fldChar")
    fld3.set(qn("w:fldCharType"), "end")

    r._r.append(fld1)
    r._r.append(ins)
    r._r.append(fld2)
    r._r.append(fld3)


def add_toc_line(
    doc: DocObject,
    title: str,
    page_str: str,
    level: int = 1,
    bold: bool = False,
) -> None:
    p = doc.add_paragraph()
    p.paragraph_format.tab_stops.add_tab_stop(
        Cm(14.0), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS
    )
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_before = Pt(1.5)
    p.paragraph_format.space_after = Pt(1.5)

    if level == 2:
        p.paragraph_format.left_indent = Cm(0.6)
    elif level == 3:
        p.paragraph_format.left_indent = Cm(1.2)
    else:
        p.paragraph_format.left_indent = Cm(0)

    r_title = p.add_run(title)
    r_title.bold = bold
    r_title.font.name = "Times New Roman"
    r_title.font.size = Pt(11)

    r_tab = p.add_run(f"\t{page_str}")
    r_tab.bold = bold
    r_tab.font.name = "Times New Roman"
    r_tab.font.size = Pt(11)


def build_report_document(toc_page_map: dict[str, str] | None = None) -> DocObject:
    if toc_page_map is None:
        toc_page_map = {
            "BAB I": "1",
            "1.1": "1",
            "1.2": "2",
            "1.3": "3",
            "1.4": "3",
            "BAB II": "4",
            "2.1": "4",
            "2.2": "4",
            "2.3": "5",
            "2.4": "6",
            "2.5": "7",
            "BAB III": "8",
            "3.1": "8",
            "3.2": "9",
            "3.3": "10",
            "3.4": "11",
            "3.5": "11",
            "BAB IV": "13",
            "4.1": "13",
            "4.2": "14",
            "4.3": "15",
            "4.4": "16",
            "4.5": "17",
            "BAB V": "19",
            "5.1": "19",
            "5.2": "20",
            "5.3": "21",
            "DAFTAR PUSTAKA": "22",
        }

    doc = Document()

    # ==================== SECTION 1: FRONT MATTER ====================
    sec1 = doc.sections[0]
    sec1.page_width = Cm(21.0)
    sec1.page_height = Cm(29.7)
    sec1.left_margin = Cm(4.0)
    sec1.top_margin = Cm(3.0)
    sec1.right_margin = Cm(3.0)
    sec1.bottom_margin = Cm(3.0)

    # Different first page to hide page number on cover
    sec1.different_first_page_header_footer = True
    sectPr1 = sec1._sectPr
    pgNum1 = OxmlElement("w:pgNumType")
    pgNum1.set(qn("w:fmt"), "lowerRoman")
    sectPr1.append(pgNum1)
    setup_footer_page_number(sec1)

    # Base Normal Style
    normal_style = cast(Any, doc.styles["Normal"])
    normal_style.font.name = "Times New Roman"
    normal_style.font.size = Pt(12)
    normal_style.font.color.rgb = RGBColor(0, 0, 0)
    normal_style.paragraph_format.line_spacing = 1.5
    normal_style.paragraph_format.space_after = Pt(0)
    normal_style.paragraph_format.space_before = Pt(0)

    # Cover Page Content
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(8)
    p_title.paragraph_format.line_spacing = 1.15

    r1 = p_title.add_run("LAPORAN AKHIR PROJECT MACHINE LEARNING\n")
    r1.bold = True
    r1.font.name = "Times New Roman"
    r1.font.size = Pt(14)
    r1.font.color.rgb = RGBColor(0, 0, 0)

    r2 = p_title.add_run(
        "PREDIKSI KEBERHASILAN AKADEMIK DAN DETEKSI DINI RISIKO PUTUS STUDI (DROPOUT) MAHASISWA "
        "MENGGUNAKAN KOMPARASI DECISION TREE DAN K-NEAREST NEIGHBORS"
    )
    r2.bold = True
    r2.font.name = "Times New Roman"
    r2.font.size = Pt(13)
    r2.font.color.rgb = RGBColor(0, 0, 0)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(8)
    p_sub.paragraph_format.space_after = Pt(18)
    r_sub = p_sub.add_run(
        "Disusun untuk Memenuhi Tugas Akhir Mata Kuliah Machine Learning (Kelas A)\n"
        "Dosen Pengampu: Ach. Khozaimi, S.Kom., M.Kom."
    )
    r_sub.font.name = "Times New Roman"
    r_sub.font.size = Pt(10.5)
    r_sub.font.italic = True

    # Logo UTM
    logo_path = "resource/ML/report/figures/logo_utm.jpg"
    if not os.path.exists(logo_path):
        logo_path = "resource/ML/proposal/figures/logo_utm.jpg"

    if os.path.exists(logo_path):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_before = Pt(6)
        p_logo.paragraph_format.space_after = Pt(20)
        p_logo.add_run().add_picture(logo_path, width=Cm(4.8))

    # Authors block
    p_auth = doc.add_paragraph()
    p_auth.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_auth.paragraph_format.space_before = Pt(10)
    p_auth.paragraph_format.space_after = Pt(24)
    p_auth.paragraph_format.line_spacing = 1.15

    r_by = p_auth.add_run("Disusun Oleh (Kelompok):\n")
    r_by.font.name = "Times New Roman"
    r_by.font.size = Pt(11)
    r_by.bold = True

    r_names = p_auth.add_run(
        "1. Achmad Ridho Fa'iz (NIM: 230411100197) — Ketua Kelompok\n"
        "2. [Nama Rekan Kelompok] (NIM: [NIM Rekan Kelompok]) — Anggota Kelompok"
    )
    r_names.font.name = "Times New Roman"
    r_names.font.size = Pt(11)

    # Institution block
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_before = Pt(16)
    p_inst.paragraph_format.space_after = Pt(0)
    p_inst.paragraph_format.line_spacing = 1.15

    r_inst = p_inst.add_run(
        "PROGRAM STUDI S1 TEKNIK INFORMATIKA\n"
        "FAKULTAS TEKNIK\n"
        "UNIVERSITAS TRUNOJOYO MADURA\n"
        "2026"
    )
    r_inst.bold = True
    r_inst.font.name = "Times New Roman"
    r_inst.font.size = Pt(12)

    # ==================== DAFTAR ISI (PAGE ii) ====================
    doc.add_page_break()

    p_toc_head = doc.add_paragraph()
    p_toc_head.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_toc_head.paragraph_format.space_before = Pt(0)
    p_toc_head.paragraph_format.space_after = Pt(18)
    r_th = p_toc_head.add_run("DAFTAR ISI")
    r_th.bold = True
    r_th.font.name = "Times New Roman"
    r_th.font.size = Pt(14)

    add_toc_line(doc, "HALAMAN JUDUL", "i", level=1, bold=True)
    add_toc_line(doc, "DAFTAR ISI", "ii", level=1, bold=True)

    add_toc_line(
        doc,
        "BAB I PENDAHULUAN",
        toc_page_map.get("BAB I", "1"),
        level=1,
        bold=True,
    )
    add_toc_line(
        doc,
        "1.1 Latar Belakang",
        toc_page_map.get("1.1", "1"),
        level=2,
        bold=False,
    )
    add_toc_line(
        doc,
        "1.2 Rumusan Masalah",
        toc_page_map.get("1.2", "2"),
        level=2,
        bold=False,
    )
    add_toc_line(
        doc,
        "1.3 Tujuan Project",
        toc_page_map.get("1.3", "3"),
        level=2,
        bold=False,
    )
    add_toc_line(
        doc,
        "1.4 Manfaat Project",
        toc_page_map.get("1.4", "3"),
        level=2,
        bold=False,
    )

    add_toc_line(
        doc,
        "BAB II KAJIAN PUSTAKA DAN LANDASAN TEORI",
        toc_page_map.get("BAB II", "4"),
        level=1,
        bold=True,
    )
    add_toc_line(
        doc,
        "2.1 Educational Data Mining & Deteksi Dini Atrisi",
        toc_page_map.get("2.1", "4"),
        level=2,
        bold=False,
    )
    add_toc_line(
        doc,
        "2.2 Supervised Binary Classification vs Regression",
        toc_page_map.get("2.2", "4"),
        level=2,
        bold=False,
    )
    add_toc_line(
        doc,
        "2.3 Algoritma Decision Tree (CART)",
        toc_page_map.get("2.3", "5"),
        level=2,
        bold=False,
    )
    add_toc_line(
        doc,
        "2.4 Algoritma K-Nearest Neighbors (KNN)",
        toc_page_map.get("2.4", "6"),
        level=2,
        bold=False,
    )
    add_toc_line(
        doc,
        "2.5 Metrik Evaluasi Diagnostik & The Accuracy Trap",
        toc_page_map.get("2.5", "7"),
        level=2,
        bold=False,
    )

    add_toc_line(
        doc,
        "BAB III METODOLOGI DAN PREPROCESSING DATA",
        toc_page_map.get("BAB III", "8"),
        level=1,
        bold=True,
    )
    add_toc_line(
        doc,
        "3.1 Gambaran Umum Dataset",
        toc_page_map.get("3.1", "8"),
        level=2,
        bold=False,
    )
    add_toc_line(
        doc,
        "3.2 Isolasi Sampel Transisi Enrolled & Formulasi Target Biner Definitif",
        toc_page_map.get("3.2", "9"),
        level=2,
        bold=False,
    )
    add_toc_line(
        doc,
        "3.3 Rekayasa Fitur Rasio Akademik",
        toc_page_map.get("3.3", "10"),
        level=2,
        bold=False,
    )
    add_toc_line(
        doc,
        "3.4 Desain Partisi 3-Arah Berstrata 70:15:15 Bebas Kebocoran Data",
        toc_page_map.get("3.4", "11"),
        level=2,
        bold=False,
    )
    add_toc_line(
        doc,
        "3.5 Arsitektur Dual Preprocessing Pipeline",
        toc_page_map.get("3.5", "11"),
        level=2,
        bold=False,
    )

    add_toc_line(
        doc,
        "BAB IV HASIL EKSPERIMEN DAN PEMBAHASAN KOMPARATIF",
        toc_page_map.get("BAB IV", "13"),
        level=1,
        bold=True,
    )
    add_toc_line(
        doc,
        "4.1 Hyperparameter Tuning pada Data Validasi",
        toc_page_map.get("4.1", "13"),
        level=2,
        bold=False,
    )
    add_toc_line(
        doc,
        "4.2 Evaluasi Komparatif pada Data Uji Murni",
        toc_page_map.get("4.2", "14"),
        level=2,
        bold=False,
    )
    add_toc_line(
        doc,
        "4.3 Analisis Matriks Kebingungan (Confusion Matrix) & Trade-off Error",
        toc_page_map.get("4.3", "15"),
        level=2,
        bold=False,
    )
    add_toc_line(
        doc,
        "4.4 Kurva ROC-AUC & Transparansi Feature Importance",
        toc_page_map.get("4.4", "16"),
        level=2,
        bold=False,
    )
    add_toc_line(
        doc,
        "4.5 Simulasi Peringatan Dini pada 794 Mahasiswa Aktif",
        toc_page_map.get("4.5", "17"),
        level=2,
        bold=False,
    )

    add_toc_line(
        doc,
        "BAB V KESIMPULAN DAN REKOMENDASI MANAJERIAL",
        toc_page_map.get("BAB V", "19"),
        level=1,
        bold=True,
    )
    add_toc_line(
        doc,
        "5.1 Kesimpulan Hasil Eksperimen",
        toc_page_map.get("5.1", "19"),
        level=2,
        bold=False,
    )
    add_toc_line(
        doc,
        "5.2 Rekomendasi Kebijakan & SOP Manajerial Kampus",
        toc_page_map.get("5.2", "20"),
        level=2,
        bold=False,
    )
    add_toc_line(
        doc,
        "5.3 Saran Pengembangan Sistem Selanjutnya",
        toc_page_map.get("5.3", "21"),
        level=2,
        bold=False,
    )

    add_toc_line(
        doc,
        "DAFTAR PUSTAKA",
        toc_page_map.get("DAFTAR PUSTAKA", "22"),
        level=1,
        bold=True,
    )

    # ==================== SECTION 2: BODY (BAB I s.d. DAFTAR PUSTAKA) ====================
    sec2 = doc.add_section()
    sec2.page_width = Cm(21.0)
    sec2.page_height = Cm(29.7)
    sec2.left_margin = Cm(4.0)
    sec2.top_margin = Cm(3.0)
    sec2.right_margin = Cm(3.0)
    sec2.bottom_margin = Cm(3.0)
    sec2.header.is_linked_to_previous = False
    sec2.footer.is_linked_to_previous = False

    sectPr2 = sec2._sectPr
    pgNum2 = OxmlElement("w:pgNumType")
    pgNum2.set(qn("w:fmt"), "decimal")
    pgNum2.set(qn("w:start"), "1")
    sectPr2.append(pgNum2)
    setup_footer_page_number(sec2)

    def add_heading_1(title: str) -> None:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(12)
        p.paragraph_format.line_spacing = 1.15
        r = p.add_run(title)
        r.bold = True
        r.font.name = "Times New Roman"
        r.font.size = Pt(14)

    def add_heading_2(title: str) -> None:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        r = p.add_run(title)
        r.bold = True
        r.font.name = "Times New Roman"
        r.font.size = Pt(12)

    def add_heading_3(title: str) -> None:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.15
        r = p.add_run(title)
        r.bold = True
        r.font.name = "Times New Roman"
        r.font.size = Pt(11)

    def add_body(text: str, indent: bool = True) -> None:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(4)
        if indent:
            p.paragraph_format.first_line_indent = Cm(1.0)
        r = p.add_run(text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(12)

    def add_bullet(lead: str, text: str) -> None:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.left_indent = Cm(1.0)
        p.paragraph_format.first_line_indent = Cm(-0.5)

        r_l = p.add_run(f"• {lead}")
        r_l.bold = True
        r_l.font.name = "Times New Roman"
        r_l.font.size = Pt(11)

        r_t = p.add_run(text)
        r_t.font.name = "Times New Roman"
        r_t.font.size = Pt(11)

    def add_figure(fig_path: str, caption: str, width_cm: float = 13.5) -> None:
        if os.path.exists(fig_path):
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(6)
            p_img.paragraph_format.space_after = Pt(3)
            p_img.add_run().add_picture(fig_path, width=Cm(width_cm))

            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_before = Pt(0)
            p_cap.paragraph_format.space_after = Pt(8)
            r_cap = p_cap.add_run(caption)
            r_cap.font.name = "Times New Roman"
            r_cap.font.size = Pt(10)
            r_cap.font.italic = True

    # ==================== BAB I. PENDAHULUAN ====================
    add_heading_1("BAB I\nPENDAHULUAN")

    add_heading_2("1.1 Latar Belakang")
    add_body(
        "Tingginya angka putus studi (student dropout) merupakan salah satu ancaman sistemik paling kritis yang dihadapi "
        "oleh perguruan tinggi di seluruh dunia. Fenomena atrisi mahasiswa ini tidak hanya merugikan individu mahasiswa dari segi masa depan karier "
        "dan psikososial, tetapi juga mendegradasi reputasi akademik institusi, menurunkan angka efisiensi edukasi, serta menimbulkan kerugian finansial "
        "institusional yang substansial akibat hilangnya potensi perolehan Sumbangan Pembinaan Pendidikan (SPP) berkelanjutan. "
        "Dalam tata kelola universitas modern, pencegahan putus studi menuntut transformasi dari pendekatan birokrasi reaktif menjadi sistem deteksi dini "
        "yang proaktif dan preventif [1]."
    )
    add_body(
        "Kajian literatur Educational Data Mining (EDM) menunjukkan bahwa peristiwa putus studi jarang terjadi secara spontan atau tiba-tiba. "
        "Sebaliknya, atrisi merupakan proses penurunan keterlibatan (disengagement) bertahap yang jejak gejalanya telah terekam secara jelas "
        "sejak semester-semester awal perkuliahan, seperti akumulasi beban SKS yang tidak lulus, anjloknya indeks prestasi, penunggakan cicilan uang kuliah, "
        "hingga kerentanan sosio-demografis [2]. Sayangnya, data historis yang melimpah pada sistem informasi akademik kampus acap kali hanya berakhir "
        "sebagai arsip administratif pasif tanpa diolah menjadi wawasan prediktif yang bernilai strategis."
    )
    add_body(
        "Oleh karena itu, proyek akhir ini memanfaatkan kekuatan metodologi Machine Learning terawasi (Supervised Learning) untuk membangun "
        "sistem peringatan dini (Early Warning System) keberhasilan studi mahasiswa. Menggunakan dataset rujukan internasional dari UCI Machine Learning Repository "
        "berjudul 'Predict Students' Dropout and Academic Success' (Martins et al., 2021) [1], penelitian ini membandingkan dua paradigma pembelajaran "
        "yang saling melengkapi: algoritma pohon keputusan Decision Tree (CART) yang mengedepankan interpretabilitas aturan hierarkis berbasis logika IF-THEN, "
        "dan algoritma berbasis memori tetangga terdekat K-Nearest Neighbors (KNN) yang menangkap batas keputusan non-linear berbasis kemiripan profil holistik mahasiswa."
    )

    add_heading_2("1.2 Rumusan Masalah")
    add_body(
        "Berdasarkan latar belakang krisis atrisi di atas, rumusan masalah dalam proyek akhir ini ditetapkan sebagai berikut:",
        indent=False,
    )
    add_bullet(
        "1. Identifikasi Faktor Risiko Determinan: ",
        "Variabel kurikuler, finansial, dan demografis manakah yang memiliki bobot kepentingan tertinggi (feature importance) "
        "dalam memicu kegagalan studi mahasiswa?",
    )
    add_bullet(
        "2. Evaluasi Kinerja Komparatif Model: ",
        "Bagaimana perbandingan performa empiris antara Decision Tree dan K-Nearest Neighbors pada data uji murni bebas kebocoran (test set 15%), "
        "khususnya pada metrik sensitivitas Recall dan F1-Score pada kelas berisiko tinggi (Dropout)?",
    )
    add_bullet(
        "3. Efektivitas Simulasi Sistem Deteksi Dini: ",
        "Seberapa efektif model klasifikasi terbaik dalam memetakan tingkat risiko (triage) pada 794 data mahasiswa aktif (Enrolled) "
        "guna memicu Standard Operating Procedure (SOP) intervensi manajerial kampus?",
    )

    add_heading_2("1.3 Tujuan Project")
    add_body(
        "Tujuan yang dicapai melalui pengerjaan proyek akhir Machine Learning ini mencakup:",
        indent=False,
    )
    add_bullet(
        "1. Membangun Pipeline Klasifikasi Biner Terstandarisasi: ",
        "Mengembangkan alur komputasi mandiri dari penyaringan 3.630 data biner definitif, rekayasa 4 fitur rasio akademik, "
        "partisi 3-arah berstrata (70:15:15), hingga arsitektur Dual Preprocessing Pipeline.",
    )
    add_bullet(
        "2. Menemukan Hyperparameter Optimal Bebas Data Leakage: ",
        "Melakukan penalaan sistematis parameter kedalaman max_depth pada Decision Tree dan jumlah tetangga K pada KNN murni pada data validasi.",
    )
    add_bullet(
        "3. Membuktikan Kemenangan Model & Merumuskan SOP Manajerial: ",
        "Mengevaluasi kedua model pada data uji independen untuk membuktikan keunggulan Decision Tree dalam menekan angka False Negative, "
        "serta mensimulasikan sistem deteksi dini bagi 794 mahasiswa aktif.",
    )

    add_heading_2("1.4 Manfaat Project")
    add_body(
        "Manfaat yang dihasilkan dari proyek akhir ini terbagi ke dalam dimensi praktis dan akademis:",
        indent=False,
    )
    add_bullet(
        "1. Bagi Pimpinan Universitas & BAAK: ",
        "Menyediakan landasan analitik berbasis bukti untuk mengalokasikan anggaran beasiswa darurat dan restrukturisasi cicilan SPP secara proaktif.",
    )
    add_bullet(
        "2. Bagi Dosen Wali (Pembimbing Akademik): ",
        "Memperoleh instrumen deteksi dini transparan (White-Box rules) untuk memetakan mahasiswa bimbingan yang membutuhkan konseling intensif.",
    )
    add_bullet(
        "3. Bagi Mahasiswa: ",
        "Memperoleh kesempatan intervensi akademik dan finansial sedini mungkin sebelum terlanjur dijatuhi sanksi pemutusan hak studi permanen.",
    )

    # ==================== BAB II. KAJIAN PUSTAKA & METODE ====================
    doc.add_page_break()
    add_heading_1("BAB II\nKAJIAN PUSTAKA DAN LANDASAN TEORI")

    add_heading_2("2.1 Educational Data Mining & Deteksi Dini Atrisi")
    add_body(
        "Educational Data Mining (EDM) merupakan disiplin keilmuan yang berkembang pesat dalam menganalisis data riil "
        "dari lingkungan institusi pendidikan guna memahami karakteristik belajar mahasiswa dan pola keberlanjutan studi [2]. "
        "Penelitian acuan oleh Martins et al. (2021) [1] pada institusi pendidikan tinggi Instituto Politécnico de Portalegre, Portugal, "
        "membuktikan bahwa integrasi data multi-sumber (sosial-ekonomi, pendaftaran, dan catatan nilai per semester) mampu mendeteksi potensi "
        "kegagalan studi dengan tingkat akurasi tinggi. Atrisi mahasiswa di perguruan tinggi dicirikan oleh dua mekanisme pemicu utama: "
        "kendala finansial yang termanifestasi dalam penunggakan SPP, serta defisit kompetensi kurikuler yang terlihat dari rasio kelulusan SKS semester pertama."
    )

    add_heading_2("2.2 Supervised Binary Classification vs Regression")
    add_body(
        "Salah satu keputusan arsitektural terpenting dalam penelitian ini adalah memformulasikan permasalahan ke dalam tugas "
        "Supervised Binary Classification (Klasifikasi Biner Terawasi) dan secara tegas menolak pendekatan Regression (Regresi). "
        "Penolakan terhadap pendekatan regresi didasari oleh tiga landasan teoritis dan praktis yang fundamental:"
    )
    add_bullet(
        "1. Sifat Alami Variabel Target Diskrit Nominal: ",
        "Kolom Target pada dataset berisi status administratif kualitatif: 'Graduate', 'Dropout', dan 'Enrolled'. Ini adalah label diskrit nominal, "
        "bukan besaran angka riil kontinu. Kita tidak bisa meregresikan kata 'Lulus' atau 'Dropout' karena tidak ada makna fisik atau interpretasi logis "
        "dari nilai kontinu seperti 'mahasiswa ini lulus 0,73' atau 'mahasiswa ini DO 1,45'.",
    )
    add_bullet(
        "2. Kebutuhan Intervensi Manajerial Kampus (Actionable Boundary): ",
        "Pihak biro kemahasiswaan dan dosen wali memerlukan batas keputusan (decision boundary) yang tegas untuk memicu Standard Operating Procedure (SOP) "
        "penanganan darurat. Model regresi yang sekadar memprediksi angka IPK akhir tidak secara langsung menjawab pertanyaan biner apakah mahasiswa bersangkutan "
        "akan bertahan di kampus atau keluar.",
    )
    add_bullet(
        "3. Pelanggaran Asumsi Matematis Regresi Linear: ",
        "Menerapkan model regresi pada target biner (Linear Probability Model) menghasilkan estimasi di luar probabilitas valid (< 0 atau > 1) "
        "serta melanggar asumsi homoskedastisitas residual. Sebaliknya, klasifikasi berbasis probabilitas posterior terkalibrasi memungkinkan sistem "
        "melakukan pemeringkatan risiko (risk triage) bertingkat secara presisi.",
    )

    add_heading_2("2.3 Algoritma Decision Tree (CART)")
    add_body(
        "Decision Tree (Classification and Regression Trees - CART) yang diperkenalkan oleh Breiman et al. (1984) [3] merupakan algoritma "
        "eager learning non-parametrik yang mempartisi ruang fitur secara rekursif menjadi subset-subset biner yang homogen. "
        "Pada setiap simpul internal, algoritma memilih fitur dan nilai pemisah (split point) terbaik yang memaksimalkan penurunan ketidakmurnian Gini (Gini Impurity):"
    )
    add_body(
        "Gini(D) = 1 - sum_{i=1}^{C} p_i^2",
        indent=True,
    )
    add_body(
        "Keunggulan utama Decision Tree terletak pada sifat transparansi interpretabilitasnya yang bersifat 'White Box'. "
        "Model menghasilkan pohon keputusan yang dapat diekstraksi menjadi seperangkat aturan IF-THEN konkret berbahasa alami yang dapat diverifikasi "
        "langsung oleh pemangku kepentingan akademik kampus tanpa memerlukan latar belakang matematika tingkat lanjut. Selain itu, Decision Tree "
        "kebal terhadap penskalaan fitur monotonik dan mampu memproses data campuran (kategorikal biner dan numerik kontinu) secara simultan."
    )

    add_heading_2("2.4 Algoritma K-Nearest Neighbors (KNN)")
    add_body(
        "K-Nearest Neighbors (Cover & Hart, 1967) [4] merupakan algoritma instance-based learning (lazy learner) yang menunda proses generalisasi "
        "hingga fase inferensi tiba. Untuk mengklasifikasikan sampel data baru, KNN mengukur kedekatan jarak geometris terhadap seluruh titik data latih "
        "menggunakan metrik jarak Euclidean dalam ruang d-dimensi:"
    )
    add_body(
        "d(x, z) = sqrt( sum_{j=1}^{d} (x_j - z_j)^2 )",
        indent=True,
    )
    add_body(
        "Kelas prediksi ditentukan melalui mekanisme pemungutan suara terbanyak (majority voting) atau pembobotan jarak terbalik (distance-weighted) "
        "dari K tetangga terdekat. KNN sangat efektif menangkap pola pengelompokan alami dan batas kelas non-linear yang kompleks. "
        "Namun, KNN memiliki kelemahan mendasar: sangat sensitif terhadap perbedaan skala fitur (curse of dimensionality) dan kode nominal fiktif, "
        "sehingga memerlukan standarisasi fitur (StandardScaler) ketat dan memiliki biaya komputasi inferensi yang lebih tinggi daripada Decision Tree."
    )

    add_heading_2("2.5 Metrik Evaluasi Diagnostik & The Accuracy Trap")
    add_body(
        "Pada populasi 3.630 data biner definitif, terdapat ketidakseimbangan kelas moderat: 2.209 mahasiswa Lulus (60,85%) dan 1.421 mahasiswa DO (39,15%) "
        "(rasio 1,55 : 1). Kondisi ini menimbulkan bahaya metodologis yang disebut The Accuracy Trap [6]. Jika model bersikap naif dengan selalu memprediksi "
        "setiap mahasiswa akan 'Lulus' (Dummy Baseline), model tersebut akan memperoleh akurasi semu sebesar 60,85% padahal gagal mendeteksi 1 orang pun mahasiswa DO (Recall = 0%)."
    )
    add_body(
        "Dalam aplikasi sistem deteksi dini institusional, biaya kesalahan prediksi tidaklah setara (asymmetric cost matrix). "
        "Kesalahan False Negative (mahasiswa yang sebenarnya akan DO namun diprediksi Lulus oleh sistem) memiliki dampak institusional fatal karena kampus kehilangan "
        "kesempatan menyelamatkan mahasiswa tersebut. Sebaliknya, kesalahan False Positive (mahasiswa lulus yang terprediksi DO) hanya memicu pemanggilan konseling yang "
        "tetap bernilai positif bagi pembinaan mahasiswa. Oleh karena itu, penelitian ini menetapkan metrik Recall pada kelas Dropout dan F1-Score sebagai kriteria utama evaluasi."
    )

    # ==================== BAB III. METODOLOGI & PREPROCESSING ====================
    doc.add_page_break()
    add_heading_1("BAB III\nMETODOLOGI DAN PREPROCESSING DATA")

    add_heading_2("3.1 Gambaran Umum Dataset")
    add_body(
        "Dataset penelitian bersumber dari UCI Machine Learning Repository yang dipublikasikan oleh Valentim Realinho, Mónica V. Martins, Jorge Machado, "
        "dan Luís Baptista dari Instituto Politécnico de Portalegre, Portugal [1]. Dataset mencakup 4.424 baris data mahasiswa dengan 36 atribut prediktor "
        "yang terbagi ke dalam 3 dimensi informasi: demografis (usia, jenis kelamin, status pernikahan), sosial-ekonomi (kualifikasi dan pekerjaan orang tua, "
        "kondisi ekonomi makro), dan performa kurikuler akademik (SKS terdaftar, SKS dievaluasi, SKS disetujui, dan nilai pada semester 1 dan semester 2)."
    )

    # Tabel 3.1
    p_t31 = doc.add_paragraph()
    p_t31.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_t31.paragraph_format.space_before = Pt(8)
    p_t31.paragraph_format.space_after = Pt(3)
    r_t31 = p_t31.add_run(
        "Tabel 3.1 Distribusi Komposisi Status Mahasiswa pada Dataset Mentah UCI"
    )
    r_t31.bold = True
    r_t31.font.name = "Times New Roman"
    r_t31.font.size = Pt(10.5)

    tbl_raw = doc.add_table(rows=5, cols=4)
    tbl_raw.alignment = WD_TABLE_ALIGNMENT.CENTER
    raw_data = [
        (
            "Status Kelulusan (Target)",
            "Jumlah Baris (Mahasiswa)",
            "Proporsi (%)",
            "Peranan dalam Proyek Machine Learning",
        ),
        (
            "Graduate (Lulus)",
            "2.209 mahasiswa",
            "49,93%",
            "Kelas Negatif (0) pada pemodelan klasifikasi biner definitif",
        ),
        (
            "Dropout (Putus Studi)",
            "1.421 mahasiswa",
            "32,12%",
            "Kelas Positif Risiko (1) yang diprioritaskan deteksi dininya",
        ),
        (
            "Enrolled (Mahasiswa Aktif)",
            "794 mahasiswa",
            "17,95%",
            "Diisolasi murni sebagai kolam simulasi inferensi intervensi kampus",
        ),
        (
            "Total Dataset Mentah",
            "4.424 mahasiswa",
            "100,00%",
            "Populasi data mentah awal sebelum proses partisi dan pemisahan",
        ),
    ]
    for r_idx, row in enumerate(raw_data):
        for c_idx, val in enumerate(row):
            cell = tbl_raw.cell(r_idx, c_idx)
            cell.text = val
            set_cell_margins(cell, top=50, bottom=50, left=90, right=90)
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.05
            p.paragraph_format.space_after = Pt(1.5)
            if r_idx == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                set_cell_shading(cell, "EAEAEA")
                for r in p.runs:
                    r.bold = True
                    r.font.name = "Times New Roman"
                    r.font.size = Pt(9.5)
            else:
                p.alignment = (
                    WD_ALIGN_PARAGRAPH.CENTER
                    if c_idx in [0, 1, 2]
                    else WD_ALIGN_PARAGRAPH.LEFT
                )
                for r in p.runs:
                    r.font.name = "Times New Roman"
                    r.font.size = Pt(9.0)

    add_heading_2(
        "3.2 Isolasi Sampel Transisi Enrolled & Formulasi Target Biner Definitif"
    )
    add_body(
        "Dalam dataset mentah, terdapat 794 baris data berstatus 'Enrolled' (17,95%). Berdasarkan dokumentasi institusional dan publikasi rujukan "
        "Martins et al. (2021) [1], status kelulusan diekstraksi pada akhir durasi normal kurikulum sarjana (3 tahun / 6 semester). "
        "Mahasiswa 'Enrolled' adalah mahasiswa yang masih aktif menyelesaikan sisa SKS atau perbaikan nilai. Status ini merupakan proses yang sedang berjalan "
        "(censored ongoing process), bukan takdir akhir (terminal outcome). Memasukkan sampel Enrolled ke dalam data pelatihan terbukti menimbulkan ambiguitas "
        "label (label noise) yang menjatuhkan akurasi model menjadi ~77% [1]."
    )
    add_body(
        "Oleh karena itu, penelitian ini mengisolasi seluruh 794 sampel Enrolled ke dalam berkas 'data/ML/processed/enrolled_simulation.csv' "
        "yang dialokasikan khusus sebagai kolam simulasi sistem deteksi dini. Proses pelatihan dan pengujian murni difokuskan pada 3.630 baris data "
        "berstatus pasti: Lulus (Graduate = 0) vs Putus Studi (Dropout = 1). Formulasi biner definitif ini membersihkan batas kelas dan menaikkan potensi "
        "akurasi diskriminasi model ke kisaran 88% hingga 92%."
    )

    add_heading_2("3.3 Rekayasa Fitur Rasio Akademik")
    add_body(
        "Eksplorasi data awal pada Proposal.ipynb mengungkap adanya multikolinearitas linear sangat tinggi antara performa semester 1 dan semester 2 "
        "(korelasi Pearson r mencapai 0,90 hingga 0,94). Redundansi dimensi ini tidak efisien bagi algoritma machine learning. "
        "Untuk mengatasi permasalahan tersebut, dilakukan rekayasa fitur (feature engineering) dengan membentuk 4 fitur rasio akademik baru:"
    )
    add_bullet(
        "1. curricular_sem1_success_ratio: ",
        "Rasio kelulusan SKS semester 1, dihitung dari pembagian SKS disetujui terhadap SKS terdaftar (approved / enrolled).",
    )
    add_bullet(
        "2. curricular_sem2_success_ratio: ",
        "Rasio kelulusan SKS semester 2, dihitung dari pembagian SKS disetujui terhadap SKS terdaftar (approved / enrolled).",
    )
    add_bullet(
        "3. curricular_eval_efficiency: ",
        "Efisiensi evaluasi akademik, mengukur efektivitas mahasiswa dalam mengonversi ujian menjadi kelulusan (approved / evaluations).",
    )
    add_bullet(
        "4. curricular_grade_delta: ",
        "Dinamika tren prestasi akademik, mengukur perubahan kenaikan atau penurunan nilai rata-rata dari semester 1 ke semester 2 (grade sem 2 - grade sem 1).",
    )

    add_heading_2("3.4 Desain Partisi 3-Arah Berstrata 70:15:15 Bebas Kebocoran Data")
    add_body(
        "Untuk menjamin integritas ilmiah dan mencegah kebocoran data (data leakage), dataset biner 3.630 baris dipartisi menggunakan metode "
        "Stratified 3-Way Splitting menjadi tiga himpunan independen:"
    )

    # Tabel 3.2
    p_t32 = doc.add_paragraph()
    p_t32.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_t32.paragraph_format.space_before = Pt(8)
    p_t32.paragraph_format.space_after = Pt(3)
    r_t32 = p_t32.add_run(
        "Tabel 3.2 Alokasi Partisi Dataset 3-Arah Berstrata dan Kolam Simulasi"
    )
    r_t32.bold = True
    r_t32.font.name = "Times New Roman"
    r_t32.font.size = Pt(10.5)

    tbl_split = doc.add_table(rows=5, cols=4)
    tbl_split.alignment = WD_TABLE_ALIGNMENT.CENTER
    split_data = [
        (
            "Himpunan Data",
            "Jumlah Baris",
            "Proporsi (%)",
            "Fungsi dan Peruntukan Metodologis",
        ),
        (
            "Data Latih (Train Set)",
            "2.541 baris",
            "70,00%",
            "Mempelajari pola bobot fitur, struktur pohon CART, dan basis memori KNN",
        ),
        (
            "Data Validasi (Val Set)",
            "544 baris",
            "15,00%",
            "Hyperparameter tuning (mencari max_depth optimal Tree dan K terbaik KNN)",
        ),
        (
            "Data Uji Murni (Test Set)",
            "545 baris",
            "15,00%",
            "Evaluasi performa akhir objektif yang belum pernah dilihat model sebelumnya",
        ),
        (
            "Kolam Simulasi Enrolled",
            "794 baris",
            "-",
            "Simulasi prediksi probabilitas risiko pada mahasiswa aktif (Deployment Phase)",
        ),
    ]
    for r_idx, row in enumerate(split_data):
        for c_idx, val in enumerate(row):
            cell = tbl_split.cell(r_idx, c_idx)
            cell.text = val
            set_cell_margins(cell, top=50, bottom=50, left=90, right=90)
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.05
            p.paragraph_format.space_after = Pt(1.5)
            if r_idx == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                set_cell_shading(cell, "EAEAEA")
                for r in p.runs:
                    r.bold = True
                    r.font.name = "Times New Roman"
                    r.font.size = Pt(9.5)
            else:
                p.alignment = (
                    WD_ALIGN_PARAGRAPH.CENTER
                    if c_idx in [0, 1, 2]
                    else WD_ALIGN_PARAGRAPH.LEFT
                )
                for r in p.runs:
                    r.font.name = "Times New Roman"
                    r.font.size = Pt(9.0)

    add_heading_2("3.5 Arsitektur Dual Preprocessing Pipeline")
    add_body(
        "Membandingkan Decision Tree dan KNN menggunakan satu bentuk data mentah yang sama adalah sebuah kecacatan eksperimen "
        "karena kedua algoritma memiliki asumsi matematis yang bertolak belakang. Oleh karena itu, dirancang arsitektur Dual Preprocessing Pipeline:"
    )
    add_bullet(
        "1. Pipeline Decision Tree (Skala Asli): ",
        "Decision Tree bekerja berdasarkan perangkingan nilai, sehingga data dibiarkan dalam skala asli (unscaled). Hal ini menjamin aturan keputusan "
        "yang dihasilkan bersifat konkret dan manusiawi (misal: 'Curricular units 2nd sem approved <= 3.0' bukan angka abstrak z-score). "
        "Selain itu, diaktifkan pembobotan kelas seimbang (class_weight='balanced') untuk menghukum penalti kesalahan pada kelas Dropout secara proporsional.",
    )
    add_bullet(
        "2. Pipeline KNN (StandardScaler Terstandarisasi): ",
        "KNN wajib menggunakan StandardScaler (mean = 0, std = 1) yang di-*fit* murni pada data latih agar fitur bernilai besar (seperti pendapatan atau nilai) "
        "tidak mendominasi fitur biner (seperti beasiswa dan tunggakan SPP) dalam perhitungan jarak Euclidean. Selain itu, fitur kode jurusan nominal dinetralkan "
        "agar KNN tidak mengukur kedekatan numerik fiktif antar-jurusan.",
    )

    # ==================== BAB IV. HASIL EKSPERIMEN & PEMBAHASAN ====================
    doc.add_page_break()
    add_heading_1("BAB IV\nHASIL EKSPERIMEN DAN PEMBAHASAN KOMPARATIF")

    add_heading_2("4.1 Hyperparameter Tuning pada Data Validasi")
    add_body(
        "Penalaan hyperparameter dilakukan secara ketat pada Data Validasi (544 baris) untuk memilih konfigurasi model paling prima tanpa data leakage. "
        "Pada Decision Tree, dieksplorasi kedalaman pohon (max_depth) dari rentang 2 hingga 15 serta opsi tak terbatas (None). "
        "Sedangkan pada KNN, dieksplorasi nilai K (jumlah tetangga) dari 3 hingga 21 dengan pembobotan jarak terbalik (weights='distance')."
    )

    fig_tree = "resource/ML/report/figures/tree_tuning.png"
    add_figure(
        fig_tree,
        "Gambar 4.1 Kurva Penalaan Hyperparameter Kedalaman Pohon (max_depth) Decision Tree pada Data Validasi",
    )

    add_body(
        "Kurva validasi pada Gambar 4.1 memperlihatkan karakteristik pembelajaran pohon CART: saat max_depth ditingkatkan dari 2 ke 5, metrik akurasi "
        "dan F1-Score melonjak tajam. Namun pada max_depth > 6, model mulai mengalami gejala overfitting di mana varians meningkat dan performa validasi menurun. "
        "Kedalaman max_depth = 5 terpilih sebagai titik optimal yang memberikan keseimbangan sempurna antara Recall Dropout tinggi (83,1%) dan F1-Score stabil (80,4%)."
    )

    fig_knn = "resource/ML/report/figures/knn_tuning.png"
    add_figure(
        fig_knn,
        "Gambar 4.2 Kurva Penalaan Hyperparameter Jumlah Tetangga (K) KNN pada Data Validasi Terstandarisasi",
    )

    add_body(
        "Pada Gambar 4.2, kurva penalaan KNN menunjukkan bahwa nilai K yang terlalu kecil (K = 3) rentan terhadap noise data, sedangkan K yang terlalu besar "
        "(K > 15) menyebabkan batasan kelas menjadi terlalu halus (oversmoothing) sehingga mereduksi sensitivitas deteksi. Nilai K = 11 terpilih sebagai "
        "parameter terbaik yang menghasilkan F1-score puncak (78,4%) dan akurasi validasi tertinggi (84,2%)."
    )

    add_heading_2("4.2 Evaluasi Komparatif pada Data Uji Murni")
    add_body(
        "Setelah parameter optimal terkunci (Decision Tree max_depth=5 dan KNN K=11), kedua model diuji secara independen pada Data Uji Murni (Test Set 545 baris). "
        "Data uji ini belum pernah dilihat sama sekali oleh model selama proses pelatihan maupun penalaan parameter, sehingga menjamin objektivitas hasil evaluasi."
    )

    # Tabel 4.1
    p_t41 = doc.add_paragraph()
    p_t41.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_t41.paragraph_format.space_before = Pt(8)
    p_t41.paragraph_format.space_after = Pt(3)
    r_t41 = p_t41.add_run(
        "Tabel 4.1 Perbandingan Kinerja Komparatif Decision Tree vs KNN pada Data Uji Murni (545 Sampel)"
    )
    r_t41.bold = True
    r_t41.font.name = "Times New Roman"
    r_t41.font.size = Pt(10.5)

    tbl_eval = doc.add_table(rows=6, cols=4)
    tbl_eval.alignment = WD_TABLE_ALIGNMENT.CENTER
    eval_data = [
        (
            "Metrik Evaluasi Diagnostik",
            "Decision Tree (max_depth=5)",
            "K-Nearest Neighbors (K=11)",
            "Model Pemenang & Keterangan Analitik",
        ),
        (
            "Akurasi Keseluruhan (Accuracy)",
            "91,56% (499 / 545)",
            "88,99% (485 / 545)",
            "Decision Tree unggul +2,57% lebih presisi secara global",
        ),
        (
            "Precision (Kelas Dropout)",
            "90,73%",
            "96,36%",
            "KNN unggul +5,63% (menghasilkan False Positive lebih sedikit)",
        ),
        (
            "Recall / Sensitivitas (Dropout)",
            "87,32% (186 / 213)",
            "74,65% (159 / 213)",
            "Decision Tree unggul mutlak +12,67% (Menekan False Negative)",
        ),
        (
            "F1-Score (Harmonic Mean)",
            "89,00%",
            "84,13%",
            "Decision Tree unggul +4,87% dalam keseimbangan deteksi",
        ),
        (
            "Area Under Curve (ROC-AUC)",
            "0,9458",
            "0,9304",
            "Decision Tree unggul dalam kapabilitas diskriminasi probabilitas",
        ),
    ]
    for r_idx, row in enumerate(eval_data):
        for c_idx, val in enumerate(row):
            cell = tbl_eval.cell(r_idx, c_idx)
            cell.text = val
            set_cell_margins(cell, top=50, bottom=50, left=90, right=90)
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.05
            p.paragraph_format.space_after = Pt(1.5)
            if r_idx == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                set_cell_shading(cell, "EAEAEA")
                for r in p.runs:
                    r.bold = True
                    r.font.name = "Times New Roman"
                    r.font.size = Pt(9.5)
            else:
                p.alignment = (
                    WD_ALIGN_PARAGRAPH.CENTER
                    if c_idx in [0, 1, 2]
                    else WD_ALIGN_PARAGRAPH.LEFT
                )
                for r in p.runs:
                    r.font.name = "Times New Roman"
                    r.font.size = Pt(9.0)

    add_heading_2(
        "4.3 Analisis Matriks Kebingungan (Confusion Matrix) & Trade-off Error"
    )
    add_body(
        "Tabel perbandingan pada Tabel 4.1 membuktikan secara empiris bahwa Decision Tree keluar sebagai pemenang utama di hampir seluruh metrik kritis. "
        "Untuk memahami mengapa Decision Tree jauh lebih superior bagi kepentingan manajerial kampus dibandingkan KNN, "
        "kita harus menelaah distribusi matriks kebingungan (Confusion Matrix) pada Gambar 4.3:"
    )

    fig_cm = "resource/ML/report/figures/confusion_matrices.png"
    add_figure(
        fig_cm,
        "Gambar 4.3 Matriks Kebingungan (Confusion Matrix) Decision Tree vs KNN pada Data Uji Independen",
    )

    add_body(
        "Berdasarkan Gambar 4.3, dari total 213 mahasiswa berstatus faktual 'Dropout' pada data uji:\n"
        "1. Decision Tree berhasil mendeteksi 186 mahasiswa (True Positive) dan hanya melewatkan 27 mahasiswa (False Negative = 27).\n"
        "2. KNN hanya berhasil mendeteksi 159 mahasiswa (True Positive) dan melewatkan 54 mahasiswa berisiko (False Negative = 54).\n\n"
        "Bagi institusi pendidikan, angka 54 mahasiswa yang gagal terdeteksi oleh KNN adalah kerugian fatal. "
        "Sebanyak 54 mahasiswa tersebut tidak akan pernah menerima panggilan konseling dosen wali atau bantuan restrukturisasi biaya SPP "
        "karena sistem KNN salah menebak mereka sebagai mahasiswa aman (Lulus). Sebaliknya, Decision Tree sukses memangkas separuh angka kegagalan deteksi tersebut "
        "sehingga menghasilkan Recall sebesar 87,32%. Hal ini membuktikan bahwa pembobotan biaya (class_weight='balanced') pada Decision Tree berhasil "
        "mengatasi ketidakseimbangan kelas tanpa memanipulasi data sintetis SMOTE."
    )

    add_heading_2("4.4 Kurva ROC-AUC & Transparansi Feature Importance")
    add_body(
        "Gambar 4.4 memperlihatkan perbandingan kurva Receiver Operating Characteristic (ROC). Decision Tree mencatat skor ROC-AUC sebesar 0,9458, "
        "sedikit mengungguli KNN (0,9304). Nilai AUC yang mendekati 1,0 membuktikan bahwa kedua model memiliki kapabilitas separasi probabilitas yang sangat kuat "
        "jauh di atas garis tebakan acak (AUC = 0,500)."
    )

    fig_roc = "resource/ML/report/figures/roc_curve.png"
    add_figure(
        fig_roc,
        "Gambar 4.4 Kurva ROC-AUC Perbandingan Decision Tree vs K-Nearest Neighbors pada Data Uji",
    )

    add_body(
        "Kelebihan mutlak lain dari Decision Tree adalah sifat transparansi keputusan yang dapat diaudit secara ilmiah. "
        "Gambar 4.5 menyajikan 10 fitur penentu risiko paling dominan (Gini Feature Importance):"
    )

    fig_fi = "resource/ML/report/figures/feature_importance.png"
    add_figure(
        fig_fi,
        "Gambar 4.5 Sepuluh Variabel Determinan Utama Risiko Putus Studi Berdasarkan Feature Importance Decision Tree",
    )

    add_body(
        "Berdasarkan Gambar 4.5, tiga pilar penentu kelulusan mahasiswa adalah:\n"
        "1. Jumlah SKS yang disetujui pada semester 2 dan semester 1 ('Curricular units approved') menempati peringkat tertinggi. Mahasiswa yang gagal meluluskan minimal separuh SKS di tahun pertama hampir dipastikan mengalami atrisi studi.\n"
        "2. Status tunggakan biaya kuliah ('Tuition fees up to date') menjadi fitur non-akademik paling mematikan. Sesuai temuan EDA, mahasiswa yang menunggak SPP mencatat angka DO mencapai 86,6%.\n"
        "3. Fitur rasio kelulusan tahun pertama ('curricular_sem1_success_ratio' dan efisiensi evaluasi) yang kita rekayasa terbukti masuk ke jajaran top prediktor, memvalidasi keberhasilan tahap Data Preparation."
    )

    add_heading_2("4.5 Simulasi Peringatan Dini pada 794 Mahasiswa Aktif")
    add_body(
        "Pada tahap Deployment Simulation, model Decision Tree terbaik yang telah dilatih diumpankan ke 794 data mahasiswa aktif (Enrolled) "
        "yang sebelumnya diisolasi. Model menghitung probabilitas risiko putus studi P(Dropout) untuk setiap mahasiswa dan membaginya ke dalam 3 kuadran triage intervensi:"
    )

    # Tabel 4.2
    p_t42 = doc.add_paragraph()
    p_t42.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_t42.paragraph_format.space_before = Pt(8)
    p_t42.paragraph_format.space_after = Pt(3)
    r_t42 = p_t42.add_run(
        "Tabel 4.2 Hasil Simulasi Sistem Deteksi Dini pada 794 Mahasiswa Aktif (Enrolled)"
    )
    r_t42.bold = True
    r_t42.font.name = "Times New Roman"
    r_t42.font.size = Pt(10.5)

    tbl_sim = doc.add_table(rows=4, cols=4)
    tbl_sim.alignment = WD_TABLE_ALIGNMENT.CENTER
    sim_data = [
        (
            "Tingkat Risiko Intervensi",
            "Ambang Batas Probabilitas",
            "Jumlah Mahasiswa",
            "Persentase (%) & Tindakan SOP Kampus",
        ),
        (
            "Risiko Tinggi (Intervensi Mendesak)",
            "P(Dropout) >= 70%",
            "362 mahasiswa",
            "45,59% — Pemanggilan BAAK, restrukturisasi SPP & konseling darurat",
        ),
        (
            "Risiko Sedang (Pendampingan Dosen Wali)",
            "40% <= P(Dropout) < 70%",
            "142 mahasiswa",
            "17,88% — Monitoring berkala dosen wali & bimbingan perbaikan SKS",
        ),
        (
            "Risiko Rendah (Jalur Reguler Aman)",
            "P(Dropout) < 40%",
            "290 mahasiswa",
            "36,52% — Pemantauan rutin sistem tanpa intervensi khusus",
        ),
    ]
    for r_idx, row in enumerate(sim_data):
        for c_idx, val in enumerate(row):
            cell = tbl_sim.cell(r_idx, c_idx)
            cell.text = val
            set_cell_margins(cell, top=50, bottom=50, left=90, right=90)
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.05
            p.paragraph_format.space_after = Pt(1.5)
            if r_idx == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                set_cell_shading(cell, "EAEAEA")
                for r in p.runs:
                    r.bold = True
                    r.font.name = "Times New Roman"
                    r.font.size = Pt(9.5)
            else:
                p.alignment = (
                    WD_ALIGN_PARAGRAPH.CENTER
                    if c_idx in [0, 1, 2]
                    else WD_ALIGN_PARAGRAPH.LEFT
                )
                for r in p.runs:
                    r.font.name = "Times New Roman"
                    r.font.size = Pt(9.0)

    fig_sim = "resource/ML/report/figures/risk_segmentation.png"
    add_figure(
        fig_sim,
        "Gambar 4.6 Distribusi Hasil Simulasi Segmentasi Risiko pada 794 Mahasiswa Aktif",
    )

    add_body(
        "Hasil simulasi pada Gambar 4.6 membuktikan nilai guna manajerial nyata bagi perguruan tinggi. "
        "Sistem berhasil menemukan 362 mahasiswa aktif (45,59%) yang berada di zona merah risiko tinggi. Mahasiswa kelompok ini didominasi oleh individu "
        "yang menunggak pembayaran SPP dan mengalami kegagalan kelulusan beban SKS semester awal. Tanpa intervensi aktif, 362 mahasiswa ini diperkirakan "
        "akan berujung pada status pemutusan studi pada akhir masa evaluasi kurikulum."
    )

    # ==================== BAB V. KESIMPULAN & REKOMENDASI ====================
    doc.add_page_break()
    add_heading_1("BAB V\nKESIMPULAN DAN REKOMENDASI MANAJERIAL")

    add_heading_2("5.1 Kesimpulan Hasil Eksperimen")
    add_body(
        "Berdasarkan serangkaian proses komputasi saintifik berpedoman metodologi CRISP-DM yang dieksekusi dari tahap formulasi biner, "
        "rekayasa fitur rasio, partisi 3-arah, hingga pengujian murni, ditarik kesimpulan komparatif sebagai berikut:"
    )
    add_bullet(
        "1. Kemenangan Mutlak Decision Tree: ",
        "Model Decision Tree (max_depth=5) dinobatkan sebagai pemenang utama atas K-Nearest Neighbors (K=11). "
        "Decision Tree unggul di metrik Akurasi (91,56% vs 88,99%), ROC-AUC (0,9458 vs 0,9304), dan terutama pada metrik paling kritis yaitu "
        "Recall Dropout (87,32% vs 74,65%). Decision Tree hanya meluputkan 27 kasus DO berbanding 54 kasus pada KNN.",
    )
    add_bullet(
        "2. Keunggulan White-Box vs Black-Box: ",
        "Selain unggul secara metrik statistik, Decision Tree menyediakan aturan keputusan hierarkis konkret yang mudah dipahami dosen wali, "
        "sedangkan KNN bekerja sebagai 'black box' berbasis jarak yang sulit ditelusuri alasan logis di balik rekomendasinya.",
    )
    add_bullet(
        "3. Keberhasilan Validasi Bebas Leakage: ",
        "Penerapan partisi 3-arah berstrata (70:15:15) dan Dual Preprocessing Pipeline sukses melindungi model dari bias data leakage "
        "dan membuktikan bahwa penanganan outlier usia (jalur M23) secara tepat mampu meningkatkan daya generalisasi model.",
    )

    add_heading_2("5.2 Rekomendasi Kebijakan & SOP Manajerial Kampus")
    add_body(
        "Hasil temuan empiris proyek akhir ini merekomendasikan tiga pilar kebijakan strategis bagi pengelola perguruan tinggi:",
        indent=False,
    )
    add_bullet(
        "1. SOP Intervensi Finansial Cepat Tanggap: ",
        "Mengingat tunggakan SPP memicu angka DO hingga 86,6%, universitas disarankan membentuk skema restrukturisasi cicilan SPP otomatis "
        "dan bantuan beasiswa darurat sebelum batas akhir registrasi semester ditutup, khususnya bagi 362 mahasiswa aktif di zona merah.",
    )
    add_bullet(
        "2. Program Pendampingan Mahasiswa Dewasa Jalur M23: ",
        "Mahasiswa pendaftaran usia dewasa (>25 tahun) terbukti memiliki kerentanan atrisi tinggi akibat konflik peran kerja dan keluarga. "
        "Kampus perlu menyediakan fleksibilitas jam konsultasi akademik malam hari serta program bimbingan adaptasi belajar khusus.",
    )
    add_bullet(
        "3. Sistem Monitoring Dini Terintegrasi (Dashboard Kampus): ",
        "Mengintegrasikan model Decision Tree ke dalam Sistem Informasi Akademik (SIAKAD) kampus sehingga dosen wali menerima notifikasi otomatis "
        "apabila mahasiswa bimbingannya tidak lulus lebih dari separuh beban SKS di semester 1.",
    )

    add_heading_2("5.3 Saran Pengembangan Sistem Selanjutnya")
    add_body(
        "Untuk pengembangan penelitian dan implementasi sistem di masa mendatang, disarankan:",
        indent=False,
    )
    add_bullet(
        "1. Integrasi Data Aktivitas LMS Real-Time: ",
        "Menghubungkan model dengan log aktivitas mahasiswa pada Learning Management System (LMS seperti Moodle atau Canvas), "
        "seperti frekuensi login, pengumpulan tugas mingguan, dan keaktifan forum diskusi.",
    )
    add_bullet(
        "2. Eksplorasi Model Ensemble Berbobot: ",
        "Mengeksplorasi algoritma ensemble seperti Random Forest atau XGBoost dengan teknik kalibrasi probabilitas isotonic regression "
        "untuk melihat potensi kenaikan Recall lebih lanjut.",
    )

    # ==================== DAFTAR PUSTAKA ====================
    doc.add_page_break()
    add_heading_1("DAFTAR PUSTAKA")

    references = [
        (
            "[1]",
            'M. V. Martins, D. Tolledo, J. Machado, L. M. T. Baptista, and V. Realinho, "Early prediction of student\'s performance in higher education: A case study," in Trends and Innovations in Information Systems and Technologies (WorldCIST 2021), Advances in Intelligent Systems and Computing, vol. 1367, pp. 166–175, Springer, Cham, 2021. DOI: 10.1007/978-3-030-72660-7_16.',
        ),
        (
            "[2]",
            'C. Romero and S. Ventura, "Educational data mining: A review of the state of the art," IEEE Transactions on Systems, Man, and Cybernetics, Part C (Applications and Reviews), vol. 40, no. 6, pp. 601–618, Nov. 2010. DOI: 10.1109/TSMCC.2010.2053532.',
        ),
        (
            "[3]",
            "L. Breiman, J. H. Friedman, R. A. Olshen, and C. J. Stone, Classification and Regression Trees, 1st ed. Belmont, CA: Wadsworth International Group, 1984.",
        ),
        (
            "[4]",
            'T. M. Cover and P. E. Hart, "Nearest neighbor pattern classification," IEEE Transactions on Information Theory, vol. 13, no. 1, pp. 21–27, Jan. 1967. DOI: 10.1109/TIT.1967.1053964.',
        ),
        (
            "[5]",
            'R. Wirth and J. Hipp, "CRISP-DM: Towards a standard process model for data mining," in Proceedings of the 4th International Conference on the Practical Applications of Knowledge Discovery and Data Mining (PADD 2000), Manchester, UK, 2000, pp. 29–39.',
        ),
        (
            "[6]",
            'H. He and E. A. Garcia, "Learning from imbalanced data," IEEE Transactions on Knowledge and Data Engineering, vol. 21, no. 9, pp. 1263–1284, Sept. 2009. DOI: 10.1109/TKDE.2008.239.',
        ),
        (
            "[7]",
            'F. Pedregosa et al., "Scikit-learn: Machine learning in Python," Journal of Machine Learning Research, vol. 12, pp. 2825–2830, Nov. 2011.',
        ),
    ]

    for tag, text in references:
        p_ref = doc.add_paragraph()
        p_ref.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_ref.paragraph_format.line_spacing = 1.15
        p_ref.paragraph_format.space_before = Pt(2)
        p_ref.paragraph_format.space_after = Pt(4)
        p_ref.paragraph_format.left_indent = Cm(0.8)
        p_ref.paragraph_format.first_line_indent = Cm(-0.8)

        r_tag = p_ref.add_run(f"{tag} ")
        r_tag.bold = True
        r_tag.font.name = "Times New Roman"
        r_tag.font.size = Pt(11)

        r_text = p_ref.add_run(text)
        r_text.font.name = "Times New Roman"
        r_text.font.size = Pt(11)

    return doc


def generate_and_calibrate_report(output_docx: str, output_pdf: str) -> None:
    # First pass: generate with default TOC page map
    doc1 = build_report_document()
    os.makedirs(os.path.dirname(output_docx), exist_ok=True)
    doc1.save(output_docx)

    # Convert to PDF
    cmd_pdf = (
        f"libreoffice -env:UserInstallation=file:///tmp/libreoffice_conv "
        f"--headless --convert-to pdf {output_docx} --outdir {os.path.dirname(output_docx)}"
    )
    os.system(cmd_pdf)

    # Inspect PDF to find actual page numbers for each heading
    from pypdf import PdfReader

    reader = PdfReader(output_pdf)
    headings_to_find = {
        "BAB I": ["BAB I", "PENDAHULUAN"],
        "1.1": ["1.1 Latar Belakang"],
        "1.2": ["1.2 Rumusan Masalah"],
        "1.3": ["1.3 Tujuan Project"],
        "1.4": ["1.4 Manfaat Project"],
        "BAB II": ["BAB II", "KAJIAN PUSTAKA"],
        "2.1": ["2.1 Educational Data Mining"],
        "2.2": ["2.2 Supervised Binary Classification"],
        "2.3": ["2.3 Algoritma Decision Tree"],
        "2.4": ["2.4 Algoritma K-Nearest Neighbors"],
        "2.5": ["2.5 Metrik Evaluasi"],
        "BAB III": ["BAB III", "METODOLOGI DAN PREPROCESSING"],
        "3.1": ["3.1 Gambaran Umum Dataset"],
        "3.2": ["3.2 Isolasi Sampel Transisi"],
        "3.3": ["3.3 Rekayasa Fitur Rasio"],
        "3.4": ["3.4 Desain Partisi 3-Arah"],
        "3.5": ["3.5 Arsitektur Dual Preprocessing"],
        "BAB IV": ["BAB IV", "HASIL EKSPERIMEN"],
        "4.1": ["4.1 Hyperparameter Tuning"],
        "4.2": ["4.2 Evaluasi Komparatif"],
        "4.3": ["4.3 Analisis Matriks Kebingungan"],
        "4.4": ["4.4 Kurva ROC-AUC"],
        "4.5": ["4.5 Simulasi Peringatan Dini"],
        "BAB V": ["BAB V", "KESIMPULAN DAN REKOMENDASI"],
        "5.1": ["5.1 Kesimpulan Hasil Eksperimen"],
        "5.2": ["5.2 Rekomendasi Kebijakan"],
        "5.3": ["5.3 Saran Pengembangan"],
        "DAFTAR PUSTAKA": ["DAFTAR PUSTAKA"],
    }

    calibrated_map: dict[str, str] = {}
    for i, page in enumerate(reader.pages):
        # Section 2 starts at page index 2 (which is Page 1 in Arabic numerals)
        arabic_page = (
            i - 1
        )  # Cover is page 0, TOC is page 1, BAB I is page 2 -> arabic 1
        txt = page.extract_text()
        for key, markers in headings_to_find.items():
            if (
                key not in calibrated_map
                and any(m in txt for m in markers)
                and arabic_page >= 1
            ):
                calibrated_map[key] = str(arabic_page)

    print("Detected Calibrated Page Map:", calibrated_map)

    # Second pass: re-generate with calibrated TOC page map
    doc2 = build_report_document(toc_page_map=calibrated_map)
    doc2.save(output_docx)

    # Convert again to produce finalized calibrated PDF
    os.system(cmd_pdf)
    print(f"Final report DOCX & PDF successfully created at: {output_pdf}")


if __name__ == "__main__":
    out_docx = "resource/ML/report/Laporan-Akhir-ML-230411100197.docx"
    out_pdf = "resource/ML/report/Laporan-Akhir-ML-230411100197.pdf"
    generate_and_calibrate_report(out_docx, out_pdf)
