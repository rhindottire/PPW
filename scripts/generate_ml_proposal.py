"""Script to generate the official Machine Learning Project Akhir Proposal (.docx).

Adhering strictly to UTM Academic Writing Governance & Course Assignment Guidelines:
- Paper: A4, Margins: 4-3-3-3 cm (Left 4.0 cm, Top 3.0 cm, Right 3.0 cm, Bottom 3.0 cm)
- Typography: Times New Roman, 12 pt body, 1.5 spacing, justify alignment
- Formal UTM Elements:
  * Front Matter: Cover page (clean, no printed page num) + Daftar Isi (Page ii) with dot leaders
  * Dynamic Page Numbering: Lower Roman for front matter, Decimal Arabic (1, 2, 3...) for body
  * Team format: 2-person group (Achmad Ridho Fa'iz as Ketua + Rekan Kelompok)
  * Tables with titles on TOP (Tabel 2.1 Profil Dataset & Tabel 3.1 Matriks Rencana Kerja)
  * Figures with captions on BOTTOM (Gambar 2.1 to 2.6 EDA visual evidence)
  * Strict IEEE style references [1] through [7] with contextual in-text citations
  * Zero AI slop, zero conversational meta-commentary
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


def build_proposal_document(toc_page_map: dict[str, str] | None = None) -> DocObject:
    if toc_page_map is None:
        toc_page_map = {
            "BAB I": "1",
            "1.1": "1",
            "1.2": "2",
            "1.3": "3",
            "BAB II": "3",
            "2.1": "3",
            "2.2": "4",
            "2.3": "5",
            "2.4": "7",
            "BAB III": "10",
            "3.1": "10",
            "3.2": "10",
            "3.3": "11",
            "DAFTAR PUSTAKA": "12",
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

    def add_title_p(
        text: str,
        bold: bool = True,
        size: float = 12,
        space_before: float = 0,
        space_after: float = 6,
    ) -> Any:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        run = p.add_run(text)
        run.bold = bold
        run.font.name = "Times New Roman"
        run.font.size = Pt(size)
        return p

    def add_heading_1(text: str) -> Any:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(10)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.name = "Times New Roman"
        run.font.size = Pt(14)
        return p

    def add_heading_2(text: str) -> Any:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.name = "Times New Roman"
        run.font.size = Pt(12)
        return p

    def add_body(text: str, indent: bool = True) -> Any:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(4)
        if indent:
            p.paragraph_format.first_line_indent = Cm(1.0)
        run = p.add_run(text)
        run.font.name = "Times New Roman"
        run.font.size = Pt(12)
        return p

    def add_bullet(prefix: str, text: str) -> Any:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.left_indent = Cm(1.0)
        p.paragraph_format.first_line_indent = Cm(-0.5)

        r_pre = p.add_run(f"• {prefix}")
        r_pre.bold = True
        r_pre.font.name = "Times New Roman"
        r_pre.font.size = Pt(12)

        r_text = p.add_run(text)
        r_text.font.name = "Times New Roman"
        r_text.font.size = Pt(12)
        return p

    def add_figure(image_path: str, caption: str) -> None:
        if os.path.exists(image_path):
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(6)
            p_img.paragraph_format.space_after = Pt(2)
            p_img.paragraph_format.keep_with_next = True
            run = p_img.add_run()
            run.add_picture(image_path, width=Cm(9.5))

            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_before = Pt(2)
            p_cap.paragraph_format.space_after = Pt(6)
            r_cap = p_cap.add_run(caption)
            r_cap.font.name = "Times New Roman"
            r_cap.font.size = Pt(10)
            r_cap.italic = True
            r_cap.bold = True

    def add_table_title(title: str) -> None:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(title)
        r.bold = True
        r.font.name = "Times New Roman"
        r.font.size = Pt(10.5)

    # ==================== HALAMAN JUDUL ====================
    add_title_p(
        "PROPOSAL PROJECT AKHIR MACHINE LEARNING",
        bold=True,
        size=14,
        space_before=0,
        space_after=10,
    )

    add_title_p(
        "PREDIKSI KEBERHASILAN AKADEMIK DAN DETEKSI DINI RISIKO PUTUS STUDI (STUDENT DROPOUT) MENGGUNAKAN ALGORITMA DECISION TREE DAN K-NEAREST NEIGHBORS (KNN)",
        bold=True,
        size=12.5,
        space_before=0,
        space_after=14,
    )

    add_title_p(
        "Diajukan untuk Memenuhi Tugas Besar Proyek Akhir Mata Kuliah Machine Learning",
        bold=False,
        size=11,
        space_before=0,
        space_after=10,
    )

    # Logo Resmi Universitas Trunojoyo Madura
    logo_path = "resource/ML/proposal/figures/logo_utm.jpg"
    if os.path.exists(logo_path):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_before = Pt(4)
        p_logo.paragraph_format.space_after = Pt(10)
        p_logo.paragraph_format.line_spacing = 1.0
        run_logo = p_logo.add_run()
        run_logo.add_picture(logo_path, width=Cm(4.5))

    add_title_p(
        "Disusun Oleh:\nKELOMPOK [Placeholder]",
        bold=True,
        size=11.5,
        space_before=0,
        space_after=6,
    )

    # Identitas Tim: 2 Mahasiswa
    tbl_team = doc.add_table(rows=3, cols=3)
    tbl_team.alignment = WD_TABLE_ALIGNMENT.CENTER
    team_data = [
        ("No.", "Nama Mahasiswa", "Nomor Induk Mahasiswa (NIM)"),
        ("1.", "Achmad Ridho Fa'iz (Ketua)", "230411100197"),
        ("2.", "[Nama Rekan Kelompok]", "[NIM Rekan Kelompok]"),
    ]
    for r_idx, row in enumerate(team_data):
        for c_idx, val in enumerate(row):
            cell = tbl_team.cell(r_idx, c_idx)
            cell.text = val
            set_cell_margins(cell, top=60, bottom=60, left=120, right=120)
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.0
            p.paragraph_format.space_after = Pt(2)
            if r_idx == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                set_cell_shading(cell, "EAEAEA")
                for r in p.runs:
                    r.bold = True
                    r.font.name = "Times New Roman"
                    r.font.size = Pt(10.5)
            else:
                p.alignment = (
                    WD_ALIGN_PARAGRAPH.CENTER if c_idx != 1 else WD_ALIGN_PARAGRAPH.LEFT
                )
                for r in p.runs:
                    r.font.name = "Times New Roman"
                    r.font.size = Pt(10.5)

    add_title_p(
        "Dosen Pengampu:\nAch. Khozaimi, S.Kom., M.Kom.",
        bold=True,
        size=11.5,
        space_before=8,
        space_after=12,
    )

    add_title_p(
        "PROGRAM STUDI TEKNIK INFORMATIKA\nFAKULTAS TEKNIK\nUNIVERSITAS TRUNOJOYO MADURA\n2026",
        bold=True,
        size=12,
        space_before=0,
        space_after=0,
    )

    doc.add_page_break()

    # ==================== HALAMAN DAFTAR ISI ====================
    add_heading_1("DAFTAR ISI")

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
        "BAB II METODE DAN DATASET",
        toc_page_map.get("BAB II", "3"),
        level=1,
        bold=True,
    )
    add_toc_line(
        doc,
        "2.1 Jenis Machine Learning",
        toc_page_map.get("2.1", "3"),
        level=2,
        bold=False,
    )
    add_toc_line(
        doc,
        "2.2 Algoritma yang Digunakan",
        toc_page_map.get("2.2", "4"),
        level=2,
        bold=False,
    )
    add_toc_line(doc, "2.3 Dataset", toc_page_map.get("2.3", "5"), level=2, bold=False)
    add_toc_line(
        doc,
        "2.4 Rencana Pengolahan Data & Temuan EDA Awal",
        toc_page_map.get("2.4", "6"),
        level=2,
        bold=False,
    )
    add_toc_line(
        doc,
        "BAB III RENCANA IMPLEMENTASI",
        toc_page_map.get("BAB III", "9"),
        level=1,
        bold=True,
    )
    add_toc_line(
        doc,
        "3.1 Tools yang Digunakan",
        toc_page_map.get("3.1", "9"),
        level=2,
        bold=False,
    )
    add_toc_line(
        doc,
        "3.2 Tahapan dan Jadwal Implementasi",
        toc_page_map.get("3.2", "10"),
        level=2,
        bold=False,
    )
    add_toc_line(
        doc,
        "3.3 Evaluasi Model",
        toc_page_map.get("3.3", "11"),
        level=2,
        bold=False,
    )
    add_toc_line(
        doc,
        "DAFTAR PUSTAKA",
        toc_page_map.get("DAFTAR PUSTAKA", "12"),
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

    # ==================== BAB I. PENDAHULUAN ====================
    add_heading_1("BAB I\nPENDAHULUAN")

    add_heading_2("1.1 Latar Belakang")
    add_body(
        "Pendidikan tinggi memegang peranan fundamental dalam pembentukan modal manusia dan akselerasi daya saing bangsa. "
        "Namun demikian, fenomena putus studi mahasiswa (student dropout) masih menjadi salah satu tantangan paling kritis yang dihadapi "
        "oleh perguruan tinggi di seluruh dunia [1]. Tingginya angka putus studi tidak hanya berdampak negatif pada efisiensi alokasi "
        "anggaran dan status akreditasi institusi, melainkan juga menimbulkan kerugian psikologis serta finansial yang signifikan bagi mahasiswa "
        "dan keluarga mereka [2]. Oleh karena itu, kemampuan institusi untuk mendeteksi potensi kegagalan akademik sedini mungkin merupakan prasyarat "
        "mutlak bagi perumusan kebijakan pendampingan mahasiswa yang efektif dan tepat sasaran."
    )
    add_body(
        "Topik prediksi keberhasilan akademik dan deteksi dini putus studi ini sangat menarik dan mendesak untuk diteliti karena proses "
        "pengambilan keputusan retensi mahasiswa saat ini sering kali terlambat. Di banyak institusi, intervensi baru dilakukan setelah mahasiswa "
        "mengumpulkan akumulasi nilai buruk berturut-turut atau ketika tunggakan biaya kuliah telah menumpuk, di mana kemungkinan pemulihan "
        "studi sudah sangat kecil [2]. Melalui pemanfaatan data historis akademik terintegrasi, institusi dapat bertransformasi dari pendekatan "
        "reaktif menjadi sistem intervensi preventif yang proaktif."
    )
    add_body(
        "Machine Learning menjadi instrumen metodologis yang sangat tepat untuk menyelesaikan permasalahan ini karena relasi antara latar belakang "
        "sosio-ekonomi, beban finansial, dan dinamika performa akademik semester awal bersifat non-linear serta berdimensi tinggi. Melalui Machine "
        "Learning terawasi (Supervised Learning), pola tersembunyi dari rekam jejak mahasiswa terdahulu dapat diekstraksi secara otomatis "
        "untuk membangun model klasifikasi biner yang andal: membedakan secara tegas antara mahasiswa yang berhasil menyelesaikan studi (Graduate) "
        "dan mahasiswa yang putus studi (Dropout) [1], [2]. Dalam penelitian proyek akhir ini, algoritma Decision Tree dan K-Nearest "
        "Neighbors (KNN) dipilih sebagai pendekatan komparatif. Kedua algoritma ini mewakili dua paradigma pembelajaran terawasi yang saling "
        "melengkapi dalam klasifikasi data tabular: pembentukan model partisi aturan hierarkis eksplisit (eager learner) versus penaksiran "
        "kedekatan berbasis metrik jarak instans (lazy learner) [3], [4]."
    )

    add_heading_2("1.2 Rumusan Masalah")
    add_body(
        "Berdasarkan latar belakang yang telah diuraikan, rumusan masalah dalam proyek akhir ini adalah:",
        indent=False,
    )
    add_bullet(
        "1. ",
        "Bagaimana karakteristik profil mahasiswa dan variabel determinan dominan (antara kewajiban finansial SPP, latar belakang demografi, dan rekam jejak akademik awal) yang mendorong peningkatan risiko putus studi (dropout) berdasarkan analisis data eksploratif?",
    )
    add_bullet(
        "2. ",
        "Bagaimana perbandingan kinerja klasifikasi biner antara algoritma Decision Tree (rule-based eager learner) dan K-Nearest Neighbors (distance-based lazy learner) dalam memprediksi status kelulusan mahasiswa pada dataset 3.630 baris data tervalidasi?",
    )
    add_bullet(
        "3. ",
        "Bagaimana perancangan strategi partisi 3-arah (Train-Validation-Test) serta arsitektur preprocessing khusus (Dual Pipeline) agar perbandingan model adil, bebas kebocoran data (anti-leakage), dan menghasilkan model berakurasi tinggi?",
    )

    add_heading_2("1.3 Tujuan Project")
    add_body(
        "Tujuan yang ingin dicapai melalui pelaksanaan proyek akhir ini adalah:",
        indent=False,
    )
    add_bullet(
        "1. ",
        "Mengidentifikasi variabel-variabel kunci pemicu atrisi mahasiswa melalui eksplorasi data komprehensif, khususnya membuktikan dampak signifikan tunggakan SPP dan kegagalan SKS tahun pertama.",
    )
    add_bullet(
        "2. ",
        "Membangun dan menguji kinerja model klasifikasi biner menggunakan algoritma Decision Tree dan K-Nearest Neighbors (KNN) dengan kerangka partisi data 3-arah (70% Latih : 15% Validasi : 15% Uji) untuk optimasi parameter tanpa kebocoran data.",
    )
    add_bullet(
        "3. ",
        "Menerapkan arsitektur preprocessing terpisah yang adil (skala asli untuk Decision Tree dan StandardScaler untuk KNN) guna menghasilkan batas aturan pohon keputusan yang konkret serta metrik jarak tetangga yang akurat.",
    )
    add_bullet(
        "4. ",
        "Menyediakan model inferensi yang dapat disimulasikan pada 794 data mahasiswa aktif (Enrolled) guna memberikan sistem peringatan dini (early warning system) bagi pengelola program studi.",
    )

    # ==================== BAB II. METODE DAN DATASET ====================
    doc.add_page_break()
    add_heading_1("BAB II\nMETODE DAN DATASET")

    add_heading_2("2.1 Jenis Machine Learning")
    add_body(
        "Pendekatan yang digunakan dalam proyek akhir ini adalah Supervised Learning (Pembelajaran Terawasi) untuk tugas Klasifikasi Biner (Binary Classification). "
        "Berdasarkan dokumentasi resmi dan penelitian acuan Martins et al. (2021) [1], dataset asli mencakup 3 (tiga) status mahasiswa: Graduate (Lulus), "
        "Dropout (Putus Studi), dan Enrolled (Masih Aktif Kuliah). Namun, status Enrolled pada hakikatnya merupakan status proses yang sedang berjalan "
        "(intermediate status) di mana mahasiswa bersangkutan pada akhirnya akan bermuara pada dua takdir studi: Lulus atau Putus Studi. Memasukkan kelas Enrolled "
        "ke dalam data pelatihan terbukti secara empiris menimbulkan ambiguitas batas kelas (noise) yang menurunkan akurasi model [1]."
    )
    add_body(
        "Oleh karena itu, penelitian ini memformulasikan masalah ke dalam Klasifikasi Biner yang fokus pada mahasiswa dengan status kelulusan definitif: "
        "Target y in {0, 1}, di mana 1 merepresentasikan kelas positif 'Dropout' (kejadian risiko yang ingin dideteksi sedini mungkin) dan 0 merepresentasikan "
        "'Graduate' (mahasiswa yang berhasil lulus). Sebanyak 794 baris data mahasiswa berstatus Enrolled dipisahkan dari proses pelatihan/pengujian "
        "dan dialokasikan secara khusus sebagai data simulasi pemantauan mahasiswa aktif."
    )
    add_body(
        "Justifikasi Pemilihan Klasifikasi Dibandingkan Regresi: "
        "Pemilihan tugas klasifikasi biner dan bukan regresi didasari oleh tiga pertimbangan teoritis dan praktis yang fundamental: "
        "1) Sifat Alami Variabel Target: Kolom Target pada dataset berisi status administratif kualitatif: 'Dropout', 'Enrolled', dan 'Graduate'. Ini adalah label kualitatif nominal, bukan besaran angka kontinu. Kita tidak bisa meregresikan kata 'Lulus' atau 'Dropout' karena tidak ada makna fisik dari nilai kontinu seperti 'mahasiswa ini lulus 0,73' atau 'mahasiswa ini DO 1,45'. "
        "2) Kebutuhan Intervensi Manajerial Kampus: Pihak kampus dan dosen wali memerlukan batas keputusan (decision boundary) yang tegas untuk memicu Standard Operating Procedure (SOP) intervensi (seperti panggilan konseling akademik darurat atau restrukturisasi cicilan SPP bagi mahasiswa berlabel 'Dropout'). Model regresi yang sekadar memprediksi nilai IPK tidak secara langsung menjawab pertanyaan kritis apakah mahasiswa bersangkutan akan bertahan atau keluar. "
        "3) Pelanggaran Asumsi Matematis Regresi: Penerapan regresi linear pada variabel target biner (Linear Probability Model) berisiko menghasilkan estimasi di luar rentang probabilitas valid ([0, 1]) serta melanggar asumsi homoskedastisitas varians residual. Sebaliknya, model klasifikasi berbasis probabilitas posterior terkalibrasi memungkinkan sistem melakukan pemeringkatan risiko (risk triage) bertingkat secara presisi."
    )

    add_heading_2("2.2 Algoritma yang Digunakan")
    add_body(
        "Untuk memecahkan permasalahan klasifikasi biner tersebut, penelitian ini menerapkan dan membandingkan dua "
        "algoritma komplementer, yaitu:",
        indent=False,
    )
    add_bullet(
        "1. Decision Tree (Pohon Keputusan - Algoritma CART/C4.5): ",
        "Decision Tree merupakan algoritma eager learner yang membangun model pohon keputusan hierarkis melalui partisi rekursif ruang fitur. "
        "Pemilihan pemisahan cabang (split) didasarkan pada optimasi kriteria kemurnian, seperti Gini Impurity atau Information Gain (Entropy) [3]. "
        "Alasan utama pemilihan Decision Tree adalah sifat transparansi interpretabilitasnya yang sangat tinggi (white-box model). Model menghasilkan "
        "aturan logika IF-THEN yang konkret dan terukur, sehingga memudahkan pemangku kepentingan institusi pendidikan untuk memahami ambang "
        "batas nilai dan kondisi spesifik yang memicu prediksi mahasiswa putus studi. Selain itu, Decision Tree tangguh menangani kombinasi "
        "fitur kontinu dan diskrit tanpa memerlukan normalisasi data ketat.",
    )
    add_bullet(
        "2. K-Nearest Neighbors (KNN - Pembelajaran Berbasis Instans): ",
        "KNN merupakan algoritma klasifikasi non-parametrik yang tergolong dalam keluarga lazy learner [4]. Algoritma ini tidak membentuk parameter "
        "model eksplisit selama fase pelatihan, melainkan menyimpan seluruh data latih ke dalam memori. Saat mengklasifikasikan sampel data baru, "
        "KNN menghitung jarak metrik (Euclidean Distance) antara sampel uji dengan seluruh titik data latih, memilih K tetangga terdekat, dan "
        "menetapkan kelas prediksi berdasarkan voting mayoritas [4]. Alasan pemilihannya didasarkan pada kekuatannya dalam menangkap struktur "
        "geometri data secara non-linear tanpa memaksakan batas linear kaku. Secara intuitif, KNN mengelompokkan mahasiswa berdasarkan kesamaan "
        "profil holistik (finansial, usia, dan rekam jejak akademik) dengan asumsi bahwa mahasiswa dengan karakteristik serupa memiliki "
        "kecenderungan status kelulusan yang serupa.",
    )

    add_heading_2("2.3 Dataset")
    add_body(
        "Dataset yang dijadikan bahan eksperimen adalah data publik berstandar internasional yang diperoleh dari UCI Machine Learning Repository "
        "dengan judul Predict Students' Dropout and Academic Success (DOI: 10.24432/C5MC89) [1]. Dataset ini dikompilasi oleh Martins et al. dari "
        "institusi pendidikan tinggi Instituto Politecnico de Portalegre dan telah divalidasi kebersihannya. Ringkasan spesifikasi dataset disajikan pada Tabel 2.1.",
        indent=False,
    )

    # Tabel 2.1 Ringkasan Profil dan Metadata Dataset
    add_table_title("Tabel 2.1 Ringkasan Profil dan Metadata Dataset Penelitian")
    tbl_ds = doc.add_table(rows=8, cols=3)
    tbl_ds.alignment = WD_TABLE_ALIGNMENT.CENTER
    ds_metadata = [
        ("No.", "Parameter Spesifikasi", "Keterangan / Nilai Karakteristik"),
        ("1.", "Nama Resmi Dataset", "Predict Students' Dropout and Academic Success"),
        (
            "2.",
            "Sumber & Repositori",
            "UCI Machine Learning Repository (DOI: 10.24432/C5MC89)",
        ),
        (
            "3.",
            "Jumlah Data Mentah",
            "4.424 observasi mahasiswa (0 missing values, 0 duplikat)",
        ),
        (
            "4.",
            "Alokasi Data Pemodelan",
            "3.630 baris data definitif (2.209 Graduate / 60,9% & 1.421 Dropout / 39,1%)",
        ),
        (
            "5.",
            "Alokasi Data Simulasi",
            "794 baris data Enrolled (17,9%) untuk uji simulasi inferensi sistem deteksi dini",
        ),
        (
            "6.",
            "Dimensi Fitur Prediktor",
            "36 fitur asli + 4 fitur rekayasa rasio & delta akademik (Total 40 prediktor)",
        ),
        (
            "7.",
            "Domain Atribut",
            "Demografi, Sosio-Ekonomi, Kualifikasi Masuk, Beban Finansial, Akademik Sem 1-2, & Makroekonomi",
        ),
    ]
    for r_idx, row in enumerate(ds_metadata):
        for c_idx, val in enumerate(row):
            cell = tbl_ds.cell(r_idx, c_idx)
            cell.text = val
            set_cell_margins(cell, top=50, bottom=50, left=100, right=100)
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.05
            p.paragraph_format.space_after = Pt(1.5)
            if r_idx == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                set_cell_shading(cell, "EAEAEA")
                for r in p.runs:
                    r.bold = True
                    r.font.name = "Times New Roman"
                    r.font.size = Pt(10)
            else:
                p.alignment = (
                    WD_ALIGN_PARAGRAPH.CENTER if c_idx == 0 else WD_ALIGN_PARAGRAPH.LEFT
                )
                for r in p.runs:
                    r.font.name = "Times New Roman"
                    r.font.size = Pt(9.5)

    add_heading_2("2.4 Rencana Pengolahan Data & Temuan EDA Awal")
    add_body(
        "Berdasarkan eksplorasi data awal (Exploratory Data Analysis) yang telah dieksekusi pada lingkungan komputasi, diperoleh beberapa temuan empiris "
        "kritis yang menjadi fondasi perancangan tahap Data Preparation:"
    )

    add_bullet(
        "1. Distribusi Kelas Definitif: ",
        "Pada populasi 3.630 mahasiswa bertarget definitif, perbandingan kelas adalah 2.209 mahasiswa Lulus (60,9%) dan 1.421 mahasiswa Dropout (39,1%). "
        "Rasio ini jauh lebih seimbang dibandingkan struktur multi-class awal (Gambar 2.1), sehingga meminimalkan bias model terhadap kelas mayoritas.",
    )
    add_figure(
        "resource/ML/proposal/figures/target_distribution.png",
        "Gambar 2.1 Distribusi Frekuensi Kategori Target Mahasiswa",
    )

    add_bullet(
        "2. Anomali Beban Finansial (Tunggakan SPP): ",
        "Analisis tabulasi silang membuktikan bahwa kewajiban finansial merupakan pembeda paling tajam. Pada mahasiswa yang menunggak pembayaran SPP "
        "(Tuition fees up to date = 0), proporsi putus studi melonjak drastis hingga mencapai 86,6%. Sebaliknya, kepatuhan pembayaran SPP berkorelasi "
        "kuat dengan keberhasilan kelulusan (Gambar 2.2). Indikator status debitur (Debtor = 1) juga melipatgandakan risiko dropout menjadi 61,4%.",
    )
    add_figure(
        "resource/ML/proposal/figures/financial_risk.png",
        "Gambar 2.2 Analisis Risiko Finansial (Tunggakan SPP & Status Debitur) terhadap Status Studi",
    )

    add_bullet(
        "3. Efek Protektif Beasiswa: ",
        "Penerima beasiswa (Scholarship holder = 1) memiliki tingkat kelulusan mencapai 76,2% dengan angka putus studi hanya 11,8% (Gambar 2.3). "
        "Hal ini membuktikan secara kuantitatif bahwa intervensi bantuan biaya memberikan proteksi stabilitas yang signifikan terhadap keberlangsungan studi.",
    )
    add_figure(
        "resource/ML/proposal/figures/scholarship_protection.png",
        "Gambar 2.3 Distribusi Status Kelulusan Berdasarkan Kepemilikan Beasiswa",
    )

    add_bullet(
        "4. Multikolinearitas SKS & Disparitas Nilai: ",
        "Matriks korelasi akademik (Gambar 2.4 dan Gambar 2.5) memperlihatkan korelasi linear sangat kuat (r > 0,85) antara jumlah SKS yang disetujui "
        "pada semester 1 dan semester 2. Mahasiswa yang gagal meluluskan minimal separuh beban SKS di semester 1 hampir dipastikan mengalami kegagalan "
        "studi pada semester-semester berikutnya.",
    )
    add_figure(
        "resource/ML/proposal/figures/academic_correlation.png",
        "Gambar 2.4 Matriks Korelasi Pearson Fitur Kinerja Akademik Mahasiswa",
    )
    add_figure(
        "resource/ML/proposal/figures/academic_disparity.png",
        "Gambar 2.5 Disparitas Jumlah SKS yang Disetujui terhadap Status Kelulusan",
    )

    add_bullet(
        "5. Kerentanan Usia Pendaftaran: ",
        "Distribusi usia pendaftaran (Gambar 2.6) menunjukkan bahwa mahasiswa yang mendaftar pada usia dewasa (> 25 tahun) memiliki densitas putus studi "
        "yang jauh lebih tinggi dibandingkan mahasiswa jalur reguler usia 18-20 tahun, yang dipicu oleh konflik peran antara tuntutan kerja dan studi.",
    )
    add_figure(
        "resource/ML/proposal/figures/age_demographics.png",
        "Gambar 2.6 Distribusi Densitas Usia Saat Pendaftaran Berdasarkan Kategori Target",
    )

    add_body(
        "Rencana Pengolahan Data (Data Preparation) yang dirancang mencakup: "
        "1) Penyaringan Sampel Definitif: Mengisolasi 3.630 data mahasiswa biner (Dropout = 1, Graduate = 0) serta mengalokasikan 794 data Enrolled ke kolam simulasi. "
        "2) Feature Engineering: Penambahan 4 fitur rasio akademik turunan (rasio SKS lulus sem 1, rasio SKS lulus sem 2, rasio SKS tahun pertama, dan selisih nilai antar-semester). "
        "3) Stratified 3-Way Splitting: Pembagian dataset menjadi 70% Data Latih (2.541 baris), 15% Data Validasi (544 baris), dan 15% Data Uji (545 baris). "
        "4) Arsitektur Dual Preprocessing: Pipeline khusus untuk Decision Tree (mempertahankan skala asli fitur agar aturan pohon konkret) dan Pipeline khusus untuk KNN "
        "(StandardScaler pada fitur numerik serta netralisasi variabel kode nominal agar jarak Euclidean tidak terdistorsi).",
        indent=True,
    )

    # ==================== BAB III. RENCANA IMPLEMENTASI ====================
    doc.add_page_break()
    add_heading_1("BAB III\nRENCANA IMPLEMENTASI")

    add_heading_2("3.1 Tools yang Digunakan")
    add_body(
        "Implementasi proyek akhir ini memanfaatkan ekosistem open-source berbasis bahasa Python dengan rincian perangkat berikut:",
        indent=False,
    )
    add_bullet(
        "1. Bahasa Pemrograman: ",
        "Python versi 3.14 / 3.11 sebagai fondasi komputasi saintifik.",
    )
    add_bullet(
        "2. Lingkungan Pengembangan: ",
        "Jupyter Lab dan IPython Notebook untuk dokumentasi interaktif berbasis siklus CRISP-DM.",
    )
    add_bullet(
        "3. Pustaka Manipulasi & Komputasi Numerik: ",
        "Pandas untuk manipulasi data tabular dan NumPy untuk komputasi matriks.",
    )
    add_bullet(
        "4. Pustaka Machine Learning: ",
        "Scikit-Learn (sklearn) untuk implementasi DecisionTreeClassifier, KNeighborsClassifier, train_test_split, StandardScaler, GridSearchCV, dan metrik klasifikasi [7].",
    )
    add_bullet(
        "5. Pustaka Visualisasi: ",
        "Matplotlib dan Seaborn untuk visualisasi matriks korelasi, kurva ROC, dan diagram alur pohon keputusan.",
    )

    add_heading_2("3.2 Tahapan dan Jadwal Implementasi")
    add_body(
        "Alur kerja proyek dirancang secara sistematis mengadopsi metodologi CRISP-DM yang diintegrasikan dengan jadwal pelaksanaan proyek "
        "dari Minggu ke-10 hingga presentasi evaluasi akhir pada Minggu ke-13 [5]. Matriks tahapan kerja disajikan pada Tabel 3.1.",
        indent=False,
    )

    # Tabel 3.1 Matriks Rencana Kerja dan Jadwal Pelaksanaan Proyek
    add_table_title(
        "Tabel 3.1 Matriks Rencana Kerja dan Jadwal Pelaksanaan Proyek (Minggu 10–13)"
    )
    tbl_sched = doc.add_table(rows=5, cols=4)
    tbl_sched.alignment = WD_TABLE_ALIGNMENT.CENTER
    sched_data = [
        (
            "Fase Metodologis",
            "Aktivitas Teknis Spesifik",
            "Waktu Pelaksanaan",
            "Luaran / Deliverables",
        ),
        (
            "1. Business & Data Understanding",
            "Formulasi sasaran biner, audit kebersihan dataset 4.424 baris, dan ekstraksi 6 grafik visualisasi EDA",
            "Minggu ke-10",
            "Naskah Proposal & Slide Presentasi",
        ),
        (
            "2. Data Preparation",
            "Penyaringan 3.630 data definitif, rekayasa 4 fitur rasio/delta, partisi 70:15:15, & setup Dual Pipeline",
            "Minggu ke-11",
            "Dataset latih, validasi, & uji tervalidasi",
        ),
        (
            "3. Modeling & Parameter Tuning",
            "Pelatihan Decision Tree & KNN pada Train (2.541 baris) serta pencarian K dan max_depth optimal pada Val (544 baris)",
            "Minggu ke-12",
            "Model terbaik tersimpan & grafik tuning",
        ),
        (
            "4. Evaluation & Deployment Simulation",
            "Pengujian objektif pada Test (545 baris), simulasi inferensi pada 794 data Enrolled, penyusunan laporan akhir, & presentasi kelas",
            "Minggu ke-13",
            "Laporan Akhir, Dashboard Interaktif, & Presentasi",
        ),
    ]
    for r_idx, row in enumerate(sched_data):
        for c_idx, val in enumerate(row):
            cell = tbl_sched.cell(r_idx, c_idx)
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
                    if c_idx in [0, 2]
                    else WD_ALIGN_PARAGRAPH.LEFT
                )
                for r in p.runs:
                    r.font.name = "Times New Roman"
                    r.font.size = Pt(9.0)

    add_heading_2("3.3 Evaluasi Model")
    add_body(
        "Evaluasi model klasifikasi biner akan bertumpu pada metrik-metrik standar diagnostik yang komprehensif:"
    )
    add_bullet(
        "1. Confusion Matrix (2x2): ",
        "Memetakan frekuensi True Positive (TP - Dropout terdeteksi benar), False Negative (FN - Dropout gagal terdeteksi), False Positive (FP - Lulus diprediksi Dropout), dan True Negative (TN - Lulus diprediksi Lulus).",
    )
    add_bullet(
        "2. Recall (Sensitivity) Kelas Dropout: ",
        "Merupakan metrik evaluasi prioritas tertinggi. Dalam konteks pencegahan putus studi, False Negative memiliki biaya risiko institusional yang jauh lebih fatal daripada False Positive [6]. Recall tinggi memastikan hampir seluruh mahasiswa rentan berhasil terdeteksi untuk diberikan bimbingan.",
    )
    add_bullet(
        "3. F1-Score (Harmonic Mean): ",
        "Menilai keseimbangan optimal antara Precision dan Recall, khususnya untuk menangani disparitas proporsi kelas target (60,9% Graduate vs 39,1% Dropout) [6].",
    )
    add_bullet(
        "4. ROC-AUC (Area Under the Receiver Operating Characteristic): ",
        "Mengukur kapabilitas diskriminasi model dalam memisahkan kelas kelulusan di berbagai ambang batas probabilitas (threshold-independent metric).",
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


def generate_and_calibrate_proposal(output_docx: str, output_pdf: str) -> None:
    # First pass: generate with default TOC page map
    doc1 = build_proposal_document()
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
        "BAB II": ["BAB II", "METODE DAN DATASET"],
        "2.1": ["2.1 Jenis Machine Learning"],
        "2.2": ["2.2 Algoritma yang Digunakan"],
        "2.3": ["2.3 Dataset"],
        "2.4": ["2.4 Rencana Pengolahan Data"],
        "BAB III": ["BAB III", "RENCANA IMPLEMENTASI"],
        "3.1": ["3.1 Tools yang Digunakan"],
        "3.2": ["3.2 Tahapan dan Jadwal"],
        "3.3": ["3.3 Evaluasi Model"],
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

    # Second pass: re-build document with calibrated page map
    doc2 = build_proposal_document(calibrated_map)
    doc2.save(output_docx)
    os.system(cmd_pdf)
    print(f"Final proposal DOCX & PDF successfully created at: {output_pdf}")


if __name__ == "__main__":
    out_docx = "resource/ML/proposal/Proposal-Project-Akhir-ML-230411100197.docx"
    out_pdf = "resource/ML/proposal/Proposal-Project-Akhir-ML-230411100197.pdf"
    generate_and_calibrate_proposal(out_docx, out_pdf)
