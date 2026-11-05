# Web Structure Mining

Penambangan struktur web (*web structure mining*) berfokus pada analisis topologi
tautan antardokumen di *World Wide Web*. Jika penambangan konten membedah teks
halaman, struktur web memodelkan keterhubungan antarsitus sebagai graf berskala
masif $G=(V, E)$, di mana simpul (*vertex*) adalah dokumen/URL dan busur (*directed edge*)
adalah tautan hiperteks (*hyperlink*). Topologi tautan ini menjadi fondasi mesin
pencari modern dalam mengukur otoritas, reputasi, dan navigasi informasi.

## Graph Topology Fundamentals

Model graf formal didefinisikan sebagai pasangan terurut $G = (V, E)$, di mana $V$
adalah himpunan simpul tidak kosong dan $E \subseteq V \times V$ adalah himpunan
sisi atau busur.

- **Graf Tak Berarah (*Undirected Graph*)** — Relasi bersifat simetris dua arah
  $(u, v) = (v, u)$. Contoh nyata di dunia web meliputi jaringan kolaborasi
  penulis (*co-authorship*) atau koneksi pertemanan mutual.
- **Graf Berarah (*Directed Graph / Digraph*)** — Relasi asimetris memiliki arah
  panah tertentu dari sumber (*source*) ke target (*target*), $(u, v) \neq (v, u)$.
  Setiap *hyperlink* web adalah busur berarah dari halaman perujuk ke halaman yang dirujuk.
- **Matriks Ketetanggaan (*Adjacency Matrix*)** — Struktur data matematis $A$
  berukuran $|V| \times |V|$:

  $$A_{ij} = \begin{cases} 1, & \text{jika } (i, j) \in E \\ 0, & \text{lainnya} \end{cases}$$

  Pada graf tidak berarah, matriks ketetanggaan bersifat simetris sempurna ($A = A^T$).
  Sebaliknya, pada graf berarah matriks umumnya asimetris, di mana jumlahan baris
  memetakan derajat keluar (*out-degree*), sedangkan jumlahan kolom memetakan derajat
  masuk (*in-degree*):

  $$k_{\text{out}}(i) = \sum_{j=1}^{|V|} A_{ij}, \quad k_{\text{in}}(j) = \sum_{i=1}^{|V|} A_{ij}$$

- **Varian Graf Tambahan** — Meliputi graf berbobot (*weighted graph*, bobot menyatakan
  kapasitas atau jarak tautan), graf bipartit (*bigraph*, simpul terbagi menjadi dua
  himpunan saling lepas seperti relasi pengguna-halaman web), serta graf beranotasi
  atribut simpul dan busur.

## Network Metric Characterization

Karakterisasi topologi kuantitatif dilakukan dengan menghitung metrik lokal hingga
makro jaringan:

- **Derajat & Distribusi Derajat** — Derajat $k_v$ menyatakan total koneksi lokal
  suatu simpul. Derajat rata-rata jaringan didefinisikan sebagai:

  $$\langle k \rangle = \frac{2|E|}{|V|} \quad (\text{tak berarah}), \qquad \langle k_{\text{in}} \rangle = \langle k_{\text{out}} \rangle = \frac{|E|}{|V|} \quad (\text{berarah})$$

  Distribusi derajat $P(k)$ memetakan proporsi simpul yang memiliki derajat $k$.
  Graf web riil tidak mengikuti distribusi acak Poisson, melainkan hukum pangkat
  (*Power Law*) $P(k) \sim k^{-\gamma}$, membentuk jaringan bebas skala (*scale-free network*)
  di mana sedikit simpul (*hub*) menguasai mayoritas tautan.
- **Kepadatan Graf (*Graph Density*)** — Rasio antara jumlah sisi nyata terhadap
  jumlah sisi maksimal yang secara teoretis dapat terbentuk:

  $$\rho = \frac{2|E|}{|V|(|V|-1)} \quad (\text{tak berarah}), \qquad \rho = \frac{|E|}{|V|(|V|-1)} \quad (\text{berarah})$$

  Nilai $\rho$ berkisar antara 0 (graf kosong tanpa koneksi) hingga 1 (graf lengkap / *clique*).
- **Koefisien Klasterisasi (*Clustering Coefficient*)** — Mengukur tendensi
  antartetangga dari suatu simpul untuk saling terhubung membentuk siklus segitiga
  tertutup:

  $$C_i = \frac{2 e_i}{k_i (k_i - 1)}$$

  di mana $e_i$ adalah jumlah sisi aktual yang menghubungkan sesama tetangga dari simpul $i$.
  Koefisien klaster rata-rata jaringan $\langle C \rangle = \frac{1}{|V|} \sum_i C_i$
  merefleksikan modularitas lokal komunitas web.
- **Lintasan Terpendek & Diameter** — Lintasan terpendek $d(i, j)$ (*geodesic distance*)
  adalah jumlah langkah minimum yang menghubungkan simpul $i$ dan $j$. Jarak rata-rata
  $\langle d \rangle$ dan diameter $D = \max_{i, j} d(i, j)$ membuktikan fenomena
  dunia kecil (*small-world effect*): halaman web yang sangat jauh dapat dijangkau
  hanya dalam sedikit lompatan tautan (*six degrees of separation*).

## Node Prominence Measures

Banyak simpul strategis di web tidak memiliki derajat tertinggi, melainkan berfungsi
sebagai jembatan kritis (*bridge*) antar-kluster komunitas. Metrik sentralitas
mengukur derajat kepentingan struktural tersebut:

- **Sentralitas Derajat (*Degree Centrality*)** — Mengukur konektivitas langsung
  ternormalisasi terhadap ukuran jaringan:

  $$C_D(v) = \frac{k_v}{|V| - 1}$$

- **Sentralitas Keperantaraan (*Betweenness Centrality*)** — Menghitung frekuensi
  suatu simpul dilewati oleh lintasan terpendek antarpasangan simpul lain dalam jaringan:

  $$C_B(v) = \sum_{s \neq v \neq t} \frac{\sigma_{st}(v)}{\sigma_{st}}$$

  di mana $\sigma_{st}$ adalah total lintasan terpendek dari simpul $s$ ke $t$, dan
  $\sigma_{st}(v)$ adalah jumlah lintasan terpendek yang melintasi simpul $v$. Simpul
  dengan $C_B$ tinggi bertindak sebagai gerbang pengendali arus informasi (*gatekeeper*).
- **Sentralitas Kedekatan (*Closeness Centrality*)** — Kebalikan dari jarak rata-rata
  suatu simpul ke seluruh simpul lain dalam graf:

  $$C_C(i) = \left[ \frac{\sum_{j=1}^{|V|} d(i, j)}{|V| - 1} \right]^{-1}$$

  Simpul dengan sentralitas kedekatan tinggi mampu menyebarkan atau mengonsumsi informasi
  dengan latensi minimal ke seluruh penjuru web.

## Web Prestige Algorithms

Pada graf berarah, arah tautan membawa makna sosial dan otoritas: tautan masuk
menunjukkan pengakuan, rujukan, atau rekomendasi (*endorsement*).

- **Prestise Derajat (*Degree Prestige*)** — Prestise paling mendasar dihitung dari
  jumlah tautan masuk (*in-degree*):

  $$P_D(v) = k_{\text{in}}(v), \qquad C'_D(v) = \frac{k_{\text{in}}(v)}{|V| - 1}$$

- **Domain Masukan (*Input Domain*)** — Himpunan simpul $I_v \subseteq V$ yang dapat
  mencapai simpul $v$ melalui lintasan terarah, baik secara langsung maupun tidak langsung.
- **Prestise Kedekatan (*Proximity Prestige*)** — Menghitung proporsi simpul dalam
  domain masukan terhadap jarak rata-rata ke simpul target:

  $$P_P(v) = \frac{|I_v| / (|V| - 1)}{\sum_{i \in I_v} d(i, v) / |I_v|}$$

  Tautan rujukan langsung berbobot jauh lebih besar dibanding rujukan jauh berantai.
- **Rank Prestise & PageRank** — Evaluasi rekursif di mana skor suatu halaman
  ditentukan oleh prestise halaman-halaman yang merujuknya. Dalam algoritma PageRank,
  otoritas halaman perujuk dibagi rata ke seluruh tautan keluarnya (*out-degree*),
  dilengkapi faktor redaman (*damping factor* $d \approx 0{,}85$) untuk menjamin
  konvergensi rantai Markov acak (*random surfer model*):

  $$PR(i) = \frac{1 - d}{|V|} + d \sum_{(j, i) \in E} \frac{PR(j)}{k_{\text{out}}(j)}$$

Model matematis ini memastikan halaman web tidak dapat memanipulasi peringkat semata-mata
dengan membuat ribuan tautan spam dari situs berkualitas rendah.
