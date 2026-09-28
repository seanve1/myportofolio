Nama : Jotham Seanvedi Takin Allo
NPM : 2506584161
Kelas : PBP F
Hobi : Badminton

### Tugas 1

1. Pada proyek ini, saya menggunakan elemen semantik HTML5 seperti `<header>`, `<main>`, `<section>`, `<nav>`, dan `<footer>`. Elemen-elemen ini sangat membantu saya dalam membagi struktur page dari website saya menjadi bagian-bagian yang lebih jelas secara fungsinya. Penggunaan tag (seperti `<section id="experience">`) membuat kode saya juga jauh lebih rapi dan mudah dibaca dibandingkan jika saya hanya menggunakan tag `<div>` untuk seluruh bagian dari pagenya.

2. Tantangan terbesar yang saya temukan adalah mengatur card pada section `Experience` agar tetap terlihat bagus untuk tampilan mobile. Di desktop, card tersebut berjajar dua kolom menyamping. Namun, untuk tampilan mobile, teks di dalamnya menjadi bertumpuk dan sulit dibaca. Saya kemudian melihat bahwa yang harus kita perhatikan di mobile (yang ukuran layarnya lebih kecil) adalah readability dari teks yang ada. Oleh karena itu, saya menggunakan `@media (max-width: 800px)` untuk mengubah tata letak menjadi satu kolom memanjang ke bawah, sehingga teks memiliki space yang cukup.

3. Batasan utama dari static web ini adalah kesulitan dalam memperbarui konten. Jika saya ingin menambah 1 pengalaman organisasi baru, saya harus copy-paste seluruh blok kode HTML secara manual. Hal ini bisa jadi memicu kesalahan penulisan. Berdasarkan batasan tersebut, fungsionalitas dinamis yang paling ingin saya tambahkan selanutnya adalah sistem database. Dengan database, saya bisa memasukkan data pengalaman dari tools admin, dan biarkan sistem yang memunculkan cardnya secara otomatis.

**AI Disclosure:**
Alat yang digunakan: Gemini.
Saya memfokuskan perintah (prompt) hanya untuk mencari solusi dari masalah spesifik pada CSS. Saya memberikan sebagian potongan kode yang bermasalah dan meminta penjelasan serta saran perbaikan.
Struktur dokumen HTML dan pengaturan desain dasar saya kerjakan secara mandiri. Bantuan AI secara khusus saya gunakan untuk memahami cara kerja susunan kolom responsif pada ukuran layar yang berbeda dan mencari referensi aturan transisi visual (hover) pada card yang ada di section Experience.
Saran dari AI terkadang mengganggu kode yang sudah berjalan dengan baik, seperti menghapus fitur tautan kontak email saya atau mencoba mengubah warna yang sudah saya tentukan. Oleh karena itu, saya tidak pernah menyalin hasil AI secara langsung. Saya menyaring kode tersebut dan memasukkannya secara manual untuk memastikan design asli saya tetap utuh.

Berikut merupakan salah satu chat yang saya ajukan ke AI:
--> jelaskan apa maksud dari 1fr
Answer (from AI): fr adalah singkatan dari fraction (bagian). Satuan 1fr berarti kolom tersebut akan mengambil satu bagian dari ruang kosong yang tersedia. Jika Anda menggunakan repeat(2, 1fr), sistem akan membagi ruang tersebut menjadi dua kolom dengan lebar yang sama rata. 

### Tugas 2

1. Alur ketika pengguna membuka halaman portofolio baru dimulai saat browser mengirimkan permintaan HTTP ke server Django. `urls.py` kemudian menerima permintaan tersebut dan meneruskannya ke  `urls.py` pada aplikasi `main`. Selanjutnya, `urls.py` aplikasi mencocokkan URL route dengan fungsi tampilan (*view*) yang ada di `views.py`. Fungsi *view* tersebut kemudian berinteraksi dengan `models.py` untuk meminta data dari database. Data dari model dikembalikan ke *view*, dimasukkan ke dalam wadah konteks (*context*), lalu dirender dan dikirimkan kembali kepada user dalam bentuk HTML melalui *template*.
2. Data disimpan pada model agar terpisah secara bersih dari struktur interface HTML. Hal ini berdampak positif terhadap kemudahan pemeliharaan dan pengembangan aplikasi karena penambahan, pembaruan, maupun penghapusan data dapat dilakukan secara dinamis melalui database atau halaman Admin Django tanpa harus mengubah kode sumber HTML secara manual.
3. Perintah `makemigrations` digunakan untuk merekam modifikasi pada `models.py` ke dalam berkas migrasi sebagai rancangan blueprint. Sementara itu, perintah `migrate` berfungsi untuk mengeksekusi dan menerapkan rancangan perubahan skema tersebut secara nyata ke dalam database. Contoh situasi yang memerlukan kedua perintah ini adalah ketika kita baru saja membuat model baru seperti `Education` atau menambahkan kolom baru ke dalam model yang sudah ada.

**AI Disclosure:**
Alat yang digunakan: Gemini.
Saya memfokuskan perintah (prompt) hanya untuk mencari solusi dari masalah spesifik pada styling CSS dan alternatif cara memanipulasi database Django. Saya memberikan sebagian potongan kode yang bermasalah dan meminta penjelasan serta saran perbaikan.
Struktur dokumen HTML, pengaturan routing (URL), dan pembuatan model dasar saya kerjakan secara mandiri. Bantuan AI secara khusus saya gunakan untuk mencari tahu cara menonaktifkan efek hover pada satu tipe card saja agar class CSS-nya tidak bertabrakan, serta menanyakan alternatif cara memasukkan data ke database melalui antarmuka web.
Saran dari AI terkadang mengganggu kode yang sudah berjalan dengan baik, seperti menyarankan nama class yang berlebihan (misalnya memakai awalan "pure-") atau tidak sengaja mengubah warna teks bawaan di dalam card. Oleh karena itu, saya tidak pernah menyalin hasil AI secara langsung. Saya menyaring logika kodenya, menyesuaikan nama class-nya, dan memasukkannya secara manual untuk memastikan desain asli saya tetap utuh.

Berikut merupakan beberapa chat yang saya ajukan ke AI:

--> gimana cara bikin card di halaman education bener-bener statis dan ga ada efek hover, tanpa ngerusak efek hover di halaman organization?
Answer (from AI): Karena sebelumnya menggunakan class dasar yang sama, Anda perlu memisahkan class-nya. Ubah pembungkus di halaman education menjadi .education-card, lalu di file CSS atur properti transform: none !important; pada pseudo-class :hover. Ini akan menimpa efek bawaan sehingga card tersebut tetap diam.

--> selain nambahin data ke database langsung dari terminal (django shell), kita bisa tambahin datanya lewat halaman admin web ga sih?
Answer (from AI): Bisa, Anda dapat menggunakan panel bawaan Django Admin. Caranya, buka file admin.py di aplikasi Anda lalu daftarkan modelnya dengan kode admin.site.register(Education). Setelah itu, buat akun admin di terminal menggunakan perintah python manage.py createsuperuser. Anda kemudian bisa login ke 127.0.0.1:8000/admin di peramban web untuk menambah dan mengelola data melalui tampilan antarmuka (UI).

### Tugas 3
1. ModelForm digunakan pada Django karena dapat membuat form secara otomatis berdasarkan model yang sudah dibuat. Dengan menggunakan ModelForm, setiap field pada form akan mengikuti struktur field yang ada pada model sehingga mengurangi penulisan kode HTML secara manual dan mempermudah proses validasi data. Selain itu, ModelForm juga memudahkan proses penyimpanan data karena data yang telah diisi pengguna dapat langsung disimpan ke database menggunakan fungsi `save()`. Penggunaan `{% csrf_token %}` diwajibkan pada form Django untuk memberikan perlindungan terhadap serangan Cross-Site Request Forgery (CSRF). Token ini memastikan bahwa request POST yang dikirim benar-benar berasal dari website yang sedang aktif dan bukan request palsu dari pihak lain.

2. JSON lebih banyak digunakan dalam pengembangan aplikasi web modern dibandingkan XML karena memiliki struktur yang lebih sederhana, ukuran data yang lebih ringan, serta lebih mudah diproses oleh berbagai bahasa pemrograman. Selain itu, format JSON sangat cocok digunakan dalam REST API karena struktur key-value pada JSON mudah digunakan oleh frontend maupun backend.

3. Pada saat data portofolio dikembalikan dalam bentuk JSON, Django terlebih dahulu mengambil data dari model/database, kemudian melakukan proses serialization untuk mengubah object Django menjadi format JSON yang dapat dikirim melalui HTTP response. Serialization diperlukan karena object yang berasal dari database belum dapat langsung dikirimkan sebagai response JSON. Setelah data diterima, proses deserialization dapat dilakukan untuk mengubah kembali data JSON menjadi object Django sehingga dapat digunakan kembali oleh aplikasi.

**AI Disclosure:**

Alat yang digunakan: ChatGPT.

Saya menggunakan bantuan AI untuk memahami implementasi lanjutan Django pada topik Form & Data Delivery, khususnya dalam menyusun alur Create, Update, Delete, serta penyajian data dalam format JSON menggunakan ModelForm dan serialization. Saya memberikan potongan kode yang sudah saya buat sebelumnya dan meminta penjelasan mengenai struktur implementasi serta kemungkinan perbaikan.

Struktur utama aplikasi, pemilihan model Education sebagai bagian yang dikembangkan, pengaturan routing, serta penyesuaian tampilan website tetap saya kerjakan dan pahami secara mandiri. Bantuan AI saya gunakan terutama untuk membantu mengecek urutan implementasi fitur CRUD, memahami hubungan antara view, form, URL, dan template, serta membantu melakukan debugging ketika terdapat kesalahan pada proses pengembangan.

Beberapa saran dari AI tidak selalu langsung saya terapkan karena terkadang menghasilkan perubahan kode yang terlalu besar atau tidak sesuai dengan struktur project yang sudah saya bangun. Oleh karena itu, saya melakukan pengecekan ulang terhadap setiap saran, menyesuaikan nama class, struktur file, serta mempertahankan desain awal website agar tetap konsisten.

Berikut merupakan beberapa chat yang saya ajukan ke AI:

--> bagaimana cara membuat update form pada Django menggunakan ModelForm dengan data yang sudah ada?

Answer (from AI): Update form pada Django dapat dilakukan dengan memberikan parameter `instance` pada ModelForm. Dengan instance tersebut, Django akan mengambil data lama berdasarkan object yang dipilih dan mengisi nilai tersebut ke dalam form sehingga pengguna dapat memperbarui data tanpa membuat data baru.

--> bagaimana cara mengubah data Django menjadi JSON lalu menampilkannya kembali di halaman web?

Answer (from AI): Data dari model Django dapat diubah menjadi JSON menggunakan serializer. Setelah dikirim sebagai response, data tersebut dapat diproses kembali menggunakan deserialization untuk mengubah format JSON menjadi object Django yang dapat digunakan kembali oleh template.

### Tugas 4

Pada Individual Assignment 4, saya melanjutkan pengembangan website portofolio dengan menerapkan sistem authentication, session, cookie, dan authorization menggunakan Django. Implementasi dilakukan dengan memanfaatkan sistem autentikasi bawaan Django untuk mengelola pengguna, serta menambahkan pembagian hak akses berdasarkan role pengguna.

Pada tugas ini, saya menambahkan role Editor menggunakan Django Group. Role Editor memiliki hak untuk memperbarui data organization, tetapi tidak memiliki izin untuk membuat atau menghapus data. Sementara itu, superuser tetap memiliki seluruh hak akses sebagai pemilik portofolio.

Selain pengaturan hak akses, saya juga mengembangkan fitur interaktif star pada Organization menggunakan relasi ManyToManyField antara User dan Organization. Fitur ini memungkinkan pengguna yang sudah login memberikan atau membatalkan star dengan mekanisme POST yang dilindungi CSRF token.

Pengujian dilakukan menggunakan Selenium End-to-End Test untuk memastikan proses login, session, cookie, dan pembatasan akses berdasarkan role berjalan sesuai kebutuhan.

**AI Disclosure:**

Alat yang digunakan: ChatGPT.

Saya menggunakan bantuan AI untuk memahami implementasi lanjutan Django pada topik authentication, session, cookie, dan authorization. Bantuan AI digunakan untuk membantu debugging ketika terdapat masalah pada routing, permission, serta implementasi role Editor menggunakan Django Group.

Struktur aplikasi, pemilihan model Organization sebagai objek yang dikembangkan, desain antarmuka, serta keputusan pembagian hak akses tetap saya kerjakan dan sesuaikan secara mandiri. Setiap saran dari AI diperiksa kembali dan tidak langsung diterapkan tanpa penyesuaian terhadap struktur project yang sudah ada.

Beberapa saran AI terkadang menghasilkan perubahan kode yang terlalu besar atau tidak sesuai dengan desain awal website. Oleh karena itu, saya melakukan evaluasi ulang, mempertahankan kode yang sudah berjalan, dan hanya menerapkan bagian yang relevan untuk menyelesaikan kebutuhan implementasi.

Berikut merupakan beberapa chat yang saya ajukan ke AI:

--> bagaimana membatasi akses create update delete berdasarkan role pengguna?

Answer (from AI):
Pembatasan akses tidak cukup hanya dilakukan pada template. Validasi harus dilakukan pada sisi server melalui view agar pengguna yang mencoba mengakses URL secara langsung tetap mendapatkan penolakan apabila tidak memiliki permission.