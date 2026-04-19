"""
╔══════════════════════════════════════════════════════════════╗
║  OmegaClass v3 — Holistik Öğrenci Gelişim Platformu         ║
║  Streamlit Community Cloud uyumlu · SQLite · PedagogyEngine  ║
╚══════════════════════════════════════════════════════════════╝
"""

# ── stdlib ──────────────────────────────────────────────────
import os
import hashlib
import sqlite3
from datetime import date
from pathlib import Path

# ── third-party ─────────────────────────────────────────────
import streamlit as st
import pandas as pd

# ════════════════════════════════════════════════════════════
#  BULUT-UYUMLU VERİTABANI YOLU
#  Streamlit Cloud'da __file__ /mount/src/<repo>/app.py
#  olduğu için parent dir her zaman yazılabilirdir.
# ════════════════════════════════════════════════════════════
_HERE   = Path(__file__).resolve().parent
DB_PATH = str(_HERE / "omegaclass.db")


# ════════════════════════════════════════════════════════════
#  VERİTABANI KATMANI
# ════════════════════════════════════════════════════════════

def _conn() -> sqlite3.Connection:
    c = sqlite3.connect(DB_PATH, check_same_thread=False)
    c.row_factory = sqlite3.Row
    c.execute("PRAGMA journal_mode=WAL")
    c.execute("PRAGMA foreign_keys=ON")
    return c


def _hp(pw: str) -> str:
    """SHA-256 parola özeti."""
    return hashlib.sha256(pw.encode()).hexdigest()


def init_db() -> None:
    """Tüm tabloları oluştur; ilk kez çalışıyorsa tohumla."""
    db = _conn()
    cur = db.cursor()

    cur.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        id        INTEGER PRIMARY KEY AUTOINCREMENT,
        username  TEXT    UNIQUE NOT NULL,
        password  TEXT    NOT NULL,
        role      TEXT    NOT NULL CHECK(role IN ('admin','teacher')),
        full_name TEXT    NOT NULL DEFAULT ''
    );
    CREATE TABLE IF NOT EXISTS students (
        id         INTEGER PRIMARY KEY AUTOINCREMENT,
        teacher_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        name       TEXT    NOT NULL,
        grade      TEXT    NOT NULL,
        created_at TEXT    NOT NULL DEFAULT (date('now'))
    );
    CREATE TABLE IF NOT EXISTS subjects (
        id   INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL
    );
    CREATE TABLE IF NOT EXISTS outcomes (
        id         INTEGER PRIMARY KEY AUTOINCREMENT,
        subject_id INTEGER NOT NULL REFERENCES subjects(id) ON DELETE CASCADE,
        grade      TEXT    NOT NULL,
        code       TEXT    NOT NULL,
        text       TEXT    NOT NULL
    );
    CREATE TABLE IF NOT EXISTS academic_symptoms (
        id         INTEGER PRIMARY KEY AUTOINCREMENT,
        subject_id INTEGER REFERENCES subjects(id) ON DELETE CASCADE,
        text       TEXT NOT NULL,
        theory_tag TEXT NOT NULL DEFAULT ''
    );
    CREATE TABLE IF NOT EXISTS social_symptoms (
        id         INTEGER PRIMARY KEY AUTOINCREMENT,
        dimension  TEXT NOT NULL,
        text       TEXT NOT NULL,
        theory_tag TEXT NOT NULL DEFAULT ''
    );
    CREATE TABLE IF NOT EXISTS academic_logs (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        teacher_id  INTEGER NOT NULL REFERENCES users(id)    ON DELETE CASCADE,
        student_id  INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
        subject_id  INTEGER NOT NULL REFERENCES subjects(id),
        outcome_id  INTEGER NOT NULL REFERENCES outcomes(id),
        symptom_ids TEXT    NOT NULL DEFAULT '',
        notes       TEXT    NOT NULL DEFAULT '',
        log_date    TEXT    NOT NULL DEFAULT (date('now'))
    );
    CREATE TABLE IF NOT EXISTS social_logs (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        teacher_id  INTEGER NOT NULL REFERENCES users(id)    ON DELETE CASCADE,
        student_id  INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
        symptom_id  INTEGER NOT NULL REFERENCES social_symptoms(id),
        intensity   INTEGER NOT NULL DEFAULT 3,
        notes       TEXT    NOT NULL DEFAULT '',
        log_date    TEXT    NOT NULL DEFAULT (date('now'))
    );
    """)
    db.commit()
    _seed(db, cur)
    db.close()


# ── Başlangıç verisi ────────────────────────────────────────

def _seed(db: sqlite3.Connection, cur: sqlite3.Cursor) -> None:
    # Yalnızca tablo tamamen boşsa ekle
    if cur.execute("SELECT COUNT(*) FROM users").fetchone()[0] > 0:
        return

    # ── Kullanıcılar ────────────────────────────────────────
    cur.executemany(
        "INSERT INTO users(username,password,role,full_name) VALUES(?,?,?,?)",
        [
            ("admin",      _hp("admin123"),    "admin",   "Sistem Yöneticisi"),
            ("ogretmen1",  _hp("ogretmen123"), "teacher", "Ayşe Yıldız"),
            ("ogretmen2",  _hp("ogretmen456"), "teacher", "Mehmet Demir"),
        ]
    )

    # ── Dersler ─────────────────────────────────────────────
    subjects = [
        "Matematik", "Türkçe", "Fen Bilimleri", "Sosyal Bilgiler",
        "Hayat Bilgisi", "İngilizce", "Görsel Sanatlar", "Müzik", "Beden Eğitimi",
    ]
    cur.executemany("INSERT INTO subjects(name) VALUES(?)", [(s,) for s in subjects])

    # ── Yardımcı: subject_id lookup ─────────────────────────
    def sid(name: str) -> int:
        return cur.execute("SELECT id FROM subjects WHERE name=?", (name,)).fetchone()[0]

    # ── Kazanımlar ──────────────────────────────────────────
    outcomes_raw = [
        # Matematik
        (sid("Matematik"), "1", "M.1.1.1", "Nesneleri belirli bir özelliğe göre sınıflandırır."),
        (sid("Matematik"), "1", "M.1.1.2", "1-20 arası doğal sayıları okur, yazar ve sıralar."),
        (sid("Matematik"), "1", "M.1.1.3", "20 içinde toplama ve çıkarma işlemi yapar."),
        (sid("Matematik"), "1", "M.1.2.1", "Düzlemsel şekilleri tanır ve adlarını söyler."),
        (sid("Matematik"), "1", "M.1.3.1", "Standart olmayan ölçme araçlarıyla uzunluk ölçer."),
        (sid("Matematik"), "1", "M.1.3.2", "Tam ve yarım saati okur."),
        (sid("Matematik"), "2", "M.2.1.1", "100'e kadar doğal sayıları okur, yazar ve sıralar."),
        (sid("Matematik"), "2", "M.2.1.2", "Eldeli toplama işlemi yapar."),
        (sid("Matematik"), "2", "M.2.1.3", "Borçlu çıkarma işlemi yapar."),
        (sid("Matematik"), "2", "M.2.1.4", "2, 3, 4, 5 çarpım tablolarını oluşturur ve kullanır."),
        (sid("Matematik"), "2", "M.2.1.5", "Yarım, çeyrek ve dörtte üç kavramlarını anlar."),
        (sid("Matematik"), "2", "M.2.2.1", "Çokgenleri tanır; köşe ve kenar sayılarını belirler."),
        (sid("Matematik"), "2", "M.2.3.1", "Santimetre ve metre ile uzunluk ölçer."),
        (sid("Matematik"), "2", "M.2.4.1", "Tablo ve çubuk grafik oluşturur, yorumlar."),
        (sid("Matematik"), "3", "M.3.1.1", "1000'e kadar doğal sayıları okur, yazar, sıralar."),
        (sid("Matematik"), "3", "M.3.1.2", "Üç basamaklı sayılarla toplama ve çıkarma yapar."),
        (sid("Matematik"), "3", "M.3.1.3", "6, 7, 8, 9 çarpım tablolarını oluşturur ve kullanır."),
        (sid("Matematik"), "3", "M.3.1.4", "İki basamaklı sayıyı bir basamaklıya böler."),
        (sid("Matematik"), "3", "M.3.1.5", "Kesir kavramını açıklar; birim kesirleri karşılaştırır."),
        (sid("Matematik"), "3", "M.3.2.1", "Dikdörtgen ve karenin çevresi ile alanını hesaplar."),
        (sid("Matematik"), "3", "M.3.2.2", "Dar, geniş ve dik açıları ayırt eder."),
        (sid("Matematik"), "3", "M.3.3.1", "Kilogram ve gramla tartma yapar."),
        (sid("Matematik"), "3", "M.3.4.1", "Sütun grafiği oluşturur ve yorumlar."),
        (sid("Matematik"), "4", "M.4.1.1", "10.000'e kadar doğal sayıları okur, yazar, sıralar."),
        (sid("Matematik"), "4", "M.4.1.2", "Doğal sayıları yuvarlama kurallarına göre yuvarlar."),
        (sid("Matematik"), "4", "M.4.1.3", "Dört işlemi yapar; problemlerde kullanır."),
        (sid("Matematik"), "4", "M.4.1.4", "Kesirlerle toplama ve çıkarma işlemi yapar."),
        (sid("Matematik"), "4", "M.4.1.5", "Ondalık kesirleri okur, yazar ve karşılaştırır."),
        (sid("Matematik"), "4", "M.4.2.1", "Çevre ve alan kavramlarını problem çözmede kullanır."),
        (sid("Matematik"), "4", "M.4.2.2", "Koordinat sisteminde noktaların yerini belirler."),
        (sid("Matematik"), "4", "M.4.2.3", "Yansıma, öteleme ve dönme dönüşümlerini modeller."),
        (sid("Matematik"), "4", "M.4.3.1", "Zaman ölçü birimlerini dönüştürür."),
        (sid("Matematik"), "4", "M.4.4.1", "Çizgi grafiği oluşturur ve yorumlar."),
        (sid("Matematik"), "4", "M.4.4.2", "Ortalama kavramını açıklar ve hesaplar."),
        # Türkçe
        (sid("Türkçe"), "1", "T.1.1.1", "Dinlediklerinin konusunu belirler."),
        (sid("Türkçe"), "1", "T.1.1.2", "Dinlediklerinde olayların sırasını belirler."),
        (sid("Türkçe"), "1", "T.1.2.1", "Konuşurken ses tonu ve beden dilini uygun kullanır."),
        (sid("Türkçe"), "1", "T.1.3.1", "Metni doğru, akıcı ve anlayarak okur."),
        (sid("Türkçe"), "1", "T.1.3.2", "Okuduğunda ana fikri belirler."),
        (sid("Türkçe"), "1", "T.1.4.1", "Büyük harf ve nokta kullanım kurallarını uygular."),
        (sid("Türkçe"), "2", "T.2.1.1", "Dinlediklerinde ana duygu ve düşünceyi belirler."),
        (sid("Türkçe"), "2", "T.2.2.1", "Olayları sıralı biçimde anlatır."),
        (sid("Türkçe"), "2", "T.2.3.1", "Noktalama işaretlerine dikkat ederek akıcı okur."),
        (sid("Türkçe"), "2", "T.2.3.2", "Ana fikri ve yardımcı fikirleri belirler."),
        (sid("Türkçe"), "2", "T.2.3.3", "Neden-sonuç, amaç-sonuç ilişkileri kurar."),
        (sid("Türkçe"), "2", "T.2.4.1", "Görsellerden yola çıkarak kısa metinler yazar."),
        (sid("Türkçe"), "3", "T.3.1.1", "Dinlediklerinde duygu-düşünce değişimini fark eder."),
        (sid("Türkçe"), "3", "T.3.2.1", "Tartışmalarda görüşlerini gerekçeyle savunur."),
        (sid("Türkçe"), "3", "T.3.3.1", "Metinde örtük anlamları fark eder ve yorumlar."),
        (sid("Türkçe"), "3", "T.3.3.2", "Metni kendi cümleleriyle özetler."),
        (sid("Türkçe"), "3", "T.3.4.1", "Giriş-gelişme-sonuç bölümlerinden oluşan hikâye yazar."),
        (sid("Türkçe"), "4", "T.4.1.1", "Gerçek ile kurgu arasındaki farkı belirler."),
        (sid("Türkçe"), "4", "T.4.1.2", "Yansız ve taraflı bilgiyi ayırt eder."),
        (sid("Türkçe"), "4", "T.4.3.1", "Yazarın bakış açısını belirler."),
        (sid("Türkçe"), "4", "T.4.3.2", "Sözcüklerin gerçek, mecaz ve yan anlamlarını ayırt eder."),
        (sid("Türkçe"), "4", "T.4.4.1", "Paragraf oluşturarak giriş-gelişme-sonuç bütünlüğüyle yazar."),
        (sid("Türkçe"), "4", "T.4.4.2", "Bilgilendirici metin (haber, rapor) yazar."),
        # Fen Bilimleri
        (sid("Fen Bilimleri"), "3", "FEN.3.1.1", "Bitkilerin yapısını tanır; görevlerini açıklar."),
        (sid("Fen Bilimleri"), "3", "FEN.3.1.2", "Hayvanları omurgalı-omurgasız olarak sınıflandırır."),
        (sid("Fen Bilimleri"), "3", "FEN.3.1.3", "Besin zinciri oluşturur."),
        (sid("Fen Bilimleri"), "3", "FEN.3.2.1", "Maddelerin katı, sıvı ve gaz hallerini açıklar."),
        (sid("Fen Bilimleri"), "3", "FEN.3.2.2", "Karışımları ayırma yöntemlerini deneyle gösterir."),
        (sid("Fen Bilimleri"), "3", "FEN.3.3.1", "Kuvveti ve kuvvetin etkilerini açıklar."),
        (sid("Fen Bilimleri"), "4", "FEN.4.1.1", "İnsan vücudunun sistemlerini açıklar."),
        (sid("Fen Bilimleri"), "4", "FEN.4.1.2", "Sağlıklı yaşam için beslenme ve egzersizin önemini savunur."),
        (sid("Fen Bilimleri"), "4", "FEN.4.2.1", "Maddelerin fiziksel ve kimyasal özelliklerini karşılaştırır."),
        (sid("Fen Bilimleri"), "4", "FEN.4.2.2", "Çözünme olayını etkileyen faktörleri deneyle inceler."),
        (sid("Fen Bilimleri"), "4", "FEN.4.3.1", "Elektrik devresi kurar; çalışma prensibini açıklar."),
        (sid("Fen Bilimleri"), "4", "FEN.4.3.2", "Mıknatısların özelliklerini araştırır."),
        (sid("Fen Bilimleri"), "4", "FEN.4.4.1", "Güneş, Dünya ve Ay'ın hareketlerini açıklar."),
        (sid("Fen Bilimleri"), "4", "FEN.4.4.2", "Hava olaylarını oluşum sebepleriyle açıklar."),
        # Sosyal Bilgiler
        (sid("Sosyal Bilgiler"), "3", "SB.3.1.1", "Yakın çevresindeki meslekleri ve işlevlerini açıklar."),
        (sid("Sosyal Bilgiler"), "3", "SB.3.2.1", "Türk kültürüne ait gelenek ve görenekleri açıklar."),
        (sid("Sosyal Bilgiler"), "3", "SB.3.3.1", "Türkiye'nin coğrafi bölgelerini harita üzerinde gösterir."),
        (sid("Sosyal Bilgiler"), "4", "SB.4.1.1", "Milli bayram ve önemli günlerin anlam ve önemini açıklar."),
        (sid("Sosyal Bilgiler"), "4", "SB.4.1.2", "Türk Devleti'nin temel kurumlarını açıklar."),
        (sid("Sosyal Bilgiler"), "4", "SB.4.2.1", "Türk-İslam medeniyetinin bilim-sanat katkılarını açıklar."),
        (sid("Sosyal Bilgiler"), "4", "SB.4.3.1", "Türkiye'nin ekonomik faaliyetlerini bölgelerle ilişkilendirir."),
        (sid("Sosyal Bilgiler"), "4", "SB.4.4.1", "Üretim, dağıtım ve tüketim kavramlarını açıklar."),
        # Hayat Bilgisi
        (sid("Hayat Bilgisi"), "1", "HB.1.1.1", "Okulunun bölümlerini ve görevlilerini tanır."),
        (sid("Hayat Bilgisi"), "1", "HB.1.1.2", "Okul kurallarını uygular."),
        (sid("Hayat Bilgisi"), "1", "HB.1.2.1", "Aile büyüklerine karşı saygılı davranır."),
        (sid("Hayat Bilgisi"), "1", "HB.1.3.1", "Canlı ve cansız varlıkları ayırt eder."),
        (sid("Hayat Bilgisi"), "2", "HB.2.1.1", "Farklı görüşlere saygı duyar; empati kurar."),
        (sid("Hayat Bilgisi"), "2", "HB.2.2.1", "Sağlıklı beslenme ve egzersizin önemini açıklar."),
        (sid("Hayat Bilgisi"), "2", "HB.2.3.1", "Tasarrufun ve kaynakların sınırlılığını açıklar."),
        (sid("Hayat Bilgisi"), "3", "HB.3.1.1", "Teknoloji kullanımında bilinçli davranır."),
        (sid("Hayat Bilgisi"), "3", "HB.3.2.1", "Çevresinin doğal ve kültürel değerlerini tanır."),
        # İngilizce
        (sid("İngilizce"), "1", "İNG.1.1.1", "Greetings and farewells kullanır."),
        (sid("İngilizce"), "1", "İNG.1.1.2", "Numbers 1-10 söyler ve tanır."),
        (sid("İngilizce"), "1", "İNG.1.1.3", "Colors and shapes ile ilgili kelimeleri kullanır."),
        (sid("İngilizce"), "2", "İNG.2.1.1", "Family members ile ilgili kelimeleri kullanır."),
        (sid("İngilizce"), "2", "İNG.2.1.2", "Simple present tense ile kendini tanıtır."),
        (sid("İngilizce"), "2", "İNG.2.1.3", "Animals konusunda diyaloglar kurar."),
        (sid("İngilizce"), "3", "İNG.3.1.1", "Daily routines konusunda kısa konuşmalar yapar."),
        (sid("İngilizce"), "3", "İNG.3.1.2", "Simple present tense ile aktivitelerini anlatır."),
        (sid("İngilizce"), "3", "İNG.3.1.3", "Directions and places konusunda yönergeler verir."),
        (sid("İngilizce"), "4", "İNG.4.1.1", "Past simple tense ile geçmiş olayları anlatır."),
        (sid("İngilizce"), "4", "İNG.4.1.2", "Shopping diyaloglarında fiyat sorar ve yanıtlar."),
        (sid("İngilizce"), "4", "İNG.4.1.3", "Health and body parts konusunda soru-cevap yapar."),
        (sid("İngilizce"), "4", "İNG.4.1.4", "5-6 cümlelik kısa bir paragraf yazar."),
    ]
    cur.executemany(
        "INSERT INTO outcomes(subject_id,grade,code,text) VALUES(?,?,?,?)",
        outcomes_raw
    )

    # ── Akademik semptomlar ─────────────────────────────────
    def as_rows(name, rows):
        s = sid(name)
        return [(s, t, tag) for t, tag in rows]

    math_syms = as_rows("Matematik", [
        ("Yönergeleri kısa süreli bellekte tutamıyor",         "Sweller-BilişselYük"),
        ("Yeni kavramı mevcut şemasına entegre edemiyor",      "Piaget-ŞemaUyumsuzluğu"),
        ("Soyut temsili somut modelle ilişkilendiremiyor",     "Piaget-Soyutlama"),
        ("Çok adımlı süreçlerde aşama takibini yitiriyor",    "Sweller-BilişselYük"),
        ("Sayısal örüntüyü fark edemiyor",                     "Piaget-Tümevarım"),
        ("Problem çözme stratejilerini transfer edemiyor",     "Piaget-Transfer"),
        ("İşlem basamaklarını hatalı sıralıyor",               "Sweller-ProsedurelBellek"),
        ("Matematiksel sembolleri anlamsal bağlamda kullanamıyor", "Piaget-SembolikTemsil"),
        ("Sonucu tahmin etmeden işleme başlıyor",              "Metakognitif-Eksiklik"),
        ("Prosedürel bilgiden kavramsal anlayışa geçemiyor",   "Piaget-Soyutlama"),
    ])
    turkish_syms = as_rows("Türkçe", [
        ("Metindeki örtük anlamı çıkarsamakta güçlük",        "Üstbiliş-Okuma"),
        ("Dinleme sırasında dikkat ve odak kaybı",             "Sweller-DikkatYükü"),
        ("Düşüncelerini sıralı organize edemiyor",             "Piaget-ŞemaOrganizasyonu"),
        ("Yeni sözcüğü dil şemasına bağlayamıyor",            "Piaget-SözcükselŞema"),
        ("Yazıda yapısal bütünlüğü koruyamıyor",              "Üstbiliş-Yazma"),
        ("Sesletim güçlüğü — akıcı okuma bozuluyor",          "Fonolojik-Farkındalık"),
        ("Neden-sonuç ilişkisini metinden çıkaramıyor",        "Piaget-MantıksalDüşünce"),
        ("Kendi yorumunu orijinal içerikle karıştırıyor",     "Üstbiliş-Metacognition"),
    ])
    fen_syms = as_rows("Fen Bilimleri", [
        ("Bilimsel kavramı yaşam deneyimiyle ilişkilendiremiyor", "Piaget-BağlamTransfer"),
        ("Gözlem ile çıkarım arasındaki farkı ayırt edemiyor",    "Bilimsel-Düşünce"),
        ("Hipotez oluşturmakta güçlük çekiyor",                   "Piaget-Formal-İşlemsel"),
        ("Soyut bilimsel modeli somutlaştıramıyor",               "Piaget-SoyutlamaEksikliği"),
        ("Deney sürecinde adım takibini yitiriyor",               "Sweller-BilişselYük"),
        ("Sınıflandırmada tutarsız kriter kullanıyor",            "Piaget-Kategorizasyon"),
    ])
    ing_syms = as_rows("İngilizce", [
        ("Yabancı dil kaygısı — konuşmadan kaçınıyor",        "Bandura-ÖzYeterlilik"),
        ("Anadil şeması yabancı dil işlemeyi engelliyor",     "Piaget-L1TransferEngeli"),
        ("Fonetik ayrımları yapamıyor",                        "Fonolojik-YabancıDil"),
        ("Kelime yetersizliği iletişim stratejisini çöküyor", "Sweller-SözcükselYük"),
        ("Grameri ezber biliyor, bağlamda kullanamıyor",       "Piaget-UygulamaEksikliği"),
    ])
    general_syms = [
        (None, "Dikkat dağınıklığı — görevde kalma süresi kısa",   "Sweller-DikkatYükü"),
        (None, "Görev başlatmada dürtü kontrolü zorluğu",           "EF-DürtüKontrolü"),
        (None, "Hata aldığında öğrenmeyi tamamen durduruyor",       "Bandura-HataKaygısı"),
        (None, "Öğrenilen bilgiyi farklı bağlamlara transfer edemiyor", "Piaget-Transfer"),
        (None, "Metakognitif farkındalık yetersiz",                 "Üstbiliş-Farkındalık"),
    ]
    all_syms = math_syms + turkish_syms + fen_syms + ing_syms + general_syms
    cur.executemany(
        "INSERT INTO academic_symptoms(subject_id,text,theory_tag) VALUES(?,?,?)",
        all_syms
    )

    # ── Sosyal semptomlar ───────────────────────────────────
    social_raw = [
        # Öz-Yeterlilik
        ("Öz-Yeterlilik (Bandura)", "Hata korkusuyla yeni görevleri reddediyor",               "Bandura-DüşükÖzYeterlilik"),
        ("Öz-Yeterlilik (Bandura)", "Başarısını şansa bağlıyor, çabasına değil",               "Bandura-DışsalAtıf"),
        ("Öz-Yeterlilik (Bandura)", "Zorluğu ilk anda görünce pes ediyor",                     "Bandura-AzimEksikliği"),
        ("Öz-Yeterlilik (Bandura)", "Kendi yeterliliği hakkında kronik olumsuz değerlendirme", "Bandura-NegatifÖzAlgı"),
        ("Öz-Yeterlilik (Bandura)", "Başarı deneyimlerini genellemiyor",                       "Bandura-ÖzYeterlilikGenelleme"),
        # Duygusal Regülasyon
        ("Duygusal Regülasyon (Goleman)", "Frustrasyon anında ani öfke patlaması",              "Goleman-ÖfkeDüzenleme"),
        ("Duygusal Regülasyon (Goleman)", "Kaygı yoğunlaştığında zihinsel blok oluşuyor",      "Goleman-AnksiyeteBlok"),
        ("Duygusal Regülasyon (Goleman)", "Olumsuz geri bildirimi kişisel saldırı olarak algılıyor", "Goleman-GeriBildirimAlgısı"),
        ("Duygusal Regülasyon (Goleman)", "Duygusal tepkiyi davranışa döküyor, sözle değil",   "Goleman-DavranışsalIfade"),
        ("Duygusal Regülasyon (Goleman)", "Geçiş anlarında ani duygusal çöküş",                "Goleman-GeçişAnksiyetesi"),
        ("Duygusal Regülasyon (Goleman)", "Bekleme gerektiren durumlarda sabır eşiği çok düşük", "Goleman-DürtüKontrolü"),
        # Sosyal Katılım
        ("Sosyal Katılım ve Akran İlişkileri", "Akranlarıyla olumlu iletişim kurmakta güçlük", "Vygotsky-SosyalÖğrenme"),
        ("Sosyal Katılım ve Akran İlişkileri", "Grup etkinliklerinde dışlanıyor ya da dışlıyor", "Sosyal-DışlanmaRiski"),
        ("Sosyal Katılım ve Akran İlişkileri", "İşbirliği görevlerinde bireysel çalışma ısrarı", "Vygotsky-İşbirliğiEksikliği"),
        ("Sosyal Katılım ve Akran İlişkileri", "Çatışmada şiddet ya da kaçınma — müzakere yok", "Sosyal-ÇatışmaYönetimi"),
        # Erdem-Değer
        ("Erdem-Değer-Eylem Çerçevesi", "Sorumluluk: Görevleri kabul etmekte isteksiz",        "Değer-Sorumluluk"),
        ("Erdem-Değer-Eylem Çerçevesi", "Dürüstlük: Hata örtbas etme davranışı",               "Değer-Dürüstlük"),
        ("Erdem-Değer-Eylem Çerçevesi", "Empati: Başkasının duygusunu fark etmekte güçlük",    "Değer-Empati"),
        ("Erdem-Değer-Eylem Çerçevesi", "Öz-disiplin: Dürtü kontrolü ve kurallara uyum yetersiz", "Değer-Disiplin"),
        # Aile/Çevre
        ("Aile ve Ev Ortamı", "Ev desteği eksikliği ödev tamamlamayı etkiliyor",               "Çevre-EvDesteği"),
        ("Aile ve Ev Ortamı", "Uyku düzensizliği dikkat ve odak sorunlarına yol açıyor",       "Çevre-Biyolojik"),
        ("Aile ve Ev Ortamı", "Ekran süresi aşımı — uyku ve dikkat kalitesi bozuk",            "Çevre-Dijital"),
        ("Aile ve Ev Ortamı", "Aile içi stres akademik performansa yansıyor",                  "Çevre-AileStres"),
    ]
    cur.executemany(
        "INSERT INTO social_symptoms(dimension,text,theory_tag) VALUES(?,?,?)",
        social_raw
    )

    db.commit()


# ════════════════════════════════════════════════════════════
#  AUTH
# ════════════════════════════════════════════════════════════

def authenticate(username: str, password: str) -> dict | None:
    db  = _conn()
    row = db.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, _hp(password))
    ).fetchone()
    db.close()
    return dict(row) if row else None


# ════════════════════════════════════════════════════════════
#  PEDAGOGY ENGINE  — Kural Tabanlı Uzman Sistem
# ════════════════════════════════════════════════════════════

class PedagogyEngine:
    """
    Eğitim bilimleri temelli kural + ağırlık motoru.
    Dışarıya bağlantı yok; yalnızca SQLite loglarını okur.
    """

    # ── Teorik etiket ağırlıkları ──────────────────────────
    W = {
        "Sweller-BilişselYük":          3,
        "Sweller-DikkatYükü":           2,
        "Sweller-ProsedurelBellek":      2,
        "Sweller-SözcükselYük":         2,
        "Piaget-ŞemaUyumsuzluğu":       3,
        "Piaget-Soyutlama":             2,
        "Piaget-Transfer":              2,
        "Piaget-Tümevarım":             1,
        "Piaget-MantıksalDüşünce":       2,
        "Piaget-ŞemaOrganizasyonu":      2,
        "Piaget-BağlamTransfer":         2,
        "Piaget-Formal-İşlemsel":        1,
        "Piaget-SoyutlamaEksikliği":     2,
        "Piaget-Kategorizasyon":         1,
        "Piaget-SözcükselŞema":          2,
        "Piaget-UygulamaEksikliği":      1,
        "Piaget-SembolikTemsil":         2,
        "Piaget-L1TransferEngeli":       2,
        "Metakognitif-Eksiklik":        2,
        "Üstbiliş-Okuma":               2,
        "Üstbiliş-Yazma":               2,
        "Üstbiliş-Farkındalık":         2,
        "Üstbiliş-Metacognition":       2,
        "Bandura-DüşükÖzYeterlilik":    3,
        "Bandura-AzimEksikliği":        2,
        "Bandura-NegatifÖzAlgı":        3,
        "Bandura-ÖzYeterlilikGenelleme":2,
        "Bandura-DışsalAtıf":           2,
        "Bandura-HataKaygısı":          3,
        "Bandura-ÖzYeterlilik":         3,
        "Goleman-ÖfkeDüzenleme":        3,
        "Goleman-AnksiyeteBlok":         3,
        "Goleman-GeriBildirimAlgısı":   2,
        "Goleman-DavranışsalIfade":      2,
        "Goleman-GeçişAnksiyetesi":     2,
        "Goleman-DürtüKontrolü":        2,
        "Vygotsky-SosyalÖğrenme":       2,
        "Vygotsky-İşbirliğiEksikliği":  2,
        "Sosyal-DışlanmaRiski":         3,
        "Sosyal-ÇatışmaYönetimi":       2,
        "Fonolojik-Farkındalık":        2,
        "Fonolojik-YabancıDil":         2,
        "Bilimsel-Düşünce":             1,
        "EF-DürtüKontrolü":             2,
        "Değer-Sorumluluk":             1,
        "Değer-Dürüstlük":              1,
        "Değer-Empati":                 1,
        "Değer-Disiplin":               2,
        "Çevre-EvDesteği":              2,
        "Çevre-Biyolojik":              3,
        "Çevre-Dijital":                2,
        "Çevre-AileStres":              3,
    }

    def __init__(self, student_id: int, student_name: str, grade: str):
        self.sid   = student_id
        self.name  = student_name
        self.grade = grade
        self._load()

    # ── Veri yükleme ────────────────────────────────────────
    def _load(self):
        db = _conn()

        self.ak_rows = [dict(r) for r in db.execute("""
            SELECT al.log_date, su.name subject, o.code, o.text outcome,
                   al.symptom_ids, al.notes
            FROM   academic_logs al
            JOIN   subjects su ON su.id = al.subject_id
            JOIN   outcomes  o  ON o.id  = al.outcome_id
            WHERE  al.student_id = ?
            ORDER  BY al.log_date DESC
        """, (self.sid,)).fetchall()]

        self.so_rows = [dict(r) for r in db.execute("""
            SELECT sl.log_date, ss.dimension, ss.text symptom,
                   ss.theory_tag, sl.intensity, sl.notes
            FROM   social_logs sl
            JOIN   social_symptoms ss ON ss.id = sl.symptom_id
            WHERE  sl.student_id = ?
            ORDER  BY sl.log_date DESC
        """, (self.sid,)).fetchall()]

        # Akademik semptom etiketleri + metinleri
        all_ids: list[str] = []
        for row in self.ak_rows:
            all_ids += [x for x in str(row["symptom_ids"]).split(",") if x.strip().isdigit()]

        self.ak_tags:  list[str] = []
        self.ak_texts: list[str] = []
        if all_ids:
            ph = ",".join("?" * len(all_ids))
            for r in db.execute(
                f"SELECT text, theory_tag FROM academic_symptoms WHERE id IN ({ph})", all_ids
            ).fetchall():
                self.ak_texts.append(r["text"])
                if r["theory_tag"]:
                    self.ak_tags.append(r["theory_tag"])

        self.so_tags  = [r["theory_tag"] for r in self.so_rows if r["theory_tag"]]
        self.so_texts = [r["symptom"]    for r in self.so_rows]
        self.so_intens= {r["symptom"]: r["intensity"] for r in self.so_rows}
        db.close()

    # ── Puan hesaplama yardımcıları ─────────────────────────
    def _score(self, tags: list[str]) -> dict[str, int]:
        s: dict[str, int] = {}
        for t in tags:
            s[t] = s.get(t, 0) + self.W.get(t, 1)
        return s

    def _prefix(self, scores: dict, prefix: str) -> int:
        return sum(v for k, v in scores.items() if k.startswith(prefix))

    # ── Yardımcı: seviye metni ──────────────────────────────
    @staticmethod
    def _level(score: int, thresholds: list[tuple[int, str]]) -> str:
        for thr, label in sorted(thresholds, key=lambda x: x[0], reverse=True):
            if score >= thr:
                return label
        return thresholds[0][1]

    # ════════════════════════════════════════════════════════
    #  ANA ANALİZ
    # ════════════════════════════════════════════════════════
    def analyze(self) -> str:
        if not self.ak_rows and not self.so_rows:
            return (
                "⚠️  Bu öğrenci için henüz hiçbir gözlem kaydı girilmemiş.\n"
                "Lütfen önce Bilişsel ve Davranışsal Veri Girişi sekmelerinden\n"
                "en az bir kayıt ekleyin."
            )

        ak_sc = self._score(self.ak_tags)
        so_sc = self._score(self.so_tags)

        cog_load   = self._prefix(ak_sc, "Sweller")
        schema_sc  = self._prefix(ak_sc, "Piaget")
        meta_sc    = self._prefix(ak_sc, "Üstbiliş") + self._prefix(ak_sc, "Metakognitif")
        self_eff   = self._prefix(so_sc, "Bandura")
        emo_reg    = self._prefix(so_sc, "Goleman")
        social_sc  = self._prefix(so_sc, "Vygotsky") + self._prefix(so_sc, "Sosyal")
        env_sc     = self._prefix(so_sc, "Çevre")

        ak_total = len(self.ak_rows)
        so_total = len(self.so_rows)

        # Ders frekansı
        subj_freq: dict[str, int] = {}
        for r in self.ak_rows:
            subj_freq[r["subject"]] = subj_freq.get(r["subject"], 0) + 1

        # Semptom frekansı
        sym_freq: dict[str, int] = {}
        for t in self.ak_texts:
            sym_freq[t] = sym_freq.get(t, 0) + 1
        top_syms = sorted(sym_freq.items(), key=lambda x: x[1], reverse=True)[:5]

        # Yüksek yoğunluklu sosyal
        hi_social = [(t, i) for t, i in self.so_intens.items() if i >= 4]
        hi_social.sort(key=lambda x: x[1], reverse=True)

        # ── Bölüm 1: BİLİŞSEL HARİTA ──────────────────────
        cog_lbl = self._level(cog_load, [
            (0,  "🟢 DÜŞÜK — Belirgin bir bilişsel yük sorunu kaydedilmedi"),
            (2,  "🟡 ORTA — Belirli görevlerde bilişsel yük belirtileri var"),
            (5,  "🟠 YÜKSEK — Tutarlı aşırı yük; çalışma belleği baskı altında"),
            (9,  "🔴 KRİTİK — Çalışma belleği sistematik olarak aşılmış durumda"),
        ])
        sch_lbl = self._level(schema_sc, [
            (0,  "🟢 YETERLİ — Şema gelişimi büyük ölçüde sağlıklı"),
            (2,  "🟡 ORTA — Belirli kavramlarda şema boşlukları mevcut"),
            (5,  "🟠 ZAYIF — Asimilasyon/akomodasyon güçlüğü belirgin"),
            (10, "🔴 KRİTİK — Şema yapılanması ciddi biçimde sekteye uğramış"),
        ])

        # Ders barları
        ders_bar = ""
        for subj, cnt in sorted(subj_freq.items(), key=lambda x: x[1], reverse=True):
            bar = "█" * min(cnt, 8) + "░" * max(0, 8 - cnt)
            ders_bar += f"\n    {subj:<20} {bar}  ({cnt} kayıt)"

        # Semptom listesi
        sym_str = ""
        for t, cnt in top_syms:
            sym_str += f"\n    • {t}  [{cnt}×]"

        # Kazanım listesi
        outcomes_seen = list({r["outcome"] for r in self.ak_rows})[:6]
        outcome_str = "\n    • ".join(outcomes_seen) if outcomes_seen else "—"

        b1 = f"""
╔══════════════════════════════════════════════════════════════╗
║  BÖLÜM 1 — BİLİŞSEL HARİTA                                  ║
║  Teorik Çerçeve: Piaget (Şema Kuramı) · Sweller (BYK)       ║
╚══════════════════════════════════════════════════════════════╝

  Öğrenci : {self.name}
  Sınıf   : {self.grade}. Sınıf
  Tarih   : {date.today().isoformat()}
  Kayıt   : {ak_total} akademik gözlem

  ▌BİLİŞSEL YÜK DURUMU (Sweller)
  {cog_lbl}
  Bilişsel yük skoru: {cog_load} puan

  {"→ BULGULAR: Sweller'ın Bilişsel Yük Kuramı'na göre çalışma belleğinin kapasitesi " +
   ("aşılmış durumda. Öğrenci eş zamanlı birden fazla bilgiyi işlemekte ciddi güçlük " +
    "yaşamakta; bu durum kalıcı öğrenmeyi doğrudan engellemektedir. Çok adımlı " +
    "görevlerde aşama takibini yitirmesi, yönergeleri kısa süreli bellekte " +
    "tutamaması bu tablonun somut göstergeleridir."
    if cog_load >= 5 else
    "belirli görev türlerinde baskı altında. Bazı çok adımlı işlemlerde " +
    "performans düşüşü gözlemlenmektedir. Bu eşiğin üzerine çıkmadan önce " +
    "önleyici müdahale önerilmektedir."
    if cog_load >= 2 else
    "şu an için yeterli. Bilişsel yük kaynaklı belirgin bir sorun gözlemlenmedi."
   )}

  ▌ŞEMA YAPISI (Piaget)
  {sch_lbl}
  Şema skoru: {schema_sc} puan

  {"→ BULGULAR: Piaget'nin asimilasyon-akomodasyon dengesi bu öğrencide " +
   ("ciddi ölçüde bozulmuş. Yeni kavramlar mevcut bilişsel şemalara " +
    "yerleştirilememekte; bu da yüzeysel, geçici ezber davranışlarına yol " +
    "açmaktadır. Soyut matematiksel sembolleri somut anlamıyla ilişkilendirememe " +
    "ve öğrenilen stratejiyi yeni bağlamlara transfer edememe bu durumun " +
    "akademik yansımalarıdır."
    if schema_sc >= 5 else
    "belirli kavramlarda güçlükler gözlemleniyor. Soyut ve sembolik bilgilerin " +
    "somutlaştırılmasına yönelik ek destek önerilmektedir."
    if schema_sc >= 2 else
    "büyük ölçüde sağlıklı."
   )}

  ▌GÖZLEM YOĞUNLUĞU (Ders Bazlı){ders_bar}

  ▌EN SIK RASTLANAN BİLİŞSEL GÜÇLÜKLER{sym_str if sym_str else chr(10) + "    Veri yetersiz."}

  ▌GÖZLEM YAPILAN ÖĞRENME ÇIKTILARI
    • {outcome_str}

  ▌METAKOGNİTİF DURUM
  {"⚠️  SORUN VAR: Öğrenci ne bildiğini ve ne bilmediğini fark etmekte güçlük çekiyor." +
   " Kendi öğrenme sürecini izleyememesi, var olan boşlukları doldurmak için yardım aramasını engelliyor." +
   " Bu 'metakognitif kör nokta' şema gelişimini yavaşlatan gizli bir etkendir."
   if meta_sc >= 2 else
   "✓ Belirgin bir metakognitif eksiklik kaydedilmedi."}
"""

        # ── Bölüm 2: SOSYO-DUYGUSAL PROFİL ────────────────
        se_lbl = self._level(self_eff, [
            (0,  "🟢 YETERLİ — Öz-yeterlilik büyük ölçüde gelişmiş"),
            (2,  "🟡 GELİŞTİRİLEBİLİR — Belirli alanlarda öz-yeterlilik düşük"),
            (5,  "🟠 ZAYIF — Sistemik düşük öz-yeterlilik inancı"),
            (9,  "🔴 KRİTİK — Öz-yeterlilik inancı derinden zedelenmiş"),
        ])
        er_lbl = self._level(emo_reg, [
            (0,  "🟢 YETERLİ"),
            (2,  "🟡 GELİŞTİRİLEBİLİR — Belirli tetikleyicilerde düzensizlik"),
            (5,  "🟠 ZAYIF — Duygusal tepkiler çoğunlukla orantısız"),
            (9,  "🔴 KRİTİK — Duygusal düzenlemede sistemik bozukluk"),
        ])

        # Tüm sosyal gözlemler
        so_list = ""
        for r in self.so_rows:
            i = r["intensity"]
            bar = "●" * i + "○" * (5 - i)
            so_list += f"\n    {bar} [{i}/5]  {r['symptom']}"

        hi_str = ""
        if hi_social:
            hi_str = "\n\n  ⚠️  KRİTİK YOĞUNLUKTA GÖZLEMLER (4-5/5):"
            for t, i in hi_social:
                hi_str += f"\n    → {t}  (yoğunluk: {i}/5)"

        b2 = f"""
╔══════════════════════════════════════════════════════════════╗
║  BÖLÜM 2 — SOSYO-DUYGUSAL PROFİL                            ║
║  Teorik Çerçeve: Bandura (Öz-Yeterlilik) · Goleman (EQ)     ║
╚══════════════════════════════════════════════════════════════╝

  Toplam sosyal gözlem: {so_total}

  ▌ÖZ-YETERLİLİK ALGI DÜZEYİ (Bandura)
  {se_lbl}
  Öz-yeterlilik skoru: {self_eff} puan

  {"→ BULGULAR: Bandura'nın sosyal öğrenme kuramına göre öz-yeterlilik inancı " +
   ("bu öğrencide akademik katılımı ciddi biçimde kısıtlamaktadır. Başarısızlık " +
    "korkusu kalıcı bir kaçınma döngüsü oluşturmuştur. Başarısını şansa " +
    "bağlaması ve zorluğu görünce anında pes etmesi, öz-yeterlilik inancının " +
    "yeniden inşa edilmesini gerektirdiğini açıkça göstermektedir."
    if self_eff >= 5 else
    "belirli görev türlerinde düşük kalmaktadır. Başarı deneyimlerinin birikmesi " +
    "ve akran modellemesinin artırılması öncelikli müdahale alanıdır."
    if self_eff >= 2 else
    "büyük ölçüde sağlıklı görünmektedir."
   )}

  ▌DUYGUSAL REGÜLASYON (Goleman)
  {er_lbl}
  Duygusal regülasyon skoru: {emo_reg} puan

  {"→ BULGULAR: " +
   ("Öğrenci, duygusal tetikleyiciler (hata, bekleme, olumsuz geri bildirim) " +
    "karşısında yoğun ve ani tepkiler vermektedir. Bu durum sınıf içi öğrenmeyi " +
    "sekteye uğratmakta ve akran ilişkilerini olumsuz etkilemektedir. " +
    "Goleman'a göre prefrontal korteks işlevi duygusal aktivasyon anında " +
    "geçici olarak devre dışı kalmakta; bu da akademik performansı doğrudan " +
    "düşürmektedir."
    if emo_reg >= 5 else
    "Belirli durumlarda (hata anı, geçiş dönemleri) duygusal düzenlemede " +
    "güçlük yaşanmaktadır. Önleyici ko-regülasyon stratejileri önerilir."
    if emo_reg >= 2 else
    "Duygusal regülasyon becerileri büyük ölçüde gelişmiştir."
   )}

  ▌SOSYAL KATILIM (Vygotsky)
  {"⚠️  Akran ilişkilerinde ve işbirliğinde güçlükler mevcut. Vygotsky'nin ZPD modelinin " +
   "temelini oluşturan akran aracılığıyla öğrenme kapasitesi kısıtlı durumda."
   if social_sc >= 4 else
   "✓ Sosyal katılım büyük ölçüde işlevsel."}

  ▌ÇEVRESEL / AİLE FAKTÖRLERİ
  {"⚠️  Çevre kaynaklı faktörler akademik performansı olumsuz etkiliyor. " +
   "Uyku yetersizliği, aile stresi veya dijital ekran aşımı çalışma " +
   "belleği kapasitesini fizyolojik düzeyde kısıtlıyor olabilir. " +
   "Akademik müdahaleler bu faktörler çözümsüz kaldığı sürece " +
   "sınırlı etki yaratacaktır."
   if env_sc >= 4 else
   "✓ Belirgin bir çevresel risk faktörü kaydedilmedi."}

  ▌TÜM SOSYAL GÖZLEMLER (Yoğunluk Barı){so_list if so_list else chr(10) + "    Henüz kayıt yok."}{hi_str}
"""

        # ── Bölüm 3: KÖK NEDEN SENTEZİ ────────────────────
        diagnoses: list[str] = []

        if cog_load >= 4 and self_eff >= 4:
            diagnoses.append(
                "🔁 KİSİR DÖNGÜ: BİLİŞSEL YÜK ↔ ÖZ-YETERLİLİK ÇÖKÜŞÜ\n"
                "   Öğrenci bilişsel aşırı yük nedeniyle başarısız oluyor\n"
                "   → Başarısızlık öz-yeterlilik algısını daha da düşürüyor\n"
                "   → Düşük öz-yeterlilik yeni görevlerden kaçınmaya yol açıyor\n"
                "   → Kaçınma nedeniyle bilişsel pratik azalıyor\n"
                "   → Azalan pratikle bilişsel yük bir sonraki görevde daha erken aşılıyor.\n"
                "   ⚡ Bu döngü kırılmadan tek başına akademik müdahale yetersiz kalır."
            )
        if emo_reg >= 4 and cog_load >= 3:
            diagnoses.append(
                "⚡ DUYGUSAL BLOK → BİLİŞSEL ERİŞİM ENGELİ\n"
                "   Goleman: Kaygı ve öfke, prefrontal korteks işlevini geçici\n"
                "   olarak devre dışı bırakır. Bu öğrencide frustrasyon veya\n"
                "   kaygı anı oluştuğunda çalışma belleği kapasitesi dramatik\n"
                "   biçimde düşmektedir. Görünürde akademik olan güçlük aslında\n"
                "   duygusal kökenlidir — bu, öncelikli müdahale alanını değiştirir."
            )
        if schema_sc >= 4 and meta_sc >= 2:
            diagnoses.append(
                "🧩 FARKINDALIKSIZ ŞEMA BOŞLUĞU\n"
                "   Öğrenci hangi kavramları anlamadığını fark etmemektedir.\n"
                "   Bu 'metakognitif kör nokta', boşlukları doldurmak için\n"
                "   yardım aramasını engellemekte ve şema gelişimini kronik\n"
                "   biçimde yavaşlatmaktadır. Öğretmen geri bildirimi olmadan\n"
                "   öğrenci kendi eksikliğinin farkına varamaz."
            )
        if env_sc >= 4 and cog_load >= 2:
            diagnoses.append(
                "🏠 ÇEVRESEL STRES → BİYOLOJİK BİLİŞSEL KISITLAMA\n"
                "   Uyku yetersizliği, beslenme sorunları veya ev içi stres\n"
                "   çocuğun çalışma belleği kapasitesini ve dikkat süresini\n"
                "   fizyolojik düzeyde azaltmaktadır. Bu öğrenci akademik\n"
                "   ortama geldiğinde bilişsel kaynakları zaten tükenmiş\n"
                "   olabilir. Çevresel faktörler ele alınmadan sınıf içi\n"
                "   müdahaleler kalıcı sonuç vermez."
            )
        if social_sc >= 4:
            diagnoses.append(
                "🚪 SOSYAL ÖĞRENME KAPISI KAPALI (Vygotsky)\n"
                "   Öğrenci akranlarla işbirliği ve diyalog yoluyla gerçekleşen\n"
                "   ZPD sürecinden yeterince yararlanamamaktadır. Bu durum,\n"
                "   grup aktivitelerinin sağladığı doğal bilişsel iskele kurma\n"
                "   fırsatlarını ortadan kaldırmakta ve öğrenme yalnızlaşmaktadır."
            )
        if self_eff >= 3 and social_sc >= 3:
            diagnoses.append(
                "👁  SOSYAL KARŞILAŞTIRMA TUZAĞI (Bandura)\n"
                "   Hem düşük öz-yeterlilik hem de akran ilişkilerinde güçlük\n"
                "   birlikte var olduğunda öğrenci kendini akranlarıyla olumsuz\n"
                "   karşılaştırır. Bu durum utanç ve çekilme döngüsünü\n"
                "   pekiştirerek hem sosyal hem akademik katılımı azaltır."
            )

        if not diagnoses:
            diagnoses.append(
                "ℹ️  Mevcut verilerle belirgin bir sistemik döngü saptanamadı.\n"
                "   Daha kapsamlı analiz için en az 3-5 akademik ve\n"
                "   3-5 sosyal gözlem kaydı girilmesi önerilir."
            )

        b3 = f"""
╔══════════════════════════════════════════════════════════════╗
║  BÖLÜM 3 — KÖK NEDEN SENTEZİ                                ║
║  Çapraz teorik analiz: Bilişsel × Duygusal × Çevresel        ║
╚══════════════════════════════════════════════════════════════╝

  Bu bölüm yüzeysel belirtilerin ötesine geçerek öğrencinin
  zorluklarının birbirleriyle nasıl iç içe geçtiğini ortaya koyar.

  {'  ─────────────────────────────────────────────────' + chr(10) + '  '.join([''] + diagnoses)}
"""

        # ── Bölüm 4: MÜDAHALEsi PLANI ─────────────────────
        tactics: list[str] = []
        t_no = 1

        if cog_load >= 3:
            tactics.append(
                f"  TAKTİK {t_no} — CHUNKING (Mikro Adım Yönetimi)\n"
                "  Kuram: Sweller / Bilişsel Yük Kuramı\n"
                "  Uygulama:\n"
                "  → Her görevi maksimum 2-3 alt adıma bölün.\n"
                "    Bir adım tamamlanmadan bir sonrakini vermeyin.\n"
                "  → Tahtaya görsel adım listesi asın:\n"
                "    '1. şunu yap  →  2. şunu yap  →  3. kontrol et'\n"
                "  → Çalışma kağıdında her sayfaya yalnızca tek bir kazanım koyun.\n"
                "  → Sözlü yönergeyi hem söyleyin hem yazılı olarak sunun.\n"
                "  Hedef: Çalışma belleğindeki eş zamanlı yükü azaltmak;\n"
                "          her adımın başarıyla tamamlanması güven biriktirir."
            )
            t_no += 1

        if self_eff >= 3:
            tactics.append(
                f"  TAKTİK {t_no} — SCAFFOLDING (İskele Kurma)\n"
                "  Kuram: Vygotsky / ZPD + Bandura / Öz-Yeterlilik\n"
                "  Uygulama:\n"
                "  → ZPD testi: Öğrencinin tam bağımsız çözebildiği en kolay\n"
                "    görevi belirleyin. Bir üst düzey hedef olarak alın.\n"
                "  → Her doğru adımı süreç odaklı övgüyle pekiştirin:\n"
                "    'Aferin, bu adımı sen buldun çünkü...' (sonuç odaklı değil).\n"
                "  → Akran modeli: Benzer geçmişi olan birini sesli düşünürken\n"
                "    izletin. 'O yapabiliyorsa ben de yapabilirim' etkisi yaratır.\n"
                "  → İpucu kartları verin; zamanla kartları kaldırın (fading).\n"
                "  Hedef: Küçük başarılar öz-yeterlilik inancını adım adım yeniden inşa eder."
            )
            t_no += 1

        if schema_sc >= 4:
            tactics.append(
                f"  TAKTİK {t_no} — KÖPRÜLEYİCİ ANALOJİ (Şema İnşası)\n"
                "  Kuram: Piaget / Asimilasyon-Akomodasyon\n"
                "  Uygulama:\n"
                "  → Yeni kavramı tanıtmadan önce sorun:\n"
                "    'Bunu daha önce öğrendiğin neye benzetebiliriz?'\n"
                "  → Manipülatif materyaller kullanın: sayı çubukları, kesir\n"
                "    kartları, nesne modelleri. Soyut sembollere geçişi erteleyin.\n"
                "  → Her yeni bilgiyi daha önce öğrenilene açıkça bağlayın:\n"
                "    'Geçen hafta öğrendiğimiz X, bugünkü Y'ye şöyle bağlanır...'\n"
                "  → 'Çarpım' öğretirken önce fiziksel gruplama, sonra çizim,\n"
                "    sonra sembol şeklinde somuttan soyuta ilerleyin.\n"
                "  Hedef: Akomodasyon yeni şemayla bağlantı kurulduğunda çok daha\n"
                "          hızlı ve kalıcı gerçekleşir."
            )
            t_no += 1

        if emo_reg >= 3:
            tactics.append(
                f"  TAKTİK {t_no} — KO-REGÜLASYON ve GÜVENLİ HATA ORTAMI\n"
                "  Kuram: Goleman / Duygusal Zeka\n"
                "  Uygulama:\n"
                "  → Tüm sınıfa açıkça öğretin: 'Hata yapmak öğrenmenin parçası.'\n"
                "    Hata yapan öğrenciyi küçümsemek yerine modelleme yapın:\n"
                "    'Ben de bazen yanılırım, şimdi birlikte düzeltelim.'\n"
                "  → 'Dur-Nefes-Dene' rutinini kurun: Frustrasyon başladığında\n"
                "    öğrenci kendi kendine bu adımları uygulasın.\n"
                "  → Görev tesliminden sonra 1 dk 'nasıl hissettim' paylaşımı:\n"
                "    duyguyu isimlendirmek regülasyon kapasitesini artırır.\n"
                "  → Zorlayıcı görevleri sabah saatlerine alın;\n"
                "    öğrencinin yorgun veya sinirli olduğu zamanlarda yeni\n"
                "    kavram sunumundan kaçının.\n"
                "  Hedef: Güvenli ortamda amigdala aktivasyonu azalır;\n"
                "          prefrontal korteks kapasitesi korunur."
            )
            t_no += 1

        if social_sc >= 3:
            tactics.append(
                f"  TAKTİK {t_no} — İŞBİRLİKLİ ÖĞRENME YAPILARI\n"
                "  Kuram: Vygotsky / ZPD + Akran Aracılığıyla Öğrenme\n"
                "  Uygulama:\n"
                "  → 'Daha yetenekli akran' eşleştirmesi yapın:\n"
                "    Biraz ileride bir sınıf arkadaşıyla çift çalışma.\n"
                "  → Düşük riskli grup görevleri: öğrenci bir parçayı tamamlar,\n"
                "    bütünü grup birleştirir. Başarı kolektif, risk minimal.\n"
                "  → Sosyal beceri ipucu kartı: 'Fikirlerimi paylaşmak istiyorum'\n"
                "    / 'Sana katılmıyorum çünkü...' gibi ifadeler.\n"
                "  → Grup rotasyonu yapın: farklı arkadaşlarla deneyim biriktirsin.\n"
                "  Hedef: ZPD hem aktive olur hem de sosyal yetkinlik inancı gelişir."
            )
            t_no += 1

        if env_sc >= 4:
            tactics.append(
                f"  TAKTİK {t_no} — ÇEVRESEL DESTEK KÖPRÜSÜ\n"
                "  Kuram: Bronfenbrenner / Ekolojik Sistem\n"
                "  Uygulama:\n"
                "  → Aile görüşmesi: Uyku rutini ve ekran süresini konuşun.\n"
                "    Akademik baskı artırmak yerine rutin oluşturmayı önerin.\n"
                "  → Rehber öğretmen veya sosyal hizmet desteği için sevk\n"
                "    değerlendirilmeli.\n"
                "  → Okul içinde öğrenciye küçük sorumluluklar vererek\n"
                "    okul bağını ve güvenli alan hissini güçlendirin.\n"
                "  Hedef: Çevresel stres kaynakları azalmadan bilişsel ve\n"
                "          duygusal müdahalelerin kalıcı etkisi sınırlı kalır."
            )
            t_no += 1

        if meta_sc >= 2:
            tactics.append(
                f"  TAKTİK {t_no} — METAKOGNİTİF RUTİN ('Ne biliyorum, ne bilmiyorum?')\n"
                "  Kuram: Flavell / Üstbiliş Kuramı\n"
                "  Uygulama:\n"
                "  → Her görev öncesi sorun: 'Bu konudan emin olduğun\n"
                "    1 şey, emin olmadığın 1 şey nedir?'\n"
                "  → 'Öğrenme günlüğü' tutturun: bugün öğrendim, anlamadım,\n"
                "    yarın sormak istiyorum.\n"
                "  → 'Kendi testini yaz': Öğrenci kendi sorularını oluştursun.\n"
                "    Bu, kavramı ne kadar anladığını görünür kılar.\n"
                "  Hedef: Öz-izleme kapasitesi gelişince boşluklar görünür hale\n"
                "          gelir ve yardım arama davranışı kendiliğinden artar."
            )
            t_no += 1

        if not tactics:
            tactics.append(
                "  ℹ️  Henüz hedefli müdahale planı oluşturmak için yeterli\n"
                "  veri yok. Ek gözlem kaydı girildiğinde öncelikli\n"
                "  taktikler otomatik olarak belirlenir."
            )

        priority = (
            "→ ÖNCELİK: Önce duygusal/sosyal müdahalelerle güvenli ortam oluşturun,\n"
            "  ardından bilişsel taktikler uygulamaya alınabilir.\n"
            "  (Güvensiz ortamda bilişsel müdahaleler işe yaramaz.)"
            if (emo_reg + self_eff) > (cog_load + schema_sc)
            else
            "→ ÖNCELİK: Bilişsel müdahaleler öne çekilebilir; sosyal destek paralel yürütülür."
        )

        b4 = f"""
╔══════════════════════════════════════════════════════════════╗
║  BÖLÜM 4 — ZPD KÖPRÜSÜ & MÜDAHALEsi PLANI                  ║
║  Kuram: Vygotsky / Yakınsal Gelişim Alanı                    ║
╚══════════════════════════════════════════════════════════════╝

  Mevcut Gelişim Düzeyi  → öğrencinin bağımsız yapabildiği düzey
  ZPD Hedefi             → destekle ulaşılabilecek bir üst basamak
  Yöntem                 → aşağıdaki somut taktikler

  {"─" * 58}
{chr(10).join(["  " + t for t in tactics])}
  {"─" * 58}

  PUAN TABLOSU
  ┌─────────────────────────────┬──────────┐
  │ Alan                        │  Skor    │
  ├─────────────────────────────┼──────────┤
  │ Bilişsel Yük (Sweller)      │  {cog_load:>5}   │
  │ Şema Güçlüğü (Piaget)       │  {schema_sc:>5}   │
  │ Öz-Yeterlilik (Bandura)     │  {self_eff:>5}   │
  │ Duygusal Regülasyon (Golem) │  {emo_reg:>5}   │
  │ Sosyal Katılım (Vygotsky)   │  {social_sc:>5}   │
  │ Çevresel Risk               │  {env_sc:>5}   │
  └─────────────────────────────┴──────────┘

  {priority}

  ═══════════════════════════════════════════════════════════
  Bu rapor OmegaClass PedagogyEngine v3 tarafından üretilmiştir.
  Dış bir yapay zeka API'si kullanılmamıştır.
  ═══════════════════════════════════════════════════════════
"""

        return b1 + b2 + b3 + b4


# ════════════════════════════════════════════════════════════
#  SAYFA YAPISI & CSS
# ════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="OmegaClass",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
html,body,[class*="css"]{font-family:'Inter',sans-serif}
.stApp{background:#080c15;color:#dde2f0}
/* Hero */
.hero{background:linear-gradient(135deg,#140d2e 0%,#0a1428 100%);
      border:1px solid #2a2248;border-radius:16px;
      padding:2rem 2.5rem;margin-bottom:2rem}
.hero h1{margin:0;font-size:2rem;
         background:linear-gradient(90deg,#a78bfa,#38bdf8);
         -webkit-background-clip:text;-webkit-text-fill-color:transparent}
.hero p{margin:.4rem 0 0;color:#64748b;font-size:.88rem}
/* Cards */
.card{background:linear-gradient(135deg,#111827,#0d1220);
      border:1px solid #1e2640;border-radius:12px;
      padding:1.2rem 1.5rem;margin-bottom:.8rem}
.cv{border-left:4px solid #7c3aed}
.ct{border-left:4px solid #0d9488}
.ca{border-left:4px solid #b45309}
.cb{border-left:4px solid #1d4ed8}
.cr{border-left:4px solid #be123c}
/* Buttons */
.stButton>button{background:linear-gradient(135deg,#5b21b6,#3730a3)!important;
                 color:#fff!important;border:none!important;border-radius:8px!important;
                 padding:.5rem 1.4rem!important;font-weight:600!important;
                 transition:all .2s!important}
.stButton>button:hover{transform:translateY(-1px)!important;
                       box-shadow:0 4px 16px rgba(91,33,182,.45)!important}
/* Tabs */
.stTabs [data-baseweb="tab-list"]{background:#0d1018;border-radius:10px;padding:3px;gap:1px}
.stTabs [data-baseweb="tab"]{color:#3d4a6b;font-weight:600;border-radius:7px;padding:7px 18px}
.stTabs [aria-selected="true"]{background:#1a1540!important;color:#a78bfa!important}
/* Sidebar */
[data-testid="stSidebar"]{background:#060910;border-right:1px solid #141c2e}
/* Labels */
.stSelectbox label,.stMultiSelect label,
.stTextInput label,.stTextArea label{color:#64748b!important;font-weight:500}
/* Analysis output */
.analysis{background:#04070d;border:1px solid #1a2535;border-radius:10px;
           padding:1.4rem 1.6rem;
           font-family:'Courier New',Courier,monospace;
           font-size:.8rem;line-height:1.8;color:#94a3b8;
           white-space:pre-wrap;max-height:72vh;overflow-y:auto}
/* Badges */
.badge{display:inline-block;padding:2px 10px;border-radius:20px;
       font-size:.7rem;font-weight:700}
.ba{background:#2e1065;color:#c084fc}
.bt{background:#052e16;color:#4ade80}
/* Misc */
hr{border-color:#1e2640}
</style>
""", unsafe_allow_html=True)

# ── Session state ────────────────────────────────────────────
if "user" not in st.session_state:
    st.session_state.user = None


# ════════════════════════════════════════════════════════════
#  LOGIN
# ════════════════════════════════════════════════════════════

def page_login() -> None:
    st.markdown("""
    <div style='text-align:center;padding:3rem 0 1.5rem'>
      <div style='font-size:3.5rem'>🧠</div>
      <h1 style='background:linear-gradient(90deg,#a78bfa,#38bdf8);
                 -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                 font-size:2.4rem;margin:.4rem 0'>OmegaClass</h1>
      <p style='color:#3d4a6b;margin-bottom:2.5rem'>
        Holistik Öğrenci Gelişim Platformu</p>
    </div>""", unsafe_allow_html=True)

    _, mid, _ = st.columns([1, 1.2, 1])
    with mid:
        st.markdown('<div class="card cv">', unsafe_allow_html=True)
        username = st.text_input("Kullanıcı Adı", key="li_u")
        password = st.text_input("Şifre", type="password", key="li_p")
        if st.button("Giriş Yap →", use_container_width=True):
            user = authenticate(username, password)
            if user:
                st.session_state.user = user
                st.rerun()
            else:
                st.error("Hatalı kullanıcı adı veya şifre.")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <p style='text-align:center;color:#1e2a42;font-size:.75rem;margin-top:1rem'>
      Admin: admin / admin123 &nbsp;·&nbsp;
      Öğretmen: ogretmen1 / ogretmen123
    </p>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
#  SIDEBAR
# ════════════════════════════════════════════════════════════

def sidebar() -> None:
    u = st.session_state.user
    with st.sidebar:
        st.markdown(f"### {u['full_name']}")
        role = "Admin" if u["role"] == "admin" else "Öğretmen"
        cls  = "ba" if u["role"] == "admin" else "bt"
        st.markdown(f'<span class="badge {cls}">{role}</span>', unsafe_allow_html=True)
        st.markdown("---")
        st.caption(f"DB: `{Path(DB_PATH).name}`")
        st.caption("OmegaClass v3 · Cloud-Ready")
        st.markdown("---")
        if st.button("🚪 Çıkış Yap", use_container_width=True):
            st.session_state.user = None
            st.rerun()


# ════════════════════════════════════════════════════════════
#  ADMIN PANELİ
# ════════════════════════════════════════════════════════════

def page_admin() -> None:
    u = st.session_state.user
    st.markdown(f"""
    <div class="hero"><h1>🧠 OmegaClass — Admin</h1>
    <p>Müfredat ve Kural Motoru Paneli &nbsp;·&nbsp;
       <b>{u['full_name']}</b> <span class="badge ba">ADMIN</span></p>
    </div>""", unsafe_allow_html=True)

    db = _conn()
    t1, t2, t3, t4 = st.tabs(["📚 Dersler & Kazanımlar", "🧠 Akademik Semptomlar",
                                "💛 Sosyal Semptomlar",    "👥 Kullanıcılar"])

    # ── Dersler & Kazanımlar ─────────────────────────────────
    with t1:
        col1, col2 = st.columns(2)

        with col1:
            st.markdown('<div class="card cv">', unsafe_allow_html=True)
            st.markdown("**➕ Yeni Ders**")
            new_s = st.text_input("Ders adı", key="a_ns")
            if st.button("Ekle", key="a_sadd"):
                if new_s.strip():
                    try:
                        db.execute("INSERT INTO subjects(name) VALUES(?)", (new_s.strip(),))
                        db.commit(); st.success("Eklendi."); st.rerun()
                    except Exception:
                        st.warning("Bu ders zaten var.")
            st.markdown("</div>", unsafe_allow_html=True)

            subs = pd.read_sql("SELECT id,name FROM subjects ORDER BY name", db)
            if not subs.empty:
                st.markdown("**Mevcut Dersler**")
                st.dataframe(subs, hide_index=True, use_container_width=True)
                del_id = st.number_input("Silinecek Ders ID", 0, step=1, key="a_sdel")
                if st.button("🗑️ Ders Sil", key="a_sdelb"):
                    if del_id:
                        db.execute("DELETE FROM subjects WHERE id=?", (int(del_id),))
                        db.commit(); st.success("Silindi."); st.rerun()

        with col2:
            st.markdown('<div class="card ct">', unsafe_allow_html=True)
            st.markdown("**➕ Kazanım Ekle**")
            subs2 = pd.read_sql("SELECT id,name FROM subjects ORDER BY name", db)
            if not subs2.empty:
                sub_sel = st.selectbox("Ders", subs2["name"].tolist(), key="a_osubsel")
                osid    = int(subs2[subs2["name"] == sub_sel]["id"].values[0])
                ograde  = st.selectbox("Sınıf", ["1","2","3","4"], key="a_ograde")
                ocode   = st.text_input("Kod (örn: M.4.1.2)", key="a_ocode")
                otext   = st.text_area("Kazanım metni", key="a_otext", height=70)
                if st.button("Kazanım Ekle", key="a_oadd"):
                    if ocode.strip() and otext.strip():
                        db.execute(
                            "INSERT INTO outcomes(subject_id,grade,code,text) VALUES(?,?,?,?)",
                            (osid, ograde, ocode.strip(), otext.strip())
                        )
                        db.commit(); st.success("Eklendi."); st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

            outs = pd.read_sql("""
                SELECT o.id, s.name ders, o.grade sinif, o.code kod, o.text metin
                FROM outcomes o JOIN subjects s ON s.id=o.subject_id
                ORDER BY s.name, o.grade, o.code
            """, db)
            if not outs.empty:
                st.markdown("**Kazanımlar**")
                filt = st.selectbox("Filtrele", ["Tümü"] + subs2["name"].tolist(), key="a_ofilt")
                show = outs if filt == "Tümü" else outs[outs["ders"] == filt]
                st.dataframe(show, hide_index=True, use_container_width=True)
                del_oid = st.number_input("Silinecek Kazanım ID", 0, step=1, key="a_odel")
                if st.button("🗑️ Kazanım Sil", key="a_odelb"):
                    if del_oid:
                        db.execute("DELETE FROM outcomes WHERE id=?", (int(del_oid),))
                        db.commit(); st.success("Silindi."); st.rerun()

    # ── Akademik Semptomlar ──────────────────────────────────
    with t2:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="card ca">', unsafe_allow_html=True)
            st.markdown("**➕ Akademik Semptom Ekle**")
            subs3    = pd.read_sql("SELECT id,name FROM subjects ORDER BY name", db)
            sym_opts = ["Genel (NULL)"] + (subs3["name"].tolist() if not subs3.empty else [])
            sym_sub  = st.selectbox("Ders (boş = genel)", sym_opts, key="a_ssub")
            ssid     = None if sym_sub == "Genel (NULL)" else (
                int(subs3[subs3["name"] == sym_sub]["id"].values[0]) if not subs3.empty else None
            )
            stext  = st.text_area("Semptom metni", key="a_stext", height=70)
            stag   = st.text_input("Teorik etiket (örn: Sweller-BilişselYük)", key="a_stag")
            if st.button("Ekle", key="a_sadd2"):
                if stext.strip():
                    db.execute(
                        "INSERT INTO academic_symptoms(subject_id,text,theory_tag) VALUES(?,?,?)",
                        (ssid, stext.strip(), stag.strip())
                    )
                    db.commit(); st.success("Eklendi."); st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            as_df = pd.read_sql("""
                SELECT a.id, COALESCE(s.name,'Genel') ders, a.text, a.theory_tag
                FROM academic_symptoms a LEFT JOIN subjects s ON s.id=a.subject_id
                ORDER BY ders, a.id
            """, db)
            if not as_df.empty:
                st.dataframe(as_df, hide_index=True, use_container_width=True)
                del_asid = st.number_input("Silinecek ID", 0, step=1, key="a_asdel")
                if st.button("🗑️ Sil", key="a_asdelb"):
                    if del_asid:
                        db.execute("DELETE FROM academic_symptoms WHERE id=?", (int(del_asid),))
                        db.commit(); st.success("Silindi."); st.rerun()

    # ── Sosyal Semptomlar ────────────────────────────────────
    with t3:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="card ct">', unsafe_allow_html=True)
            st.markdown("**➕ Sosyal Semptom Ekle**")
            dims = ["Öz-Yeterlilik (Bandura)","Duygusal Regülasyon (Goleman)",
                    "Sosyal Katılım ve Akran İlişkileri",
                    "Erdem-Değer-Eylem Çerçevesi","Aile ve Ev Ortamı"]
            sdim  = st.selectbox("Boyut", dims, key="a_sdim")
            sstext= st.text_area("Semptom metni", key="a_sstext", height=70)
            sstag = st.text_input("Teorik etiket", key="a_sstag")
            if st.button("Ekle", key="a_ssadd"):
                if sstext.strip():
                    db.execute(
                        "INSERT INTO social_symptoms(dimension,text,theory_tag) VALUES(?,?,?)",
                        (sdim, sstext.strip(), sstag.strip())
                    )
                    db.commit(); st.success("Eklendi."); st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            ss_df = pd.read_sql("SELECT * FROM social_symptoms ORDER BY dimension,id", db)
            if not ss_df.empty:
                st.dataframe(ss_df, hide_index=True, use_container_width=True)
                del_ssid = st.number_input("Silinecek ID", 0, step=1, key="a_ssdel")
                if st.button("🗑️ Sil", key="a_ssdelb"):
                    if del_ssid:
                        db.execute("DELETE FROM social_symptoms WHERE id=?", (int(del_ssid),))
                        db.commit(); st.success("Silindi."); st.rerun()

    # ── Kullanıcılar ─────────────────────────────────────────
    with t4:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="card cb">', unsafe_allow_html=True)
            st.markdown("**➕ Öğretmen Hesabı Ekle**")
            nu = st.text_input("Kullanıcı adı", key="a_nu")
            nf = st.text_input("Ad Soyad",      key="a_nf")
            np = st.text_input("Şifre", type="password", key="a_np")
            if st.button("Ekle", key="a_uadd"):
                if nu.strip() and np.strip():
                    try:
                        db.execute(
                            "INSERT INTO users(username,password,role,full_name) VALUES(?,?,?,?)",
                            (nu.strip(), _hp(np), "teacher", nf.strip())
                        )
                        db.commit(); st.success(f"'{nu}' hesabı oluşturuldu.")
                    except Exception:
                        st.warning("Bu kullanıcı adı zaten var.")
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            users_df = pd.read_sql(
                "SELECT id,username,role,full_name FROM users ORDER BY role,username", db
            )
            st.dataframe(users_df, hide_index=True, use_container_width=True)

    db.close()


# ════════════════════════════════════════════════════════════
#  ÖĞRETMEN PANELİ
# ════════════════════════════════════════════════════════════

def page_teacher() -> None:
    u   = st.session_state.user
    tid = u["id"]

    st.markdown(f"""
    <div class="hero"><h1>🧠 OmegaClass</h1>
    <p><b>{u['full_name']}</b>
       <span class="badge bt">ÖĞRETMEN</span></p>
    </div>""", unsafe_allow_html=True)

    db = _conn()
    t1, t2, t3, t4 = st.tabs([
        "👩‍🏫 Sınıf Yönetimi",
        "📚 Bilişsel Veri Girişi",
        "💛 Davranışsal Veri Girişi",
        "🔬 Arşiv & Analiz",
    ])

    # ── Sınıf Yönetimi ──────────────────────────────────────
    with t1:
        st.markdown('<div class="card cv">', unsafe_allow_html=True)
        st.markdown("#### ➕ Öğrenci Ekle")
        c1, c2 = st.columns([3, 1])
        with c1:
            stn  = st.text_input("Ad Soyad", key="t_stn")
        with c2:
            stg  = st.selectbox("Sınıf", ["1","2","3","4"], key="t_stg")
        if st.button("Ekle", key="t_stadd", use_container_width=True):
            if stn.strip():
                db.execute("INSERT INTO students(teacher_id,name,grade) VALUES(?,?,?)",
                           (tid, stn.strip(), stg))
                db.commit(); st.success(f"'{stn}' eklendi."); st.rerun()
            else:
                st.warning("İsim girin.")
        st.markdown("</div>", unsafe_allow_html=True)

        sts = pd.read_sql(
            "SELECT id,name,grade,created_at FROM students WHERE teacher_id=? ORDER BY grade,name",
            db, params=(tid,)
        )
        if not sts.empty:
            st.metric("Toplam Öğrenci", len(sts))
            st.dataframe(sts, hide_index=True, use_container_width=True)
            del_st = st.selectbox("Sil", ["— seçin —"] + sts["name"].tolist(), key="t_stdel")
            if st.button("🗑️ Sil", key="t_stdelb"):
                if del_st != "— seçin —":
                    del_id = int(sts[sts["name"] == del_st]["id"].values[0])
                    db.execute("DELETE FROM students WHERE id=? AND teacher_id=?", (del_id, tid))
                    db.commit(); st.success(f"'{del_st}' silindi."); st.rerun()
        else:
            st.info("Henüz öğrenci eklenmedi.")

    # ── Bilişsel Veri Girişi ─────────────────────────────────
    with t2:
        sts = pd.read_sql(
            "SELECT id,name,grade FROM students WHERE teacher_id=? ORDER BY name",
            db, params=(tid,)
        )
        if sts.empty:
            st.info("Önce Sınıf Yönetimi sekmesinden öğrenci ekleyin.")
        else:
            c1, c2 = st.columns(2)
            with c1:
                st.markdown('<div class="card cv">', unsafe_allow_html=True)
                ak_st    = st.selectbox("Öğrenci", sts["name"].tolist(), key="t_akst")
                ak_sid   = int(sts[sts["name"] == ak_st]["id"].values[0])
                ak_grade = sts[sts["name"] == ak_st]["grade"].values[0]
                subs     = pd.read_sql("SELECT id,name FROM subjects ORDER BY name", db)
                ak_sub   = st.selectbox("Ders", subs["name"].tolist(), key="t_aksub")
                ak_subid = int(subs[subs["name"] == ak_sub]["id"].values[0])
                outs     = pd.read_sql(
                    "SELECT id,code,text FROM outcomes WHERE subject_id=? AND grade=? ORDER BY code",
                    db, params=(ak_subid, ak_grade)
                )
                st.markdown("</div>", unsafe_allow_html=True)

            with c2:
                st.markdown('<div class="card ct">', unsafe_allow_html=True)
                if outs.empty:
                    st.warning(f"{ak_sub} / {ak_grade}. sınıf için kazanım yok.")
                    ak_outid = None
                else:
                    labels   = (outs["code"] + " — " + outs["text"]).tolist()
                    ak_out   = st.selectbox("Kazanım", labels, key="t_akout")
                    ak_outid = int(outs.iloc[labels.index(ak_out)]["id"])

                syms = pd.read_sql("""
                    SELECT id,text FROM academic_symptoms
                    WHERE subject_id=? OR subject_id IS NULL
                    ORDER BY subject_id DESC, id
                """, db, params=(ak_subid,))

                if syms.empty:
                    st.info("Bu ders için semptom tanımlanmamış.")
                    ak_syms = []
                else:
                    ak_syms = st.multiselect("Bilişsel Semptomlar",
                                             syms["text"].tolist(), key="t_aksyms")
                ak_notes = st.text_area("Öğretmen Notu", height=80, key="t_aknotes")
                st.markdown("</div>", unsafe_allow_html=True)

            if st.button("💾 Kaydet", key="t_aksave", use_container_width=True):
                if not ak_outid:
                    st.warning("Kazanım seçin.")
                elif not ak_syms:
                    st.warning("En az bir semptom seçin.")
                else:
                    sym_ids = ",".join(
                        str(int(syms[syms["text"] == s]["id"].values[0])) for s in ak_syms
                    )
                    db.execute("""
                        INSERT INTO academic_logs
                        (teacher_id,student_id,subject_id,outcome_id,symptom_ids,notes)
                        VALUES(?,?,?,?,?,?)
                    """, (tid, ak_sid, ak_subid, ak_outid, sym_ids, ak_notes))
                    db.commit()
                    st.success("✅ Akademik gözlem kaydedildi.")

    # ── Davranışsal Veri Girişi ──────────────────────────────
    with t3:
        sts = pd.read_sql(
            "SELECT id,name FROM students WHERE teacher_id=? ORDER BY name",
            db, params=(tid,)
        )
        if sts.empty:
            st.info("Önce öğrenci ekleyin.")
        else:
            c1, c2 = st.columns(2)
            with c1:
                st.markdown('<div class="card ct">', unsafe_allow_html=True)
                so_st   = st.selectbox("Öğrenci", sts["name"].tolist(), key="t_sost")
                so_sid  = int(sts[sts["name"] == so_st]["id"].values[0])
                dims    = pd.read_sql(
                    "SELECT DISTINCT dimension FROM social_symptoms ORDER BY dimension", db
                )["dimension"].tolist()
                so_dim  = st.selectbox("Boyut", dims, key="t_sodim")
                st.markdown("</div>", unsafe_allow_html=True)

            with c2:
                st.markdown('<div class="card ca">', unsafe_allow_html=True)
                dim_syms = pd.read_sql(
                    "SELECT id,text FROM social_symptoms WHERE dimension=? ORDER BY id",
                    db, params=(so_dim,)
                )
                if dim_syms.empty:
                    st.info("Bu boyut için semptom yok.")
                    so_symid = None
                else:
                    so_sym   = st.selectbox("Gözlemlenen Davranış",
                                            dim_syms["text"].tolist(), key="t_sosym")
                    so_symid = int(dim_syms[dim_syms["text"] == so_sym]["id"].values[0])
                so_int  = st.slider("Yoğunluk (1=Nadir, 5=Sürekli)", 1, 5, 3, key="t_soint")
                so_note = st.text_area("Bağlam / Notlar", height=80, key="t_sonote")
                st.markdown("</div>", unsafe_allow_html=True)

            if st.button("💾 Kaydet", key="t_sosave", use_container_width=True):
                if not so_symid:
                    st.warning("Semptom seçin.")
                else:
                    db.execute("""
                        INSERT INTO social_logs(teacher_id,student_id,symptom_id,intensity,notes)
                        VALUES(?,?,?,?,?)
                    """, (tid, so_sid, so_symid, so_int, so_note))
                    db.commit()
                    st.success("✅ Sosyal gözlem kaydedildi.")

    # ── Arşiv & Analiz ───────────────────────────────────────
    with t4:
        sts = pd.read_sql(
            "SELECT id,name,grade FROM students WHERE teacher_id=? ORDER BY name",
            db, params=(tid,)
        )
        if sts.empty:
            st.info("Henüz öğrenci yok."); db.close(); return

        sel_st    = st.selectbox("Öğrenci Seç", sts["name"].tolist(), key="t_arch")
        sel_sid   = int(sts[sts["name"] == sel_st]["id"].values[0])
        sel_grade = sts[sts["name"] == sel_st]["grade"].values[0]

        ak_logs = pd.read_sql("""
            SELECT al.id, al.log_date tarih, s.name ders, o.code kazanim,
                   o.text kazanim_metin, al.notes notlar
            FROM   academic_logs al
            JOIN   subjects s ON s.id = al.subject_id
            JOIN   outcomes  o ON o.id = al.outcome_id
            WHERE  al.student_id=? AND al.teacher_id=?
            ORDER  BY al.log_date DESC
        """, db, params=(sel_sid, tid))

        so_logs = pd.read_sql("""
            SELECT sl.id, sl.log_date tarih, ss.dimension boyut,
                   ss.text semptom, sl.intensity yogunluk, sl.notes not
            FROM   social_logs sl
            JOIN   social_symptoms ss ON ss.id = sl.symptom_id
            WHERE  sl.student_id=? AND sl.teacher_id=?
            ORDER  BY sl.log_date DESC
        """, db, params=(sel_sid, tid))

        m1, m2 = st.columns(2)
        m1.metric("Akademik Kayıt", len(ak_logs))
        m2.metric("Sosyal Kayıt",   len(so_logs))

        # PedagogyEngine
        st.markdown("---")
        if st.button("🔬 PedagogyEngine Analizi Başlat", use_container_width=True, type="primary"):
            with st.spinner("Kural motoru işliyor..."):
                engine = PedagogyEngine(sel_sid, sel_st, sel_grade)
                result = engine.analyze()
            st.markdown(f'<div class="analysis">{result}</div>', unsafe_allow_html=True)

        # Log görüntüle / sil
        st.markdown("---")
        st.markdown("**📚 Akademik Kayıtlar**")
        if not ak_logs.empty:
            st.dataframe(ak_logs, hide_index=True, use_container_width=True)
            del_ak = st.number_input("Silinecek Akademik Log ID", 0, step=1, key="t_dakid")
            if st.button("🗑️ Akademik Kaydı Sil", key="t_dakb"):
                if del_ak:
                    db.execute("DELETE FROM academic_logs WHERE id=? AND teacher_id=?",
                               (int(del_ak), tid))
                    db.commit(); st.success("Silindi."); st.rerun()
        else:
            st.info("Akademik kayıt yok.")

        st.markdown("**💛 Sosyal Kayıtlar**")
        if not so_logs.empty:
            st.dataframe(so_logs, hide_index=True, use_container_width=True)
            del_so = st.number_input("Silinecek Sosyal Log ID", 0, step=1, key="t_dsoid")
            if st.button("🗑️ Sosyal Kaydı Sil", key="t_dsob"):
                if del_so:
                    db.execute("DELETE FROM social_logs WHERE id=? AND teacher_id=?",
                               (int(del_so), tid))
                    db.commit(); st.success("Silindi."); st.rerun()
        else:
            st.info("Sosyal kayıt yok.")

    db.close()


# ════════════════════════════════════════════════════════════
#  ANA AKIŞ
# ════════════════════════════════════════════════════════════
init_db()

if st.session_state.user is None:
    page_login()
else:
    sidebar()
    if st.session_state.user["role"] == "admin":
        page_admin()
    else:
        page_teacher()
