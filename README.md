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