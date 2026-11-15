"""Script to build and execute Proposal.ipynb and Report.ipynb following canonical CRISP-DM methodology."""

import os

import nbformat
from nbclient import NotebookClient
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook


def build_proposal_notebook() -> None:
    cells = []
    cells.append(
        new_markdown_cell(
            "# Academic Success Prediction: Project Proposal\n**Mata Kuliah**: Machine Learning | **Dosen Pengampu**: Ach. Khozaimi, S.Kom., M.Kom.\n\n**Tim Pelaksana (Kelompok)**:\n1. **Achmad Ridho Fa'iz** (NIM: 230411100197) - Ketua Kelompok\n2. **[Nama Rekan Kelompok]** (NIM: [NIM Rekan Kelompok]) - Anggota Kelompok\n\nProgram Studi Teknik Informatika, Fakultas Teknik, Universitas Trunojoyo Madura (2026)"
        )
    )
    cells.append(
        new_markdown_cell(
            "## 1. Business Understanding\n\nFase pertama metodologi CRISP-DM berfokus pada pemahaman mendalam terhadap masalah fundamental institusi pendidikan tinggi, perumusan sasaran bisnis dan teknis, pemetaan pemangku kepentingan (*stakeholders*), serta penetapan kriteria keberhasilan proyek."
        )
    )
    cells.append(
        new_markdown_cell(
            "### 1.1 Define the Problem\n\nFenomena putus studi (*student dropout*) merupakan tantangan struktural kritis yang dihadapi oleh institusi pendidikan tinggi di seluruh dunia. Kegagalan mahasiswa dalam menyelesaikan studi menimbulkan kerugian multidimensi yang signifikan:\n1. **Bagi Mahasiswa**: Kerugian finansial pribadi, hilangnya waktu produktif, dan penurunan peluang mobilitas sosial-ekonomi di masa depan.\n2. **Bagi Universitas**: Penurunan efisiensi operasional, penurunan skor akreditasi institusi, pemborosan kapasitas kuota kelas, serta hilangnya pendapatan biaya kuliah (SPP).\n3. **Bagi Negara**: Pemborosan subsidi pendidikan tinggi publik dan terhambatnya target pembentukan modal manusia (*human capital*) berdaya saing global.\n\nPendekatan manajerial konvensional yang bersifat reaktif—seperti memanggil mahasiswa setelah nilai IPK anjlok di semester akhir atau setelah menunggak pembayaran SPP berbulan-bulan—terbukti tidak efektif karena intervensi datang terlambat. Oleh karena itu, diperlukan pendekatan prediktif menggunakan **Machine Learning** untuk mendeteksi indikasi dini risiko putus studi pada semester 1 dan semester 2, sehingga pihak kampus memiliki jendela waktu intervensi preventif yang memadai."
        )
    )
    cells.append(
        new_markdown_cell(
            "### 1.2 Set Objectives\n\n"
            "Proyek Machine Learning ini menetapkan dua pilar sasaran yang saling mendukung:\n"
            "1. **Sasaran Bisnis (Manajerial Kampus)**: Membangun sistem peringatan dini (*Early Warning System*) berbasis analitik prediktif untuk memetakan mahasiswa berisiko tinggi putus studi, sehingga pihak kampus dapat mengalokasikan program bimbingan akademik, restrukturisasi skema pembayaran SPP, dan bantuan beasiswa secara proaktif dan tepat sasaran.\n"
            "2. **Sasaran Machine Learning**: Mengembangkan dan membandingkan model klasifikasi biner (*Binary Classification*) untuk memprediksi apakah seorang mahasiswa akan berhasil lulus (`Graduate: 0`) atau berisiko mengalami putus studi (`Dropout: 1`) berdasarkan indikator demografis, sosio-ekonomi, dan performa kurikuler awal.\n\n"
            "**Justifikasi Pemilihan Klasifikasi Dibandingkan Regresi**:\n"
            "Pemilihan pendekatan **Supervised Classification** dan bukan **Regression** didasari oleh tiga landasan teoritis dan praktis yang mendasar:\n"
            "- **Sifat Alami Variabel Target (Diskrit Kategorikal)**: Kolom `Target` pada dataset berisi status administratif kualitatif: `Dropout`, `Enrolled`, dan `Graduate`. Ini adalah label kualitatif nominal, bukan besaran angka kontinu. Kita tidak bisa meregresikan kata 'Lulus' atau 'Dropout' karena tidak ada makna fisik dari nilai kontinu seperti *'mahasiswa ini lulus 0,73'* atau *'mahasiswa ini DO 1,45'*.\n"
            "- **Kebutuhan Intervensi Manajerial Kampus (Actionable Decision Boundary)**: Pihak kampus dan dosen wali memerlukan batas keputusan (*decision boundary*) yang tegas untuk memicu *Standard Operating Procedure (SOP)* penanganan (seperti panggilan konseling akademik darurat atau restrukturisasi cicilan SPP bagi mahasiswa berlabel 'Dropout'). Model regresi yang sekadar memprediksi angka IPK akhir tidak secara langsung menjawab pertanyaan kritis apakah mahasiswa bersangkutan akan bertahan atau keluar.\n"
            "- **Pelanggaran Asumsi Matematis Regresi Linear**: Menerapkan regresi pada target biner (*Linear Probability Model*) menghasilkan prediksi nilai yang melanggar batas probabilitas logis (bisa bernilai $< 0$ atau $> 1$) serta melanggar asumsi homoskedastisitas residual. Sebaliknya, model klasifikasi berbasis probabilitas posterior terkalibrasi memungkinkan sistem melakukan pemeringkatan risiko (*risk triage*) bertingkat secara presisi."
        )
    )
    cells.append(
        new_markdown_cell(
            "### 1.3 Identify Stakeholders\n\nPemangku kepentingan yang terlibat langsung dan menerima manfaat dari proyek ini meliputi:\n- **Pimpinan Universitas & Fakultas**: Memanfaatkan wawasan manajerial untuk merancang kebijakan retensi mahasiswa, alokasi anggaran beasiswa, dan evaluasi kurikulum.\n- **Biro Administrasi Akademik & Kemahasiswaan (BAAK)**: Memantau status pembayaran SPP dan kepatuhan registrasi secara terotomasi.\n- **Dosen Pembimbing Akademik (Dosen Wali)**: Menerima peringatan dini (*risk alert*) mengenai mahasiswa bimbingan yang terindikasi berisiko tinggi untuk segera diberikan konseling personal.\n- **Mahasiswa**: Memperoleh pendampingan akademik dan dukungan finansial sebelum terlanjur terancam sanksi putus studi.\n- **Tim Pengembang Proyek (Kelompok)**: Mahasiswa pelaksana yang bertanggung jawab mengeksekusi pipeline CRISP-DM dari eksplorasi data, rekayasa fitur, pemodelan, hingga pelaporan ilmiah."
        )
    )
    cells.append(
        new_markdown_cell(
            "### 1.4 Define Success Criteria\n\nKeberhasilan implementasi proyek diukur berdasarkan kriteria kuantitatif dan kualitatif berikut:\n1. **Kriteria Evaluasi Teknis Machine Learning**:\n   - **Recall Kelas Dropout $\\ge 85\\%$**: Mengutamakan sensitivitas deteksi terhadap kelas minoritas mahasiswa rentan DO guna meminimalkan *False Negative* (mahasiswa berisiko yang luput dari pantauan sistem).\n   - **F1-Score $\\ge 88\\%$**: Menjaga keseimbangan harmonis antara ketepatan deteksi (*Precision*) dan cakupan deteksi (*Recall*).\n   - **Akurasi Model Uji $\\ge 88\\%$**: Mengungguli secara signifikan batas *The Accuracy Trap* (baseline tebakan kelas mayoritas sebesar 60,85%).\n   - **ROC-AUC $\\ge 0,90$**: Memastikan daya pemisah probabilitas model berada pada kategori *Excellent Discrimination*.\n2. **Kriteria Transparansi & Operasional**:\n   - Menghasilkan aturan pohon keputusan (*white-box decision rules*) yang konkret dan mudah dipahami oleh pengambil kebijakan non-teknis di lingkungan kampus."
        )
    )
    cells.append(
        new_markdown_cell(
            "## 2. Data Understanding\n\nFase kedua metodologi CRISP-DM bertujuan untuk mengumpulkan data, mendeskripsikan struktur dan tipe data, melakukan eksplorasi data mendalam (*Exploratory Data Analysis / EDA*), serta memverifikasi kualitas dan integritas dataset sebelum memasuki tahap persiapan data."
        )
    )
    cells.append(
        new_markdown_cell(
            "### 2.1 Collect Data\n\nDataset yang digunakan dalam penelitian ini bersumber dari repositori terkemuka **UCI Machine Learning Repository** berjudul *'Predict Students' Dropout and Academic Success'* yang dikontribusikan oleh Valentim Realinho, Mónica V. Martins, Jorge Machado, dan Luís Baptista dari Instituto Politécnico de Portalegre, Portugal (2021).\n\n**Penjelasan Parameter Institusional Riil Ketiga Label Target**:\nBerdasarkan dokumentasi resmi institusi dan publikasi ilmiah aslinya, status kelulusan mahasiswa diekstraksi pada batas akhir durasi kurikulum normal sarjana (3 tahun / 6 semester) dengan tiga kategori institusional:\n1. **`Graduate` (Lulus)**: Mahasiswa yang berhasil menyelesaikan seluruh beban kurikulum penuh (180 ECTS / SKS sistem Eropa) pada akhir masa studi dan secara administratif dinyatakan lulus serta berhak menyandang gelar sarjana.\n2. **`Dropout` (Putus Studi / Keluar)**: Mahasiswa yang secara formal mengundurkan diri (*deregistered*) ATAU mahasiswa yang tidak melakukan registrasi ulang / menunggak pembayaran SPP (*tuition fees overdue*) melebihi batas semester toleransi sehingga hak akademiknya ditutup permanen oleh kampus sebelum mencapai 180 ECTS.\n3. **`Enrolled` (Masih Terdaftar Aktif)**: Mahasiswa yang pada saat akhir durasi normal kurikulum status registrasinya masih tercatat aktif kuliah (karena mengulang mata kuliah yang belum lulus atau sedang menyelesaikan tugas akhir). Mahasiswa ini belum memenuhi 180 ECTS, namun belum mengundurkan diri dan tetap membayar biaya registrasi.\n\n**Alasan Ilmiah Pemisahan Label `Enrolled`**:\nDalam perumusan **Binary Classification** (*Dropout vs Graduate*), kelas `Enrolled` merupakan status transisi yang sedang berjalan (*censored ongoing process*), bukan takdir akhir (*terminal outcome*). Memasukkan data `Enrolled` ke dalam data latih klasifikasi biner akan menimbulkan ambiguitas label (*label noise*) yang menurunkan akurasi model menjadi ~77%. Oleh karena itu, **794 baris data mahasiswa berstatus Enrolled disisihkan dari data latih/uji klasifikasi biner, dan dialokasikan khusus sebagai kolam simulasi inferensi sistem deteksi dini (*Early Warning System*) pada tahap deployment.**"
        )
    )
    cells.append(
        new_code_cell(
            "import os\n\nimport pandas as pd\n\n# Load dataset using semicolon delimiter\nfile_path = '../../data/ML/data.csv' if os.path.exists('../../data/ML/data.csv') else 'data/ML/data.csv'\ndf = pd.read_csv(file_path, sep=';')\n\n# Clean column names by stripping trailing whitespace or special characters\ndf.columns = df.columns.str.strip().str.replace('\"', '').str.replace('\\t', '', regex=True)\n\ndf.head(20)"
        )
    )
    cells.append(
        new_markdown_cell(
            "Tabel di atas menampilkan 20 baris pertama dari dataset mentah. Setiap baris merepresentasikan data profil individu mahasiswa yang mencakup dimensi demografis, sosio-ekonomi, dan kinerja kurikuler semester 1 dan semester 2."
        )
    )
    cells.append(
        new_markdown_cell(
            "### 2.2 Describe Data\n\nDataset terdiri atas **4.424 baris data (mahasiswa)** dan **36 kolom fitur** ditambah 1 kolom target (`Target`). Terdapat 4 kelompok besar atribut:\n1. **Fitur Demografis**: Usia saat pendaftaran (*Age at enrollment*), jenis kelamin (*Gender*), status perkawinan (*Marital status*), kewarganegaraan (*Nacionality*), dan kebutuhan pendidikan khusus (*Educational special needs*).\n2. **Fitur Sosio-Ekonomi**: Kualifikasi pendidikan ayah/ibu (*Mother's/Father's qualification*) dan pekerjaan orang tua (*Mother's/Father's occupation*).\n3. **Fitur Akademik Kurikuler (Semester 1 & 2)**: Jumlah SKS dikreditkan (*credited*), SKS didaftarkan (*enrolled*), SKS dievaluasi (*evaluations*), SKS disetujui/lulus (*approved*), dan rata-rata nilai (*grade* skala 0–20).\n4. **Fitur Finansial & Makroekonomi**: Kepatuhan SPP (*Tuition fees up to date*), status debitur utang (*Debtor*), kepemilikan beasiswa (*Scholarship holder*), serta indikator ekonomi makro (tingkat pengangguran, inflasi, dan GDP)."
        )
    )
    cells.append(
        new_code_cell(
            "summary_df = pd.DataFrame({\n    'Metric': [\n        'Total Rows (Instances)',\n        'Total Columns (Features)',\n        'Total Missing Values (NaN)',\n        'Duplicate Rows'\n    ],\n    'Value': [\n        f\"{len(df):,}\",\n        f\"{len(df.columns)}\",\n        f\"{df.isnull().sum().sum()}\",\n        f\"{df.duplicated().sum()}\"\n    ]\n})\nsummary_df"
        )
    )
    cells.append(
        new_markdown_cell(
            "Tabel ringkasan struktur di atas membuktikan bahwa dataset memiliki integritas struktural yang sangat tinggi: 4.424 observasi lengkap tanpa satupun nilai hilang (*0 missing values*) dan tanpa duplikasi baris (*0 duplicate rows*)."
        )
    )
    cells.append(
        new_code_cell(
            "key_numeric_cols = [\n    'Admission grade', 'Age at enrollment',\n    'Curricular units 1st sem (evaluations)', 'Curricular units 1st sem (approved)', 'Curricular units 1st sem (grade)',\n    'Curricular units 2nd sem (evaluations)', 'Curricular units 2nd sem (approved)', 'Curricular units 2nd sem (grade)',\n    'Unemployment rate', 'Inflation rate', 'GDP'\n]\n\nstats_summary = df[key_numeric_cols].describe().T[['count', 'mean', 'std', 'min', '50%', 'max']]\nstats_summary.columns = ['Count', 'Mean', 'Std Dev', 'Min', 'Median', 'Max']\nstats_summary.round(2)"
        )
    )
    cells.append(
        new_markdown_cell(
            "Tabel statistik deskriptif di atas memperlihatkan rentang variasi yang signifikan pada variabel kunci:\n- Nilai masuk (*Admission grade*) memiliki rata-rata 126,98 (skala 0–200).\n- Usia saat pendaftaran (*Age at enrollment*) memiliki median 20 tahun dengan nilai maksimum mencapai 70 tahun, mengindikasikan adanya populasi mahasiswa dewasa yang terdaftar melalui jalur khusus.\n- SKS yang disetujui pada semester 1 memiliki rata-rata 4,71 unit dengan deviasi standar 3,09, menunjukkan disparitas kelulusan mata kuliah yang sangat lebar antar-mahasiswa."
        )
    )
    cells.append(
        new_markdown_cell(
            "### 2.3 Explore Data (EDA)\n\nTahap Exploratory Data Analysis (EDA) dilakukan secara komprehensif melalui 6 sudut pandang analisis grafis untuk mengungkap korelasi linear, disparitas performa, anomali beban finansial, dan karakteristik demografis mahasiswa."
        )
    )
    cells.append(
        new_markdown_cell(
            "**A. Target Distribution Analysis**\n\nMemeriksa persebaran frekuensi kelas pada dataset mentah (3 kelas) dan perbandingannya dengan formulasi biner definitif:"
        )
    )
    cells.append(
        new_code_cell(
            "target_counts = df['Target'].value_counts()\ntarget_pct = (df['Target'].value_counts(normalize=True) * 100).round(2)\n\ntarget_summary = pd.DataFrame({\n    'Target Class': target_counts.index,\n    'Count (Students)': target_counts.values,\n    'Percentage (%)': target_pct.values\n})\ntarget_summary"
        )
    )
    cells.append(
        new_code_cell(
            "import matplotlib.pyplot as plt\nimport seaborn as sns\n\nplt.figure(figsize=(7, 4.5))\npalette = {'Graduate': '#2ca02c', 'Dropout': '#d62728', 'Enrolled': '#1f77b4'}\nax = sns.countplot(\n    data=df,\n    x='Target',\n    order=['Graduate', 'Dropout', 'Enrolled'],\n    hue='Target',\n    palette=palette,\n    legend=False\n)\n\nplt.title('Distribution of Student Academic Outcomes', fontsize=12, pad=12)\nplt.xlabel('Academic Outcome (Target)', fontsize=10)\nplt.ylabel('Number of Students', fontsize=10)\nplt.grid(axis='y', linestyle='--', alpha=0.5)\n\nfor p in ax.patches:\n    height = int(p.get_height())\n    pct = (height / len(df)) * 100\n    ax.annotate(f'{height:,}\\n({pct:.1f}%)', \n                (p.get_x() + p.get_width() / 2., height / 2),\n                ha='center', va='center', fontsize=10, color='white', weight='bold')\n\nplt.tight_layout()\nplt.show()"
        )
    )
    cells.append(
        new_markdown_cell(
            "Diagram batang di atas memperlihatkan komposisi kelas mentah: **Graduate 49,9% (2.209 mahasiswa)**, **Dropout 32,1% (1.421 mahasiswa)**, dan **Enrolled 18,0% (794 mahasiswa)**. Pada saat kelas Enrolled disisihkan ke kolam simulasi, proporsi kelas biner definitif menjadi **60,85% Graduate** vs **39,15% Dropout** (rasio 1,55 : 1)."
        )
    )
    cells.append(
        new_markdown_cell(
            "**B. Academic Correlation Matrix**\n\nMemeriksa korelasi Pearson antar-variabel kurikuler pada semester 1 dan semester 2 untuk mendeteksi multikolinearitas:"
        )
    )
    cells.append(
        new_code_cell(
            "acad_cols = [\n    'Curricular units 1st sem (credited)', 'Curricular units 1st sem (enrolled)',\n    'Curricular units 1st sem (evaluations)', 'Curricular units 1st sem (approved)',\n    'Curricular units 1st sem (grade)',\n    'Curricular units 2nd sem (credited)', 'Curricular units 2nd sem (enrolled)',\n    'Curricular units 2nd sem (evaluations)', 'Curricular units 2nd sem (approved)',\n    'Curricular units 2nd sem (grade)'\n]\n\nplt.figure(figsize=(9.5, 7))\ncorr_acad = df[acad_cols].corr()\n\nsns.heatmap(\n    corr_acad,\n    annot=True,\n    fmt='.2f',\n    cmap='coolwarm',\n    vmin=-1,\n    vmax=1,\n    linewidths=0.5,\n    cbar_kws={'label': 'Pearson Correlation'}\n)\n\nplt.title('Correlation Matrix of Academic Curricular Features (Semesters 1 & 2)', fontsize=12, pad=12)\nplt.xticks(rotation=45, ha='right', fontsize=8.5)\nplt.yticks(fontsize=8.5)\nplt.tight_layout()\nplt.show()"
        )
    )
    cells.append(
        new_markdown_cell(
            "Matriks korelasi di atas mengungkap multikolinearitas linear sangat tinggi:\n- Korelasi antara SKS terdaftar semester 1 dan 2 mencapai **$r = 0,94$**.\n- Korelasi antara SKS disetujui semester 1 dan 2 mencapai **$r = 0,90$**.\n- Korelasi antara nilai rata-rata semester 1 dan 2 mencapai **$r = 0,84$**.\n\nTingginya redundansi informasi ini membenarkan perlunya rekayasa fitur rasio kelulusan SKS dan selisih nilai antar-semester pada tahap Data Preparation guna meningkatkan efisiensi pembelajaran algoritma."
        )
    )
    cells.append(
        new_markdown_cell(
            "**C. Financial Risk Analysis**\n\nMenganalisis dampak tunggakan biaya kuliah (SPP) dan status debitur utang terhadap risiko putus studi:"
        )
    )
    cells.append(
        new_code_cell(
            "fig, axes = plt.subplots(1, 2, figsize=(13, 4.8))\npalette = {'Graduate': '#2ca02c', 'Dropout': '#d62728', 'Enrolled': '#1f77b4'}\n\n# 1. Tuition fees status\ntuition_pct = pd.crosstab(df['Tuition fees up to date'], df['Target'], normalize='index') * 100\ntuition_pct = tuition_pct[['Graduate', 'Dropout', 'Enrolled']]\ntuition_pct.plot(\n    kind='bar',\n    ax=axes[0],\n    color=[palette[c] for c in tuition_pct.columns],\n    width=0.7,\n    edgecolor='black',\n    linewidth=0.5\n)\naxes[0].set_title('Academic Outcome by Tuition Fees Status', fontsize=11, pad=10)\naxes[0].set_xlabel('Tuition Fees Status', fontsize=10)\naxes[0].set_ylabel('Percentage within Group (%)', fontsize=10)\naxes[0].set_xticklabels(['Unpaid / In Arrears (0)', 'Up to Date (1)'], rotation=0)\naxes[0].grid(axis='y', linestyle='--', alpha=0.5)\naxes[0].legend(title='Outcome', loc='upper right')\n\nfor container in axes[0].containers:\n    axes[0].bar_label(container, fmt='%.1f%%', label_type='edge', padding=2, fontsize=8.5)\n\n# 2. Debtor status\ndebtor_pct = pd.crosstab(df['Debtor'], df['Target'], normalize='index') * 100\ndebtor_pct = debtor_pct[['Graduate', 'Dropout', 'Enrolled']]\ndebtor_pct.plot(\n    kind='bar',\n    ax=axes[1],\n    color=[palette[c] for c in debtor_pct.columns],\n    width=0.7,\n    edgecolor='black',\n    linewidth=0.5\n)\naxes[1].set_title('Academic Outcome by Debtor Status', fontsize=11, pad=10)\naxes[1].set_xlabel('Debtor Status', fontsize=10)\naxes[1].set_ylabel('Percentage within Group (%)', fontsize=10)\naxes[1].set_xticklabels(['No Debt (0)', 'Has Debt (1)'], rotation=0)\naxes[1].grid(axis='y', linestyle='--', alpha=0.5)\naxes[1].legend(title='Outcome', loc='upper right')\n\nfor container in axes[1].containers:\n    axes[1].bar_label(container, fmt='%.1f%%', label_type='edge', padding=2, fontsize=8.5)\n\nplt.tight_layout()\nplt.show()"
        )
    )
    cells.append(
        new_markdown_cell(
            "Grafik di atas membuktikan bahwa faktor finansial merupakan salah satu pemisah paling tajam:\n- Mahasiswa yang menunggak pembayaran SPP (*Tuition fees = 0*) memiliki angka **Dropout melonjak hingga 86,6%** dengan tingkat kelulusan hanya 6,8%.\n- Mahasiswa dengan status berutang (*Debtor = 1*) memiliki angka **Dropout sebesar 61,4%**, dua kali lipat lebih tinggi dari mahasiswa tanpa utang (28,3%)."
        )
    )
    cells.append(
        new_markdown_cell(
            "**D. Scholarship Protection Analysis**\n\nMengevaluasi peran protektif bantuan pembiayaan beasiswa terhadap stabilitas kelulusan mahasiswa:"
        )
    )
    cells.append(
        new_code_cell(
            "scholar_pct = pd.crosstab(df['Scholarship holder'], df['Target'], normalize='index') * 100\nscholar_pct = scholar_pct[['Graduate', 'Dropout', 'Enrolled']]\n\nax = scholar_pct.plot(\n    kind='bar',\n    color=[palette[c] for c in scholar_pct.columns],\n    width=0.6,\n    edgecolor='black',\n    linewidth=0.5,\n    figsize=(7, 4.5)\n)\n\nplt.title('Academic Outcome Distribution by Scholarship Status', fontsize=12, pad=12)\nplt.xlabel('Scholarship Status', fontsize=10)\nplt.ylabel('Percentage within Group (%)', fontsize=10)\nplt.xticks([0, 1], ['Non-Scholarship Holder (0)', 'Scholarship Holder (1)'], rotation=0)\nplt.grid(axis='y', linestyle='--', alpha=0.5)\nplt.legend(title='Outcome', loc='upper right')\n\nfor container in ax.containers:\n    ax.bar_label(container, fmt='%.1f%%', label_type='edge', padding=2, fontsize=8.5)\n\nplt.tight_layout()\nplt.show()"
        )
    )
    cells.append(
        new_markdown_cell(
            "Hasil tabulasi silang membuktikan peran protektif beasiswa secara signifikan:\n- Penerima beasiswa (*Scholarship holder = 1*) mencapai **tingkat kelulusan 76,2%** dengan angka putus studi hanya **11,8%**.\n- Sebaliknya, mahasiswa non-beasiswa memiliki tingkat putus studi hampir 3 kali lipat lebih tinggi (38,0%). Hal ini membuktikan bahwa intervensi finansial merupakan tuas kebijakan retensi yang sangat efektif bagi universitas."
        )
    )
    cells.append(
        new_markdown_cell(
            "**E. Age Demographic & Lifelong Learning Analysis (Kasus Nyata Jalur M23)**\n\nMenganalisis distribusi usia mahasiswa saat mendaftar kuliah dan fenomena mahasiswa usia dewasa (25 hingga 70 tahun):"
        )
    )
    cells.append(
        new_code_cell(
            "plt.figure(figsize=(9, 4.5))\nfor target_label, color in palette.items():\n    subset = df[df['Target'] == target_label]\n    sns.kdeplot(\n        subset['Age at enrollment'],\n        label=f\"{target_label} (Mean: {subset['Age at enrollment'].mean():.1f} yrs)\",\n        color=color,\n        linewidth=2,\n        fill=True,\n        alpha=0.15\n    )\n\nplt.title('Distribution of Age at Enrollment Across Academic Outcomes', fontsize=12, pad=12)\nplt.xlabel('Age at Enrollment (Years)', fontsize=10)\nplt.ylabel('Probability Density', fontsize=10)\nplt.xlim(15, 60)\nplt.grid(axis='both', linestyle='--', alpha=0.5)\nplt.legend(title='Target Outcome', loc='upper right')\nplt.tight_layout()\nplt.show()"
        )
    )
    cells.append(
        new_markdown_cell(
            "**Highlight Kasus Nyata Pendidikan Tinggi Portugal (*Maiores de 23*)**:\nKurva kepadatan probabilitas (*KDE*) di atas menunjukkan distribusi usia yang condong ke kanan (*right-skewed*), dengan rentang usia pendaftaran dari **17 tahun hingga 70 tahun**. Temuan adanya mahasiswa berusia 40, 50, bahkan 70 tahun bukanlah kesalahan input data (*input error*), melainkan fenomena nyata kebijakan pendidikan tinggi di Portugal:\n1. **Jalur Akses Dewasa (*Maiores de 23 / M23*)**: Berdasarkan Perjanjian Bologna, institusi politeknik di Portugal menyediakan jalur khusus bagi orang dewasa berusia 23 tahun ke atas tanpa memerlukan ujian masuk SMA reguler. Mereka umumnya adalah pekerja profesional, orang tua, atau pensiunan yang ingin meraih gelar sarjana terapan (seperti keperawatan, agronomi, atau administrasi publik).\n2. **Kuliah Malam (*Evening Attendance*)**: Mahasiswa dewasa ini mayoritas terdaftar pada kelas malam (`Daytime/evening attendance = 0`) setelah jam kerja.\n3. **Kerentanan Dropout Tinggi**: Terlihat jelas bahwa puncak kurva mahasiswa Graduate terkonsentrasi rapat pada usia muda (18–21 tahun, rata-rata 21,3 tahun). Sebaliknya, kurva mahasiswa Dropout memiliki ekor tebal melebar ke kanan (rata-rata 26,4 tahun). Mahasiswa dewasa menghadapi konflik peran berat antara beban pekerjaan profesional, tanggung jawab keluarga, dan tuntutan akademik, sehingga risiko putus studi mereka meningkat drastis."
        )
    )
    cells.append(
        new_markdown_cell(
            "**F. Academic Performance Disparity**\n\nMenganalisis disparitas nilai rata-rata semester 1 dan semester 2 antara kelompok kelulusan:"
        )
    )
    cells.append(
        new_code_cell(
            "fig, axes = plt.subplots(1, 2, figsize=(13, 5))\n\nsns.boxplot(\n    data=df,\n    x='Target',\n    y='Curricular units 1st sem (grade)',\n    order=['Graduate', 'Dropout', 'Enrolled'],\n    palette=palette,\n    hue='Target',\n    legend=False,\n    ax=axes[0],\n    boxprops={'alpha': 0.85}\n)\naxes[0].set_title('1st Semester Grade Distribution by Outcome', fontsize=11, pad=10)\naxes[0].set_xlabel('Academic Outcome', fontsize=10)\naxes[0].set_ylabel('Grade (Scale 0 - 20)', fontsize=10)\naxes[0].grid(axis='y', linestyle='--', alpha=0.5)\n\nsns.boxplot(\n    data=df,\n    x='Target',\n    y='Curricular units 2nd sem (grade)',\n    order=['Graduate', 'Dropout', 'Enrolled'],\n    palette=palette,\n    hue='Target',\n    legend=False,\n    ax=axes[1],\n    boxprops={'alpha': 0.85}\n)\naxes[1].set_title('2nd Semester Grade Distribution by Outcome', fontsize=11, pad=10)\naxes[1].set_xlabel('Academic Outcome', fontsize=10)\naxes[1].set_ylabel('Grade (Scale 0 - 20)', fontsize=10)\naxes[1].grid(axis='y', linestyle='--', alpha=0.5)\n\nplt.tight_layout()\nplt.show()"
        )
    )
    cells.append(
        new_markdown_cell(
            "Diagram *boxplot* di atas memperlihatkan disparitas nilai yang sangat tajam:\n- Mahasiswa Graduate memiliki median nilai konsisten di atas 12,5 (skala 0–20).\n- Mahasiswa Dropout memiliki median nilai yang jatuh di bawah 10, bahkan terkonsentrasi mendekati angka 0 karena banyaknya mata kuliah yang tidak diikuti ujiannya (*unattended evaluations*).\n- Mahasiswa Enrolled berada di tengah-tengah dengan variasi nilai yang lebar, memvalidasi bahwa mereka adalah kelompok transisi yang memerlukan pemantauan berkelanjutan."
        )
    )
    cells.append(
        new_markdown_cell(
            "### 2.4 Verify Data Quality\n\nTahap verifikasi kualitas data memastikan bahwa dataset memenuhi standar kebersihan teknis, mengevaluasi pencilan statistik, membedah jebakan ketidakseimbangan kelas (*class imbalance*), serta merumuskan matriks sintesis persiapan data."
        )
    )
    cells.append(
        new_markdown_cell(
            "**1. Missing Values, Duplicates, and Domain Integrity**\n\nPemeriksaan kebersihan data dasar dan konsistensi logis domain akademik:"
        )
    )
    cells.append(
        new_code_cell(
            "quality_summary = pd.DataFrame({\n    'Pemeriksaan Kualitas': [\n        'Missing Values (Sel Kosong)',\n        'Duplikasi Baris (Duplicate Rows)',\n        'Rentang Nilai Semester (Valid Skala 0 - 20)',\n        'Konsistensi SKS (Approved <= Enrolled)'\n    ],\n    'Hasil Pemeriksaan': [\n        f\"{df.isnull().sum().sum()} nilai kosong\",\n        f\"{df.duplicated().sum()} baris duplikat\",\n        f\"Min: {df['Curricular units 1st sem (grade)'].min():.1f}, Max: {df['Curricular units 1st sem (grade)'].max():.1f} (Valid)\",\n        f\"Inkonsistensi: {sum(df['Curricular units 1st sem (approved)'] > df['Curricular units 1st sem (enrolled)'])} kasus\"\n    ],\n    'Status Integritas': [\n        'Bersih 100%',\n        'Bersih 100%',\n        'Sesuai Standar Portugal',\n        'Konsisten Logis'\n    ]\n})\nquality_summary"
        )
    )
    cells.append(
        new_markdown_cell(
            "Tabel di atas mengonfirmasi bahwa dataset bebas dari nilai kosong (*missing values*) dan duplikasi. Seluruh nilai akademik berada dalam batas sah sistem pendidikan Portugal (skala 0–20), serta jumlah SKS yang lulus (*approved*) tidak pernah melebihi SKS yang didaftarkan (*enrolled*)."
        )
    )
    cells.append(
        new_markdown_cell(
            "**2. Outlier Analysis (Metode IQR) pada Usia Pendaftaran**\n\nMendeteksi pencilan statistik pada usia pendaftaran menggunakan metode *Interquartile Range* (IQR) dan mengevaluasi justifikasi ilmiahnya:"
        )
    )
    cells.append(
        new_code_cell(
            "# Analisis Pencilan Usia dengan Metode IQR\nq1_age = df['Age at enrollment'].quantile(0.25)\nq3_age = df['Age at enrollment'].quantile(0.75)\niqr_age = q3_age - q1_age\nupper_bound_age = q3_age + 1.5 * iqr_age\noutliers_age = df[df['Age at enrollment'] > upper_bound_age]\n\noutlier_age_df = pd.DataFrame({\n    'Parameter Statistik IQR': [\n        'Kuartil 1 (Q1 - 25%)',\n        'Median (Q2 - 50%)',\n        'Kuartil 3 (Q3 - 75%)',\n        'Interquartile Range (IQR)',\n        'Ambang Batas Atas (Q3 + 1.5*IQR)',\n        'Jumlah Outlier Statistik (Usia > 34 Thn)',\n        'Persentase Outlier terhadap Populasi',\n        'Usia Maksimum dalam Dataset'\n    ],\n    'Nilai': [\n        f\"{q1_age:.1f} tahun\",\n        f\"{df['Age at enrollment'].median():.1f} tahun\",\n        f\"{q3_age:.1f} tahun\",\n        f\"{iqr_age:.1f} tahun\",\n        f\"{upper_bound_age:.1f} tahun\",\n        f\"{len(outliers_age):,} mahasiswa\",\n        f\"{len(outliers_age) / len(df) * 100:.2f}%\",\n        f\"{df['Age at enrollment'].max()} tahun\"\n    ]\n})\noutlier_age_df"
        )
    )
    cells.append(
        new_markdown_cell(
            "**Justifikasi Domain terhadap Outlier Usia (*No Trimming Policy*)**:\nSecara matematis murni, rumus IQR menetapkan batas atas usia sebesar **34,0 tahun**, sehingga sebanyak **442 mahasiswa (9,99%)** terdeteksi sebagai *outlier statistik*. Namun, dalam konteks ilmu data terapan (*applied data science*):\n1. **Bukan Kesalahan Pengukuran**: Nilai usia 35 hingga 70 tahun adalah data manusia nyata yang mendaftar secara sah melalui program jalur dewasa (*Maiores de 23*).\n2. **Bahaya Pemotongan (*Trimming Danger*)**: Menghapus 442 mahasiswa ini akan membuang 10% data riil dan menciptakan *blind spot* (kebutaan model) di mana sistem tidak akan mampu mengenali risiko mahasiswa dewasa di dunia nyata.\n3. **Keputusan Preprocessing**: Seluruh data usia dipertahankan 100% tanpa pemotongan. Untuk algoritma Decision Tree, skala usia tidak mempengaruhi pemisahan (*split*); sedangkan untuk algoritma KNN, fitur usia akan distandarisasi (*StandardScaler*) pada Data Preparation agar besaran angka tidak mendistorsi perhitungan jarak Euclidean."
        )
    )
    cells.append(
        new_markdown_cell(
            "**3. Class Imbalance Analysis & The Accuracy Trap**\n\nMenganalisis proporsi kelas biner definitif dan membongkar jebakan akurasi semu (*The Accuracy Trap*):"
        )
    )
    cells.append(
        new_code_cell(
            "# Analisis The Accuracy Trap pada Populasi Biner Definitif\ndf_bin = df[df['Target'].isin(['Graduate', 'Dropout'])]\nn_grad = sum(df_bin['Target'] == 'Graduate')\nn_drop = sum(df_bin['Target'] == 'Dropout')\ntotal_bin = len(df_bin)\n\ndummy_accuracy = (n_grad / total_bin) * 100\nimbalance_ratio = n_grad / n_drop\n\nimbalance_df = pd.DataFrame({\n    'Metrik Kelas Biner': [\n        'Total Sampel Definitif',\n        'Kelas Mayoritas: Graduate (0)',\n        'Kelas Minoritas: Dropout (1)',\n        'Rasio Ketidakseimbangan (Disproportion)',\n        'The Accuracy Trap (Dummy Classifier Baseline)',\n        'Konsekuensi Evaluasi'\n    ],\n    'Nilai Kuantitatif': [\n        f\"{total_bin:,} mahasiswa\",\n        f\"{n_grad:,} ({n_grad / total_bin * 100:.2f}%)\",\n        f\"{n_drop:,} ({n_drop / total_bin * 100:.2f}%)\",\n        f\"{imbalance_ratio:.2f} : 1 (~61% vs ~39%)\",\n        f\"{dummy_accuracy:.2f}% (Tebak Graduate Selalu)\",\n        \"Akurasi mentah menyesatkan; Wajib Recall & F1-Score\"\n    ]\n})\nimbalance_df"
        )
    )
    cells.append(
        new_markdown_cell(
            "**Analisis Dampak Ketidakseimbangan Kelas (*The Accuracy Trap*)**:\nPada populasi 3.630 data biner definitif, proporsi kelas adalah **60,85% Graduate** dan **39,15% Dropout** (rasio 1,55 : 1):\n1. **Bukan Extreme Imbalance**: Rasio 60:40 tergolong *mild imbalance* yang merupakan cerminan sehat dunia pendidikan (lebih banyak yang lulus daripada DO). Oleh karena itu, teknik manipulasi sintetis agresif seperti **SMOTE tidak direkomendasikan** karena berisiko menginterpolasi data palsu pada variabel biner (seperti beasiswa dan status debitur).\n2. **Bahaya The Accuracy Trap**: Jika model bersikap malas dan selalu memprediksi 'Graduate' untuk semua mahasiswa (*Zero-Rule / Dummy Classifier*), model akan mendapatkan **akurasi semu sebesar 60,85%** padahal gagal total mendeteksi 1 orang pun mahasiswa yang akan DO (*Recall = 0%*).\n3. **Solusi Metodologis**: Menetapkan pembobotan biaya (`class_weight='balanced'`) pada Decision Tree dan memprioritaskan metrik **Recall** dan **F1-Score** pada kelas Dropout agar model dihukum lebih berat jika melewatkan mahasiswa yang berisiko."
        )
    )
    cells.append(
        new_markdown_cell(
            "**4. Data Understanding Synthesis Matrix**\n\nTabel sintesis di bawah memetakan secara kausal bagaimana setiap temuan empiris pada Data Understanding diterjemahkan menjadi rencana aksi konkret pada tahap Data Preparation di [Report.ipynb](Report.ipynb):\n\n| No | Dimensi Temuan Data Understanding | Fakta Empiris & Statistik | Risiko terhadap Pemodelan | Rencana Aksi Data Preparation |\n| :---: | :--- | :--- | :--- | :--- |\n| **1** | **Label Target Transisi (Enrolled)** | 794 data (18,0%) belum memiliki status akhir kelulusan | Ambiguitas label (*label noise*) menurunkan performa biner | Isolasi 794 sampel Enrolled ke kolam simulasi deployment; gunakan 3.630 sampel definitif untuk pelatihan. |\n| **2** | **Korelasi Curricular Units** | Korelasi SKS sem 1 & sem 2 sangat tinggi ($r = 0,90$ s.d. $0,94$) | Multikolinearitas dan pemborosan dimensi fitur | Rekayasa fitur rasio kelulusan SKS dan delta nilai antar-semester. |\n| **3** | **Tunggakan SPP & Debitur** | SPP tertunggak melonjakkan angka DO hingga 86,6% | Fitur prediktor dominan yang rawan mengabaikan fitur lain | Pertahankan skala asli biner pada Decision Tree untuk ekstraksi aturan keputusan konkret. |\n| **4** | **Proteksi Beasiswa** | Mahasiswa penerima beasiswa memiliki tingkat lulus 76,2% | Fitur protektif pembeda signifikan | Sertakan fitur beasiswa sebagai variabel kunci tanpa transformasi destruktif. |\n| **5** | **Pencilan Usia Jalur M23** | Usia pendaftaran mencapai 70 tahun dengan 442 outlier IQR ($>34$ thn) | Distorsi fungsi jarak Euclidean pada algoritma KNN | Jangan hapus data usia; terapkan *StandardScaler* pada KNN dan biarkan skala asli pada Decision Tree. |\n| **6** | **Disparitas Kelas (61% vs 39%)** | Rasio 1,55:1 dengan baseline akurasi semu 60,85% | Bias prediksi condong ke kelas mayoritas Graduate | Terapkan *Stratified 3-Way Split* (70:15:15) dan gunakan *Cost-Sensitive Learning* (`class_weight='balanced'`). |"
        )
    )
    cells.append(
        new_markdown_cell(
            "## 3. Conclusion & Next Steps for Proposal Milestone\n\nDua fase awal dari siklus metodologi **CRISP-DM** (**1. Business Understanding** dan **2. Data Understanding**) telah diselesaikan secara komprehensif sebagai landasan kokoh bagi pelaksanaan proyek akhir Machine Learning:\n\n1. **Business Understanding**: Berhasil merumuskan urgensi krisis putus studi di perguruan tinggi, menetapkan sasaran klasifikasi biner definitif (`Dropout: 1` vs `Graduate: 0`) dengan fokus metrik Recall dan F1-Score, memetakan peran pemangku kepentingan kampus, serta mengalokasikan 794 data mahasiswa aktif (`Enrolled`) untuk sistem deteksi dini.\n2. **Data Understanding**: Memvalidasi kebersihan teknis dataset (4.424 baris, 0 missing value, 0 duplikat), mengungkap fenomena nyata mahasiswa dewasa jalur *Maiores de 23* (usia s.d. 70 tahun), mendiagnosis faktor risiko determinan (tunggakan SPP dengan DO 86,6%), serta membongkar jebakan akurasi semu (*The Accuracy Trap*) pada rasio 61:39.\n3. **Kesiapan Eksekusi**: Seluruh temuan empiris telah dipetakan secara kausal melalui Matriks Sintesis menuju tahap **3. Data Preparation**, **4. Modeling**, **5. Evaluation**, **6. Deployment Simulation**, dan **7. Rekomendasi Manajerial** yang dieksekusi secara mandiri pada notebook [Report.ipynb](Report.ipynb)."
        )
    )

    nb_prop = new_notebook(cells=cells)

    prop_path = "notebook/ML/Proposal.ipynb"
    with open(prop_path, "w", encoding="utf-8") as f:
        nbformat.write(nb_prop, f)

    print("Executing Proposal.ipynb with NotebookClient...")
    client = NotebookClient(
        nb_prop,
        timeout=600,
        kernel_name="python3",
        resources={"metadata": {"path": "notebook/ML"}},
    )
    client.execute()

    with open(prop_path, "w", encoding="utf-8") as f:
        nbformat.write(nb_prop, f)

    print("Successfully created and executed notebook/ML/Proposal.ipynb")


def build_report_notebook() -> None:
    cells = []

    # Title
    cells.append(
        new_markdown_cell(
            "# Academic Success Prediction: Final Report & Implementation\n"
            "**Mata Kuliah**: Machine Learning | **Dosen Pengampu**: Ach. Khozaimi, S.Kom., M.Kom.\n\n"
            "**Tim Pelaksana (Kelompok)**:\n"
            "1. **Achmad Ridho Fa'iz** (NIM: 230411100197) - Ketua Kelompok\n"
            "2. **[Nama Rekan Kelompok]** (NIM: [NIM Rekan Kelompok]) - Anggota Kelompok\n\n"
            "Program Studi Teknik Informatika, Fakultas Teknik, Universitas Trunojoyo Madura (2026)"
        )
    )

    # Executive Summary
    cells.append(
        new_markdown_cell(
            "## Executive Summary & Architectural Overview\n\n"
            "Notebook ini merupakan dokumen implementasi komputasi mandiri (*self-contained technical report*) yang merealisasikan fase **Data Preparation**, **Modeling**, **Evaluation**, dan **Deployment Simulation** berdasarkan hasil diagnosis empiris pada [Proposal.ipynb](Proposal.ipynb).\n\n"
            "Arsitektur teknis yang dieksekusi mencakup:\n"
            "1. **Formulasi Biner Definitif (Klasifikasi, Bukan Regresi)**: Mengisolasi $N = 3.630$ data mahasiswa berstatus kelulusan definitif (`Dropout = 1` vs `Graduate = 0`), serta menyisihkan 794 data `Enrolled` sebagai kumpulan data simulasi inferensi intervensi aktif. Status mahasiswa merupakan label kualitatif diskrit tanpa interpretasi fisik bagi nilai kontinu (seperti *'lulus 0,73'* atau *'DO 1,45'*), sehingga tugas ini dirumuskan sebagai Supervised Classification untuk menghasilkan *decision boundary* tegas bagi intervensi kampus.\n"
            "2. **Rekayasa Fitur Rasio**: Membentuk 4 fitur baru untuk mengatasi multikolinearitas SKS dan mengukur efisiensi kelulusan akademik.\n"
            "3. **Partisi 3-Arah Berstrata**: Membagi dataset menjadi **70% Data Latih** (2.541 baris), **15% Data Validasi** (544 baris untuk tuning parameter tanpa *test leakage*), dan **15% Data Uji** (545 baris untuk evaluasi akhir murni).\n"
            "4. **Dual Preprocessing Pipeline**: Menyediakan data unscaled untuk *Decision Tree* (menjaga kejelasan aturan IF-THEN) dan data terstandarisasi *StandardScaler* untuk *K-Nearest Neighbors* (menjaga keadilan fungsi jarak Euclidean).\n"
            "5. **Deployment Simulation**: Mensimulasikan deteksi dini risiko putus studi pada 794 mahasiswa aktif untuk memetakan prioritas intervensi konseling kampus."
        )
    )

    # Phase 3: Data Preparation
    cells.append(
        new_markdown_cell(
            "## 3. Data Preparation\n\n"
            "Tahap Data Preparation mentransformasikan dataset mentah `data/ML/data.csv` menjadi representasi fitur yang terstandarisasi, bebas kebocoran data (*data leakage*), dan siap diumpankan ke model Machine Learning."
        )
    )

    cells.append(
        new_markdown_cell(
            "### Data Ingestion & Target Formulation\n\n"
            "Membaca dataset mentah, menyaring sampel definitif biner (`Graduate: 0` vs `Dropout: 1`), dan mengisolasi sampel aktif (`Enrolled`).\n\n"
            "> **Justifikasi Klasifikasi vs Regresi**: Variabel target adalah status administratif kualitatif diskrit ('Graduate' vs 'Dropout'). Tidak ada makna fisik bagi nilai kontinu seperti *'mahasiswa ini lulus 0,73'* atau *'mahasiswa ini DO 1,45'*. Pendekatan Supervised Classification menyediakan *decision boundary* tegas yang dibutuhkan pihak kampus untuk memicu SOP intervensi akademik."
        )
    )

    cells.append(
        new_code_cell(
            "import os\n\n"
            "import matplotlib.pyplot as plt\n"
            "import numpy as np\n"
            "import pandas as pd\n"
            "import seaborn as sns\n\n"
            "# 1. Load raw dataset\n"
            "file_path = '../../data/ML/data.csv' if os.path.exists('../../data/ML/data.csv') else 'data/ML/data.csv'\n"
            "df_raw = pd.read_csv(file_path, sep=';')\n"
            "df_raw.columns = df_raw.columns.str.strip().str.replace('\"', '').str.replace('\\t', '', regex=True)\n\n"
            "# 2. Filter definitive binary target (Graduate vs Dropout)\n"
            "df_binary = df_raw[df_raw['Target'].isin(['Dropout', 'Graduate'])].copy()\n"
            "target_mapping = {'Graduate': 0, 'Dropout': 1}\n"
            "df_binary['Target_Code'] = df_binary['Target'].map(target_mapping)\n\n"
            "# 3. Isolate active enrolled students for simulation\n"
            "df_enrolled = df_raw[df_raw['Target'] == 'Enrolled'].copy()\n\n"
            "summary_target = pd.DataFrame({\n"
            "    'Kategori Mahasiswa': ['Graduate (Non-DO)', 'Dropout (DO Risk)', 'Enrolled (Simulation Pool)', 'Total Raw Dataset'],\n"
            "    'Kode Target': ['0 (Negatif)', '1 (Positif)', 'Inference Only', '-'],\n"
            "    'Jumlah Baris': [sum(df_binary['Target'] == 'Graduate'), sum(df_binary['Target'] == 'Dropout'), len(df_enrolled), len(df_raw)],\n"
            "    'Proporsi (%)': [\n"
            "        round(sum(df_binary['Target'] == 'Graduate') / len(df_binary) * 100, 2),\n"
            "        round(sum(df_binary['Target'] == 'Dropout') / len(df_binary) * 100, 2),\n"
            "        round(len(df_enrolled) / len(df_raw) * 100, 2),\n"
            "        100.0\n"
            "    ]\n"
            "})\n"
            "summary_target"
        )
    )

    cells.append(
        new_markdown_cell(
            "Tabel di atas mengonfirmasi keberhasilan isolasi dataset: 3.630 sampel biner definitif (60,85% Graduate dan 39,15% Dropout) siap digunakan untuk pemodelan klasifikasi biner, sedangkan 794 sampel Enrolled disimpan untuk simulasi inferensi."
        )
    )

    # Feature Engineering
    cells.append(
        new_markdown_cell(
            "### Academic Feature Engineering\n\n"
            "Merekayasa 4 fitur rasio kelulusan SKS dan delta nilai guna mereduksi multikolinearitas linear ($r \\ge 0,85$) yang ditemukan pada Data Understanding:"
        )
    )

    cells.append(
        new_code_cell(
            "# Feature engineering on binary dataset\n"
            "enrolled_1st = df_binary['Curricular units 1st sem (enrolled)']\n"
            "approved_1st = df_binary['Curricular units 1st sem (approved)']\n"
            "df_binary['Curricular units 1st sem (pass rate)'] = np.where(enrolled_1st > 0, approved_1st / enrolled_1st, 0.0)\n\n"
            "enrolled_2nd = df_binary['Curricular units 2nd sem (enrolled)']\n"
            "approved_2nd = df_binary['Curricular units 2nd sem (approved)']\n"
            "df_binary['Curricular units 2nd sem (pass rate)'] = np.where(enrolled_2nd > 0, approved_2nd / enrolled_2nd, 0.0)\n\n"
            "total_enrolled = enrolled_1st + enrolled_2nd\n"
            "total_approved = approved_1st + approved_2nd\n"
            "df_binary['Curricular units 1st year (total pass rate)'] = np.where(total_enrolled > 0, total_approved / total_enrolled, 0.0)\n\n"
            "df_binary['Curricular units grade delta'] = df_binary['Curricular units 2nd sem (grade)'] - df_binary['Curricular units 1st sem (grade)']\n\n"
            "# Apply identical feature engineering to enrolled simulation dataset\n"
            "e_enrolled_1st = df_enrolled['Curricular units 1st sem (enrolled)']\n"
            "e_approved_1st = df_enrolled['Curricular units 1st sem (approved)']\n"
            "df_enrolled['Curricular units 1st sem (pass rate)'] = np.where(e_enrolled_1st > 0, e_approved_1st / e_enrolled_1st, 0.0)\n\n"
            "e_enrolled_2nd = df_enrolled['Curricular units 2nd sem (enrolled)']\n"
            "e_approved_2nd = df_enrolled['Curricular units 2nd sem (approved)']\n"
            "df_enrolled['Curricular units 2nd sem (pass rate)'] = np.where(e_enrolled_2nd > 0, e_approved_2nd / e_enrolled_2nd, 0.0)\n\n"
            "e_total_enrolled = e_enrolled_1st + e_enrolled_2nd\n"
            "e_total_approved = e_approved_1st + e_approved_2nd\n"
            "df_enrolled['Curricular units 1st year (total pass rate)'] = np.where(e_total_enrolled > 0, e_total_approved / e_total_enrolled, 0.0)\n\n"
            "df_enrolled['Curricular units grade delta'] = df_enrolled['Curricular units 2nd sem (grade)'] - df_enrolled['Curricular units 1st sem (grade)']\n\n"
            "engineered_cols = [\n"
            "    'Curricular units 1st sem (pass rate)',\n"
            "    'Curricular units 2nd sem (pass rate)',\n"
            "    'Curricular units 1st year (total pass rate)',\n"
            "    'Curricular units grade delta'\n"
            "]\n"
            "df_binary[engineered_cols].describe().T[['mean', 'std', 'min', '50%', 'max']].round(3)"
        )
    )

    cells.append(
        new_markdown_cell(
            "Tabel ringkasan fitur turunan membuktikan terbentuknya rasio efisiensi kelulusan SKS (rata-rata 0,693 pada tahun pertama) dan dinamika selisih nilai antar-semester (rata-rata -0,381 poin)."
        )
    )

    # Stratified 3-Way Split
    cells.append(
        new_markdown_cell(
            "### Stratified 3-Way Dataset Splitting (70:15:15)\n\n"
            "Membagi dataset menjadi 70% Latih (2.541 baris), 15% Validasi (544 baris), dan 15% Uji (545 baris) dengan mempertahankan proporsi kelas target identik (`stratify=y`)."
        )
    )

    cells.append(
        new_code_cell(
            "from sklearn.model_selection import train_test_split\n\n"
            "X = df_binary.drop(columns=['Target', 'Target_Code'])\n"
            "y = df_binary['Target_Code']\n\n"
            "# First partition: 70% Train vs 30% Temp\n"
            "X_train, X_temp, y_train, y_temp = train_test_split(\n"
            "    X, y, test_size=0.30, random_state=42, stratify=y\n"
            ")\n\n"
            "# Second partition: Temp split equally into 15% Validation and 15% Test\n"
            "X_val, X_test, y_val, y_test = train_test_split(\n"
            "    X_temp, y_temp, test_size=0.50, random_state=42, stratify=y_temp\n"
            ")\n\n"
            "split_df = pd.DataFrame({\n"
            "    'Partisi Dataset': ['Data Latih (Train 70%)', 'Data Validasi (Val 15%)', 'Data Uji (Test 15%)', 'Total Definitif (100%)'],\n"
            "    'Jumlah Baris': [len(X_train), len(X_val), len(X_test), len(X)],\n"
            "    'Jumlah Fitur': [X_train.shape[1], X_val.shape[1], X_test.shape[1], X.shape[1]],\n"
            "    'Rasio Graduate (%)': [\n"
            "        round((y_train == 0).mean() * 100, 2),\n"
            "        round((y_val == 0).mean() * 100, 2),\n"
            "        round((y_test == 0).mean() * 100, 2),\n"
            "        round((y == 0).mean() * 100, 2)\n"
            "    ],\n"
            "    'Rasio Dropout (%)': [\n"
            "        round((y_train == 1).mean() * 100, 2),\n"
            "        round((y_val == 1).mean() * 100, 2),\n"
            "        round((y_test == 1).mean() * 100, 2),\n"
            "        round((y == 1).mean() * 100, 2)\n"
            "    ]\n"
            "})\n"
            "split_df"
        )
    )

    cells.append(
        new_markdown_cell(
            "Tabel di atas memvalidasi bahwa rasio kelas target berstrata terjaga presisi di seluruh partisi (~60,85% Graduate vs ~39,15% Dropout), mengeliminasi risiko bias partisi acak."
        )
    )

    # Dual Preprocessing & Export
    cells.append(
        new_markdown_cell(
            "### Dual Preprocessing Pipeline & Dataset Export\n\n"
            "Menyiapkan data unscaled untuk Decision Tree serta standardisasi Z-score (*StandardScaler*) anti-leakage untuk KNN, kemudian mengekspor seluruh partisi bersih ke `data/ML/processed/`."
        )
    )

    cells.append(
        new_code_cell(
            "from sklearn.preprocessing import StandardScaler\n\n"
            "# 1. Setup StandardScaler exclusively fitted on X_train\n"
            "scaler = StandardScaler()\n"
            "X_train_scaled = pd.DataFrame(scaler.fit_transform(X_train), columns=X_train.columns, index=X_train.index)\n"
            "X_val_scaled = pd.DataFrame(scaler.transform(X_val), columns=X_val.columns, index=X_val.index)\n"
            "X_test_scaled = pd.DataFrame(scaler.transform(X_test), columns=X_test.columns, index=X_test.index)\n\n"
            "# 2. Prepare enrolled simulation features\n"
            "X_enrolled = df_enrolled.drop(columns=['Target'])\n"
            "X_enrolled_scaled = pd.DataFrame(scaler.transform(X_enrolled), columns=X_enrolled.columns, index=X_enrolled.index)\n\n"
            "# 3. Export clean processed datasets to disk for pipeline modularity\n"
            "out_dir = '../../data/ML/processed' if os.path.exists('../../data/ML') else 'data/ML/processed'\n"
            "os.makedirs(out_dir, exist_ok=True)\n\n"
            "train_export = X_train.copy()\n"
            "train_export['Target_Code'] = y_train\n"
            "train_export.to_csv(os.path.join(out_dir, 'train_data.csv'), index=False)\n\n"
            "val_export = X_val.copy()\n"
            "val_export['Target_Code'] = y_val\n"
            "val_export.to_csv(os.path.join(out_dir, 'val_data.csv'), index=False)\n\n"
            "test_export = X_test.copy()\n"
            "test_export['Target_Code'] = y_test\n"
            "test_export.to_csv(os.path.join(out_dir, 'test_data.csv'), index=False)\n\n"
            "X_enrolled.to_csv(os.path.join(out_dir, 'enrolled_simulation.csv'), index=False)\n\n"
            "print('Processed datasets successfully exported to:', out_dir)\n"
            "print(f'Files: train_data.csv ({len(train_export)} rows), val_data.csv ({len(val_export)} rows), ' \n"
            "      f'test_data.csv ({len(test_export)} rows), enrolled_simulation.csv ({len(X_enrolled)} rows)')"
        )
    )

    cells.append(
        new_markdown_cell(
            "Seluruh partisi data telah berhasil disimpan secara terstruktur di `data/ML/processed/`. Selanjutnya sistem memasuki fase **Modeling**."
        )
    )

    # Phase 4: Modeling & Hyperparameter Tuning
    cells.append(
        new_markdown_cell(
            "## 4. Modeling & Hyperparameter Tuning\n\n"
            "Fase Modeling menerapkan strategi optimasi berbasis **Data Validasi (Validation Set - 544 baris)** untuk memilih hyperparameter terbaik dari masing-masing algoritma tanpa menyentuh data uji murni (*anti-data leakage*):\n"
            "1. **Decision Tree Classifier**: Mencari kedalaman pohon optimal (`max_depth`) untuk menghindari *overfitting*.\n"
            "2. **K-Nearest Neighbors (KNN)**: Mencari jumlah tetangga terdekat optimal ($K$) dan fungsi pembobotan jarak."
        )
    )

    cells.append(
        new_markdown_cell(
            "### Model 1: Decision Tree Classifier & Tuning Kedalaman Pohon\n\n"
            "Melakukan iterasi eksplorasi parameter `max_depth` pada data validasi dengan mengevaluasi metrik Akurasi, F1-Score, dan Recall Dropout:"
        )
    )

    cells.append(
        new_code_cell(
            "from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score\n"
            "from sklearn.tree import DecisionTreeClassifier\n\n"
            "depth_range = [2, 3, 4, 5, 6, 7, 8, 10, 12, 15, None]\n"
            "dt_results = []\n\n"
            "for depth in depth_range:\n"
            "    dt = DecisionTreeClassifier(max_depth=depth, random_state=42, class_weight='balanced')\n"
            "    dt.fit(X_train, y_train)\n"
            "    \n"
            "    # Predict on validation set\n"
            "    y_val_pred = dt.predict(X_val)\n"
            "    \n"
            "    dt_results.append({\n"
            "        'max_depth': str(depth) if depth is not None else 'None',\n"
            "        'Val_Accuracy': accuracy_score(y_val, y_val_pred),\n"
            "        'Val_Precision': precision_score(y_val, y_val_pred, pos_label=1),\n"
            "        'Val_Recall': recall_score(y_val, y_val_pred, pos_label=1),\n"
            "        'Val_F1': f1_score(y_val, y_val_pred, pos_label=1)\n"
            "    })\n\n"
            "df_dt_tune = pd.DataFrame(dt_results)\n\n"
            "# Visualisasi kurva tuning Decision Tree\n"
            "plt.figure(figsize=(9, 4.5))\n"
            "plt.plot(df_dt_tune['max_depth'], df_dt_tune['Val_Accuracy'], marker='o', label='Accuracy', color='#1f77b4')\n"
            "plt.plot(df_dt_tune['max_depth'], df_dt_tune['Val_Recall'], marker='s', label='Recall (Dropout)', color='#d62728')\n"
            "plt.plot(df_dt_tune['max_depth'], df_dt_tune['Val_F1'], marker='^', label='F1-Score', color='#2ca02c')\n"
            "plt.title('Kurva Tuning Hyperparameter max_depth Decision Tree pada Data Validasi', fontsize=12, pad=12)\n"
            "plt.xlabel('Nilai max_depth', fontsize=10)\n"
            "plt.ylabel('Skor Kinerja Validasi', fontsize=10)\n"
            "plt.grid(True, linestyle='--', alpha=0.6)\n"
            "plt.legend()\n"
            "plt.tight_layout()\n"
            "plt.show()\n\n"
            "df_dt_tune.round(3)"
        )
    )

    cells.append(
        new_markdown_cell(
            "Grafik kurva validasi di atas memperlihatkan fenomena *overfitting*: saat `max_depth > 6`, skor F1-score pada data validasi mulai melandai dan menurun. Nilai `max_depth = 5` memberikan keseimbangan optimal antara Recall tinggi (~83%) dan F1-Score stabil (~80%). Model Decision Tree final dilatih dengan parameter optimal ini."
        )
    )

    cells.append(
        new_code_cell(
            "# Train best Decision Tree model\n"
            "best_dt = DecisionTreeClassifier(max_depth=5, random_state=42, class_weight='balanced')\n"
            "best_dt.fit(X_train, y_train)\n"
            "print('Best Decision Tree model successfully trained with max_depth=5.')"
        )
    )

    # Model 2: KNN
    cells.append(
        new_markdown_cell(
            "### Model 2: K-Nearest Neighbors (KNN) & Tuning Jumlah Tetangga K\n\n"
            "Mengevaluasi variasi jumlah tetangga $K \\in [3, 5, 7, 9, 11, 15, 21, 25]$ pada data validasi terstandarisasi (`X_val_scaled`):"
        )
    )

    cells.append(
        new_code_cell(
            "from sklearn.neighbors import KNeighborsClassifier\n\n"
            "k_values = [3, 5, 7, 9, 11, 15, 21, 25]\n"
            "knn_results = []\n\n"
            "for k in k_values:\n"
            "    knn = KNeighborsClassifier(n_neighbors=k, weights='distance', metric='euclidean')\n"
            "    knn.fit(X_train_scaled, y_train)\n"
            "    \n"
            "    y_val_pred_knn = knn.predict(X_val_scaled)\n"
            "    \n"
            "    knn_results.append({\n"
            "        'K_Neighbors': k,\n"
            "        'Val_Accuracy': accuracy_score(y_val, y_val_pred_knn),\n"
            "        'Val_Precision': precision_score(y_val, y_val_pred_knn, pos_label=1),\n"
            "        'Val_Recall': recall_score(y_val, y_val_pred_knn, pos_label=1),\n"
            "        'Val_F1': f1_score(y_val, y_val_pred_knn, pos_label=1)\n"
            "    })\n\n"
            "df_knn_tune = pd.DataFrame(knn_results)\n\n"
            "# Visualisasi kurva tuning KNN\n"
            "plt.figure(figsize=(9, 4.5))\n"
            "plt.plot(df_knn_tune['K_Neighbors'], df_knn_tune['Val_Accuracy'], marker='o', label='Accuracy', color='#1f77b4')\n"
            "plt.plot(df_knn_tune['K_Neighbors'], df_knn_tune['Val_Recall'], marker='s', label='Recall (Dropout)', color='#d62728')\n"
            "plt.plot(df_knn_tune['K_Neighbors'], df_knn_tune['Val_F1'], marker='^', label='F1-Score', color='#2ca02c')\n"
            "plt.title('Kurva Tuning Hyperparameter K-Neighbors pada Data Validasi (Scaled)', fontsize=12, pad=12)\n"
            "plt.xlabel('Nilai K (Jumlah Tetangga)', fontsize=10)\n"
            "plt.ylabel('Skor Kinerja Validasi', fontsize=10)\n"
            "plt.grid(True, linestyle='--', alpha=0.6)\n"
            "plt.legend()\n"
            "plt.tight_layout()\n"
            "plt.show()\n\n"
            "df_knn_tune.round(3)"
        )
    )

    cells.append(
        new_markdown_cell(
            "Tabel dan kurva tuning KNN menunjukkan bahwa $K = 11$ menghasilkan F1-score puncak (~78%) dan akurasi stabil (~84%). Model KNN final dilatih menggunakan konfigurasi $K = 11$ dan pembobotan berbasis jarak (`weights='distance'`)."
        )
    )

    cells.append(
        new_code_cell(
            "# Train best KNN model\n"
            "best_knn = KNeighborsClassifier(n_neighbors=11, weights='distance', metric='euclidean')\n"
            "best_knn.fit(X_train_scaled, y_train)\n"
            "print('Best KNN model successfully trained with K=11.')"
        )
    )

    # Phase 5: Evaluation
    cells.append(
        new_markdown_cell(
            "## 5. Evaluation & Model Comparison\n\n"
            "Fase Evaluation menguji performa generalisasi kedua model terbaik secara objektif pada **Data Uji Independen (Test Set - 545 baris)** yang belum pernah disentuh selama pelatihan dan tuning."
        )
    )

    cells.append(
        new_code_cell(
            "from sklearn.metrics import confusion_matrix, roc_auc_score, roc_curve\n\n"
            "# Predictions on independent Test Set\n"
            "y_test_pred_dt = best_dt.predict(X_test)\n"
            "y_test_proba_dt = best_dt.predict_proba(X_test)[:, 1]\n\n"
            "y_test_pred_knn = best_knn.predict(X_test_scaled)\n"
            "y_test_proba_knn = best_knn.predict_proba(X_test_scaled)[:, 1]\n\n"
            "# Matriks perbandingan kuantitatif\n"
            "comparison_df = pd.DataFrame({\n"
            "    'Metrik Evaluasi (Test Set)': ['Accuracy', 'Precision (Dropout)', 'Recall (Dropout)', 'F1-Score (Dropout)', 'ROC-AUC Score'],\n"
            "    'Decision Tree (max_depth=5)': [\n"
            "        accuracy_score(y_test, y_test_pred_dt),\n"
            "        precision_score(y_test, y_test_pred_dt, pos_label=1),\n"
            "        recall_score(y_test, y_test_pred_dt, pos_label=1),\n"
            "        f1_score(y_test, y_test_pred_dt, pos_label=1),\n"
            "        roc_auc_score(y_test, y_test_proba_dt)\n"
            "    ],\n"
            "    'K-Nearest Neighbors (K=11)': [\n"
            "        accuracy_score(y_test, y_test_pred_knn),\n"
            "        precision_score(y_test, y_test_pred_knn, pos_label=1),\n"
            "        recall_score(y_test, y_test_pred_knn, pos_label=1),\n"
            "        f1_score(y_test, y_test_pred_knn, pos_label=1),\n"
            "        roc_auc_score(y_test, y_test_proba_knn)\n"
            "    ]\n"
            "})\n"
            "comparison_df.round(4)"
        )
    )

    cells.append(
        new_markdown_cell(
            "Tabel perbandingan di atas memperlihatkan profil komplementer yang sangat menarik:\n"
            "- **Decision Tree**: Mengunggul secara signifikan pada **Recall Dropout (82,63%)** berkat pembobotan kelas seimbang (`class_weight='balanced'`). Dari 213 mahasiswa putus studi di data uji, model ini berhasil menjaring sebagian besar mahasiswa berisiko.\n"
            "- **K-Nearest Neighbors**: Mengunggul pada **Precision (81,77%)** dan **Akurasi Keseluruhan (84,77%)**, menghasilkan alarm palsu (*False Positive*) yang lebih sedikit."
        )
    )

    # Confusion Matrix & ROC Curves
    cells.append(
        new_code_cell(
            "fig, axes = plt.subplots(1, 2, figsize=(13, 5))\n\n"
            "# 1. Confusion Matrix DT vs KNN\n"
            "cm_dt = confusion_matrix(y_test, y_test_pred_dt)\n"
            "sns.heatmap(cm_dt, annot=True, fmt='d', cmap='Blues', ax=axes[0],\n"
            "            xticklabels=['Graduate (0)', 'Dropout (1)'], yticklabels=['Graduate (0)', 'Dropout (1)'])\n"
            "axes[0].set_title(f'Confusion Matrix: Decision Tree\\nRecall Dropout: {recall_score(y_test, y_test_pred_dt):.2%}', fontsize=11)\n"
            "axes[0].set_ylabel('Status Aktual', fontsize=10)\n"
            "axes[0].set_xlabel('Prediksi Model', fontsize=10)\n\n"
            "cm_knn = confusion_matrix(y_test, y_test_pred_knn)\n"
            "sns.heatmap(cm_knn, annot=True, fmt='d', cmap='Greens', ax=axes[1],\n"
            "            xticklabels=['Graduate (0)', 'Dropout (1)'], yticklabels=['Graduate (0)', 'Dropout (1)'])\n"
            "axes[1].set_title(f'Confusion Matrix: KNN (K=11)\\nPrecision: {precision_score(y_test, y_test_pred_knn):.2%}', fontsize=11)\n"
            "axes[1].set_ylabel('Status Aktual', fontsize=10)\n"
            "axes[1].set_xlabel('Prediksi Model', fontsize=10)\n\n"
            "plt.tight_layout()\n"
            "plt.show()"
        )
    )

    # ROC Curve Plot
    cells.append(
        new_code_cell(
            "fpr_dt, tpr_dt, _ = roc_curve(y_test, y_test_proba_dt)\n"
            "fpr_knn, tpr_knn, _ = roc_curve(y_test, y_test_proba_knn)\n\n"
            "plt.figure(figsize=(7.5, 5))\n"
            "plt.plot(fpr_dt, tpr_dt, label=f'Decision Tree (AUC = {roc_auc_score(y_test, y_test_proba_dt):.3f})', color='#1f77b4', lw=2)\n"
            "plt.plot(fpr_knn, tpr_knn, label=f'K-Nearest Neighbors (AUC = {roc_auc_score(y_test, y_test_proba_knn):.3f})', color='#2ca02c', lw=2)\n"
            "plt.plot([0, 1], [0, 1], 'k--', lw=1.5, label='Random Guessing (AUC = 0.500)')\n"
            "plt.title('Kurva ROC Perbandingan Decision Tree vs KNN pada Data Uji Independen', fontsize=11, pad=12)\n"
            "plt.xlabel('False Positive Rate (1 - Specificity)', fontsize=10)\n"
            "plt.ylabel('True Positive Rate (Recall)', fontsize=10)\n"
            "plt.grid(True, linestyle='--', alpha=0.6)\n"
            "plt.legend(loc='lower right')\n"
            "plt.tight_layout()\n"
            "plt.show()"
        )
    )

    # Feature Importance
    cells.append(
        new_markdown_cell(
            "### Feature Importance Analysis (Transparansi Decision Tree)\n\n"
            "Menganalisis 10 fitur paling berpengaruh dalam mendeteksi risiko putus studi berdasarkan pohon keputusan:"
        )
    )

    cells.append(
        new_code_cell(
            "feat_imp = pd.Series(best_dt.feature_importances_, index=X_train.columns).sort_values(ascending=False)\n\n"
            "plt.figure(figsize=(9, 4.8))\n"
            "feat_imp.head(10).plot(kind='barh', color='#2b5c8f').invert_yaxis()\n"
            "plt.title('Top 10 Feature Importance: Determinan Risiko Putus Studi (Decision Tree)', fontsize=12, pad=12)\n"
            "plt.xlabel('Tingkat Kepentingan Relatif (Gini Importance)', fontsize=10)\n"
            "plt.tight_layout()\n"
            "plt.show()\n\n"
            "pd.DataFrame({'Fitur': feat_imp.head(10).index, 'Relative Importance': feat_imp.head(10).values.round(4)})"
        )
    )

    cells.append(
        new_markdown_cell(
            "Grafik di atas memvalidasi secara empiris bahwa penentu utama kelulusan adalah: 1) `Curricular units 2nd sem (approved)` dan `Curricular units 1st sem (approved)`, 2) `Tuition fees up to date` (status tunggakan SPP), dan 3) `Curricular units 1st year (total pass rate)` (fitur hasil rekayasa kita)."
        )
    )

    # Phase 6: Deployment Simulation
    cells.append(
        new_markdown_cell(
            "## 6. Deployment Simulation: Active Student Early Warning System\n\n"
            "Mensimulasikan inferensi model Decision Tree pada **794 data mahasiswa aktif (`Enrolled`)** untuk mengidentifikasi tingkat urgensi intervensi sebelum mereka terlanjur mengalami putus studi."
        )
    )

    cells.append(
        new_code_cell(
            "# Predict probabilities on active enrolled students\n"
            "enrolled_risk_proba = best_dt.predict_proba(X_enrolled)[:, 1]\n"
            "df_enrolled_sim = df_enrolled.copy()\n"
            "df_enrolled_sim['Risk_Probability'] = enrolled_risk_proba\n\n"
            "# Triage Risk Segmentation\n"
            "def assign_risk_tier(p):\n"
            "    if p >= 0.60:\n"
            "        return 'Tinggi (Intervensi Mendesak)'\n"
            "    elif p >= 0.40:\n"
            "        return 'Sedang (Pendampingan Dosen Wali)'\n"
            "    else:\n"
            "        return 'Rendah (Jalur Reguler Aman)'\n\n"
            "df_enrolled_sim['Risk_Tier'] = df_enrolled_sim['Risk_Probability'].apply(assign_risk_tier)\n"
            "tier_counts = df_enrolled_sim['Risk_Tier'].value_counts()\n"
            "tier_pct = (df_enrolled_sim['Risk_Tier'].value_counts(normalize=True) * 100).round(2)\n\n"
            "sim_summary = pd.DataFrame({\n"
            "    'Tingkat Risiko Intervensi': tier_counts.index,\n"
            "    'Jumlah Mahasiswa Aktif': tier_counts.values,\n"
            "    'Persentase (%)': tier_pct.values\n"
            "})\n"
            "\n"
            "# Visualisasi Triage Risiko Mahasiswa Enrolled\n"
            "plt.figure(figsize=(8, 4.5))\n"
            "colors = {'Tinggi (Intervensi Mendesak)': '#d62728', 'Sedang (Pendampingan Dosen Wali)': '#ff7f0e', 'Rendah (Jalur Reguler Aman)': '#2ca02c'}\n"
            "ax = sns.barplot(data=sim_summary, x='Tingkat Risiko Intervensi', y='Jumlah Mahasiswa Aktif', palette=colors)\n"
            "for p in ax.patches:\n"
            "    ax.annotate(f'{int(p.get_height())} mhs', (p.get_x() + p.get_width() / 2., p.get_height() / 2.),\n"
            "                ha='center', va='center', color='white', fontweight='bold', fontsize=11)\n"
            "plt.title('Simulasi Early Warning System: Segmentasi Risiko pada 794 Mahasiswa Aktif', fontsize=12, pad=12)\n"
            "plt.ylabel('Jumlah Mahasiswa', fontsize=10)\n"
            "plt.xlabel('Prioritas Intervensi Kampus', fontsize=10)\n"
            "plt.tight_layout()\n"
            "plt.show()\n\n"
            "sim_summary"
        )
    )

    cells.append(
        new_markdown_cell(
            "Hasil simulasi peringatan dini (*Early Warning System*) pada 794 mahasiswa aktif membuktikan manfaat manajerial langsung bagi program studi: sistem berhasil mengidentifikasi mahasiswa berkategori risiko tinggi yang harus segera dihubungi oleh biro kemahasiswaan untuk restrukturisasi SPP atau bimbingan khusus sebelum terlambat."
        )
    )

    # Conclusion & Recommendations
    cells.append(
        new_markdown_cell(
            "## 7. Conclusion & Managerial Recommendations\n\n"
            "### Kesimpulan Proyek\n"
            "1. **Integritas Metodologi CRISP-DM**: Proyek berhasil menyelesaikan siklus penuh CRISP-DM secara modular, dimulai dari perumusan sasaran biner, pemisahan kolam simulasi 794 mahasiswa aktif, rekayasa 4 fitur rasio SKS, partisi 3-arah berstrata (70:15:15), hingga evaluasi independen anti-leakage.\n"
            "2. **Kinerja Algoritma**: Model **Decision Tree** terbukti paling efektif sebagai sistem deteksi dini berkat capaian **Recall 82,63%** pada data uji murni (menekan false negative seminimal mungkin) dengan interpretabilitas aturan IF-THEN yang transparan. Di sisi lain, **KNN** memberikan kepastian presisi tinggi (81,77%) untuk memvalidasi kemiripan profil mahasiswa.\n"
            "3. **Faktor Determinan Kunci**: Kegagalan kelulusan SKS pada semester 1 dan 2 serta penunggakan biaya SPP merupakan pemicu utama putus studi yang memerlukan penanganan terpadu.\n\n"
            "### Rekomendasi Manajerial bagi Universitas Trunojoyo Madura\n"
            "1. **Penerapan Early Warning System Otomatis**: Mengintegrasikan model Decision Tree ke dalam sistem informasi akademik (SIAKAD) UTM untuk memberikan notifikasi otomatis pada dosen wali saat mahasiswa meluluskan kurang dari separuh beban SKS semester 1.\n"
            "2. **Kebijakan Skema Angsuran SPP**: Memberikan program restrukturisasi cicilan pembayaran SPP sebelum batas waktu pembayaran berakhir, mengingat tunggakan SPP memicu risiko putus studi hingga 86,6%.\n"
            "3. **Pendampingan Khusus Mahasiswa Dewasa**: Menyelenggarakan program konseling adaptasi dan mentoring khusus bagi mahasiswa baru jalur pendaftaran usia dewasa (>25 tahun)."
        )
    )

    nb_rep = new_notebook(cells=cells)
    rep_path = "notebook/ML/Report.ipynb"
    with open(rep_path, "w", encoding="utf-8") as f:
        nbformat.write(nb_rep, f)

    print("Executing Report.ipynb with NotebookClient...")
    client = NotebookClient(
        nb_rep,
        timeout=600,
        kernel_name="python3",
        resources={"metadata": {"path": "notebook/ML"}},
    )
    client.execute()

    with open(rep_path, "w", encoding="utf-8") as f:
        nbformat.write(nb_rep, f)

    print("Successfully created and executed notebook/ML/Report.ipynb")


if __name__ == "__main__":
    build_proposal_notebook()
    build_report_notebook()
    # Remove old UAS.ipynb
    old_uas = "notebook/ML/UAS.ipynb"
    if os.path.exists(old_uas):
        os.remove(old_uas)
        print(f"Removed old legacy notebook: {old_uas}")
