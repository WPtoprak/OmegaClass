"""
╔══════════════════════════════════════════════════════════════╗
║  OmegaClass v4 — 360° Eğitim Fakültesi Destekli Platform    ║
║  Streamlit Community Cloud uyumlu · SQLite · Omni-Brain      ║
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

# ── OmegaClass Omni-Brain ───────────────────────────────────
from SymptomTaxonomy import SYMPTOM_TAXONOMY
from PedagogyBrain import PedagogyBrain, StudentInput, BehaviorRecord, OutcomeRecord

# ════════════════════════════════════════════════════════════
#  BULUT-UYUMLU VERİTABANI YOLU
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

def _seed(db: sqlite3.Connection, cur: sqlite3.Cursor) -> None:
    if cur.execute("SELECT COUNT(*) FROM users").fetchone()[0] > 0:
        return

    cur.executemany(
        "INSERT INTO users(username,password,role,full_name) VALUES(?,?,?,?)",
        [
            ("admin",      _hp("admin123"),    "admin",   "Sistem Yöneticisi"),
            ("ogretmen1",  _hp("ogretmen123"), "teacher", "Ayşe Yıldız"),
            ("ogretmen2",  _hp("ogretmen456"), "teacher", "Mehmet Demir"),
        ]
    )

    subjects = [
        "Matematik", "Türkçe", "Fen Bilimleri", "Sosyal Bilgiler",
        "Hayat Bilgisi", "İngilizce", "Görsel Sanatlar", "Müzik", "Beden Eğitimi",
    ]
    cur.executemany("INSERT INTO subjects(name) VALUES(?)", [(s,) for s in subjects])

    def sid(name: str) -> int:
        return cur.execute("SELECT id FROM subjects WHERE name=?", (name,)).fetchone()[0]

    outcomes_raw = [
        (sid("Matematik"), "4", "M.4.1.3", "Dört işlemi yapar; problemlerde kullanır."),
        (sid("Türkçe"), "4", "T.4.4.1", "Paragraf oluşturarak giriş-gelişme-sonuç bütünlüğüyle yazar."),
        (sid("Fen Bilimleri"), "4", "FEN.4.3.1", "Elektrik devresi kurar; çalışma prensibini açıklar."),
    ]
    cur.executemany("INSERT INTO outcomes(subject_id,grade,code,text) VALUES(?,?,?,?)", outcomes_raw)
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
.hero{background:linear-gradient(135deg,#140d2e 0%,#0a1428 100%);
      border:1px solid #2a2248;border-radius:16px;
      padding:2rem 2.5rem;margin-bottom:2rem}
.hero h1{margin:0;font-size:2rem;
         background:linear-gradient(90deg,#a78bfa,#38bdf8);
         -webkit-background-clip:text;-webkit-text-fill-color:transparent}
.hero p{margin:.4rem 0 0;color:#64748b;font-size:.88rem}
.card{background:linear-gradient(135deg,#111827,#0d1220);
      border:1px solid #1e2640;border-radius:12px;
      padding:1.2rem 1.5rem;margin-bottom:.8rem}
.cv{border-left:4px solid #7c3aed}
.ct{border-left:4px solid #0d9488}
.ca{border-left:4px solid #b45309}
.cb{border-left:4px solid #1d4ed8}
.cr{border-left:4px solid #be123c}
.stButton>button{background:linear-gradient(135deg,#5b21b6,#3730a3)!important;
                 color:#fff!important;border:none!important;border-radius:8px!important;
                 padding:.5rem 1.4rem!important;font-weight:600!important;
                 transition:all .2s!important}
.stButton>button:hover{transform:translateY(-1px)!important;
                       box-shadow:0 4px 16px rgba(91,33,182,.45)!important}
.stTabs [data-baseweb="tab-list"]{background:#0d1018;border-radius:10px;padding:3px;gap:1px}
.stTabs [data-baseweb="tab"]{color:#3d4a6b;font-weight:600;border-radius:7px;padding:7px 18px}
.stTabs [aria-selected="true"]{background:#1a1540!important;color:#a78bfa!important}
[data-testid="stSidebar"]{background:#060910;border-right:1px solid #141c2e}
.stSelectbox label,.stMultiSelect label,
.stTextInput label,.stTextArea label{color:#64748b!important;font-weight:500}
.badge{display:inline-block;padding:2px 10px;border-radius:20px;
       font-size:.7rem;font-weight:700}
.ba{background:#2e1065;color:#c084fc}
.bt{background:#052e16;color:#4ade80}
hr{border-color:#1e2640}
</style>
""", unsafe_allow_html=True)

if "user" not in st.session_state:
    st.session_state.user = None

# ════════════════════════════════════════════════════════════
#  LOGIN & SIDEBAR
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

def sidebar() -> None:
    u = st.session_state.user
    with st.sidebar:
        st.markdown(f"### {u['full_name']}")
        role = "Admin" if u["role"] == "admin" else "Öğretmen"
        cls  = "ba" if u["role"] == "admin" else "bt"
        st.markdown(f'<span class="badge {cls}">{role}</span>', unsafe_allow_html=True)
        st.markdown("---")
        st.caption(f"DB: `{Path(DB_PATH).name}`")
        st.caption("OmegaClass v4 · Omni-Brain")
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
    <p>Müfredat ve Kullanıcı Yönetimi &nbsp;·&nbsp;
       <b>{u['full_name']}</b> <span class="badge ba">ADMIN</span></p>
    </div>""", unsafe_allow_html=True)

    db = _conn()
    t1, t2 = st.tabs(["📚 Dersler & Kazanımlar", "👥 Kullanıcılar"])

    with t1:
        st.info("Kazanım veritabanı yönetimi (Geliştirme aşamasında).")
    with t2:
        users_df = pd.read_sql("SELECT id,username,role,full_name FROM users ORDER BY role,username", db)
        st.dataframe(users_df, hide_index=True, use_container_width=True)
    db.close()

# ════════════════════════════════════════════════════════════
#  ÖĞRETMEN PANELİ
# ════════════════════════════════════════════════════════════
def page_teacher() -> None:
    u   = st.session_state.user
    tid = u["id"]

    st.markdown(f"""
    <div class="hero"><h1>🧠 OmegaClass 360°</h1>
    <p>Dijital Eğitim Fakültesi ve Analiz Paneli &nbsp;·&nbsp;
       <b>{u['full_name']}</b> <span class="badge bt">ÖĞRETMEN</span></p>
    </div>""", unsafe_allow_html=True)

    db = _conn()
    t1, t2, t3 = st.tabs([
        "👩‍🏫 Sınıf Yönetimi",
        "🏛️ 360° Gözlem & Analiz",
        "📚 Akademik Sınav Verisi (Opsiyonel)",
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
            del_st = st.selectbox("Silinecek Öğrenci", ["— seçin —"] + sts["name"].tolist(), key="t_stdel")
            if st.button("🗑️ Sil", key="t_stdelb"):
                if del_st != "— seçin —":
                    del_id = int(sts[sts["name"] == del_st]["id"].values[0])
                    db.execute("DELETE FROM students WHERE id=? AND teacher_id=?", (del_id, tid))
                    db.commit(); st.success(f"'{del_st}' silindi."); st.rerun()

    # ── Akademik Kazanım Logları (Opsiyonel) ─────────────────
    with t3:
        st.info("Eğer öğrencinin somut sınav/kazanım hataları varsa buradan girebilirsiniz. Girilen veriler 360° analizde otomatik kullanılır.")
        if sts.empty:
            st.warning("Öğrenci yok.")
        else:
            ak_st = st.selectbox("Öğrenci", sts["name"].tolist(), key="t_akst")
            ak_sid = int(sts[sts["name"] == ak_st]["id"].values[0])
            ak_grade = sts[sts["name"] == ak_st]["grade"].values[0]
            
            subs = pd.read_sql("SELECT id,name FROM subjects ORDER BY name", db)
            ak_sub = st.selectbox("Ders", subs["name"].tolist(), key="t_aksub")
            ak_subid = int(subs[subs["name"] == ak_sub]["id"].values[0])
            
            outs = pd.read_sql(
                "SELECT id,code,text FROM outcomes WHERE subject_id=? AND grade=? ORDER BY code",
                db, params=(ak_subid, ak_grade)
            )
            
            if not outs.empty:
                labels = (outs["code"] + " — " + outs["text"]).tolist()
                ak_out = st.selectbox("Kazanım", labels, key="t_akout")
                ak_outid = int(outs.iloc[labels.index(ak_out)]["id"])
                ak_notes = st.text_area("Hata Metni / Öğretmen Notu", key="t_aknotes")
                if st.button("💾 Kaydet", key="t_aksave"):
                    db.execute("""
                        INSERT INTO academic_logs
                        (teacher_id,student_id,subject_id,outcome_id,notes)
                        VALUES(?,?,?,?,?)
                    """, (tid, ak_sid, ak_subid, ak_outid, ak_notes))
                    db.commit(); st.success("Kaydedildi.")
            else:
                st.warning("Bu derse ait kazanım bulunamadı.")

            st.markdown("---")
            ak_logs = pd.read_sql("""
                SELECT al.id, al.log_date, s.name ders, o.code kazanim, al.notes notlar
                FROM academic_logs al
                JOIN subjects s ON s.id = al.subject_id
                JOIN outcomes o ON o.id = al.outcome_id
                WHERE al.student_id=? AND al.teacher_id=?
                ORDER BY al.log_date DESC
            """, db, params=(ak_sid, tid))
            if not ak_logs.empty:
                st.dataframe(ak_logs, hide_index=True)
                del_ak = st.number_input("Silinecek Log ID", 0, step=1, key="t_dakid")
                if st.button("🗑️ Sil", key="btn_del_ak"):
                    db.execute("DELETE FROM academic_logs WHERE id=? AND teacher_id=?", (int(del_ak), tid))
                    db.commit(); st.rerun()

    # ── 360° Dijital Eğitim Fakültesi (ANA PANEL) ────────────
    with t2:
        if sts.empty:
            st.info("Lütfen önce sınıf yönetimi sekmesinden öğrenci ekleyin."); db.close(); return

        st.markdown("### 🔍 Öğrenci Seçimi")
        sel_st    = st.selectbox("Analiz Edilecek Öğrenci", sts["name"].tolist(), key="t_arch")
        sel_sid   = int(sts[sts["name"] == sel_st]["id"].values[0])
        sel_grade = sts[sts["name"] == sel_st]["grade"].values[0]

        st.markdown("---")
        st.caption("Sınıf içinde gözlemlediğiniz durumları sol panelden işaretleyin. Sağ panelde 'Analiz Et' butonuna basın.")

        c1, c2 = st.columns([1, 1])

        with c1:
            st.markdown("### 📋 Fakülte Gözlem Sözlüğü")
            # Sözlükteki maddeleri kategorilerine göre grupla ve şık menüler oluştur
            kategoriler = {}
            for k, v in SYMPTOM_TAXONOMY.items():
                cat = v.get("kategori", "Diğer")
                if cat not in kategoriler:
                    kategoriler[cat] = {}
                kategoriler[cat][k] = v

            secilen_maddeler = []
            for cat, maddeler in kategoriler.items():
                with st.expander(f"📁 {cat.replace('_', ' ')}"):
                    for k, v in maddeler.items():
                        # Öğretmen sadece saf gözlem metnini okuyacak ve seçecek
                        if st.checkbox(v["ogretmen_metni"], key=f"chk_{k}"):
                            secilen_maddeler.append((k, v))

        with c2:
            st.markdown("### 🧠 Konsey Kararı ve ZPD Reçetesi")
            if st.button("🚀 Seçilen Gözlemleri Analiz Et", type="primary", use_container_width=True):
                if not secilen_maddeler:
                    st.warning("Lütfen sol panelden en az bir gözlem seçin.")
                else:
                    with st.spinner("Fakülte profesörleri veriyi inceliyor (Bandura, Sweller, Piaget, Goleman)..."):
                        
                        # 1. ACİL DURUM (RAM) RADARI
                        acil_durumlar = [v for k, v in secilen_maddeler if v.get("aciliyet") == "ACİL" or v.get("RAM_Riski") == True]
                        if acil_durumlar:
                            st.error("🚨 DİKKAT: ACİL MÜDAHALE VEYA UZMAN YÖNLENDİRMESİ GEREKEN DURUM TESPİT EDİLDİ!")
                            for acil in acil_durumlar:
                                uyari = acil.get("akademik_uyari", "Özel eğitim veya PDR uzmanı değerlendirmesi önerilir.")
                                st.warning(f"**Kritik Sinyal:** {uyari}")

                        # 2. VERİ KÖPRÜSÜ (Sadece Saf Gözlem Motora Gider)
                        davranislar = []
                        for k, v in secilen_maddeler:
                            davranislar.append(BehaviorRecord(
                                boyut=v.get("kategori", "sosyal_davranis"),
                                yogunluk=5, # Ekrandan seçilenleri en yüksek ciddiyette işleme al
                                metin=v["ogretmen_metni"],
                                ders=""
                            ))

                        # Veritabanındaki eski "akademik başarısızlık" loglarını da hafızaya ekle (Eğer varsa)
                        kazanim_kayitlari = []
                        ak_logs_db = pd.read_sql("""
                            SELECT s.name ders, o.code kazanim, o.text kazanim_metin, al.notes notlar
                            FROM academic_logs al
                            JOIN subjects s ON s.id = al.subject_id
                            JOIN outcomes o ON o.id = al.outcome_id
                            WHERE al.student_id=? AND al.teacher_id=?
                        """, db, params=(sel_sid, tid))

                        if not ak_logs_db.empty:
                            for idx, row in ak_logs_db.iterrows():
                                kazanim_kayitlari.append(OutcomeRecord(
                                    kod=row.get("kazanim", "Bilinmiyor"),
                                    metin=row.get("kazanim_metin", ""),
                                    ders=row.get("ders", ""),
                                    basarili=False, 
                                    hata_metni=row.get("notlar", ""),
                                    tekrar_sayisi=1
                                ))

                        # 3. OMNİ-BEYNİ ÇALIŞTIR
                        brain = PedagogyBrain()
                        veri = StudentInput(
                            ad=sel_st,
                            sinif=sel_grade,
                            kazanimlar=kazanim_kayitlari,
                            davranislar=davranislar
                        )
                        rapor = brain.analyze_student(veri)

                        # 4. ANA RAPORU BAS
                        st.success("Tüm veriler akademik literatürle başarıyla çaprazlandı.")
                        st.markdown(str(rapor))

                        # 5. FAKÜLTE'NİN DERİN ANALİZLERİNİ GÖSTER (Motora girmeden sadece UI'da)
                        st.markdown("---")
                        st.markdown("#### 🏛️ Üniversite Kürsülerinin Çapraz Değerlendirmeleri")
                        for k, v in secilen_maddeler:
                            with st.expander(f"🔍 {v['ogretmen_metni'][:45]}..."):
                                for kursu, analiz in v.get("fakulte_analizi", {}).items():
                                    st.markdown(f"- **{kursu.replace('_', ' ')}:** {analiz}")

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
