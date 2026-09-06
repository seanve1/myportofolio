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