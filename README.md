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

### Tugas 5
Pada Individual Assignment 5, saya melanjutkan pengembangan website portofolio dengan menerapkan interaktivitas web modern berbasis JavaScript secara *end-to-end* pada bagian Education. Implementasi ini mencakup pemuatan data menggunakan AJAX (Fetch API) tanpa me-*reload* halaman, fitur pencarian dinamis dengan teknik *debouncing*, serta penambahan data baru melalui modal *popover* yang mengirimkan data secara asinkronus. Selain itu, saya juga mengintegrasikan sistem notifikasi *toast* untuk umpan balik pengguna, menerapkan perlindungan keamanan dari serangan *Cross-Site Scripting* (XSS) melalui *escaping* di sisi *frontend* dan `strip_tags` di *backend*, serta mempertahankan pembagian hak akses sesuai peran pengguna dari tugas sebelumnya.

**AI Disclosure:**

Alat yang digunakan: Gemini.
Saya menggunakan bantuan AI untuk memahami implementasi AJAX, Fetch API, penanganan token CSRF pada *method* POST, implementasi *debouncing* pada fitur pencarian, serta teknik *escaping* XSS di JavaScript. Saya memberikan potongan kode yang sudah saya buat sebelumnya dan meminta penjelasan mengenai struktur implementasi serta kemungkinan perbaikan.

Struktur utama aplikasi, penyesuaian desain kartu pendidikan agar tetap konsisten dengan gaya asli saya, serta pengaturan hak akses peran tetap saya kerjakan dan pahami secara mandiri. Bantuan AI saya gunakan terutama untuk membantu saya menyusun struktur respons `JsonResponse` manual, memahami alur kerja `async/await` pada `fetch()`, serta *debugging* ketika terjadi kendala pada sinkronisasi data asinkronus.

Beberapa saran dari AI terkadang tidak langsung saya terapkan karena mengubah desain kartu HTML menjadi seragam dengan bagian lain yang tidak sesuai dengan preferensi estetika saya. Oleh karena itu, saya melakukan pengecekan ulang terhadap setiap saran, memperbaiki struktur *render card* secara manual, dan memastikan fungsionalitas berjalan dengan aman.

Berikut merupakan beberapa chat yang saya ajukan ke AI:
--> bagaimana cara membuat fungsi fetch dengan AJAX untuk menampilkan data dan menangani kondisi loading, empty, serta error?
Answer (from AI): Anda dapat membuat fungsi asinkronus menggunakan async/await, melakukan pemanggilan ke endpoint JSON, lalu mengatur visibilitas elemen penanda seperti loading state, error state, atau mengosongkan kontainer grid jika data kosong sebelum merender kartu elemen satu per satu.

--> bagaimana cara mencegah serangan XSS saat merender data JSON ke dalam DOM menggunakan innerHTML di JavaScript?
Answer (from AI): Anda harus melakukan escaping pada setiap string nilai teks sebelum memasukkannya ke dalam HTML dengan membuat fungsi helper string replacement untuk karakter khusus seperti &, <, >, ", dan ' agar tidak dieksekusi sebagai tag HTML oleh browser.

1. Debouncing adalah teknik untuk menunda eksekusi suatu fungsi sampai pengguna berhenti mengetik selama jangka waktu tertentu. Teknik ini penting diterapkan pada pencarian AJAX agar permintaan (*request*) tidak dikirim setiap kali pengguna menekan satu huruf, sehingga mengurangi beban server dan menghemat penggunaan jaringan.
2. Fungsi `await` adalah untuk menghentikan sementara eksekusi kode sampai proses pengambilan data (*fetch*) selesai dan mengembalikan hasilnya. Jika kita tidak menggunakan `await`, JavaScript akan langsung menjalankan baris kode berikutnya sebelum data dari server diterima, yang menyebabkan program gagal membaca data tersebut.
3. Serangan XSS (Cross-Site Scripting) adalah celah keamanan di mana penyerang memasukkan skrip berbahaya ke dalam halaman web. Data yang dimuat melalui AJAX/JavaScript lebih rentan karena manipulasi elemen dilakukan langsung di sisi peramban (*browser*), sehingga jika tidak dibersihkan atau di-*escape* secara manual, skrip berbahaya tersebut dapat dieksekusi oleh peramban.

### Tutorial 7

Pada Tutorial 7, saya mulai menggunakan Django REST Framework (DRF) untuk membuat REST API pada model `Organization`. Sebelumnya data organisasi sudah bisa ditampilkan dalam format JSON menggunakan view Django biasa, tetapi pada tutorial ini saya mempelajari penggunaan `ModelSerializer`, `@api_view`, dan `Response` dari DRF. Saya juga mengatur endpoint untuk melihat daftar organisasi, melihat detail, menambahkan, memperbarui, menghapus, dan memberikan Star. Dengan begitu, frontend dapat berkomunikasi dengan backend melalui URL dan HTTP method yang lebih jelas.

Hal yang cukup penting bagi saya dari tutorial ini adalah perbedaan antara authentication dan permission. Pengguna yang belum login tetap boleh melihat data, pengguna biasa hanya boleh membaca dan memberikan Star, Editor dapat memperbarui data yang sudah ada, sedangkan superuser dapat mengelola seluruh data. Saya menerapkan aturan tersebut menggunakan permission class, sehingga pembatasan hak akses tidak hanya bergantung pada tombol yang muncul di halaman. Selain itu, saya menghubungkan halaman Organization dengan API DRF menggunakan Fetch API dan tetap mengirimkan CSRF token untuk request yang mengubah data.

Pengujian saya lakukan dengan Django test suite, termasuk untuk status HTTP, validasi serializer, perbedaan hak akses setiap role, dan request berbasis session. Saya juga memahami bahwa `force_authenticate()` saja belum membuktikan perlindungan CSRF, sehingga pengujian session perlu menggunakan `APIClient(enforce_csrf_checks=True)` dan proses login yang sebenarnya.

**AI Disclosure:**

Alat yang digunakan: ChatGPT dan OpenAI Codex Desktop.

Saya menggunakan bantuan AI untuk memahami struktur REST API dengan DRF, pembagian tanggung jawab antara serializer, permission class, dan API view, serta menyusun langkah implementasi yang tidak mengganggu kode Django sebelumnya. Codex juga membantu melakukan inspeksi repository, implementasi kode, dan pembuatan pengujian. Saya tetap memeriksa hasilnya berdasarkan kebutuhan tutorial dan menjalankan proses Git secara manual.

Saya menyadari bahwa API yang berhasil mengembalikan JSON belum tentu mempunyai pengaturan hak akses yang benar. Karena itu, saran AI tidak saya anggap langsung selesai hanya karena aplikasi bisa berjalan. Saya memeriksa hasil pengujian untuk beberapa role, status HTTP, dan CSRF, lalu mempertahankan struktur Organization serta fitur lama yang memang masih dibutuhkan.

### Tugas 6

Pada Individual Assignment 6, saya melanjutkan materi Tutorial 7 dengan menerapkan Django REST Framework pada bagian `Education`, bukan lagi `Organization`. Model Education sebenarnya sudah memiliki CRUD, pencarian, dan Star dari tugas sebelumnya. Pada tugas ini saya membuat `EducationSerializer`, endpoint REST API, permission untuk setiap role, serta mengubah halaman Education agar mengambil dan memperbarui data melalui Fetch API. Jadi, proses tambah, update, hapus, pencarian, dan Star dapat berjalan tanpa perlu me-*reload* halaman.

Untuk implementasinya, saya memisahkan validasi data di `main/serializers.py`, pengaturan hak akses di `main/permissions.py`, dan operasi API di `main/api_views.py`. Field `star_count` dan `is_starred` bersifat *read-only*, sedangkan identitas pengguna yang memberi Star selalu berasal dari `request.user`. Saya juga menambahkan modal Edit untuk Editor dan superuser, error toast, penanganan loading/empty state, serta pemeriksaan tampilan mobile. Perubahan ini dibuat dengan tetap mempertahankan halaman dan URL Education sebelumnya.

1. **Apa perbedaan RESTful API dengan hanya mengembalikan JSON? Apa perbedaan PUT dan PATCH?**

JSON adalah format data yang digunakan untuk mengirim informasi antara server dan client. Sementara itu, RESTful API tidak hanya membahas format respons, tetapi juga bagaimana resource diatur melalui URL, penggunaan HTTP method, serta status respons yang sesuai. Contohnya pada proyek saya, `/api/v1/educations/` digunakan untuk kumpulan data Education, sedangkan `/api/v1/educations/<uuid>/` digunakan untuk satu data tertentu. GET digunakan untuk membaca, POST untuk menambahkan, PUT/PATCH untuk memperbarui, dan DELETE untuk menghapus data.

PUT biasanya digunakan ketika client ingin mengirim data yang lengkap untuk suatu resource, sedangkan PATCH digunakan untuk memperbarui sebagian field saja. Pada Education, PUT mengharuskan field wajib seperti `school_name`, `degree`, dan `start_year` tetap dikirim. Untuk field opsional yang tidak dikirim, serializer yang digunakan pada proyek ini masih mempertahankan nilai sebelumnya. Sementara itu, pada modal Edit saya menggunakan PATCH karena hanya field yang berubah yang perlu dikirim. Misalnya ketika saya hanya ingin mengubah `degree`, field lain seperti tahun dan logo tidak ikut diubah.

2. **Apa kegunaan serializer DRF dibandingkan membuat dictionary JSON secara manual?**

`ModelSerializer` membantu mengubah object dari database menjadi representasi yang siap dikirim melalui API, sekaligus memeriksa data yang diterima dari client sebelum disimpan. Pada `EducationSerializer`, saya menuliskan daftar field secara eksplisit, menambahkan validasi input seperti `strip_tags`, dan membuat field perhitungan `star_count` serta `is_starred`. Field hasil perhitungan tersebut tidak bisa diubah dengan mengirimkan nilai palsu dari frontend.

Sebelumnya, saya menggunakan `JsonResponse` dengan dictionary yang saya susun sendiri di view. Cara tersebut tetap bisa digunakan, tetapi ketika operasi create, update, dan validasi semakin banyak, kode di view menjadi lebih sulit dipelihara. Dengan serializer, logika representasi dan validasi lebih terpusat, sedangkan permission tetap diperiksa di bagian yang berbeda. Menurut saya ini juga membuat pengujian setiap bagian lebih jelas.

3. **Apa perbedaan authentication dan authorization, serta mengapa permission di backend tetap diperlukan?**

Authentication digunakan untuk memastikan siapa pengguna yang sedang mengakses aplikasi, misalnya melalui session setelah login. Authorization menentukan tindakan apa yang diperbolehkan untuk pengguna tersebut. Pada proyek saya, pengunjung yang belum login hanya bisa membaca data. Pengguna biasa dapat membaca dan memberikan Star miliknya sendiri, Editor dapat memperbarui Education, sedangkan superuser dapat menambahkan, memperbarui, dan menghapus data.

Menyembunyikan tombol Add atau Delete dari pengguna tertentu tidak cukup untuk menjaga keamanan karena seseorang masih bisa mengirim request langsung ke URL API. Oleh sebab itu, saya menggunakan permission class di backend. Misalnya jika Editor mencoba mengirim POST untuk membuat Education baru atau DELETE untuk menghapusnya, server tetap memberikan respons 403. Status `is_staff` saja juga tidak otomatis menjadikan seseorang Editor. View Education lama ikut diperiksa agar tidak membuka akses yang lebih luas dibandingkan API baru.

4. **Mengapa SessionAuthentication memerlukan CSRF, dan mengapa force_authenticate() belum cukup untuk mengujinya?**

Ketika pengguna login, browser menyimpan cookie session yang kemudian dapat ikut terkirim bersama request. Jika aplikasi tidak memeriksa CSRF pada request yang mengubah data, ada risiko website lain mencoba memanfaatkan session pengguna yang sedang aktif. Karena itu, pada operasi seperti POST, PUT, PATCH, dan DELETE, frontend Education mengirimkan header `X-CSRFToken` yang dibaca dari cookie `csrftoken`. Halaman Education juga menggunakan `ensure_csrf_cookie` agar token tersedia untuk pengguna yang tidak mempunyai form Add atau Edit.

`force_authenticate()` pada DRF berguna untuk menguji permission karena kita bisa menentukan pengguna secara langsung. Namun, cara tersebut melewati proses login berbasis session sehingga tidak membuktikan bahwa pemeriksaan CSRF bekerja. Untuk bagian ini saya menggunakan `APIClient(enforce_csrf_checks=True)` dengan `.login()` dan menguji tiga kondisi, yaitu request tanpa token, dengan token salah, dan dengan token yang valid. Hasilnya, perubahan data ditolak jika token tidak benar dan bisa berjalan jika pengguna mempunyai hak akses serta token yang sesuai.

**Implementasi API dan cara menjalankan proyek:**

Endpoint yang digunakan pada Tugas 6 adalah `GET/POST /api/v1/educations/`, `GET/PUT/PATCH/DELETE /api/v1/educations/<uuid>/`, dan `POST /api/v1/educations/<uuid>/star/`. Pencarian menggunakan query `?title=` yang dicocokkan terhadap `school_name` tanpa memperhatikan huruf besar atau kecil. Data yang dikirim melalui API berisi `id`, `school_name`, `degree`, `start_year`, `end_year`, `logo`, `star_count`, dan `is_starred`. Tiga field yang wajib diisi adalah `school_name`, `degree`, dan `start_year`, sedangkan `end_year` dan `logo` bersifat opsional. API memakai status seperti 200, 201, 204, 400, 403, 404, dan 405 sesuai hasil request.

Untuk menjalankan proyek secara lokal, saya menggunakan Python, virtual environment, dan dependensi pada `requirements.txt`. Setelah branch tugas tersedia di GitHub, repository dapat diambil menggunakan perintah berikut pada PowerShell:

```powershell
git clone --branch feat/assignment-6 --single-branch https://github.com/seanve1/myportofolio.git
cd myportofolio
py -3.13 -m venv env
.\env\Scripts\Activate.ps1
python -m pip install -r requirements.txt
$env:SECRET_KEY = python -c "import secrets; print(secrets.token_urlsafe(50))"
$env:DEBUG = "True"
$env:PRODUCTION = "False"
python manage.py migrate
python manage.py runserver
```

Halaman Education dapat dibuka melalui `http://127.0.0.1:8000/education/` dan daftar API melalui `http://127.0.0.1:8000/api/v1/educations/`. Untuk membuat superuser, jalankan `python manage.py createsuperuser`. Role Editor menggunakan Django Group dengan nama persis `Editor`. Konfigurasi di atas ditujukan untuk lingkungan lokal dan perlu disesuaikan kembali jika aplikasi akan di-*deploy*. Langkah instalasi diperiksa terhadap konfigurasi proyek, tetapi belum diuji ulang dari *fresh clone*.

**Pengujian:**

Saya menjalankan `python manage.py check` dan `python manage.py test main`. Pada pengujian terakhir tanggal 9 November 2026, terdapat **73 tests yang lulus**. Pengujian mencakup serializer, validasi, CRUD, HTTP status, akses setiap role, Star berdasarkan pengguna yang login, perlindungan CSRF, integrasi template, serta efisiensi query saat mengambil daftar Education. Saya juga memeriksa agar API Organization pada Tutorial 7 tidak ikut rusak.

Selain automated tests, saya menggunakan bantuan QA browser melalui Chrome pada lebar 360px, 390px, 768px, dan 1280px. Beberapa masalah yang ditemukan adalah card dan header yang overflow, toast yang keluar dari layar, ukuran tombol yang kurang nyaman, serta fokus keyboard pada modal. Setelah diperbaiki, alur CRUD, pencarian, Star, dan tampilan responsif kembali diperiksa. Pengujian browser yang mengubah data memakai salinan database sementara, bukan database pengembangan asli. Pengujian ini belum mencakup perangkat fisik, browser selain Chrome, atau audit screen reader secara menyeluruh.

**AI Disclosure:**

Alat yang digunakan: ChatGPT dan OpenAI Codex Desktop.

Dalam pengerjaan Tugas 6, saya menggunakan bantuan AI untuk mendiskusikan beberapa konsep Django REST Framework, khususnya penggunaan ModelSerializer, pengaturan permission, serta integrasi API dengan JavaScript. Saya juga memanfaatkan AI untuk membantu implementasi beberapa bagian kode, mencari kemungkinan kesalahan, dan menyusun pengujian agar fitur yang dikembangkan dapat berjalan sesuai ketentuan tugas.

Pengembangan dilakukan secara bertahap dengan mengacu pada struktur proyek yang sudah saya kerjakan sebelumnya. Saya menentukan bagian Education sebagai objek pengembangan, menetapkan kebutuhan fitur, serta menyesuaikan implementasi dengan sistem autentikasi, pembagian role, dan desain website yang sudah ada. Setiap hasil bantuan AI saya periksa kembali, terutama agar perubahan yang dilakukan tidak mengganggu fitur sebelumnya. Pengelolaan Git, termasuk staging dan commit, tetap saya lakukan secara manual.

Berikut merupakan beberapa prompt yang saya gunakan selama pengerjaan:

1. Bagaimana cara menggunakan ModelSerializer untuk model Education dengan validasi field dan informasi Star?
2. Bagaimana mengatur permission pada Django REST Framework agar setiap role memiliki hak akses yang berbeda?
3. Bagaimana menghubungkan REST API dengan Fetch API agar fitur CRUD dan Star dapat berjalan tanpa reload halaman?
4. Bagaimana menangani CSRF token, kesalahan respons API, dan validasi input pada AJAX?
5. Bagaimana memeriksa responsivitas halaman, aksesibilitas modal, dan memastikan fitur lama tetap berjalan setelah integrasi DRF?

Salah satu kendala yang saya temukan adalah beberapa implementasi yang terlihat benar dari sisi kode ternyata masih memiliki masalah ketika diuji melalui browser, terutama pada tampilan mobile dan navigasi keyboard. Saya kemudian menggunakan hasil pengujian tersebut untuk mengevaluasi dan memperbaiki implementasi dengan bantuan AI. Dari proses ini, saya memahami bahwa penggunaan AI tetap membutuhkan pemeriksaan ulang, baik dari sisi fungsionalitas, keamanan, maupun kesesuaian dengan kebutuhan proyek.