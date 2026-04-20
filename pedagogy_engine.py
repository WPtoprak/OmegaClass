"""
╔══════════════════════════════════════════════════════════════════╗
║  PedagogyEngine v4                                               ║
║  Kural Tabanlı Uzman Sistem (Rule-Based Expert System)           ║
║  Sweller · Piaget · Vygotsky · Bandura · Goleman · Bloom         ║
║                                                                  ║
║  KULLANIM (app.py içinde):                                       ║
║                                                                  ║
║    from pedagogy_engine import PedagogyEngine                    ║
║                                                                  ║
║    engine = PedagogyEngine(                                      ║
║        student_name  = "Ali Veli",                               ║
║        grade         = "4",                                      ║
║        academic_logs = ak_df,   # pandas DataFrame               ║
║        social_logs   = so_df,   # pandas DataFrame               ║
║    )                                                             ║
║    report_md = engine.generate_report()                          ║
║    st.markdown(report_md, unsafe_allow_html=True)                ║
╚══════════════════════════════════════════════════════════════════╝

DataFrame sütunları:

  academic_logs  → subject (str), outcome (str), symptom_texts (str, pipe-ayrılmış),
                   notes (str), log_date (str)

  social_logs    → dimension (str), symptom (str), theory_tag (str),
                   intensity (int 1-5), notes (str), log_date (str)
"""

from __future__ import annotations

import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import date
from typing import Any

# ── isteğe bağlı pandas import ─────────────────────────────────
try:
    import pandas as pd
    _HAS_PANDAS = True
except ImportError:
    _HAS_PANDAS = False


# ════════════════════════════════════════════════════════════════
#  VERİ YAPILARI
# ════════════════════════════════════════════════════════════════

@dataclass
class Diagnosis:
    """Bir kural tarafından tetiklenen teşhis kaydı."""
    theory:      str           # Kuram adı
    label:       str           # Kısa teşhis etiketi
    evidence:    list[str]     # Tetikleyici kanıtlar
    severity:    int           # 1-5 (1=hafif, 5=kritik)
    domain:      str           # "cognitive" | "social" | "environmental"


@dataclass
class Strategy:
    """Bir teşhise bağlı pedagojik strateji."""
    title:       str
    steps:       list[str]
    theory_base: str
    priority:    int           # 1=en yüksek öncelik


@dataclass
class EngineResult:
    """Motor çıktısının tüm bölümlerini taşır."""
    diagnoses:   list[Diagnosis] = field(default_factory=list)
    strategies:  list[Strategy]  = field(default_factory=list)
    zpd_hints:   list[str]       = field(default_factory=list)
    virtue_notes: list[str]      = field(default_factory=list)
    cross_notes:  list[str]      = field(default_factory=list)
    score_table:  dict[str, int] = field(default_factory=dict)


# ════════════════════════════════════════════════════════════════
#  KURAL VE ANAHTAR KELİME SÖZLÜKLERI
# ════════════════════════════════════════════════════════════════

# ── Bilişsel yük tetikleyicileri (Sweller) ──────────────────────
_SWELLER_TRIGGERS: dict[str, list[str]] = {
    "short_term_memory": [
        "kısa süreli bellek", "kısa süreli bellekte", "yönergeleri tutamıyor",
        "bellekte tutamıyor", "hemen unutuyor", "hızlı unutuyor",
        "aşama takibini yitiriyor", "adımları karıştırıyor",
    ],
    "cognitive_overload": [
        "bilişsel aşırı yük", "aşırı yük", "çok adımlı", "eş zamanlı",
        "dikkat dağınıklığı", "odak kaybı", "görevde kalamıyor",
        "işlem hatası", "aşama hatası", "sırasını karıştırıyor",
    ],
    "procedural_error": [
        "işlem hatası", "prosedür hatası", "basamakları hatalı",
        "sırayı yanlış", "hatalı sıralıyor", "tersine uyguluyor",
    ],
    "transfer_failure": [
        "transfer edemiyor", "başka bağlamda kullanamıyor",
        "yeni duruma uygulayamıyor", "bağlam değişince yapamıyor",
    ],
}

# ── Piaget şema tetikleyicileri ─────────────────────────────────
_PIAGET_TRIGGERS: dict[str, list[str]] = {
    "schema_mismatch": [
        "şema uyumsuzluğu", "mevcut bilgisine bağlayamıyor",
        "yeni kavramı entegre edemiyor", "şemaya yerleştiremiyor",
        "kavramı anlayamıyor", "kavram karışıklığı",
    ],
    "abstraction_gap": [
        "soyutu somutlaştıramıyor", "soyut kavramı anlamıyor",
        "somut modelle ilişkilendiremiyor", "sembolik temsil",
        "soyutlama güçlüğü", "somut işlemsel",
    ],
    "metacognitive_blind": [
        "ne bilmediğini bilmiyor", "farkında değil",
        "metakognitif", "öz-izleme yok", "kör nokta",
        "boşluğunu görmüyor", "eksikliğini fark etmiyor",
    ],
    "logical_reasoning": [
        "neden-sonuç kuramıyor", "mantıksal bağ kuramıyor",
        "çıkarım yapamıyor", "ilişki kuramıyor",
        "gözlem ile çıkarım", "mantıksal düşünce",
    ],
}

# ── Bandura öz-yeterlilik tetikleyicileri ──────────────────────
_BANDURA_TRIGGERS: dict[str, list[str]] = {
    "low_self_efficacy": [
        "ağlıyor", "kaçınıyor", "görev almıyor", "reddediyor",
        "pes ediyor", "vazgeçiyor", "istemiyorum diyor",
        "düşük öz-yeterlilik", "yapamam diyor", "ben beceremem",
        "hata korkusu", "hata yapmaktan korkuyor",
    ],
    "external_attribution": [
        "şansa bağlıyor", "dışsal atıf", "benim değil diyor",
        "çabama değil", "kaderim bu diyor", "şansım yok",
        "başarısını şansa yüklüyor",
    ],
    "avoidance_pattern": [
        "görevden kaçıyor", "katılmıyor", "sınıfa gelmek istemiyor",
        "oturmak istemiyor", "cevap vermiyor", "görmezden geliyor",
        "pasif kalıyor", "geri çekiliyor",
    ],
    "learned_helplessness": [
        "öğrenilmiş çaresizlik", "her zaman böyleyim diyor",
        "değişmez diyor", "zaten yapamam", "hiç beceremedim",
    ],
}

# ── Goleman duygusal düzenleme tetikleyicileri ──────────────────
_GOLEMAN_TRIGGERS: dict[str, list[str]] = {
    "anger_regulation": [
        "öfke patlaması", "ani öfke", "bağırıyor", "kızıyor",
        "saldırgan", "kavga ediyor", "kırıyor döküyor",
        "frustrasyon", "sinirli",
    ],
    "anxiety_block": [
        "kaygı", "anksiyete", "sınav kaygısı", "zihinsel blok",
        "donan kalıyor", "cevap veremiyor", "tutuyor",
        "elleri titriyor", "ağlamak üzere",
    ],
    "feedback_rejection": [
        "geri bildirimi reddediyor", "kişisel saldırı", "alınıyor",
        "eleştiriye tahammül yok", "küsüyor", "iletişimi kesiyor",
    ],
    "impulse_control": [
        "dürtü kontrolü", "sabırsız", "sıra bekleyemiyor",
        "anında tepki veriyor", "önce düşünmeden",
        "bekleme güçlüğü", "bekleyemiyor",
    ],
}

# ── Vygotsky ZPD tetikleyicileri ────────────────────────────────
_VYGOTSKY_TRIGGERS: dict[str, list[str]] = {
    "social_isolation": [
        "yalnız çalışma ısrarı", "işbirliğini reddediyor",
        "grup çalışmasından kaçıyor", "arkadaşlarla çalışmıyor",
        "sosyal öğrenmeden kaçınıyor",
    ],
    "peer_exclusion": [
        "dışlanıyor", "dışlıyor", "kabul görmüyor",
        "akranlardan uzak", "yalnız oturuyor",
        "grup içinde yok sayılıyor",
    ],
    "scaffolding_need": [
        "destekle yapabiliyor", "yardımla tamamlıyor",
        "ipucuyla çözüyor", "rehberlik gerekiyor",
        "tek başına yapamıyor ama", "iskele gerekiyor",
    ],
}

# ── Maarif Modeli Erdem-Değer-Eylem tetikleyicileri ─────────────
_VIRTUE_TRIGGERS: dict[str, list[str]] = {
    "sabır": [
        "sabırsız", "bekleyemiyor", "anında istiyor",
        "erteleyemiyor", "çabuk bıkıyor",
    ],
    "sorumluluk": [
        "ödev yapmıyor", "görevi kabul etmiyor", "sorumluluk almıyor",
        "göreve gelmiyor", "unutuyor", "umursamıyor",
    ],
    "saygı": [
        "saygısız", "kesmek istiyor", "arkadaşını dinlemiyor",
        "öğretmene karşı geliyor", "lakap takıyor",
    ],
    "dürüstlük": [
        "hata gizliyor", "kopya çekiyor", "yalan söylüyor",
        "örtbas ediyor", "inkar ediyor",
    ],
    "empati": [
        "empati yok", "başkasını düşünmüyor", "paylaşmıyor",
        "başkasının duygusunu fark etmiyor", "bencil",
    ],
    "öz_disiplin": [
        "dürtü kontrolü", "kurala uymuyor", "disiplin sorunu",
        "sınır tanımıyor", "düzensiz",
    ],
}

# ── Çevresel risk tetikleyicileri ───────────────────────────────
_ENV_TRIGGERS: dict[str, list[str]] = {
    "sleep_issue": [
        "uyku", "yorgun geliyor", "uykusuz", "gece geç yatıyor",
        "sabah uyanamıyor", "ders sırasında uyuyor",
    ],
    "nutrition": [
        "beslenme", "aç geliyor", "kahvaltı yapmıyor",
        "öğle yemeği yemiyor", "enerjisi yok",
    ],
    "screen_time": [
        "ekran süresi", "oyun bağımlılığı", "gece oyun oynuyor",
        "telefon bağımlısı", "sosyal medya",
    ],
    "family_stress": [
        "aile stresi", "ev ortamı", "aile içi çatışma",
        "boşanma", "ekonomik sorun", "ebeveyn baskısı",
    ],
    "home_support": [
        "ev desteği yok", "ödev yardımı almıyor",
        "kimse ilgilenmiyor", "tek başına", "yalnız bırakılıyor",
    ],
}

# ── Bloom taksonomisi (kazanım seviyesi eşleme) ──────────────────
_BLOOM_LEVELS: dict[str, int] = {
    # 1 = Hatırlama, 2 = Anlama, 3 = Uygulama,
    # 4 = Analiz,   5 = Sentez, 6 = Değerlendirme
    "okur": 1, "yazar": 1, "söyler": 1, "tanır": 1, "listeler": 1,
    "açıklar": 2, "tanımlar": 2, "anlar": 2, "yorumlar": 2, "ifade eder": 2,
    "uygular": 3, "kullanır": 3, "yapar": 3, "gösterir": 3, "hesaplar": 3,
    "karşılaştırır": 4, "ayırt eder": 4, "analiz eder": 4, "inceler": 4,
    "oluşturur": 5, "tasarlar": 5, "üretir": 5, "geliştirir": 5,
    "değerlendirir": 6, "savunur": 6, "eleştirir": 6, "yargılar": 6,
}


# ════════════════════════════════════════════════════════════════
#  YARDIMCI FONKSİYONLAR
# ════════════════════════════════════════════════════════════════

def _normalize(text: str) -> str:
    """Küçük harf, fazla boşluk temizle."""
    return re.sub(r"\s+", " ", str(text).lower().strip())


def _hit(text: str, keywords: list[str]) -> list[str]:
    """Metinde eşleşen anahtar kelimeleri döndür."""
    t = _normalize(text)
    return [kw for kw in keywords if kw in t]


def _any_hit(text: str, keywords: list[str]) -> bool:
    return bool(_hit(text, keywords))


def _collect_texts(logs: Any, columns: list[str]) -> str:
    """DataFrame veya list[dict]'ten metin sütunlarını birleştir."""
    parts: list[str] = []
    if _HAS_PANDAS and isinstance(logs, pd.DataFrame):
        for col in columns:
            if col in logs.columns:
                parts.extend(logs[col].fillna("").astype(str).tolist())
    elif isinstance(logs, list):
        for row in logs:
            for col in columns:
                v = row.get(col, "") if isinstance(row, dict) else ""
                parts.append(str(v))
    return " | ".join(parts)


def _rows(logs: Any) -> list[dict]:
    """DataFrame veya list[dict]'i list[dict]'e çevir."""
    if _HAS_PANDAS and isinstance(logs, pd.DataFrame):
        return logs.fillna("").to_dict(orient="records")
    return logs if isinstance(logs, list) else []


def _severity_label(s: int) -> str:
    return {1: "⬜ Düşük", 2: "🟦 Hafif", 3: "🟨 Orta",
            4: "🟧 Yüksek", 5: "🟥 Kritik"}.get(s, "—")


def _bloom_level(outcome_text: str) -> int:
    """Kazanım metnindeki fiilden Bloom seviyesini tahmin et."""
    t = _normalize(outcome_text)
    best = 1
    for verb, lvl in _BLOOM_LEVELS.items():
        if verb in t:
            best = max(best, lvl)
    return best


# ════════════════════════════════════════════════════════════════
#  PEDAGOGY ENGINE
# ════════════════════════════════════════════════════════════════

class PedagogyEngine:
    """
    Kural Tabanlı Pedagojik Uzman Sistem.

    Dışarıdan öğrenciye ait akademik ve sosyal log verilerini alır;
    çok katmanlı bir kural ağacından geçirerek 4 bölümlü Markdown
    rapor üretir.

    Parametreler
    ────────────
    student_name  : Öğrenci adı soyadı
    grade         : Sınıf düzeyi ("1" – "4")
    academic_logs : pandas DataFrame VEYA list[dict]
                    Beklenen sütunlar:
                      subject       – ders adı
                      outcome       – kazanım metni
                      symptom_texts – semptomlar (| ile ayrılmış)
                      notes         – öğretmen notu
                      log_date      – tarih
    social_logs   : pandas DataFrame VEYA list[dict]
                    Beklenen sütunlar:
                      dimension     – boyut (Bandura, Goleman vb.)
                      symptom       – semptom metni
                      theory_tag    – teorik etiket
                      intensity     – yoğunluk (1-5)
                      notes         – öğretmen notu
                      log_date      – tarih
    """

    # ── Ağırlıklı puan tablosu (kural → etki puanı) ─────────────
    _RULE_SCORES: dict[str, int] = {
        # Sweller
        "short_term_memory":     3,
        "cognitive_overload":    3,
        "procedural_error":      2,
        "transfer_failure":      2,
        # Piaget
        "schema_mismatch":       3,
        "abstraction_gap":       2,
        "metacognitive_blind":   2,
        "logical_reasoning":     2,
        # Bandura
        "low_self_efficacy":     4,
        "external_attribution":  2,
        "avoidance_pattern":     3,
        "learned_helplessness":  4,
        # Goleman
        "anger_regulation":      3,
        "anxiety_block":         3,
        "feedback_rejection":    2,
        "impulse_control":       2,
        # Vygotsky
        "social_isolation":      2,
        "peer_exclusion":        3,
        "scaffolding_need":      2,
        # Erdem-Değer
        "sabır":                 1,
        "sorumluluk":            2,
        "saygı":                 2,
        "dürüstlük":             2,
        "empati":                1,
        "öz_disiplin":           2,
        # Çevre
        "sleep_issue":           3,
        "nutrition":             2,
        "screen_time":           2,
        "family_stress":         4,
        "home_support":          3,
    }

    def __init__(
        self,
        student_name:  str,
        grade:         str,
        academic_logs: Any,
        social_logs:   Any,
    ) -> None:
        self.student_name  = student_name
        self.grade         = str(grade)
        self._ak_rows      = _rows(academic_logs)
        self._so_rows      = _rows(social_logs)
        self._result       = EngineResult()
        self._ak_text      = ""   # tüm akademik metin (flat)
        self._so_text      = ""   # tüm sosyal metin (flat)
        self._fired_rules: set[str] = set()
        self._score: dict[str, int] = Counter()

    # ════════════════════════════════════════════════════════════
    #  PUBLIC API
    # ════════════════════════════════════════════════════════════

    def generate_report(self) -> str:
        """
        Ana giriş noktası.
        Tüm kuralları çalıştırır ve 4 bölümlü Markdown raporu döndürür.
        """
        if not self._ak_rows and not self._so_rows:
            return (
                "> ⚠️ **Bu öğrenci için henüz gözlem kaydı yok.**\n\n"
                "> Bilişsel Veri Girişi ve Davranışsal Veri Girişi "
                "sekmelerinden en az birer kayıt ekleyin."
            )

        self._prepare_texts()
        self._run_all_rules()
        self._compute_scores()
        return self._build_markdown()

    # ════════════════════════════════════════════════════════════
    #  HAZIRLIK
    # ════════════════════════════════════════════════════════════

    def _prepare_texts(self) -> None:
        """Tüm log satırlarından düz metin oluştur."""
        ak_cols = ["subject", "outcome", "symptom_texts", "notes"]
        so_cols = ["dimension", "symptom", "theory_tag", "notes"]

        if _HAS_PANDAS:
            ak_df = (
                pd.DataFrame(self._ak_rows) if self._ak_rows else pd.DataFrame()
            )
            so_df = (
                pd.DataFrame(self._so_rows) if self._so_rows else pd.DataFrame()
            )
            self._ak_text = _collect_texts(ak_df, ak_cols)
            self._so_text = _collect_texts(so_df, so_cols)
        else:
            self._ak_text = _collect_texts(self._ak_rows, ak_cols)
            self._so_text = _collect_texts(self._so_rows, so_cols)

        self._all_text = self._ak_text + " " + self._so_text

    # ════════════════════════════════════════════════════════════
    #  KURAL MOTORU — tüm kurallar
    # ════════════════════════════════════════════════════════════

    def _run_all_rules(self) -> None:
        self._rule_sweller_memory()
        self._rule_sweller_overload()
        self._rule_sweller_procedural()
        self._rule_sweller_transfer()
        self._rule_piaget_schema()
        self._rule_piaget_abstraction()
        self._rule_piaget_metacognition()
        self._rule_piaget_logical()
        self._rule_bandura_self_efficacy()
        self._rule_bandura_attribution()
        self._rule_bandura_avoidance()
        self._rule_bandura_helplessness()
        self._rule_goleman_anger()
        self._rule_goleman_anxiety()
        self._rule_goleman_feedback()
        self._rule_goleman_impulse()
        self._rule_vygotsky_isolation()
        self._rule_vygotsky_peer()
        self._rule_vygotsky_scaffolding()
        self._rule_virtue_all()
        self._rule_env_all()
        # Çapraz kurallar (birden fazla alandan tetiklenir)
        self._cross_rule_overload_x_selfefficacy()
        self._cross_rule_emotion_x_cognition()
        self._cross_rule_env_x_cognition()
        self._cross_rule_social_x_learning()
        self._zpd_inference()

    # ── SWELLER ─────────────────────────────────────────────────

    def _rule_sweller_memory(self) -> None:
        hits = _hit(self._ak_text, _SWELLER_TRIGGERS["short_term_memory"])
        if hits:
            self._fire("short_term_memory")
            self._result.diagnoses.append(Diagnosis(
                theory   = "Sweller — Bilişsel Yük Kuramı",
                label    = "Kısa Süreli Bellek Kapasitesi Aşımı",
                evidence = hits,
                severity = min(2 + len(hits), 5),
                domain   = "cognitive",
            ))
            self._result.strategies.append(Strategy(
                title = "CHUNKING — Bilgiyi Mikro Parçalara Bölme",
                steps = [
                    "Her görevi **en fazla 2-3 alt adıma** ayırın; bir adım tamamlanmadan "
                    "sonrakini vermeyin.",
                    "Tahtaya veya kağıda **görsel adım listesi** asın "
                    "('1 → 2 → 3' formatında) — sözlü yönergeyi her zaman yazılı da sunun.",
                    "Tek bir çalışma kağıdında **yalnızca bir kazanım** hedefleyin; "
                    "sayfayı bilgiyle doldurmayın.",
                    "Yönergeyi verdikten 30 saniye sonra 'Peki, ilk adım ne?' diye sorun — "
                    "hafıza izini pekiştirir.",
                ],
                theory_base = "Sweller (1988) — Çalışma belleği kapasitesi 7±2 öğeyle sınırlıdır.",
                priority    = 1,
            ))

    def _rule_sweller_overload(self) -> None:
        hits = _hit(self._ak_text, _SWELLER_TRIGGERS["cognitive_overload"])
        if hits:
            self._fire("cognitive_overload")
            self._result.diagnoses.append(Diagnosis(
                theory   = "Sweller — Bilişsel Yük Kuramı",
                label    = "Bilişsel Aşırı Yüklenme (Cognitive Overload)",
                evidence = hits,
                severity = min(3 + len(hits), 5),
                domain   = "cognitive",
            ))
            self._result.strategies.append(Strategy(
                title = "MODALITY EFFECT — Çoklu Ortam İlkesi",
                steps = [
                    "Sözel anlatıma **görsel şema veya diyagram** ekleyin; "
                    "sözel + görsel kanal ayrı işlenerek yük azalır.",
                    "Ders içinde **'dinleme durakları'** koyun: 10 dakika içerik, "
                    "2 dakika sessiz düşünme.",
                    "Gereksiz süslü slayt ve animasyonları kaldırın — "
                    "her ekstra görsel element yük ekler (Coherence İlkesi).",
                    "Öğrencinin önceki bilgisini **açıkça aktive edin**: "
                    "'Geçen hafta öğrendiğimiz X'i hatırlayalım...' — "
                    "bağlantı yükü azaltır.",
                ],
                theory_base = "Sweller (2011) — Öğretimsel tasarımda dışsal bilişsel yük minimize edilmelidir.",
                priority    = 1,
            ))

    def _rule_sweller_procedural(self) -> None:
        hits = _hit(self._ak_text, _SWELLER_TRIGGERS["procedural_error"])
        if hits:
            self._fire("procedural_error")
            self._result.diagnoses.append(Diagnosis(
                theory   = "Sweller — Prosedürel Bellek",
                label    = "Prosedürel Sıra Hatası",
                evidence = hits,
                severity = 2,
                domain   = "cognitive",
            ))
            self._result.strategies.append(Strategy(
                title = "WORKED EXAMPLES — Çözülmüş Örnek Stratejisi",
                steps = [
                    "Öğrenciye önce **tamamen çözülmüş bir örnek** verin; "
                    "adım adım sesli düşünerek inceletin.",
                    "Ardından **yarı tamamlanmış örnek** verin (bazı adımlar boş) — "
                    "öğrenci boşlukları doldurun.",
                    "Son olarak **bağımsız çözüm** talep edin; "
                    "bu üçlü geçiş prosedürel belleği inşa eder.",
                    "Kontrol listesi (checklist) verin: "
                    "'Adım 1 ✓ Adım 2 ✓...' — öz-izleme geliştirir.",
                ],
                theory_base = "Sweller & Cooper (1985) — Worked examples etkisi.",
                priority    = 2,
            ))

    def _rule_sweller_transfer(self) -> None:
        hits = _hit(self._ak_text, _SWELLER_TRIGGERS["transfer_failure"])
        if hits:
            self._fire("transfer_failure")
            self._result.diagnoses.append(Diagnosis(
                theory   = "Sweller — Transfer Başarısızlığı",
                label    = "Bilgi Transferi Gerçekleşmiyor",
                evidence = hits,
                severity = 2,
                domain   = "cognitive",
            ))
            self._result.strategies.append(Strategy(
                title = "VARIED PRACTICE — Bağlam Çeşitlendirme",
                steps = [
                    "Aynı kazanımı **en az 3 farklı bağlamda** uygulayın "
                    "(farklı problem tipleri, farklı materyaller).",
                    "Yeni bağlamı sunmadan önce 'Bu neye benziyor?' diye sorun — "
                    "analoji köprüsü kurar.",
                    "Bağlamlar arası benzerlikleri ve farklılıkları **açıkça konuşun**; "
                    "transfer kendiliğinden gerçekleşmez.",
                ],
                theory_base = "Sweller (1994) — Uygulama çeşitliliği transferi güçlendirir.",
                priority    = 3,
            ))

    # ── PİAGET ──────────────────────────────────────────────────

    def _rule_piaget_schema(self) -> None:
        hits = _hit(self._ak_text, _PIAGET_TRIGGERS["schema_mismatch"])
        if hits:
            self._fire("schema_mismatch")
            self._result.diagnoses.append(Diagnosis(
                theory   = "Piaget — Bilişsel Gelişim / Şema Kuramı",
                label    = "Şema Uyumsuzluğu — Asimilasyon/Akomodasyon Dengesi Bozuk",
                evidence = hits,
                severity = min(2 + len(hits), 5),
                domain   = "cognitive",
            ))
            self._result.strategies.append(Strategy(
                title = "BRIDGING ANALOGY — Köprüleyici Analoji",
                steps = [
                    "Yeni kavramı tanıtmadan önce sorun: "
                    "'Bu sana daha önce öğrendiğin **neyi** hatırlatıyor?'",
                    "Öğrencinin verdiği yanıtı köprü olarak kullanın; "
                    "yeni bilgiyi eski şemaya **açıkça bağlayın**.",
                    "Somut → yarı-somut → soyut sıralamasını **her zaman** koruyun "
                    "(manipülatif → çizim → sembol).",
                    "Kavramı öğrettikten sonra 'Bunu kendi cümlenle anlat' deyin — "
                    "akomodasyonun gerçekleşip gerçekleşmediğini test eder.",
                ],
                theory_base = "Piaget (1952) — Asimilasyon ve akomodasyon bilişsel gelişimin motorudur.",
                priority    = 1,
            ))

    def _rule_piaget_abstraction(self) -> None:
        hits = _hit(self._ak_text, _PIAGET_TRIGGERS["abstraction_gap"])
        if hits:
            self._fire("abstraction_gap")
            self._result.diagnoses.append(Diagnosis(
                theory   = "Piaget — Somut İşlemsel Evre",
                label    = "Soyut Düşünme Güçlüğü — Somut Desteğe İhtiyaç Var",
                evidence = hits,
                severity = 2,
                domain   = "cognitive",
            ))
            self._result.strategies.append(Strategy(
                title = "CONCRETE MATERIALS — Somut Materyal Stratejisi",
                steps = [
                    "Sayı çubukları, kesir kartları, küpler gibi "
                    "**manipülatif materyaller** kullanın.",
                    "Sembolik gösterime (sayı, formül) geçişi **erteleyebilirsiniz** — "
                    "somut anlama sağlamlanmadan soyut gösterim anlamsız kalır.",
                    "Öğrencinin kendi eliyle nesneyi hareket ettirdiği "
                    "**yaparak öğrenme** fırsatları yaratın.",
                ],
                theory_base = "Piaget — Somut işlemsel dönem (7-11 yaş): soyutlama somut deneyime dayanır.",
                priority    = 2,
            ))

    def _rule_piaget_metacognition(self) -> None:
        hits = _hit(self._ak_text, _PIAGET_TRIGGERS["metacognitive_blind"])
        if hits:
            self._fire("metacognitive_blind")
            self._result.diagnoses.append(Diagnosis(
                theory   = "Piaget / Flavell — Üstbiliş (Metacognition)",
                label    = "Metakognitif Kör Nokta — Ne Bilmediğini Bilmiyor",
                evidence = hits,
                severity = 3,
                domain   = "cognitive",
            ))
            self._result.strategies.append(Strategy(
                title = "METACOGNITIVE ROUTINE — Öz-İzleme Rutini",
                steps = [
                    "Her ders başında sorun: "
                    "'Bu konudan **emin olduğun** 1 şey, **emin olmadığın** 1 şey nedir?'",
                    "'Öğrenme günlüğü' tutturun: "
                    "bugün öğrendim / anlamadım / yarın sormak istiyorum.",
                    "Öğrencinin kendi sorusunu yazmasını isteyin — "
                    "soru üretmek kavramsal boşlukları görünür kılar.",
                    "Test sonrası 'Hangi soruyu neden yanlış yaptın?' diye analiz ettirin — "
                    "yanıt 'bilmiyordum' değil, 'şunu karıştırdım' olana kadar devam edin.",
                ],
                theory_base = "Flavell (1979) — Metakognisyon: öğrenmeyi öğrenmenin temelidir.",
                priority    = 2,
            ))

    def _rule_piaget_logical(self) -> None:
        hits = _hit(self._ak_text, _PIAGET_TRIGGERS["logical_reasoning"])
        if hits:
            self._fire("logical_reasoning")
            self._result.diagnoses.append(Diagnosis(
                theory   = "Piaget — Mantıksal-Matematiksel Düşünce",
                label    = "Neden-Sonuç / Çıkarım Güçlüğü",
                evidence = hits,
                severity = 2,
                domain   = "cognitive",
            ))
            self._result.strategies.append(Strategy(
                title = "CAUSAL CHAIN — Neden-Sonuç Zinciri Görselleştirme",
                steps = [
                    "Okuma ve fen derslerinde **'Neden → Çünkü → Sonuç'** şablonu kullanın.",
                    "Öğrencinin her 'çünkü' ifadesini **cümleyle yazmasını** isteyin.",
                    "Tartışma ortamlarında 'Bunun arkasında ne var?' veya "
                    "'Başka ne olabilirdi?' sorularıyla çıkarım pratiği yaptırın.",
                ],
                theory_base = "Piaget — Somut işlemsel dönemde mantıksal düşünce somut destek gerektirir.",
                priority    = 3,
            ))

    # ── BANDURA ─────────────────────────────────────────────────

    def _rule_bandura_self_efficacy(self) -> None:
        hits = _hit(self._so_text + self._ak_text, _BANDURA_TRIGGERS["low_self_efficacy"])
        if hits:
            self._fire("low_self_efficacy")
            self._result.diagnoses.append(Diagnosis(
                theory   = "Bandura — Sosyal Öğrenme / Öz-Yeterlilik",
                label    = "Düşük Öz-Yeterlilik İnancı",
                evidence = hits,
                severity = min(3 + len(hits), 5),
                domain   = "social",
            ))
            self._result.strategies.append(Strategy(
                title = "MASTERY EXPERIENCES — Küçük Başarı Deneyimleri",
                steps = [
                    "Öğrencinin **bağımsız başarabileceği** en kolay görevi bulun; "
                    "oradan başlayın. Bu 'ilk başarı' inancın çekirdeğini oluşturur.",
                    "Övgüyü **sonuç değil süreç** odaklı yapın: "
                    "'Aferin, doğru buldun' değil → "
                    "'Aferin, ikinci adımda şunu fark edip geri döndün.'",
                    "**Akran modeli** kullanın: benzer geçmişi olan bir öğrencinin "
                    "bir problemi nasıl çözdüğünü sesli düşünerek göstermesini sağlayın.",
                    "Başarı anını **somut kayıt** altına alın: "
                    "öğrenciye başardığı görevlerin listesini verin, "
                    "günde bir kez görmesi öz-yeterliliği pekiştirir.",
                ],
                theory_base = (
                    "Bandura (1977) — Öz-yeterlilik inancının en güçlü kaynağı "
                    "doğrudan başarı deneyimidir (Mastery Experiences)."
                ),
                priority = 1,
            ))

    def _rule_bandura_attribution(self) -> None:
        hits = _hit(self._so_text, _BANDURA_TRIGGERS["external_attribution"])
        if hits:
            self._fire("external_attribution")
            self._result.diagnoses.append(Diagnosis(
                theory   = "Bandura / Weiner — Atıf Kuramı",
                label    = "Dışsal Atıf — Başarıyı Şansa Bağlıyor",
                evidence = hits,
                severity = 2,
                domain   = "social",
            ))
            self._result.strategies.append(Strategy(
                title = "ATTRIBUTION RETRAINING — Atıf Yeniden Çerçeveleme",
                steps = [
                    "Başarıdan sonra 'Bunu neden başardın?' sorusunu sorun; "
                    "'şans' cevabı gelirse 'Evet ama sen de şunu yaptın...' şeklinde "
                    "**çabayı ön plana çıkarın**.",
                    "Hata sonrası 'Bu seni ne öğretti?' sorusuyla "
                    "**büyüme zihniyeti (growth mindset)** modelleyin.",
                    "Sınıf panosu: 'Bu hafta ne denedim ve ne öğrendim?' — "
                    "çaba görünür kılındığında içsel atıf güçlenir.",
                ],
                theory_base = "Weiner (1985) / Dweck (2006) — Kontrol odağı ve büyüme zihniyeti.",
                priority    = 2,
            ))

    def _rule_bandura_avoidance(self) -> None:
        hits = _hit(self._so_text + self._ak_text, _BANDURA_TRIGGERS["avoidance_pattern"])
        if hits:
            self._fire("avoidance_pattern")
            self._result.diagnoses.append(Diagnosis(
                theory   = "Bandura — Kaçınma Döngüsü",
                label    = "Görev Kaçınma Örüntüsü",
                evidence = hits,
                severity = 3,
                domain   = "social",
            ))
            self._result.strategies.append(Strategy(
                title = "GRADUATED EXPOSURE — Kademeli Görev Maruziyeti",
                steps = [
                    "Kaçınan görevi **en kolay sürümüne** indirgeyin; "
                    "reddi imkânsızlaştıracak kadar küçültün.",
                    "Görevin ilk 5 dakikasını birlikte yapın, kalan kısmı öğrenciye bırakın — "
                    "'başlangıç etkisi' kaçınmayı kırar.",
                    "Katılım davranışını **hemen pekiştirin** "
                    "(sözel onay, puan, sembol) — katılım ödüllenince tekrarlanır.",
                ],
                theory_base = "Bandura (1986) — Pekiştirme ve kademeli maruziyet kaçınma döngüsünü kırar.",
                priority    = 2,
            ))

    def _rule_bandura_helplessness(self) -> None:
        hits = _hit(self._so_text, _BANDURA_TRIGGERS["learned_helplessness"])
        if hits:
            self._fire("learned_helplessness")
            self._result.diagnoses.append(Diagnosis(
                theory   = "Seligman / Bandura — Öğrenilmiş Çaresizlik",
                label    = "Öğrenilmiş Çaresizlik Örüntüsü",
                evidence = hits,
                severity = 5,
                domain   = "social",
            ))
            self._result.strategies.append(Strategy(
                title = "AGENCY BUILDING — Özne Hissi İnşa Etme",
                steps = [
                    "Öğrenciye **seçim hakkı** verin: 'Bu iki görevden hangisini önce yapmak istersin?' — "
                    "kontrol hissi çaresizlik döngüsünü kıran en hızlı yoldur.",
                    "Küçük bir sorumluluk alanı tanıyın: sınıf kitapçığını dağıtmak, "
                    "tahtayı silmek gibi — başarılı tamamlama öz-yetkinlik hissi verir.",
                    "**Rehber öğretmen veya psikolojik danışman sevki** değerlendirin; "
                    "öğrenilmiş çaresizlik tek başına pedagojik müdahaleyle çözülmeyebilir.",
                ],
                theory_base = "Seligman (1972) — Öğrenilmiş çaresizlik kontrol kaybı inancından kaynaklanır.",
                priority    = 1,
            ))

    # ── GOLEMAN ─────────────────────────────────────────────────

    def _rule_goleman_anger(self) -> None:
        hits = _hit(self._so_text, _GOLEMAN_TRIGGERS["anger_regulation"])
        if hits:
            self._fire("anger_regulation")
            sev = min(2 + sum(self.so_intensities_above(3)), 5)
            self._result.diagnoses.append(Diagnosis(
                theory   = "Goleman — Duygusal Zeka / Öfke Düzenlemesi",
                label    = "Öfke Düzenlemesi Güçlüğü",
                evidence = hits,
                severity = sev,
                domain   = "social",
            ))
            self._result.strategies.append(Strategy(
                title = "CO-REGULATION — Ko-Regülasyon ve Dur-Nefes-Dene",
                steps = [
                    "Öfke başlamadan **önceki belirtileri tanıyın** "
                    "(ses tonu değişimi, hızlı nefes, yüz kızarması) ve "
                    "proaktif müdahale yapın.",
                    "Sınıfın görünür yerine **'Sakinleşme Köşesi'** koyun: "
                    "öğrenci oraya gidip 3 derin nefes aldıktan sonra geri döner.",
                    "Öfke anında 'Dur-Nefes-Söyle' protokolü: "
                    "önce dur, sonra nefes al, sonra 'sinirli hissediyorum' de.",
                    "Sakin dönemde öfkenin tetikleyicilerini **öğrenciyle birlikte** "
                    "belirleyin ve alternatif tepkiler prova edin.",
                ],
                theory_base = "Goleman (1995) — Duygusal düzenleme kapasite inşası öğretilebilir.",
                priority    = 1,
            ))

    def _rule_goleman_anxiety(self) -> None:
        hits = _hit(self._so_text + self._ak_text, _GOLEMAN_TRIGGERS["anxiety_block"])
        if hits:
            self._fire("anxiety_block")
            self._result.diagnoses.append(Diagnosis(
                theory   = "Goleman — Kaygı ve Bilişsel Engel",
                label    = "Kaygı Kaynaklı Bilişsel Blok",
                evidence = hits,
                severity = 4,
                domain   = "social",
            ))
            self._result.strategies.append(Strategy(
                title = "ANXIETY REDUCTION — Kaygıyı Düşürme Stratejileri",
                steps = [
                    "Test/sınav ortamlarını **düşük riskli** yapın: "
                    "yanlış cevap not kırmaz, sadece bilgi verir.",
                    "Güvenli hata ortamı kurun: 'Bu sınıfta hata yapmak öğrenmenin parçası' "
                    "normunu tüm sınıfa öğretin ve **modelleyin** "
                    "('Ben de bazen yanılırım').",
                    "Kaygı yaratan görevi **zor dilim + kolay dilim** olarak bölün; "
                    "ilk kolay bölümle başlayın — başlangıç başarısı kaygıyı düşürür.",
                    "Kaygılı dönemlerde **fiziksel aktivite molası** ekleyin — "
                    "yürüyüş, dans, esneme, kortizol düşürür.",
                ],
                theory_base = "Goleman (1995) — Yüksek kaygı amigdala aktivasyonunu artırır, "
                              "prefrontal korteks kapasitesini düşürür.",
                priority    = 1,
            ))

    def _rule_goleman_feedback(self) -> None:
        hits = _hit(self._so_text, _GOLEMAN_TRIGGERS["feedback_rejection"])
        if hits:
            self._fire("feedback_rejection")
            self._result.diagnoses.append(Diagnosis(
                theory   = "Goleman — Kişilerarası Duygusal Zeka",
                label    = "Geri Bildirim Reddi — Kişisel Saldırı Algısı",
                evidence = hits,
                severity = 3,
                domain   = "social",
            ))
            self._result.strategies.append(Strategy(
                title = "DESCRIPTIVE FEEDBACK — Tanımlayıcı Geri Bildirim",
                steps = [
                    "Değerlendirmeyi **kişiden ayırın**: "
                    "'Sen yanlış yaptın' → 'Bu adımda farklı bir yol deneyelim'.",
                    "**SES (Specific-Example-Suggestion) formatını** kullanın: "
                    "Spesifik gözlem + somut örnek + öneri.",
                    "Geri bildirimi özel vermekten kaçının; sınıfta "
                    "'birlikte bakalım' şeklinde **normalize edin**.",
                    "Öğrenciye geri bildirimi aldıktan sonra "
                    "'Bir şey eklemek ister misin?' diye sorun — "
                    "söz hakkı verilince savunmacılık azalır.",
                ],
                theory_base = "Hattie & Timperley (2007) — Etkili geri bildirim göreve odaklanır, kişiye değil.",
                priority    = 2,
            ))

    def _rule_goleman_impulse(self) -> None:
        hits = _hit(self._so_text, _GOLEMAN_TRIGGERS["impulse_control"])
        if hits:
            self._fire("impulse_control")
            self._result.diagnoses.append(Diagnosis(
                theory   = "Goleman — Dürtü Kontrolü (EQ)",
                label    = "Dürtü Kontrolü Güçlüğü",
                evidence = hits,
                severity = 2,
                domain   = "social",
            ))
            self._result.strategies.append(Strategy(
                title = "SELF-REGULATION SCAFFOLDING — Dürtü Yönetimi İskelesi",
                steps = [
                    "Bekleme süresini **kademeli artırın**: "
                    "önce 30 saniye bekleme, sonra 1 dakika — 'sabır kası' geliştirilir.",
                    "Sıra beklerken yapacağı **alternatif bir görev** verin "
                    "(not alma, çizim yapma).",
                    "Anında tepki verdiğinde 'Bekleyebilirsin, çok güzel dayanıyorsun' "
                    "ile **süreci pekiştirin**.",
                ],
                theory_base = "Mischel (1972) — Dürtü kontrolü öğrenilebilir ve gelişebilir.",
                priority    = 3,
            ))

    # ── VYGOTSKY ────────────────────────────────────────────────

    def _rule_vygotsky_isolation(self) -> None:
        hits = _hit(self._so_text + self._ak_text, _VYGOTSKY_TRIGGERS["social_isolation"])
        if hits:
            self._fire("social_isolation")
            self._result.diagnoses.append(Diagnosis(
                theory   = "Vygotsky — Sosyal Yapılandırmacılık",
                label    = "Sosyal Öğrenmeden İzolasyon — ZPD Aktivasyonu Engelli",
                evidence = hits,
                severity = 3,
                domain   = "social",
            ))
            self._result.strategies.append(Strategy(
                title = "COOPERATIVE LEARNING — İşbirlikli Öğrenme Yapıları",
                steps = [
                    "**İkili çalışma** ile başlayın — grup büyütülmeden önce güven inşa edilir.",
                    "Düşük riskli görevler: öğrenci bir parçayı yapar, "
                    "bütünü çift tamamlar — başarı paylaşılır, risk bireysel değildir.",
                    "Rolü açıkça tanımlayın: 'Sen yazıyorsun, arkadaşın kontrol ediyor' — "
                    "belirsizlik sosyal kaygıyı artırır.",
                ],
                theory_base = "Vygotsky (1978) — Bilişsel gelişim sosyal etkileşim aracılığıyla gerçekleşir.",
                priority    = 2,
            ))

    def _rule_vygotsky_peer(self) -> None:
        hits = _hit(self._so_text, _VYGOTSKY_TRIGGERS["peer_exclusion"])
        if hits:
            self._fire("peer_exclusion")
            self._result.diagnoses.append(Diagnosis(
                theory   = "Vygotsky / Sosyal Katılım",
                label    = "Akran Dışlanması Riski",
                evidence = hits,
                severity = 4,
                domain   = "social",
            ))
            self._result.strategies.append(Strategy(
                title = "INCLUSIVE CLASSROOM — Kapsayıcı Sınıf Ortamı",
                steps = [
                    "Grup eşleştirmelerini **öğretmen belirlesin** — "
                    "öğrenci seçiminde dışlama güçlenir.",
                    "Öğrencinin güçlü olduğu bir alanda sınıf içinde "
                    "**görünür ve değerli** hissettirin (sunum, sergi, yardımcı rol).",
                    "Rehber öğretmenle koordinasyon: akran ilişkileri sorunu "
                    "sınıf içi müdahalenin ötesine geçebilir.",
                ],
                theory_base = "Vygotsky (1934) — Akran etkileşimi gelişim için vazgeçilmezdir.",
                priority    = 1,
            ))

    def _rule_vygotsky_scaffolding(self) -> None:
        hits = _hit(self._ak_text, _VYGOTSKY_TRIGGERS["scaffolding_need"])
        if hits:
            self._fire("scaffolding_need")
            self._result.diagnoses.append(Diagnosis(
                theory   = "Vygotsky — ZPD / İskele Kurma",
                label    = "İskele Desteği Gerekiyor — ZPD Aktif",
                evidence = hits,
                severity = 2,
                domain   = "cognitive",
            ))
            self._result.strategies.append(Strategy(
                title = "FADING SCAFFOLD — Azalan İskele Stratejisi",
                steps = [
                    "Görevi önce **tam destekle** birlikte yapın.",
                    "Ardından **ipucu kartlarıyla** yarı bağımsız yaptırın.",
                    "Son aşamada kartları kaldırın ve **tamamen bağımsız** uygulayın — "
                    "'fading' (solma) ile destek sistematik biçimde azaltılır.",
                    "Her aşamada 'Bunu kendi başına yapabilir misin?' sorusuyla "
                    "ZPD'nin güncel sınırını test edin.",
                ],
                theory_base = "Vygotsky (1978) — ZPD: yardımla yapılabilenin bağımsız yapılabilene dönüşme alanı.",
                priority    = 1,
            ))

    # ── ERDEM-DEĞER-EYLEM (Maarif Modeli) ───────────────────────

    def _rule_virtue_all(self) -> None:
        combined = self._so_text + " " + self._ak_text
        for virtue, keywords in _VIRTUE_TRIGGERS.items():
            hits = _hit(combined, keywords)
            if hits:
                self._fire(virtue)
                self._result.virtue_notes.append(
                    f"**{virtue.capitalize()}** boyutunda güçlük: " +
                    "; ".join(hits[:3])
                )

    # ── ÇEVRESEL RİSK ───────────────────────────────────────────

    def _rule_env_all(self) -> None:
        combined = self._so_text + " " + self._ak_text
        for risk, keywords in _ENV_TRIGGERS.items():
            hits = _hit(combined, keywords)
            if hits:
                self._fire(risk)
                sev = 4 if risk in ("family_stress", "sleep_issue", "home_support") else 2
                self._result.diagnoses.append(Diagnosis(
                    theory   = f"Bronfenbrenner — Çevresel Risk ({risk})",
                    label    = {
                        "sleep_issue":   "Uyku Düzensizliği — Bilişsel Kapasite Azalıyor",
                        "nutrition":     "Beslenme Yetersizliği — Enerji ve Konsantrasyon Bozuk",
                        "screen_time":   "Aşırı Ekran Süresi — Dikkat ve Uyku Kalitesi Etkileniyor",
                        "family_stress": "Aile/Ev Stresi — Akademik Performansa Yansıyor",
                        "home_support":  "Ev Desteği Eksikliği — Ödev ve Pratik Yetersiz",
                    }.get(risk, risk),
                    evidence = hits,
                    severity = sev,
                    domain   = "environmental",
                ))

    # ── ÇAPRAZ KURALLAR ─────────────────────────────────────────

    def _cross_rule_overload_x_selfefficacy(self) -> None:
        """Bilişsel aşırı yük + düşük öz-yeterlilik → kısır döngü."""
        if ("cognitive_overload" in self._fired_rules or
                "short_term_memory" in self._fired_rules) and \
                "low_self_efficacy" in self._fired_rules:
            self._result.cross_notes.append(
                "🔁 **KİSİR DÖNGÜ — Bilişsel Yük ↔ Öz-Yeterlilik Çöküşü**\n\n"
                "Sweller + Bandura birlikte aktif: Öğrenci bilişsel aşırı yük nedeniyle "
                "başarısız oluyor → başarısızlık öz-yeterlilik inancını eroduyor → "
                "düşen inanç, bir sonraki görevden kaçınmaya yol açıyor → "
                "kaçınma, bilişsel pratiği azaltıyor → yük bir sonraki görevde "
                "daha erken aşılıyor. **Bu döngü kırılmadan tek başına akademik "
                "müdahale kalıcı sonuç vermez.** Önce öz-yeterlilik inşası, "
                "ardından bilişsel destekler uygulanmalıdır."
            )

    def _cross_rule_emotion_x_cognition(self) -> None:
        """Kaygı/öfke + bilişsel güçlük → duygusal blok teşhisi."""
        has_emotion = any(r in self._fired_rules for r in
                          ["anger_regulation", "anxiety_block"])
        has_cog     = any(r in self._fired_rules for r in
                          ["cognitive_overload", "schema_mismatch", "short_term_memory"])
        if has_emotion and has_cog:
            self._result.cross_notes.append(
                "⚡ **DUYGUSAL BLOK → BİLİŞSEL ERİŞİM ENGELİ**\n\n"
                "Goleman + Sweller/Piaget birlikte aktif: Kaygı veya öfke "
                "prefrontal korteks kapasitesini geçici olarak düşürmektedir. "
                "Görünürde 'akademik başarısızlık' olan problem, özünde "
                "**duygusal kökenlidir**. Güvenli ortam oluşturulmadan yapılan "
                "bilişsel müdahaleler işe yaramayacaktır. "
                "**Önce duygusal güvenlik, sonra bilişsel öğretim.**"
            )

    def _cross_rule_env_x_cognition(self) -> None:
        """Çevresel stres + bilişsel yük → fizyolojik kısıtlama."""
        has_env = any(r in self._fired_rules for r in
                      ["sleep_issue", "family_stress", "nutrition"])
        has_cog = any(r in self._fired_rules for r in
                      ["cognitive_overload", "short_term_memory"])
        if has_env and has_cog:
            self._result.cross_notes.append(
                "🏠 **ÇEVRESEL STRES → BİYOLOJİK BİLİŞSEL KISITLAMA**\n\n"
                "Bronfenbrenner + Sweller birlikte aktif: Uyku yetersizliği, "
                "beslenme eksikliği veya aile stresi, çocuğun çalışma belleği "
                "kapasitesini **fizyolojik düzeyde** azaltmaktadır. Öğrenci "
                "okula zaten tükenmiş gelebilir. Çevresel faktörler ele "
                "alınmadan sınıf içi bilişsel müdahaleler yalnızca geçici "
                "iyileşme sağlayacaktır."
            )

    def _cross_rule_social_x_learning(self) -> None:
        """Sosyal izolasyon + ZPD → öğrenme fırsatı kaybı."""
        if ("social_isolation" in self._fired_rules or
                "peer_exclusion" in self._fired_rules) and \
                ("low_self_efficacy" in self._fired_rules or
                 "schema_mismatch" in self._fired_rules):
            self._result.cross_notes.append(
                "🚪 **SOSYAL ÖĞRENME KAPISI KAPALI (Vygotsky + Bandura)**\n\n"
                "Öğrenci hem ZPD'den (akran aracılığıyla doğal iskele kurma) "
                "hem de Bandura'nın gözlemsel öğrenmesinden yararlanamamaktadır. "
                "Akranları izleyerek 'o yapabiliyorsa ben de yapabilirim' inancı "
                "gelişemiyor; aynı zamanda grup içindeki bilişsel çatışma ortamı "
                "şema gelişimini besleyemiyor."
            )

    # ── ZPD ÇIKARIMI ────────────────────────────────────────────

    def _zpd_inference(self) -> None:
        """
        Kazanımları Bloom taksonomisine göre sırala;
        öğrencinin takıldığı noktayı ve ZPD hedefini belirle.
        """
        if not self._ak_rows:
            return

        # Kazanım → Bloom seviyesi
        outcome_levels: list[tuple[str, int, str]] = []
        for row in self._ak_rows:
            outcome = str(row.get("outcome", ""))
            subject = str(row.get("subject", ""))
            lvl     = _bloom_level(outcome)
            outcome_levels.append((subject, lvl, outcome))

        if not outcome_levels:
            return

        # En düşük Bloom seviyesindeki takılma noktası
        outcome_levels.sort(key=lambda x: x[1])
        lowest = outcome_levels[0]
        highest_possible = min(lowest[1] + 1, 6)

        bloom_labels = {
            1: "Hatırlama (Recall)",
            2: "Anlama (Comprehension)",
            3: "Uygulama (Application)",
            4: "Analiz (Analysis)",
            5: "Sentez (Synthesis)",
            6: "Değerlendirme (Evaluation)",
        }

        self._result.zpd_hints.append(
            f"**Mevcut Gelişim Düzeyi (ADL):** "
            f"Bloom Düzey {lowest[1]} — {bloom_labels.get(lowest[1],'?')} "
            f"→ *{lowest[2][:80]}*"
        )
        self._result.zpd_hints.append(
            f"**ZPD Hedefi (Potansiyel Düzey):** "
            f"Bloom Düzey {highest_possible} — {bloom_labels.get(highest_possible,'?')}"
        )

        # Derslere göre güçlük dağılımı
        subj_counter: Counter = Counter(r[0] for r in outcome_levels)
        most_troubled = subj_counter.most_common(2)
        for subj, cnt in most_troubled:
            self._result.zpd_hints.append(
                f"📌 **{subj}** dersinde {cnt} farklı kazanımda gözlem kaydedildi "
                f"— bu ders ZPD müdahalesinin odak alanı olmalıdır."
            )

    # ════════════════════════════════════════════════════════════
    #  PUAN HESAPLAMA
    # ════════════════════════════════════════════════════════════

    def _compute_scores(self) -> None:
        for rule in self._fired_rules:
            self._score["toplam"] += self._RULE_SCORES.get(rule, 1)

        cog_rules = {"short_term_memory", "cognitive_overload", "procedural_error",
                     "transfer_failure", "schema_mismatch", "abstraction_gap",
                     "metacognitive_blind", "logical_reasoning", "scaffolding_need"}
        soc_rules = {"low_self_efficacy", "external_attribution", "avoidance_pattern",
                     "learned_helplessness", "anger_regulation", "anxiety_block",
                     "feedback_rejection", "impulse_control", "social_isolation",
                     "peer_exclusion"}
        env_rules = {"sleep_issue", "nutrition", "screen_time", "family_stress", "home_support"}

        self._score["bilişsel"]   = sum(self._RULE_SCORES.get(r, 1)
                                        for r in self._fired_rules if r in cog_rules)
        self._score["sosyal"]     = sum(self._RULE_SCORES.get(r, 1)
                                        for r in self._fired_rules if r in soc_rules)
        self._score["çevresel"]   = sum(self._RULE_SCORES.get(r, 1)
                                        for r in self._fired_rules if r in env_rules)

        self._result.score_table = dict(self._score)

    # ── yardımcı ────────────────────────────────────────────────

    def _fire(self, rule: str) -> None:
        self._fired_rules.add(rule)

    def so_intensities_above(self, threshold: int) -> list[int]:
        return [
            int(r.get("intensity", 0))
            for r in self._so_rows
            if int(r.get("intensity", 0)) >= threshold
        ]

    # ════════════════════════════════════════════════════════════
    #  MARKDOWN RAPOR ÜRETİCİ
    # ════════════════════════════════════════════════════════════

    def _build_markdown(self) -> str:
        r   = self._result
        sc  = r.score_table
        today = date.today().isoformat()
        ak_n  = len(self._ak_rows)
        so_n  = len(self._so_rows)

        # Genel risk seviyesi
        total = sc.get("toplam", 0)
        if total >= 30:
            risk_label = "🔴 **KRİTİK** — Çok boyutlu ve acil müdahale gerekiyor"
        elif total >= 18:
            risk_label = "🟠 **YÜKSEK** — Öncelikli müdahale planı uygulanmalı"
        elif total >= 8:
            risk_label = "🟡 **ORTA** — İzleme ve destekleyici müdahale öneriliyor"
        else:
            risk_label = "🟢 **DÜŞÜK** — Önleyici destek yeterli"

        # Skor çubuğu
        def bar(score: int, mx: int = 20) -> str:
            filled = min(int(score / mx * 12), 12)
            return "█" * filled + "░" * (12 - filled) + f"  `{score}`"

        # Teşhis tablosu
        diag_md = ""
        if r.diagnoses:
            # Önem sırasına göre sırala
            sorted_diags = sorted(r.diagnoses, key=lambda d: d.severity, reverse=True)
            for d in sorted_diags:
                diag_md += (
                    f"\n| {_severity_label(d.severity)} | **{d.label}** "
                    f"| *{d.theory}* |"
                )

        # Strateji listesi
        strat_md = ""
        sorted_strats = sorted(r.strategies, key=lambda s: s.priority)
        for i, s in enumerate(sorted_strats, 1):
            steps_str = "\n".join(f"    {j}. {step}" for j, step in enumerate(s.steps, 1))
            strat_md += (
                f"\n#### Taktik {i}: {s.title}\n"
                f"*Teorik Dayanak: {s.theory_base}*\n\n"
                f"{steps_str}\n"
            )

        # Erdem notları
        virtue_md = ""
        if r.virtue_notes:
            virtue_md = "\n".join(f"- {n}" for n in r.virtue_notes)
        else:
            virtue_md = "*Bu alanda gözlem kaydedilmedi.*"

        # ZPD notları
        zpd_md = ""
        if r.zpd_hints:
            zpd_md = "\n".join(f"- {h}" for h in r.zpd_hints)
        else:
            zpd_md = "*Kazanım verisi henüz ZPD analizi için yetersiz.*"

        # Çapraz notlar
        cross_md = ""
        if r.cross_notes:
            cross_md = "\n\n---\n\n".join(r.cross_notes)
        else:
            cross_md = "*Mevcut verilerle sistemik bir çapraz örüntü tespit edilmedi.*"

        # Öncelik tavsiyesi
        c_score = sc.get("bilişsel", 0)
        s_score = sc.get("sosyal", 0)
        e_score = sc.get("çevresel", 0)
        if e_score > c_score and e_score > s_score:
            priority_note = (
                "🏠 **Çevresel faktörler** baskın — aile iletişimi ve "
                "refah desteği diğer müdahalelerden önce gelmelidir."
            )
        elif s_score >= c_score:
            priority_note = (
                "💛 **Sosyal-duygusal** alan baskın — güvenli öğrenme "
                "ortamı kurulmadan bilişsel müdahaleler sınırlı kalır."
            )
        else:
            priority_note = (
                "📚 **Bilişsel** alan baskın — öğretimsel tasarım ve "
                "bilişsel destek müdahaleleri öncelikli alındığında "
                "sosyal destek paralel uygulanmalıdır."
            )

        # ── Final Markdown ───────────────────────────────────────
        md = f"""
---
## 🧠 OmegaClass — Pedagojik Analiz Raporu
**Öğrenci:** {self.student_name} &nbsp;|&nbsp; **Sınıf:** {self.grade} &nbsp;|&nbsp; **Tarih:** {today}
**Kayıt:** {ak_n} akademik · {so_n} sosyal gözlem &nbsp;|&nbsp; **Genel Risk:** {risk_label}

---

### 🎯 1 — Bilişsel Harita ve Öğrenme Çıktıları Analizi
*(Sweller — Bilişsel Yük Kuramı · Piaget — Şema ve Bilişsel Gelişim · Bloom Taksonomisi)*

#### Ağırlıklı Puan Tablosu
| Alan | Skor Çubuğu |
|------|-------------|
| Bilişsel Yük & Şema | {bar(c_score)} |
| Sosyal & Duygusal   | {bar(s_score)} |
| Çevresel Risk       | {bar(e_score)} |

#### Tespit Edilen Bilişsel Teşhisler
| Şiddet | Teşhis | Teorik Kaynak |
|--------|--------|---------------|
{diag_md if diag_md else "| — | Belirgin bilişsel teşhis bulunamadı | — |"}

#### ZPD Profili (Vygotsky — Yakınsal Gelişim Alanı)
{zpd_md}

---

### 🧠 2 — Sosyo-Duygusal Profil (Erdem-Değer-Eylem Çerçevesi)
*(Bandura — Öz-Yeterlilik · Goleman — Duygusal Zeka · Maarif Modeli)*

#### Sosyal-Duygusal Teşhisler
Yukarıdaki teşhis tablosunda `social` ve `environmental` etiketli satırlar bu alanı kapsar.

#### Erdem-Değer Boyutu
{virtue_md}

---

### 🔗 3 — Çapraz Sentez (Akademik × Sosyal Kök Neden Analizi)
{cross_md}

---

### 🛠️ 4 — Stratejik Müdahale Planı
*(Hemen uygulanabilir pedagojik adımlar — öncelik sırasıyla)*

{priority_note}
{strat_md if strat_md else "*Yeterli veri biriktiğinde stratejiler otomatik üretilecektir.*"}

---

<details>
<summary>📊 Ham Puan Detayı (Geliştirici Görünümü)</summary>

```
Toplam kural skoru  : {sc.get('toplam', 0)}
Bilişsel alan       : {c_score}
Sosyal-duygusal     : {s_score}
Çevresel risk       : {e_score}
Tetiklenen kurallar : {', '.join(sorted(self._fired_rules)) or '—'}
```
</details>

---
*Bu rapor OmegaClass **PedagogyEngine v4** tarafından üretilmiştir.
Dış API kullanılmamıştır. Tüm analizler Python kural motoru ile hesaplanmıştır.*
"""
        return md.strip()


# ════════════════════════════════════════════════════════════════
#  ENTEGRASYON SNIPPET'İ  (app.py içinde nasıl kullanılır)
# ════════════════════════════════════════════════════════════════
#
#  1. Bu dosyayı app.py ile aynı klasöre koyun.
#
#  2. app.py dosyasının en üstüne ekleyin:
#       from pedagogy_engine import PedagogyEngine
#
#  3. "Arşiv & Analiz" sekmesindeki analiz butonunu şöyle değiştirin:
#
#   ─────────────────────────────────────────────────────────────
#   if st.button("🔬 PedagogyEngine Analizi Başlat",
#                use_container_width=True, type="primary"):
#
#       with st.spinner("Kural motoru işliyor..."):
#
#           # Akademik logları çek (mevcut SQL sorgunuz)
#           ak_df = pd.read_sql("""
#               SELECT al.log_date,
#                      s.name  AS subject,
#                      o.text  AS outcome,
#                      GROUP_CONCAT(asy.text, ' | ') AS symptom_texts,
#                      al.notes
#               FROM   academic_logs al
#               JOIN   subjects s  ON s.id  = al.subject_id
#               JOIN   outcomes  o  ON o.id  = al.outcome_id
#               LEFT JOIN academic_symptoms asy
#                      ON asy.id IN (
#                             SELECT value FROM json_each('[' ||
#                             REPLACE(al.symptom_ids,',',' ,') || ']')
#                         )
#               WHERE  al.student_id = ? AND al.teacher_id = ?
#               GROUP  BY al.id
#               ORDER  BY al.log_date DESC
#           """, conn, params=(sel_sid, tid))
#
#           # Sosyal logları çek
#           so_df = pd.read_sql("""
#               SELECT sl.log_date,
#                      ss.dimension,
#                      ss.text      AS symptom,
#                      ss.theory_tag,
#                      sl.intensity,
#                      sl.notes
#               FROM   social_logs sl
#               JOIN   social_symptoms ss ON ss.id = sl.symptom_id
#               WHERE  sl.student_id = ? AND sl.teacher_id = ?
#               ORDER  BY sl.log_date DESC
#           """, conn, params=(sel_sid, tid))
#
#           engine = PedagogyEngine(
#               student_name  = sel_st,
#               grade         = sel_grade,
#               academic_logs = ak_df,
#               social_logs   = so_df,
#           )
#           report_md = engine.generate_report()
#
#       st.markdown(report_md, unsafe_allow_html=True)
#   ─────────────────────────────────────────────────────────────
#
#  NOT: Mevcut app.py'deki PedagogyEngine sınıfını tamamen silin ve
#       bu dosyayı import edin. SQL sorgusu yukarıdaki gibi
#       `symptom_texts` sütununu da içerdiğinden emin olun.
#
# ════════════════════════════════════════════════════════════════
