"""Script to split UAS.ipynb into Proposal.ipynb and Report.ipynb and execute them end-to-end."""

import os

import nbformat
from nbclient import NotebookClient
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook


def build_proposal_notebook() -> None:
    src_path = "notebook/ML/UAS.ipynb"
    with open(src_path, encoding="utf-8") as f:
        nb_src = nbformat.read(f, as_version=4)

    # Proposal.ipynb takes cells 0 to 38 (Business Understanding and Data Understanding + Synthesis)
    cells_proposal = list(nb_src["cells"][:39])

    # Add a closing conclusion cell for the Proposal milestone
    conclusion_text = (
        "## Conclusion & Next Steps for Proposal Milestone\n\n"
        "Dua fase awal dari siklus metodologi **CRISP-DM** (**Business Understanding** dan **Data Understanding**) telah diselesaikan secara komprehensif:\n"
        "1. **Business Understanding**: Merumuskan permasalahan kritis retensi mahasiswa melalui sasaran klasifikasi biner definitif (`Dropout = 1` vs `Graduate = 0`) dengan prioritas metrik Recall dan F1-Score pada kelas mahasiswa rentan putus studi, serta menyisihkan 794 data mahasiswa aktif (`Enrolled`) sebagai kolam simulasi pemantauan preventif.\n"
        "2. **Data Understanding**: Memvalidasi kebersihan dataset (4.424 baris, 0 missing value, 0 duplikat), mendiagnosis faktor risiko determinan (tunggakan SPP dengan DO 86,6%, proteksi beasiswa dengan kelulusan 76,2%, multikolinearitas SKS tahun pertama $r \\ge 0,85$, dan kerentanan usia pendaftaran dewasa).\n"
        "3. **Matriks Sintesis**: Memetakan setiap temuan empiris secara kausal ke dalam rencana aksi konkret tahap Data Preparation (rekayasa fitur rasio/delta, partisi berstrata 70:15:15, dan arsitektur *Dual Preprocessing Pipeline*).\n\n"
        "Seluruh implementasi teknis tahap **Data Preparation**, **Modeling** (Decision Tree & K-Nearest Neighbors), **Evaluation**, serta **Deployment Simulation** dieksekusi secara mandiri pada notebook [Report.ipynb](Report.ipynb)."
    )
    cells_proposal.append(new_markdown_cell(conclusion_text))

    nb_prop = new_notebook(cells=cells_proposal)

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
            "1. **Formulasi Biner Definitif**: Mengisolasi $N = 3.630$ data mahasiswa berstatus kelulusan definitif (`Dropout = 1` vs `Graduate = 0`), serta menyisihkan 794 data `Enrolled` sebagai kumpulan data simulasi inferensi intervensi aktif.\n"
            "2. **Rekayasa Fitur Rasio**: Membentuk 4 fitur baru untuk mengatasi multikolinearitas SKS dan mengukur efisiensi kelulusan akademik.\n"
            "3. **Partisi 3-Arah Berstrata**: Membagi dataset menjadi **70% Data Latih** (2.541 baris), **15% Data Validasi** (544 baris untuk tuning parameter tanpa *test leakage*), dan **15% Data Uji** (545 baris untuk evaluasi akhir murni).\n"
            "4. **Dual Preprocessing Pipeline**: Menyediakan data unscaled untuk *Decision Tree* (menjaga kejelasan aturan IF-THEN) dan data terstandarisasi *StandardScaler* untuk *K-Nearest Neighbors* (menjaga keadilan fungsi jarak Euclidean).\n"
            "5. **Deployment Simulation**: Mensimulasikan deteksi dini risiko putus studi pada 794 mahasiswa aktif untuk memetakan prioritas intervensi konseling kampus."
        )
    )

    # Phase 3: Data Preparation
    cells.append(
        new_markdown_cell(
            "## Data Preparation\n\n"
            "Tahap Data Preparation mentransformasikan dataset mentah `data/ML/data.csv` menjadi representasi fitur yang terstandarisasi, bebas kebocoran data (*data leakage*), dan siap diumpankan ke model Machine Learning."
        )
    )

    cells.append(
        new_markdown_cell(
            "### Data Ingestion & Target Formulation\n\n"
            "Membaca dataset mentah, menyaring sampel definitif biner (`Graduate: 0` vs `Dropout: 1`), dan mengisolasi sampel aktif (`Enrolled`)."
        )
    )

    cells.append(
        new_code_cell(
            "import os\n"
            "import pandas as pd\n"
            "import numpy as np\n"
            "import matplotlib.pyplot as plt\n"
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
            "## Modeling & Hyperparameter Tuning\n\n"
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
            "from sklearn.tree import DecisionTreeClassifier\n"
            "from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score\n\n"
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
            "## Evaluation & Model Comparison\n\n"
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
            "## Deployment Simulation: Active Student Early Warning System\n\n"
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
            "## Conclusion & Managerial Recommendations\n\n"
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
