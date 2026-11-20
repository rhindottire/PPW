# PageRank Algorithm

Algoritma PageRank merupakan metode pengukuran prestise dan otoritas struktural
simpul dalam jaringan berarah (*directed graph*), yang pertama kali dikembangkan oleh
Larry Page dan Sergey Brin (1998) sebagai fondasi mesin pencari Google. Berbeda dari
penghitungan derajat masuk (*in-degree*) sederhana, PageRank mendefinisikan otoritas
secara rekursif: sebuah halaman bernilai penting bukan hanya karena banyak dirujuk,
melainkan karena dirujuk oleh halaman-halaman lain yang juga berbobot tinggi.

## Random Surfer Model

PageRank memodelkan navigasi penelusuran web melalui model peselancar acak
(*random surfer model*):
- Seorang pengguna maya (*surfer*) membuka suatu halaman web secara acak.
- Dari halaman saat ini, peselancar mengeklik salah satu tautan keluar (*hyperlink*)
  yang tersedia dengan probabilitas seragam $1 / k_{\text{out}}$.
- Peselancar mengulang proses penelusuran ini secara kontinu tanpa batas waktu.
- Pada batas jangka panjang (*long-run stationary state*), proporsi waktu yang dihabiskan
  peselancar pada suatu halaman merefleksikan nilai probabilitas keberadaan peselancar,
  yang menjadi skor PageRank simpul tersebut.

## Stochastic Transition Matrix

Secara matematis, graf web berarah $G = (V, E)$ dengan $N = |V|$ simpul dipetakan ke dalam
matriks probabilitas transisi stokastik kolom (*column-stochastic transition matrix*)
$M \in \mathbb{R}^{N \times N}$. Elemen baris $i$ dan kolom $j$ merepresentasikan
probabilitas transisi dari simpul $j$ menuju simpul $i$:

$$M_{ij} = \begin{cases} \frac{1}{k_{\text{out}}(j)}, & \text{jika } (j, i) \in E \\ 0, & \text{lainnya} \end{cases}$$

Sifat fundamental matriks transisi:
1. Setiap elemen bernilai non-negatif: $M_{ij} \ge 0$.
2. Jumlahan setiap kolom yang memiliki tautan keluar bernilai tepat 1:
   $$\sum_{i=1}^{N} M_{ij} = 1$$
3. Jika simpul $j$ tidak memiliki tautan keluar (*dangling node* / *dead end*), kolom $j$
   berisi angka 0 seluruhnya sehingga perlu penanganan khusus.

## Damping Factor Mechanism

Pada jaringan web riil, peselancar acak tidak selalu menelusuri tautan keluar secara
terus-menerus. Terkadang peselancar mengalami kebosanan atau terjebak, lalu memutuskan
melompat (*teleportation*) ke halaman acak mana pun di seluruh web. Perilaku ini dimodelkan
melalui faktor redaman (*damping factor*) $d \in (0, 1)$, dengan nilai standar industri
$d = 0{,}85$.

Formulasi rekursif PageRank dengan teleportasi acak didefinisikan sebagai:

$$PR(i) = \frac{1 - d}{N} + d \sum_{(j, i) \in E} \frac{PR(j)}{k_{\text{out}}(j)}$$

Dalam notasi matriks-vektor:

$$\mathbf{r} = \left(\frac{1 - d}{N}\right) \mathbf{e} + d M \mathbf{r}$$

di mana:
- $\mathbf{r} = [PR(1), PR(2), \dots, PR(N)]^T$ adalah vektor PageRank berukuran $N \times 1$
  dengan syarat normalisasi $\sum_{i=1}^N PR(i) = 1$.
- $\mathbf{e} = [1, 1, \dots, 1]^T$ adalah vektor satuan.
- $\frac{1 - d}{N}$ merepresentasikan probabilitas teleportasi acak yang terbagi rata
  ke seluruh simpul web.
- $d$ merepresentasikan probabilitas peselancar mengikuti tautan terarah yang ada.

## Power Iteration Method

Vektor PageRank $\mathbf{r}$ dihitung secara numerik menggunakan algoritma *Power Iteration*:
1. **Inisialisasi**: Berikan bobot awal yang seragam kepada seluruh simpul:
   $$\mathbf{r}^{(0)} = \left[ \frac{1}{N}, \frac{1}{N}, \dots, \frac{1}{N} \right]^T$$
2. **Pembaruan Iteratif**: Hitung nilai vektor pada iterasi $(k+1)$ dari iterasi $k$:
   $$\mathbf{r}^{(k+1)} = \left(\frac{1 - d}{N}\right) \mathbf{e} + d M \mathbf{r}^{(k)}$$
3. **Kriteria Berhenti**: Proses dihentikan saat residu perubahan vektor di bawah toleransi presisi $\epsilon$:
   $$\|\mathbf{r}^{(k+1)} - \mathbf{r}^{(k)}\|_1 = \sum_{i=1}^N |r_i^{(k+1)} - r_i^{(k)}| < \epsilon$$
   di mana toleransi standar berkisar antara $\epsilon = 10^{-6}$ hingga $10^{-8}$.

## Dead Ends & Traps

Dua anomali struktural topologi graf berarah yang dapat mengacaukan perhitungan PageRank murni:
- **Jalan Buntu (*Dead Ends*)**: Simpul tanpa tautan keluar ($k_{\text{out}} = 0$). Simpul ini
  menyerap seluruh aliran probabilitas tanpa mengalirkannya kembali (*leakage*), menyebabkan
  jumlahan probabilitas menyusut mendekati nol. Solusinya adalah membagi rata probabilitas simpul
  tersebut ke seluruh $N$ simpul web ($1/N$).
- **Perangkap Laba-laba (*Spider Traps*)**: Kelompok simpul yang saling bertaut satu sama lain
  tanpa tautan keluar ke bagian graf lain. Peselancar acak akan berputar tanpa henti di dalam
  perangkap tersebut, menyerap skor PageRank mendekati 1 dan membuat simpul lain bernilai nol.
  Faktor redaman $d < 1$ secara matematis memecahkan perangkap ini karena memberikan peluang
  $(1 - d)$ bagi peselancar untuk melompat keluar dari perangkap.

## Mathematical Convergence Properties

Menurut Teorema Perron-Frobenius:
- Matriks Google $\mathcal{G} = d M + \frac{1 - d}{N} \mathbf{e} \mathbf{e}^T$ bersifat primitif,
  stokastik kolom, dan irreducible (*tak tereduksi*) karena setiap simpul memiliki probabilitas
  positif menuju simpul mana pun.
- Nilai eigen terbesar (*dominant eigenvalue*) dari $\mathcal{G}$ tepat bernilai $\lambda_1 = 1$.
- Vektor eigen kanan terasosiasi dengan $\lambda_1 = 1$ unik, positif, dan merepresentasikan
  distribusi stasioner (*stationary distribution*) rantai Markov.
- Nilai eigen kedua dibatasi oleh $|\lambda_2| \le d$. Laju konvergensi metode *power iteration*
  ditentukan oleh rasio $|\lambda_2 / \lambda_1| \le d = 0{,}85$, yang menjamin konvergensi
  eksponensial cepat menuju solusi stabil.
