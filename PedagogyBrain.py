"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PedagogyBrain.py                                                            ║
║  Karar Destek Motoru (Decision Support Engine) - REKTİFİYE EDİLMİŞ SÜRÜM     ║
║  Sürüm: 2.0 (Yoğunluk Çarpanı ve Anti-Halüsinasyon Korumalı)                 ║
║                                                                              ║
║  Teorik Çerçeve:                                                             ║
║    Bloom (1956/2001) · Sweller (1988) · Piaget (1952) · Vygotsky (1978)      ║
║    Bandura (1977/1986) · Dweck (2006) · Gardner (1983) · Goleman (1995)      ║
║    Bronfenbrenner (1979) · Flavell (1979) · Seligman (1972)                  ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

from __future__ import annotations

import re
import math
from dataclasses import dataclass, field
from collections import Counter
from typing import Any

# ══════════════════════════════════════════════════════════════════════════════
#  VERİ GİRİŞ YAPILARI
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class OutcomeRecord:
    kod:           str
    metin:         str
    ders:          str
    basarili:      bool
    hata_metni:    str   = ""
    tekrar_sayisi: int   = 1

@dataclass
class BehaviorRecord:
    boyut:    str
    metin:    str
    yogunluk: int  = 3
    ders:     str  = ""

@dataclass
class StudentInput:
    ad:          str
    sinif:       str
    kazanimlar:  list[OutcomeRecord]  = field(default_factory=list)
    davranislar: list[BehaviorRecord] = field(default_factory=list)


# ══════════════════════════════════════════════════════════════════════════════
#  ÇIKTI VERİ YAPILARI
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class BloomAnalysis:
    seviye:    int
    etiket:    str
    kazanim:   str
    ders:      str
    kod:       str
    eksik_mi:  bool

@dataclass
class CognitiveLoad:
    yuk_skoru:    float
    seviye:       str
    tetikleyenler: list[str]
    kaynaklar:    dict[str, int]

@dataclass
class AttitudeDiagnosis:
    blok_turu:    str
    kök_neden:   str
    oz_yeterlilik_skoru: float
    buyume_zihniyeti:    float
    kaçınma_örüntüsü:   bool
    öğrenilmiş_çaresizlik: bool
    kanit:       list[str]

@dataclass
class TalentRadar:
    zeka_puanlari:   dict[str, float]
    en_güçlü:        list[str]
    gizli_yetenek:   str
    ilgi_sinyalleri: list[str]

@dataclass
class ZPDPrescription:
    mevcut_duzey:   str
    zpd_hedefi:     str
    adimlar:        list[dict]

@dataclass
class EduCheckupReport:
    ogrenci_adi:      str
    sinif:            str
    tarih:            str
    bloom_analizi:    list[BloomAnalysis]
    bilişsel_yuk:     CognitiveLoad
    tutum_analizi:    AttitudeDiagnosis
    yetenek_radari:   TalentRadar
    zpd_recetesi:     ZPDPrescription
    genel_risk_skoru: float
    oncelik_sirasi:   list[str]
    ozet_yorum:       str

    def __str__(self) -> str:
        return _report_to_str(self)


# ══════════════════════════════════════════════════════════════════════════════
#  TEMEL KURAL/SÖZLÜK KATMANI (Yanlış Alarm Korumalı)
# ══════════════════════════════════════════════════════════════════════════════

BLOOM_VERB_MAP: dict[int, list[str]] = {
    1: ["tanır", "adlandırır", "listeler", "söyler", "okur", "yazar", "sayar", "belirtir", "gösterir", "tekrar eder", "hatırlar", "tanımlar", "isimlendirir"],
    2: ["açıklar", "anlar", "yorumlar", "özetler", "ifade eder", "karşılaştırır", "sınıflandırır", "örneklendirir", "tahmin eder", "seçer", "ayırt eder", "ilişkilendirir"],
    3: ["uygular", "kullanır", "yapar", "hesaplar", "çözer", "oluşturur", "gerçekleştirir", "üretir", "dener", "gösterir", "işler"],
    4: ["analiz eder", "inceler", "karşılaştırır", "ayrıştırır", "sorgular", "sınandırır", "test eder", "sorgular", "kanıtlar", "ayırt eder", "bağ kurar", "çıkarım yapar"],
    5: ["değerlendirir", "savunur", "eleştirir", "yargılar", "tartışır", "önceliklendirir", "seçer", "destekler", "karara varır"],
    6: ["tasarlar", "üretir", "geliştirir", "inşa eder", "planlar", "formüle eder", "kurguları", "icat eder", "yaratır", "compose eder"],
}

BLOOM_LABELS: dict[int, str] = {
    1: "Hatırlama (L1)", 2: "Anlama (L2)", 3: "Uygulama (L3)",
    4: "Analiz (L4)", 5: "Değerlendirme (L5)", 6: "Yaratma (L6)",
}

SWELLER_RULES: dict[str, dict] = {
    "bellek_aşımı": {
        "keywords": ["bellekte tutamıyor", "kısa süreli bellek", "hemen unutuyor", "hızlı unutuyor", "aşama takibini yitiriyor", "adımları karıştırıyor", "yönergeleri unutuyor", "söyleneni unutuyor"],
        "yuk_puani": 3.5,
        "aciklama": "Çalışma belleği kapasitesi aşılmış; yeni bilgiler uzun süreli belleğe aktarılamıyor.",
    },
    "çoklu_görev_zorluğu": {
        "keywords": ["çok adımlı", "eş zamanlı", "birden fazla kural", "karmaşık işlem", "aşama hatası", "adım atlıyor", "sırayı karıştırıyor"],
        "yuk_puani": 2.8,
        "aciklama": "Eş zamanlı birden fazla bilişsel öğe yönetilemez hale gelmiş.",
    },
    "dikkat_dağınıklığı": {
        "keywords": ["dikkat dağınıklığı", "odak kaybı", "görevde kalamıyor", "dikkati dağılıyor", "konsantrasyon sorunu", "derste uçuyor"],
        "yuk_puani": 2.0,
        "aciklama": "Yabancı bilişsel yük (extraneous load) dikkati temel öğrenmeden uzaklaştırıyor.",
    },
    "transfer_yetersizliği": {
        "keywords": ["transfer edemiyor", "başka bağlamda kullanamıyor", "yeni duruma uygulayamıyor", "ezber yapıyor ama uygulanamıyor", "bağlam değişince yapamıyor"],
        "yuk_puani": 2.5,
        "aciklama": "Germane load (verimli yük) yetersiz; şema otomasyonu gerçekleşmemiş, bilgi izole kalmış.",
    },
    "prosedürel_hata": {
        "keywords": ["işlem hatası", "prosedür hatası", "hatalı sıralıyor", "basamakları ters uyguluyor", "formülü yanlış biliyor"],
        "yuk_puani": 1.8,
        "aciklama": "Prosedürel bellek henüz otomasyona ulaşmamış; her adım aktif çalışma belleği gerektiriyor.",
    },
}

PIAGET_RULES: dict[str, dict] = {
    "şema_uyumsuzluğu": {
        "keywords": ["mevcut bilgisine bağlayamıyor", "yeni kavramı entegre edemiyor", "şema uyumsuzluğu", "kavram karışıklığı", "kavramı anlayamıyor", "eski bilgiyle çelişiyor"],
        "aciklama": "Yeni kavram mevcut bilişsel şemaya yerleştirilemiyor; asimilasyon başarısız.",
    },
    "soyutlama_güçlüğü": {
        "keywords": ["soyutu somutlaştıramıyor", "soyut kavramı anlamıyor", "sembolik gösterim", "soyutlama güçlüğü", "somut modelle ilişkilendiremiyor"],
        "aciklama": "Öğrenci somut işlemsel dönemde; soyut sembolik temsile henüz geçiş yapamıyor.",
    },
    "metakognitif_körlük": {
        "keywords": ["ne bilmediğini bilmiyor", "boşluğunu fark etmiyor", "yanlış emin", "hatalı güven", "öz-izleme yok", "kör nokta", "eksikliğini görmüyor"],
        "aciklama": "Metakognitif farkındalık gelişmemiş; öğrenci kendi bilgi boşluklarını tespit edemiyor.",
    },
    "mantıksal_düşünce_güçlüğü": {
        "keywords": ["neden-sonuç kuramıyor", "çıkarım yapamıyor", "ilişki kuramıyor", "gözlem ile çıkarım", "mantıksal bağ kuramıyor"],
        "aciklama": "Formal işlemsel düşünce (11+ yaş) henüz gelişmemiş; soyut mantık yürütme kısıtlı.",
    },
}

BANDURA_RULES: dict[str, dict] = {
    "düşük_öz_yeterlilik": {
        "keywords": ["yapamam diyor", "ben beceremem", "hata korkusu", "ağlıyor", "ağlamaklı", "kaçınıyor", "parmak kaldırmıyor", "görev almıyor", "reddediyor", "pes ediyor", "istemiyorum", "zor diyor", "beceremiyorum"],
        "oz_yeterlilik_düşürücü": 2.5,
        "kaçınma": True,
        "aciklama": "Düşük öz-yeterlilik inancı akademik katılımı engellemiş; başarısızlık beklentisi öğrenmeyi bloke ediyor.",
    },
    "dışsal_atıf": {
        "keywords": ["şansa bağlıyor", "benim değil diyor", "kader", "zaten hep böyle", "öğretmen zor soruyor", "kötü şansım var", "başarısını şansa yüklüyor"],
        "oz_yeterlilik_düşürücü": 1.5,
        "kaçınma": False,
        "aciklama": "Dışsal atıf örüntüsü; başarı ve başarısızlık kontrol dışı nedenlere bağlanıyor.",
    },
    "kaçınma_döngüsü": {
        "keywords": ["göreve gelmiyor", "sınıfa gelmek istemiyor", "oturmak istemiyor", "pasif kalıyor", "geri çekiliyor", "katılmıyor", "cevap vermiyor", "kapanmak"],
        "oz_yeterlilik_düşürücü": 3.0,
        "kaçınma": True,
        "aciklama": "Kaçınma döngüsü yerleşmiş; görev talepleri korku tetikleyici olarak işleniyor.",
    },
}

DWECK_RULES: dict[str, dict] = {
    "sabit_zihniyet_göstergesi": {
        "keywords": ["zaten böyleyim", "değişmez", "yapamam hiç", "aptalım", "zekâm yok", "matematik kafam yok", "dilim tutmuyor", "kabiliyetsiz"],
        "buyume_zihniyeti_düşürücü": 3.0,
        "aciklama": "Sabit zihniyet (fixed mindset) inancı; zekâ ve yetenek değiştirilemez görülüyor.",
    },
    "çaba_düşmanlığı": {
        "keywords": ["çalışmak istemiyor", "uğraşmak istemez", "hemen bırakıyor", "zorlanınca bırakıyor", "çabuk pes ediyor"],
        "buyume_zihniyeti_düşürücü": 2.0,
        "aciklama": "Çabayı değersiz gören tutum; 'çalışmak aptallar içindir' sabit zihniyet koruyucu mekanizması.",
    },
    "başarı_odaklı_büyüme": {
        "keywords": ["tekrar deniyor", "hata sonrası devam ediyor", "sormaktan çekinmiyor", "farklı yol deniyor", "yardım istiyor"],
        "buyume_zihniyeti_artırıcı": 2.5,
        "aciklama": "Büyüme zihniyeti göstergesi; başarısızlığı öğrenme fırsatı olarak algılama.",
    },
}

GOLEMAN_RULES: dict[str, dict] = {
    "öfke_düzenleme_güçlüğü": {
        "keywords": ["öfke patlaması", "bağırıyor", "kızıyor", "saldırgan", "kavga ediyor", "kırıyor döküyor", "sinirli", "tepki veriyor", "patladı"],
        "olumsuz_etki": 2.5,
        "aciklama": "Öfke düzenlemesinde yetersizlik; prefrontal korteks amigdala aktivasyonunu bastıramıyor.",
    },
    "kaygı_bloku": {
        "keywords": ["kaygılı", "anksiyete", "sınav kaygısı", "zihinsel blok", "donan kalıyor", "elleri titriyor", "korku", "endişeli", "karnı ağrıyor"],
        "olumsuz_etki": 3.0,
        "aciklama": "Kaygı kaynaklı bilişsel blok; yüksek kortizol çalışma belleği kapasitesini düşürüyor.",
    },
    "frustrasyon_tolerans_düşüklüğü": {
        "keywords": ["hemen bıkıyor", "çabuk sinirlenip bırakıyor", "toleranssız", "sabırsız", "bekleme güçlüğü"],
        "olumsuz_etki": 1.5,
        "aciklama": "Frustrasyon toleransı düşük; zorlukla karşılaşmada düzenleyici kapasite yetersiz.",
    },
}

BRONFENBRENNER_RULES: dict[str, dict] = {
    "uyku_riski": {
        "keywords": ["uyku düzensizliği", "yorgun geliyor", "uykusuz", "gece geç yatıyor", "sabah uyanamıyor", "derste uyuyor", "uyku yetersizliği"],
        "etki_puani": 3.5,
        "aciklama": "Uyku yetersizliği çalışma belleği kapasitesini ve duygusal düzenlemeyi fizyolojik düzeyde bozuyor.",
    },
    "beslenme_riski": {
        "keywords": ["beslenme yetersizliği", "aç geliyor", "kahvaltı yapmıyor", "enerjisi yok", "öğle yemiyor"],
        "etki_puani": 2.5,
        "aciklama": "Beslenme yetersizliği dikkat ve bilişsel kapasite üzerinde doğrudan biyolojik etki.",
    },
    "aile_stresi": {
        "keywords": ["aile stresi", "aile içi çatışma", "boşanma", "ekonomik sorun", "ebeveyn baskısı", "ev kargaşası", "evde kavga"],
        "etki_puani": 4.0,
        "aciklama": "Aile/ev stresi kortizol seviyesini kronik biçimde artırır; öğrenme kapasitesini sistematik olarak azaltır.",
    },
    "ev_desteği_eksikliği": {
        "keywords": ["ev desteği yok", "ödev yardımı almıyor", "yalnız bırakılıyor"],
        "etki_puani": 3.0,
        "aciklama": "Ev desteği eksikliği prosedürel pratiği ve öz-düzenleme gelişimini olumsuz etkiliyor.",
    },
    "dijital_risk": {
        "keywords": ["aşırı ekran süresi", "oyun bağımlılığı", "gece oyun", "telefon bağımlısı"],
        "etki_puani": 2.0,
        "aciklama": "Aşırı ekran maruziyeti uyku kalitesini ve geciktirme yeteneğini bozuyor.",
    },
}

# Gardner Sinyalleri (Kısaltıldı, mantığı korundu)
GARDNER_SIGNALS = {
    "sözel_dilsel": {"ders_sinyalleri": ["Türkçe", "İngilizce"], "davranış_sinyalleri": ["hikâye anlatıyor", "çok konuşuyor", "okumayı seviyor", "yazmayı seviyor", "kelime oyunları", "şiir yazıyor", "anlatıcı"], "kazanım_fiilleri": ["okur", "yazar", "anlatır"], "aciklama": "Sözel-Dilsel Zeka: Dil yapılarına ve anlatıma güçlü yönelim."},
    "mantıksal_matematiksel": {"ders_sinyalleri": ["Matematik", "Fen Bilimleri"], "davranış_sinyalleri": ["sayıları seviyor", "puzzle çözüyor", "neden diye soruyor", "örüntü fark ediyor", "zihinden"], "kazanım_fiilleri": ["hesaplar", "çözer", "sınıflandırır"], "aciklama": "Mantıksal-Matematiksel Zeka: Sayısal örüntü ve sistematik düşünce."},
    "uzamsal_görsel": {"ders_sinyalleri": ["Görsel Sanatlar", "Matematik"], "davranış_sinyalleri": ["çizim yapıyor", "görsellerle anlıyor", "harita okuyor", "yapı kuruyor", "üç boyutlu düşünüyor", "lego seviyor"], "kazanım_fiilleri": ["çizer", "modeller", "tasarlar"], "aciklama": "Uzamsal-Görsel Zeka: Mekan ve görsel temsil becerisi öne çıkıyor."},
    "müzikal_ritmik": {"ders_sinyalleri": ["Müzik"], "davranış_sinyalleri": ["ritim tutuyor", "şarkı söylüyor", "melodi hatırlıyor", "sese duyarlı"], "kazanım_fiilleri": ["söyler", "ritim tutar", "dinler"], "aciklama": "Müzikal-Ritmik Zeka: Ses, ritim ve melodi duyarlılığı."},
    "bedensel_kinestetik": {"ders_sinyalleri": ["Beden Eğitimi"], "davranış_sinyalleri": ["hareket ediyor", "dokunarak öğreniyor", "yaparak öğreniyor", "aktif olmak istiyor", "spor seviyor", "sallanıyor"], "kazanım_fiilleri": ["uygular", "yapar", "gösterir"], "aciklama": "Bedensel-Kinestetik Zeka: Hareket ve dokunsal öğrenme güçlü."},
    "kişilerarası": {"ders_sinyalleri": ["Sosyal Bilgiler", "Hayat Bilgisi"], "davranış_sinyalleri": ["lider oluyor", "arkadaşlarını dinliyor", "empati kuruyor", "grup çalışmasını seviyor", "sosyal"], "kazanım_fiilleri": ["işbirliği yapar", "paylaşır"], "aciklama": "Kişilerarası Zeka: Sosyal anlayış ve empati kapasitesi yüksek."},
    "içsel_öze_dönük": {"ders_sinyalleri": [], "davranış_sinyalleri": ["yalnız çalışmayı seviyor", "kendi kendine öğreniyor", "günlük tutuyor", "içe dönük", "duygularını anlıyor"], "kazanım_fiilleri": ["değerlendirir", "sorgular"], "aciklama": "İçsel-Öze Dönük Zeka: Güçlü öz-farkındalık ve iç dünya."},
    "doğa_çevre": {"ders_sinyalleri": ["Fen Bilimleri", "Hayat Bilgisi"], "davranış_sinyalleri": ["bitkileri seviyor", "hayvanları seviyor", "doğayı gözlemliyor", "koleksiyon yapıyor"], "kazanım_fiilleri": ["gözlemler", "inceler"], "aciklama": "Doğacı Zeka: Canlı sistemlere ve doğal örüntülere duyarlılık."},
}

# Vygotsky Müdahale Kütüphanesi
ZPD_INTERVENTION_LIBRARY = {
    "chunking": {
        "başlık": "Chunking — Bilgiyi Mikro Parçalara Bölme",
        "koşul_kuralları": ["bellek_aşımı", "çoklu_görev_zorluğu"],
        "adımlar": ["Görevi 2–3 alt adıma bölün.", "Tahtaya görsel adım listesi asın.", "Çalışma kağıdında yalnızca tek kazanım koyun."],
        "kuram": "Sweller (1988) — Çalışma belleği kapasitesi korunur.",
        "sure_dakika": 10,
    },
    "mastery_experiences": {
        "başlık": "Mastery Experiences — Küçük Başarı Deneyimleri",
        "koşul_kuralları": ["düşük_öz_yeterlilik", "kaçınma_döngüsü"],
        "adımlar": ["Öğrencinin bağımsız başarabileceği en kolay görevi bulun ve oradan başlayın.", "Övgüyü sonuç değil süreç odaklı verin.", "Başarı anını somut kayıt altına alın."],
        "kuram": "Bandura (1977) — Mastery experiences öz-yeterlilik inancının en güçlü kaynağıdır.",
        "sure_dakika": 20,
    },
    "emotion_regulation": {
        "başlık": "Co-Regulation — Duygusal Ko-Regülasyon",
        "koşul_kuralları": ["öfke_düzenleme_güçlüğü", "kaygı_bloku"],
        "adımlar": ["Öfke/kaygı başlamadan önceki fiziksel belirtileri tanıyın ve proaktif müdahale yapın.", "'Dur-Nefes-Söyle' protokolü.", "Güvenli hata ortamı normunu modelleyerek öğretin."],
        "kuram": "Goleman (1995) — Duygusal düzenleme kapasite inşası öğretilebilir.",
        "sure_dakika": 10,
    },
    "graduated_exposure": {
        "başlık": "Graduated Exposure — Kademeli Görev Maruziyeti",
        "koşul_kuralları": ["kaçınma_döngüsü", "kaygı_bloku"],
        "adımlar": ["Kaçılan görevi mümkün olan en küçük sürümüne indirgeyin.", "Görevin ilk 5 dakikasını birlikte yapın.", "Katılım davranışını hemen pekiştirin."],
        "kuram": "Bandura (1986) — Kademeli maruziyet kaçınma döngüsünü kırar.",
        "sure_dakika": 15,
    },
    "growth_mindset_reframe": {
        "başlık": "Growth Mindset Reframe — Büyüme Zihniyeti Yeniden Çerçeveleme",
        "koşul_kuralları": ["sabit_zihniyet_göstergesi", "dışsal_atıf"],
        "adımlar": ["Başarı sonrası 'Bunu neden başardın?' sorusunda çabayı öne çıkarın.", "Hata sonrası 'Bu sana ne öğretti?' sorusuyla büyüme zihniyeti modelleyin.", "Sınıf panosunda 'Bu hafta ne denedim?' sorusunu görünür kılın."],
        "kuram": "Dweck (2006) — Büyüme zihniyeti çaba ve stratejiyi ön plana çıkarır.",
        "sure_dakika": 10,
    },
}

# ══════════════════════════════════════════════════════════════════════════════
#  YARDIMCI FONKSİYONLAR
# ══════════════════════════════════════════════════════════════════════════════

def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", str(text).lower().strip())

def _keyword_hits(text: str, keywords: list[str]) -> list[str]:
    t = _norm(text)
    return [kw for kw in keywords if kw in t]

def _bloom_level_from_text(text: str) -> int:
    t = _norm(text)
    best = 1
    for level, verbs in BLOOM_VERB_MAP.items():
        for verb in verbs:
            if verb in t:
                best = max(best, level)
    return best

def _clamp(value: float, lo: float = 0.0, hi: float = 10.0) -> float:
    return max(lo, min(hi, value))

def _report_to_str(report: "EduCheckupReport") -> str:
    lines: list[str] = []

    def h(level: int, text: str) -> None:
        lines.append("\n" + "#" * level + " " + text)

    def p(text: str) -> None:
        lines.append(text)

    h(1, f"📋 EduCheckup Raporu — {report.ogrenci_adi}")
    p(f"Sınıf: {report.sinif}  |  Tarih: {report.tarih}")
    p(f"Genel Risk Skoru: **{report.genel_risk_skoru:.1f}/100**")
    p(f"Öncelik Sırası: {' → '.join(report.oncelik_sirasi)}")
    p("")
    p(f"> {report.ozet_yorum}")

    # ── Bölüm 1: Bloom & Bilişsel Yük ────────────────────────────
    h(2, "🎯 1 — Bilişsel & Akademik Boyut")

    h(3, "Bloom Taksonomisi Analizi")
    eksikler = [b for b in report.bloom_analizi if b.eksik_mi]
    başarılılar = [b for b in report.bloom_analizi if not b.eksik_mi]

    if eksikler:
        p("**Tespit Edilen Eksiklikler:**")
        for b in sorted(eksikler, key=lambda x: x.seviye):
            p(f"- `{b.kod}` [{b.ders}] → **{b.etiket}** — *{b.kazanim[:80]}...*")
    else:
        p("Belirgin Bloom seviyesi eksikliği tespit edilmedi.")

    h(3, "Bilişsel Yük Değerlendirmesi (Sweller)")
    yk = report.bilişsel_yuk
    p(f"Yük Skoru: **{yk.yuk_skoru:.1f}/10** — Seviye: **{yk.seviye}**")
    if yk.tetikleyenler:
        p("Tetikleyenler:")
        for t in yk.tetikleyenler:
            p(f"  - {t}")

    # ── Bölüm 2: Tutum Analizi ─────────────────────────────────
    h(2, "🧠 2 — Duyuşsal & Tutum Boyutu")
    ta = report.tutum_analizi
    p(f"Blok Türü: **{ta.blok_turu}**")
    p(f"Kök Neden: {ta.kök_neden}")
    p(f"Öz-Yeterlilik Skoru: **{ta.oz_yeterlilik_skoru:.1f}/10** |  Büyüme Zihniyeti: **{ta.buyume_zihniyeti:.1f}/10**")
    p(f"Kaçınma Örüntüsü: {'✅ Var' if ta.kaçınma_örüntüsü else '❌ Yok'}  |  Öğrenilmiş Çaresizlik: {'✅ Var' if ta.öğrenilmiş_çaresizlik else '❌ Yok'}")
    if ta.kanit:
        p("Kanıtlar:")
        for k in ta.kanit[:5]:
            p(f"  - {k}")

    # ── Bölüm 3: Yetenek Radarı ───────────────────────────────
    h(2, "🌟 3 — Yetenek & İlgi Radarı (Gardner)")
    yr = report.yetenek_radari
    p("**Zeka Profili:**")
    sorted_z = sorted(yr.zeka_puanlari.items(), key=lambda x: x[1], reverse=True)
    for zeka, puan in sorted_z:
        bar = "█" * int(puan) + "░" * (10 - int(puan))
        p(f"  {zeka:<25} {bar}  {puan:.1f}")
    p(f"\n**En Güçlü Alanlar:** {', '.join(yr.en_güçlü)}")
    p(f"\n**Gizli Yetenek Sinyali:** _{yr.gizli_yetenek}_")

    # ── Bölüm 4: ZPD Reçetesi ─────────────────────────────────
    h(2, "🛠️ 4 — Vygotsky ZPD Müdahale Reçetesi")
    zp = report.zpd_recetesi
    p(f"**Mevcut Düzey:** {zp.mevcut_duzey}")
    p(f"**ZPD Hedefi:** {zp.zpd_hedefi}")
    p("\n**Pedagojik Adımlar:**")
    for i, adim in enumerate(zp.adimlar, 1):
        p(f"\n#### Adım {i}: {adim['baslik']}")
        p(f"*Kuram: {adim['kuram']}  |  Önerilen Süre: {adim.get('sure_dakika','?')} dk*")
        for j, s in enumerate(adim["aciklama"], 1):
            p(f"  {j}. {s}")

    return "\n".join(lines)


# ══════════════════════════════════════════════════════════════════════════════
#  PEDAGOGY BRAIN — ANA MOTOR
# ══════════════════════════════════════════════════════════════════════════════

class PedagogyBrain:

    def analyze_student(self, data: StudentInput) -> EduCheckupReport:
        from datetime import date as _date

        bloom_list = self._analyze_bloom(data.kazanimlar)
        cog_load = self._analyze_cognitive_load(bloom_list, data.kazanimlar, data.davranislar)
        tutum = self._analyze_attitude(data.kazanimlar, data.davranislar)
        radar = self._analyze_talent(data.kazanimlar, data.davranislar)
        zpd = self._build_zpd_prescription(bloom_list, cog_load, tutum, data.sinif)
        risk_score = self._compute_risk(cog_load, tutum)
        priority = self._compute_priority(cog_load, tutum, data.davranislar)
        ozet = self._generate_summary(data, bloom_list, cog_load, tutum, radar, risk_score)

        return EduCheckupReport(
            ogrenci_adi      = data.ad,
            sinif            = data.sinif,
            tarih            = _date.today().isoformat(),
            bloom_analizi    = bloom_list,
            bilişsel_yuk     = cog_load,
            tutum_analizi    = tutum,
            yetenek_radari   = radar,
            zpd_recetesi     = zpd,
            genel_risk_skoru = risk_score,
            oncelik_sirasi   = priority,
            ozet_yorum       = ozet,
        )

    def _analyze_bloom(self, records: list[OutcomeRecord]) -> list[BloomAnalysis]:
        results: list[BloomAnalysis] = []
        for r in records:
            lvl = _bloom_level_from_text(r.metin)
            results.append(BloomAnalysis(
                seviye   = lvl, etiket = BLOOM_LABELS.get(lvl, "Bilinmiyor"),
                kazanim  = r.metin, ders = r.ders, kod = r.kod, eksik_mi = not r.basarili,
            ))
        return results

    def _analyze_cognitive_load(self, bloom_list: list[BloomAnalysis], records: list[OutcomeRecord], davranislar: list[BehaviorRecord]) -> CognitiveLoad:
        raw_score   = 0.0
        tetikleyenler = []
        kaynak_sayac = Counter()

        def add_tetikleyen(kural_adi, kural):
            baslik = f"[{kural_adi}]"
            if not any(t.startswith(baslik) for t in tetikleyenler):
                tetikleyenler.append(f"{baslik} {kural['aciklama'][:80]}...")

        # 1. Sweller Kuralları
        for kural_adi, kural in SWELLER_RULES.items():
            # Kazanımları kontrol et
            for r in records:
                hits = _keyword_hits(r.metin + " " + r.hata_metni, kural["keywords"])
                if hits:
                    raw_score += kural["yuk_puani"] * math.log1p(len(hits))
                    kaynak_sayac[kural_adi] += len(hits)
                    add_tetikleyen(kural_adi, kural)
            # Davranışları kontrol et (Yoğunluk Çarpanı Devrede!)
            for b in davranislar:
                hits = _keyword_hits(b.metin, kural["keywords"])
                if hits:
                    çarpan = b.yogunluk / 3.0
                    raw_score += kural["yuk_puani"] * math.log1p(len(hits)) * çarpan
                    kaynak_sayac[kural_adi] += len(hits)
                    add_tetikleyen(kural_adi, kural)

        # 2. Piaget Kuralları
        for kural_adi, kural in PIAGET_RULES.items():
            for r in records:
                hits = _keyword_hits(r.metin + " " + r.hata_metni, kural["keywords"])
                if hits:
                    raw_score += 1.2 * math.log1p(len(hits))
                    kaynak_sayac[kural_adi] += len(hits)
                    add_tetikleyen(kural_adi, kural)
            for b in davranislar:
                hits = _keyword_hits(b.metin, kural["keywords"])
                if hits:
                    çarpan = b.yogunluk / 3.0
                    raw_score += 1.2 * math.log1p(len(hits)) * çarpan
                    kaynak_sayac[kural_adi] += len(hits)
                    add_tetikleyen(kural_adi, kural)

        # Bloom çarpanı
        eksikler = [b for b in bloom_list if b.eksik_mi]
        if eksikler:
            basarisiz_bloom_ortalama = sum(b.seviye for b in eksikler) / len(eksikler)
            raw_score += basarisiz_bloom_ortalama * 0.6

        # Tekrar sayısı katkısı
        toplam_tekrar = sum(r.tekrar_sayisi for r in records if not r.basarili)
        raw_score += math.log1p(toplam_tekrar) * 0.5

        yuk_skoru = _clamp(raw_score, 0, 10)

        if yuk_skoru >= 7.5: seviye = "🔴 KRİTİK"
        elif yuk_skoru >= 5.0: seviye = "🟠 YÜKSEK"
        elif yuk_skoru >= 2.5: seviye = "🟡 ORTA"
        else: seviye = "🟢 DÜŞÜK"

        return CognitiveLoad(yuk_skoru=round(yuk_skoru, 2), seviye=seviye, tetikleyenler=tetikleyenler[:6], kaynaklar=dict(kaynak_sayac))

    def _analyze_attitude(self, kazanimlar: list[OutcomeRecord], davranislar: list[BehaviorRecord]) -> AttitudeDiagnosis:
        oz_yeterlilik = 10.0
        buyume_z      = 7.0
        kaçınma       = False
        ogrenilmis_c  = False
        kanit_listesi = []
        blok_skoru    = {"psikolojik": 0.0, "bilişsel": 0.0, "çevresel": 0.0}

        def add_evidence(kanit):
            if kanit not in kanit_listesi:
                kanit_listesi.append(kanit)

        # ── Bandura (Yoğunluk Çarpanı İle) ──
        for kural_adi, kural in BANDURA_RULES.items():
            for b in davranislar:
                hits = _keyword_hits(b.metin, kural["keywords"])
                if hits:
                    çarpan = b.yogunluk / 3.0
                    oz_yeterlilik -= kural["oz_yeterlilik_düşürücü"] * math.log1p(len(hits)) * çarpan
                    if kural.get("kaçınma"):
                        kaçınma = True
                        blok_skoru["psikolojik"] += 3.0 * çarpan
                    else:
                        blok_skoru["psikolojik"] += 1.5 * çarpan
                    add_evidence(f"[Bandura/{kural_adi}] {kural['aciklama'][:70]}")
                    if kural_adi == "kaçınma_döngüsü":
                        oz_yeterlilik -= 1.5 * çarpan

        # ── Dweck (Yoğunluk Çarpanı İle) ──
        for kural_adi, kural in DWECK_RULES.items():
            for b in davranislar:
                hits = _keyword_hits(b.metin, kural["keywords"])
                if hits:
                    çarpan = b.yogunluk / 3.0
                    if "düşürücü" in kural:
                        buyume_z -= kural["buyume_zihniyeti_düşürücü"] * math.log1p(len(hits)) * çarpan
                        blok_skoru["psikolojik"] += kural["buyume_zihniyeti_düşürücü"] * çarpan
                        add_evidence(f"[Dweck/{kural_adi}] {kural['aciklama'][:70]}")
                    if "artırıcı" in kural:
                        buyume_z += kural.get("buyume_zihniyeti_artırıcı", 0) * çarpan

        # ── Goleman (Yoğunluk Çarpanı İle) ──
        for kural_adi, kural in GOLEMAN_RULES.items():
            for b in davranislar:
                hits = _keyword_hits(b.metin, kural["keywords"])
                if hits:
                    çarpan = b.yogunluk / 3.0
                    oz_yeterlilik -= kural["olumsuz_etki"] * 0.5 * math.log1p(len(hits)) * çarpan
                    blok_skoru["psikolojik"] += kural["olumsuz_etki"] * 0.7 * çarpan
                    add_evidence(f"[Goleman/{kural_adi}] {kural['aciklama'][:70]}")

        # ── Piaget ──
        for kural_adi, kural in PIAGET_RULES.items():
            for r in kazanimlar:
                hits = _keyword_hits(r.metin + " " + r.hata_metni, kural["keywords"])
                if hits:
                    blok_skoru["bilişsel"] += 2.0 * math.log1p(len(hits))

        # ── Bronfenbrenner (Yoğunluk Çarpanı İle) ──
        for kural_adi, kural in BRONFENBRENNER_RULES.items():
            for b in davranislar:
                hits = _keyword_hits(b.metin, kural["keywords"])
                if hits:
                    çarpan = b.yogunluk / 3.0
                    blok_skoru["çevresel"] += kural["etki_puani"] * math.log1p(len(hits)) * çarpan
                    add_evidence(f"[Bronfenbrenner/{kural_adi}] {kural['aciklama'][:70]}")

        oz_yeterlilik = _clamp(oz_yeterlilik)
        buyume_z = _clamp(buyume_z)

        # Öğrenilmiş çaresizlik dedüksiyonu
        if oz_yeterlilik < 4.0 and buyume_z < 4.0 and kaçınma:
            ogrenilmis_c = True
            blok_skoru["psikolojik"] += 4.0
            add_evidence("[Seligman/Öğrenilmiş Çaresizlik] Düşük öz-yeterlilik + sabit zihniyet + kaçınma eş zamanlı.")

        if blok_skoru["çevresel"] > blok_skoru["psikolojik"] and blok_skoru["çevresel"] > blok_skoru["bilişsel"]:
            blok_turu = "çevresel"
        elif blok_skoru["psikolojik"] > blok_skoru["bilişsel"]:
            blok_turu = "psikolojik"
        elif blok_skoru["bilişsel"] > 0:
            blok_turu = "bilişsel"
        else:
            blok_turu = "belirsiz"

        if blok_skoru["psikolojik"] >= 4 and blok_skoru["bilişsel"] >= 4:
            blok_turu = "karma"

        kok_neden_map = {
            "psikolojik": "Başarısızlığın temel kaynağı akademik değil psikolojik bir blokajdır. Düşük öz-yeterlilik inancı görev taleplerini tehdit olarak işlemekte; bu durum öğrenme sürecine katılımı sistematik biçimde kısıtlamaktadır.",
            "bilişsel": "Başarısızlığın kök nedeni bilişsel kapasite-görev uyumsuzluğudur. Kazanım talepleri çalışma belleğinin kapasitesini ya da mevcut şema yapısının sınırlarını aşmaktadır.",
            "çevresel": "Akademik performansın önünde çevresel/biyolojik engeller var. Uyku, beslenme veya aile stresi bilişsel ve duygusal kapasite üzerinde olumsuz etkisini sürdürmektedir.",
            "karma": "Akademik güçlük çok kökenlidir: hem bilişsel yük aşımı hem de psikolojik blokaj birbirini besleyen bir kısır döngü oluşturmuştur. Tek boyutlu müdahale yetersiz kalacaktır.",
            "belirsiz": "Mevcut veri, kesin kök neden tespiti için yetersizdir. Ek gözlem ve veri girişi önerilir.",
        }

        return AttitudeDiagnosis(
            blok_turu              = blok_turu,
            kök_neden             = kok_neden_map.get(blok_turu, ""),
            oz_yeterlilik_skoru   = round(oz_yeterlilik, 2),
            buyume_zihniyeti      = round(buyume_z, 2),
            kaçınma_örüntüsü      = kaçınma,
            öğrenilmiş_çaresizlik = ogrenilmis_c,
            kanit                 = kanit_listesi[:8],
        )

    def _analyze_talent(self, kazanimlar: list[OutcomeRecord], davranislar: list[BehaviorRecord]) -> TalentRadar:
        puanlar = {z: 3.0 for z in GARDNER_SIGNALS}
        ilgi_sinyalleri = []

        for r in kazanimlar:
            if not r.basarili: continue
            for zeka, meta in GARDNER_SIGNALS.items():
                if r.ders in meta["ders_sinyalleri"]: puanlar[zeka] += 1.2 * r.tekrar_sayisi
                for fiil in meta["kazanım_fiilleri"]:
                    if fiil in _norm(r.metin): puanlar[zeka] += 0.6

        for r in kazanimlar:
            if r.basarili: continue
            for zeka, meta in GARDNER_SIGNALS.items():
                if r.ders in meta["ders_sinyalleri"]: puanlar[zeka] -= 0.4

        for b in davranislar:
            combined = _norm(b.metin + " " + b.boyut)
            for zeka, meta in GARDNER_SIGNALS.items():
                hits = _keyword_hits(combined, meta["davranış_sinyalleri"])
                if hits:
                    puanlar[zeka] += len(hits) * (b.yogunluk / 3.0) * 0.8
                    ilgi_sinyalleri.append(f"[{zeka}] {', '.join(hits[:2])} (yoğunluk: {b.yogunluk}/5)")
                if b.boyut == "ilgi_alani":
                    for fiil in meta["davranış_sinyalleri"]:
                        if fiil in combined: puanlar[zeka] += 0.5 * b.yogunluk

        zeka_puanlari = {z: round(_clamp(v, 0, 10), 2) for z, v in puanlar.items()}
        sirali = sorted(zeka_puanlari.items(), key=lambda x: x[1], reverse=True)
        en_guclu = [s[0] for s in sirali[:3]]

        gizli_yetenek = "Yetenek profili için daha fazla veri gereklidir."
        if en_guclu:
            top = en_guclu[0]
            aciklama = GARDNER_SIGNALS[top]["aciklama"]
            if len(en_guclu) >= 2 and abs(puanlar[en_guclu[0]] - puanlar[en_guclu[1]]) < 1.5:
                gizli_yetenek = f"{aciklama} Ek olarak **{en_guclu[1]}** alanında da güçlü sinyaller mevcut. Proje tabanlı aktiviteler bu potansiyeli görünür kılabilir."
            else:
                gizli_yetenek = f"{aciklama} Mevcut güçlük akademik alanlarda yaşanıyor olsa da **{top}** zekasındaki güçlü sinyaller potansiyeline işaret ediyor."

        return TalentRadar(zeka_puanlari=zeka_puanlari, en_güçlü=en_guclu, gizli_yetenek=gizli_yetenek, ilgi_sinyalleri=ilgi_sinyalleri[:8])

    def _build_zpd_prescription(self, bloom_list: list[BloomAnalysis], cog_load: CognitiveLoad, tutum: AttitudeDiagnosis, sinif: str) -> ZPDPrescription:
        eksikler = [b for b in bloom_list if b.eksik_mi]
        if eksikler:
            min_eksik_lvl = min(b.seviye for b in eksikler)
            mevcut = f"Bloom L{min_eksik_lvl} ({BLOOM_LABELS[min_eksik_lvl]}) seviyesinde güçlük yaşanıyor."
            zpd_hedef_lvl = min(min_eksik_lvl + 1, 6)
        else:
            mevcut = "Tüm gözlemlenen kazanımlarda başarı var; ZPD üst sınırını genişletin."
            zpd_hedef_lvl = 4

        zpd_hedefi = f"Bloom L{zpd_hedef_lvl} ({BLOOM_LABELS[zpd_hedef_lvl]}) seviyesine destekli geçiş hedefleniyor."

        aktif_kurallar = set()
        for kural_adi, kural in SWELLER_RULES.items():
            for t in cog_load.tetikleyenler:
                if kural_adi in t: aktif_kurallar.add(kural_adi)
        if tutum.kaçınma_örüntüsü: aktif_kurallar.add("kaçınma_döngüsü")
        if tutum.oz_yeterlilik_skoru < 5: aktif_kurallar.add("düşük_öz_yeterlilik")
        if tutum.öğrenilmiş_çaresizlik: aktif_kurallar.add("sabit_zihniyet_göstergesi")

        secilen_araclar = []
        seen = set()
        for arac_adi, arac in ZPD_INTERVENTION_LIBRARY.items():
            if arac_adi in seen: continue
            kesişim = aktif_kurallar & set(arac["koşul_kuralları"])
            if kesişim:
                secilen_araclar.append({"baslik": arac["başlık"], "kuram": arac["kuram"], "aciklama": arac["adımlar"], "sure_dakika": arac["sure_dakika"], "kesisim_skoru": len(kesişim)})
                seen.add(arac_adi)

        secilen_araclar.sort(key=lambda x: x["kesisim_skoru"], reverse=True)
        adimlar = secilen_araclar[:3]
        
        if not adimlar:
            adimlar = [{"baslik": "Bridging Analogy", "kuram": "Piaget (1952)", "aciklama": ["Kavramları ilişkilendirin."], "sure_dakika": 12}]

        return ZPDPrescription(mevcut_duzey=mevcut, zpd_hedefi=zpd_hedefi, adimlar=adimlar)

    def _compute_risk(self, cog_load: CognitiveLoad, tutum: AttitudeDiagnosis) -> float:
        cog_component = (cog_load.yuk_skoru / 10.0) * 40.0
        se_component = ((10.0 - tutum.oz_yeterlilik_skoru) / 10.0) * 30.0
        gm_component = ((10.0 - tutum.buyume_zihniyeti) / 10.0) * 15.0

        bonus = 0.0
        if tutum.öğrenilmiş_çaresizlik: bonus += 10.0
        if tutum.kaçınma_örüntüsü: bonus += 5.0

        total = cog_component + se_component + gm_component + bonus
        return round(min(total, 100.0), 1)

    def _compute_priority(self, cog_load: CognitiveLoad, tutum: AttitudeDiagnosis, davranislar: list[BehaviorRecord]) -> list[str]:
        # Çevresel ve duygusal skorları davranışlar üzerinde yoğunluk çarpanı ile hesapla
        cev_skor = sum(kural["etki_puani"] * len(_keyword_hits(b.metin, kural["keywords"])) * (b.yogunluk/3.0) for kural in BRONFENBRENNER_RULES.values() for b in davranislar)
        duygu_skor = sum(kural["olumsuz_etki"] * len(_keyword_hits(b.metin, kural["keywords"])) * (b.yogunluk/3.0) for kural in GOLEMAN_RULES.values() for b in davranislar)
        
        scores = {
            "Bilişsel Yük Azaltma":      cog_load.yuk_skoru * 1.0,
            "Öz-Yeterlilik İnşası":      (10.0 - tutum.oz_yeterlilik_skoru) * 1.2,
            "Büyüme Zihniyeti Desteği":  (10.0 - tutum.buyume_zihniyeti) * 0.8,
            "Çevresel Risk Yönetimi":    cev_skor,
            "Duygusal Düzenleme Desteği": duygu_skor,
        }
        sorted_priority = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return [k for k, v in sorted_priority if v > 0][:4]

    def _generate_summary(self, data: StudentInput, bloom_list: list[BloomAnalysis], cog_load: CognitiveLoad, tutum: AttitudeDiagnosis, radar: TalentRadar, risk_score: float) -> str:
        eksik_sayisi = sum(1 for b in bloom_list if b.eksik_mi)
        basarili_sayisi = sum(1 for b in bloom_list if not b.eksik_mi)
        en_guclu_str = " ve ".join(radar.en_güçlü[:2]) if radar.en_güçlü else "henüz belirsiz"

        risk_ifade = "çok boyutlu ve acil müdahale gerektiriyor" if risk_score >= 70 else "öncelikli müdahale planı gerektiriyor" if risk_score >= 45 else "izleme ve destekleyici müdahale öneriliyor" if risk_score >= 20 else "önleyici destek yeterli görünüyor"
        blok_ifade = {"psikolojik": "psikolojik bir blokajdan kaynaklandığı", "bilişsel": "bilişsel kapasite-görev uyumsuzluğundan kaynaklandığı", "çevresel": "çevresel/biyolojik faktörlerden beslendiği", "karma": "hem bilişsel hem psikolojik kökenli olduğu ve birbirini besleyen bir kısır döngü oluşturduğu", "belirsiz": "kök nedeninin henüz yeterli veri olmaksızın belirlenemediği"}.get(tutum.blok_turu, "")

        return f"{data.ad} için yapılan analiz, {eksik_sayisi} kazanımda güçlük ve {basarili_sayisi} kazanımda başarı olduğunu ortaya koymaktadır. Genel risk skoru {risk_score:.1f}/100 olup {risk_ifade}. Mevcut akademik güçlüğün {blok_ifade} değerlendirilmektedir. Öğrencinin güçlü zeka alanları {en_guclu_str} olarak öne çıkmakta; bu alanlara dayanan müdahaleler bilişsel ve motivasyonel dönüşümü hızlandırabilir."