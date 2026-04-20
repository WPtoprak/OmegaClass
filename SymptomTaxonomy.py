"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  SymptomTaxonomy.py                                                          ║
║  Gözlem ve Ölçüt Sözlüğü — Dijital Eğitim Fakültesi                         ║
║                                                                              ║
║  Kapsam: 60+ sınıf içi gözlem                                               ║
║  Çerçeve: Piaget · Vygotsky · Bandura · Sweller · Goleman · Gardner         ║
║           Montessori · Dewey · Bloom · Bronfenbrenner · Seligman             ║
║           Dweck · Erikson · Maslow · Lev Vygotsky · Urie Bronfenbrenner     ║
║                                                                              ║
║  Kategoriler:                                                                ║
║    BütünleşikVakaAnalizi · BilişselGüçlük · DuyuşsalDurum                   ║
║    SosyalDinamik · ParıltıVeÜstünlük · SınıfYönetimi                        ║
║    ÖzelEğitimŞüphesi · ÖğrenmeTarzı · AileVeÇevre                           ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

SYMPTOM_TAXONOMY: dict = {

    # ══════════════════════════════════════════════════════════════
    #  BÖLÜM 1 — BÜTÜNLEŞİK VAKA ANALİZİ (Karma Profiller)
    # ══════════════════════════════════════════════════════════════

    "sirada_sallanma_ve_zihinden_hizli_cozme": {
        "ogretmen_metni": (
            "Sırada sürekli sallanıyor, arkadaşlarının sözünü kesiyor "
            "ama aniden sorulan çok zor bir matematik sorusunu zihinden "
            "hatasız ve anında çözüyor."
        ),
        "fakulte_analizi": {
            "Ozel_Egitim_Kursusu": (
                "İki Kere Farklı (2e) Öğrenci Profili: Üstün zeka potansiyeli "
                "ile DEHB (dürtüsellik) kesişimi şüphesi. Yüksek yetenek tek "
                "başına DEHB'i dışlamaz; aksine maskeleyebilir."
            ),
            "Bilisel_Psikoloji_Kursusu": (
                "Sweller (Bilişsel Yük): Çocuğun çalışma belleği kapasitesi "
                "mevcut ders hızına kıyasla çok yüksek — 'Bilişsel Alt-Yüklenme' "
                "(Cognitive Under-Load / boredom) yaşanıyor. Sıkıntı, "
                "dürtüsel hareketlere dönüşüyor."
            ),
            "PDR_Kursusu": (
                "Goleman (Duygusal Zeka): Dürtü kontrolü ve bekleme toleransı "
                "(delay of gratification) becerisi henüz olgunlaşmamış. "
                "Sosyal-duygusal beceri öğretimi gerekiyor."
            ),
            "Sinif_Yonetimi_Kursusu": (
                "Geleneksel otorite değil 'Kinetik Enerji Deşarjı' stratejisi: "
                "Öğrenciye hareket alanı tanıyan anlamlı görevler ver "
                "(tahta, materyal, demonstrasyon). Wong & Wong (2009) — "
                "görev odaklı sınıf yönetimi."
            ),
            "Program_ve_Ogretim_Kursusu": (
                "Dewey (Deneyimsel Öğrenme): Öğrenci zihinsel uyarım eksikliği "
                "yaşıyor. Farklılaştırılmış öğretim (DI) ile zorluk düzeyi "
                "bireyselleştirilmeli."
            ),
        },
        "kategori": "BütünleşikVakaAnalizi",
        "akademik_uyari": (
            "RAM Yönlendirmesi: DEHB ve Üstün Yetenek değerlendirmesi için "
            "okul rehber öğretmeni aracılığıyla RAM'a sevk. Beklerken "
            "zorluk derecesini artırın, fiziksel hareket alanı tanıyın."
        ),
        "aciliyet": "YÜKSEK",
    },

    "okuma_yazmada_gec_kalma_ama_sozlu_anlatimda_ustunluk": {
        "ogretmen_metni": (
            "Okuma-yazma becerisi sınıf düzeyinin belirgin biçimde altında; "
            "harfleri karıştırıyor, yazmayı yavaş ve güçlükle yapıyor. "
            "Ancak sözlü anlatımda yaşıtlarını kat kat aşıyor: soyut kavramları "
            "metaforlarla ifade ediyor, dinleyeni büyüleyen hikâyeler kuruyor."
        ),
        "fakulte_analizi": {
            "Ozel_Egitim_Kursusu": (
                "Disleksi (Özgül Öğrenme Güçlüğü) şüphesi: Fonolojik farkındalık "
                "ve harf-ses eşleştirme güçlüğü. Sözel zeka ile yazılı dil "
                "performansı arasındaki makas tanıyı güçlendirir. "
                "DSM-5 — Özgül Öğrenme Bozukluğu kriterleri taranmalı."
            ),
            "Bilisel_Psikoloji_Kursusu": (
                "Gardner (Sözel-Dilsel Zeka): Sözel üretkenlik olağanüstü yüksek; "
                "ancak grafomotor ve fonetik işleme mekanizmaları ayrı bir "
                "nörolojik güçlük barındırıyor. Zekanın kendisi değil, "
                "aktarım kanalı bozulmuş."
            ),
            "Olcme_Degerlendirme_Kursusu": (
                "Geleneksel yazılı sınav bu öğrencinin gerçek bilgisini "
                "ölçemiyor — ölçme aracı geçersizleşiyor. Sözlü sınav, "
                "sesli okuma yerine dinleme temelli değerlendirme, "
                "çoktan seçmeli format gibi uyarlamalar zorunlu."
            ),
            "PDR_Kursusu": (
                "Tanılanmamış öğrenme güçlüğü; öz-yeterlilik inancı "
                "sistematik biçimde aşınıyor (Bandura). Uzun vadede "
                "okula karşı olumsuz tutum ve okul reddi riski var."
            ),
        },
        "kategori": "ÖzelEğitimŞüphesi",
        "akademik_uyari": (
            "RAM sevki öncelikli. Beklerken: yazılı ürün yerine sözlü "
            "değerlendirme, ses kayıt cihazı ile ödev teslimi, "
            "büyük punto ve satır arası geniş kağıt kullanımı."
        ),
        "aciliyet": "YÜKSEK",
    },

    "matematik_guclugu_ama_muzik_ve_ritimde_mucize": {
        "ogretmen_metni": (
            "Dört işlemde ciddi güçlük, soyut sayı kavramını oturtamıyor. "
            "Müzik dersinde ise tek duyuşta karmaşık ritim kalıplarını "
            "ezberliyor, çalınan bir melodiyi hemen doğru nota dizisiyle "
            "mırıldanıyor."
        ),
        "fakulte_analizi": {
            "Bilisel_Psikoloji_Kursusu": (
                "Gardner (Çoklu Zeka): Müzikal-Ritmik zekanın baskın olması, "
                "Mantıksal-Matematiksel zekanın zayıflığını telafi etmiyor; "
                "ancak müzik ritmi aracılığıyla sayı örüntüsü öğretilebilir "
                "(örn: çarpım tablosunu ritimle). Modalite eşleştirme."
            ),
            "Program_ve_Ogretim_Kursusu": (
                "Dewey (Yaparak-Yaşayarak Öğrenme): Soyut sayısal sembolleri "
                "somut ses ve ritim deneyimiyle ilişkilendirmek Piaget'nin "
                "somuttan-soyuta ilkesiyle örtüşür. Müzik entegre matematik "
                "tasarımı (STEAM yaklaşımı)."
            ),
            "Sinif_Yonetimi_Kursusu": (
                "Öğrencinin güçlü alanını sınıf içinde görünür kıl; "
                "bu hem sosyal statüsünü korur hem de öz-yeterlilik "
                "inancını akademik alana taşır (Bandura transfer etkisi)."
            ),
            "Olcme_Degerlendirme_Kursusu": (
                "Standart ölçme araçları bu öğrencinin bilişsel profilini "
                "temsil etmiyor. Performansa dayalı değerlendirme "
                "(müzik ritmi ile matematik demonstrasyonu) alternatif sunuyor."
            ),
        },
        "kategori": "ParıltıVeÜstünlük",
        "akademik_uyari": (
            "Müzik ritmi ile matematik öğretimi deneyin. Çarpım tablosunu "
            "ritimle, kesirleri nota değerleriyle anlatın. Güçlü alanı "
            "köprü olarak kullanın."
        ),
        "aciliyet": "ORTA",
    },

    "sinifin_lideri_ama_yazili_sinavda_cokuyor": {
        "ogretmen_metni": (
            "Sınıfta doğal lider: grup çalışmalarını organize ediyor, "
            "çatışmaları arabuluculukla çözüyor, arkadaşlarına konuyu "
            "mükemmel açıklıyor. Yazılı sınavda ise çok düşük not alıyor."
        ),
        "fakulte_analizi": {
            "Olcme_Degerlendirme_Kursusu": (
                "Ölçme geçerliliği sorunu: Yazılı sınav bu öğrencinin "
                "gerçek bilgisini ölçemeyen bir araç. Construct validity "
                "zedelenmiş — ölçülen şey bilgi mi, yoksa yazılı ifade "
                "becerisi mi? Portfolyo ve performans değerlendirmesi zorunlu."
            ),
            "Bilisel_Psikoloji_Kursusu": (
                "Gardner (Kişilerarası Zeka): Baskın zeka türü sosyal "
                "etkileşim üzerinden aktive oluyor. Bilgi somut bağlamda "
                "(açıklama, tartışma) var; ancak soyut sembolik "
                "aktarım (yazı) zayıf. Vygotsky: bilgi sosyal zeminde inşa."
            ),
            "PDR_Kursusu": (
                "Sınav kaygısı veya yazılı görev kaygısı olasılığı. "
                "Goleman: Kaygı prefrontal korteksi geçici bloke ediyor; "
                "sosyal bağlamda yok olan kaygı, bireysel-soyut "
                "sınav ortamında tetikleniyor."
            ),
            "Program_ve_Ogretim_Kursusu": (
                "Sözlü sınav, tartışma temelli değerlendirme, akran "
                "öğretimi formatları bu profil için çok daha güvenilir "
                "ölçme aracı. Öğretim tasarımı öğrenme stiline göre çeşitlendirilmeli."
            ),
        },
        "kategori": "ÖğrenmeTarzı",
        "akademik_uyari": (
            "Sözlü sınav ve portfolyo formatları ekleyin. "
            "Sınav kaygısı açısından PDR ile görüşün. "
            "Akran öğretimi fırsatları yaratın — hem o hem sınıf kazanır."
        ),
        "aciliyet": "ORTA",
    },

    # ══════════════════════════════════════════════════════════════
    #  BÖLÜM 2 — BİLİŞSEL GÜÇLÜK GÖZLEM MATRİSİ
    # ══════════════════════════════════════════════════════════════

    "islemi_biliyor_ama_sozu_degistirince_yapamiyor": {
        "ogretmen_metni": (
            "Standart formatta sorulan matematik problemini doğru çözüyor. "
            "Aynı kazanım farklı bir bağlamla (sözel problem, farklı sayılar) "
            "sorulduğunda tamamen çözemiyor."
        ),
        "fakulte_analizi": {
            "Bilisel_Psikoloji_Kursusu": (
                "Sweller (Germane Load): Şema otomasyonu gerçekleşmemiş; "
                "bilgi izole bağlama hapsedilmiş. Öğrenci işlemi "
                "ezberliyor, kavramsal anlama kazanmıyor. "
                "Transfer başarısızlığı = yüzeysel öğrenme kanıtı."
            ),
            "Piaget_Perspektifi": (
                "Asimilasyon gerçekleşmiş ama akomodasyon yok: Yeni durum "
                "eski şemaya sokularak çarpıtılıyor, şema genişlemiyor. "
                "Somuttan soyuta geçiş tamamlanmamış."
            ),
            "Program_ve_Ogretim_Kursusu": (
                "Varied practice (çeşitlendirilmiş uygulama) eksikliği. "
                "Bloom L3 (Uygulama) hedeflenmiş ama L2 (Anlama) "
                "sağlamlaşmadan geçilmiş. Öğretim tasarım hatası."
            ),
            "Olcme_Degerlendirme_Kursusu": (
                "Yalnızca standart format sınavlarla değerlendirme "
                "gerçek öğrenmeyi gizliyor. Transfer görevi içeren "
                "değerlendirme eklenmeli (açık uçlu, bağlam değiştirilen)."
            ),
        },
        "kategori": "BilişselGüçlük",
        "akademik_uyari": (
            "Aynı kazanımı en az 3 farklı bağlamda uygulayın. "
            "'Bu neye benziyor?' sorusuyla analoji köprüsü kurun. "
            "Formülü ezberlettirmeden önce anlamı somutlaştırın."
        ),
        "aciliyet": "ORTA",
    },

    "yazili_anlatimda_parcali_cumleler": {
        "ogretmen_metni": (
            "Yazılı anlatımda cümleler parçalı ve bitimsiz; düşünceler "
            "birbirine bağlanmıyor, paragraf mantığı yok. "
            "Konuşurken ise akıcı ve düzgün."
        ),
        "fakulte_analizi": {
            "Bilisel_Psikoloji_Kursusu": (
                "Çift işleme teorisi (Kahneman): Sözlü sistem (Sistem 1) "
                "otomatik ve akıcı; yazılı sistem (Sistem 2) yüksek "
                "bilişsel yük gerektiriyor. Grafomotor ve sözdizimsel "
                "koordinasyonda aşırı yük."
            ),
            "Ozel_Egitim_Kursusu": (
                "Disgrafya (yazılı ifade bozukluğu) şüphesi: Hareket planlama "
                "ve motor koordinasyon güçlüğü. Dysgraphia ile disleksiden "
                "ayrıştırılması gerekiyor — her ikisinde yazma güçlüğü "
                "var ama mekanizma farklı."
            ),
            "Program_ve_Ogretim_Kursusu": (
                "Vygotsky (İskele Kurma): Yazılı anlatım için düşünce "
                "iskeleti (graphic organizer, zihin haritası) kullanımı. "
                "Önce sözlü planlama, sonra yazıya aktarma stratejisi."
            ),
            "PDR_Kursusu": (
                "Tekrarlayan başarısızlık deneyimi yazma öz-yeterliliğini "
                "yıkıyor. Yazma kaygısı birincil güçlüğü besliyor olabilir."
            ),
        },
        "kategori": "BilişselGüçlük",
        "akademik_uyari": (
            "Zihin haritası ve madde madde not çerçevesi verin. "
            "Sözlü planlamadan yazıya köprü stratejisi uygulayın. "
            "Disgrafya şüphesinde RAM sevki."
        ),
        "aciliyet": "ORTA",
    },

    "soyut_matematik_kavraminda_tam_donma": {
        "ogretmen_metni": (
            "Somut sayı işlemlerinde sorun yok. Kesir, ondalık sayı veya "
            "değişken gibi soyut kavramlar gelince tamamen donuyor; "
            "'anlayamıyorum' deyip kalemini bırakıyor."
        ),
        "fakulte_analizi": {
            "Bilisel_Psikoloji_Kursusu": (
                "Piaget (Somut İşlemsel → Formal İşlemsel Geçiş): Öğrenci "
                "soyut sembolik düşünme evresine henüz geçmemiş olabilir. "
                "Gelişimsel hazırbulunuşluk sorunu; öğretim zamanlaması "
                "bireyle uyumsuz."
            ),
            "Program_ve_Ogretim_Kursusu": (
                "CPA (Concrete-Pictorial-Abstract) ilkesi ihlal edilmiş: "
                "Doğrudan soyuta geçilmiş. Kesir çubuğu, sayı doğrusu, "
                "pasta modeli gibi somut materyallerle yeniden başlamak gerekiyor."
            ),
            "PDR_Kursusu": (
                "Matematiksel kaygı (math anxiety) tetiklenmiş olabilir. "
                "Ashcraft (2002): Yüksek matematik kaygısı çalışma belleği "
                "kapasitesini doğrudan düşürüyor; 'donma' tepkisi biyolojik."
            ),
            "Sinif_Yonetimi_Kursusu": (
                "Öğrencinin donduğu anı fark et ve baskı uygulamadan "
                "geri çekil: Alternatif temsil sun, grup çalışmasına al, "
                "kalemini bırakmasına izin ver ve somut materyal ver."
            ),
        },
        "kategori": "BilişselGüçlük",
        "akademik_uyari": (
            "Somut materyallerle (fiziksel kesir parçaları, sayı doğrusu) "
            "sıfırdan başlayın. Matematik kaygısı yüksekse PDR ile görüşün. "
            "Notla değil süreçle değerlendirin."
        ),
        "aciliyet": "ORTA",
    },

    "okuduğunu_anlamada_satir_atlama": {
        "ogretmen_metni": (
            "Okurken satırları atlıyor, kelime yer değiştiriyor, "
            "aynı satırı tekrarlıyor. Anlama soruları sorulduğunda "
            "hiç anlamadığı ortaya çıkıyor."
        ),
        "fakulte_analizi": {
            "Ozel_Egitim_Kursusu": (
                "Oküler motor güçlük veya disleksi kaynaklı görsel takip "
                "problemi şüphesi. Renkli transparan filtre kullanımı "
                "bazı olgularda skor artışı sağlıyor (Irlen sendromu). "
                "Göz takip muayenesi önerilebilir."
            ),
            "Bilisel_Psikoloji_Kursusu": (
                "Fonolojik bellek ve harf-ses dönüşüm (decoding) zayıflığı: "
                "Çözümleme o kadar çok kaynak harcıyor ki anlama için "
                "çalışma belleğinde kapasite kalmıyor (Sweller — "
                "içsel yük aşımı)."
            ),
            "Program_ve_Ogretim_Kursusu": (
                "Sesli okuma + işaret parmağıyla takip, büyük punto, "
                "satır arası geniş metin formatı, renkli satır ayraçları "
                "görsel takibi destekler. Shared reading stratejisi."
            ),
            "Olcme_Degerlendirme_Kursusu": (
                "Sesli metin (text-to-speech), dinleme temelli anlama "
                "soruları ile gerçek anlama kapasitesi test edilmeli. "
                "Ölçülen şeyin 'okuma' mı yoksa 'anlama' mı olduğu netleştirilmeli."
            ),
        },
        "kategori": "ÖzelEğitimŞüphesi",
        "akademik_uyari": (
            "Büyük punto, satır arası geniş metin, satır cetveli "
            "araçlarını hemen uygulayın. Disleksi değerlendirmesi için "
            "RAM sevki."
        ),
        "aciliyet": "YÜKSEK",
    },

    "siralama_ve_zaman_yonetiminde_kronik_zorluk": {
        "ogretmen_metni": (
            "Her gün defteri ve materyallerini unutuyor, ödevleri sırayla "
            "tamamlayamıyor, başladığı işi bitiremiyor, zamanı yönetemiyor. "
            "Zekası açık ama 'organizasyon' tamamen çöküyor."
        ),
        "fakulte_analizi": {
            "Ozel_Egitim_Kursusu": (
                "Yürütücü İşlev (Executive Function) güçlüğü: Planlama, "
                "önceliklendirme, başlatma, izleme ve tamamlama becerileri "
                "etkilenmiş. DEHB ve/veya Yürütücü İşlev Bozukluğu "
                "değerlendirmesi gerekiyor (Barkley, 1997)."
            ),
            "Bilisel_Psikoloji_Kursusu": (
                "Prospektif bellek (gelecekteki niyeti hatırlama) zayıf. "
                "Çalışma belleğinin işleyici bileşeni (central executive) "
                "yetersiz kaynak ayırabiliyor."
            ),
            "PDR_Kursusu": (
                "Kronik başarısızlık ve unutkanlık döngüsü öz-yeterlilik "
                "inancını aşındırıyor. Öğrenci kendini 'dağınık' ve "
                "'başarısız' olarak etiketliyor."
            ),
            "Sinif_Yonetimi_Kursusu": (
                "Görsel takvim, yapılacaklar listesi, renkli kodlama "
                "sistemi, sınıf rutinlerinin tutarlılığı bu profil için "
                "yaşam kalitesini doğrudan artırır. "
                "Çevre düzenlemesi = dış yürütücü işlev desteği."
            ),
        },
        "kategori": "ÖzelEğitimŞüphesi",
        "akademik_uyari": (
            "Görsel çizelge, yapılacaklar listesi, materyaller için "
            "renkli kodlama hemen uygulayın. DEHB/YİB değerlendirmesi "
            "için RAM sevki. Sınıf ortamını öngörülebilir yapın."
        ),
        "aciliyet": "YÜKSEK",
    },

    "yeni_konuyu_beklenmedik_hizda_kavrama": {
        "ogretmen_metni": (
            "Konu anlatılır anlatılmaz anlıyor; sınıf alıştırma yaparken "
            "o çoktan bitirmiş ve bağlantılı farklı sorular soruyor. "
            "Diğerleri birinci soruyu çözerken o beşincidedir."
        ),
        "fakulte_analizi": {
            "Ozel_Egitim_Kursusu": (
                "Üstün Zeka / Üstün Yetenek Profili: Hızlı öğrenme hızı "
                "(rapid learning pace), bilgi derinliği ve bağlantı kurma "
                "kapasitesi belirgin. Ulusal ve uluslararası üstün yetenek "
                "tanılama kriterleri taranmalı (WISC-V, Raven vb.)."
            ),
            "Bilisel_Psikoloji_Kursusu": (
                "Sweller (Bilişsel Alt-Yüklenme): Mevcut içerik bilişsel "
                "kapasitesinin çok altında. Uzun vadede 'öğrenilmiş tembellik' "
                "riski: çaba göstermeden başarı norma dönüşür."
            ),
            "Program_ve_Ogretim_Kursusu": (
                "Dikey zenginleştirme (acceleration) ve yatay "
                "zenginleştirme (enrichment) stratejileri: Aynı konu "
                "daha derin ve genişletilmiş biçimde sunulmalı. "
                "Bloom L4-L6 hedefler tasarlanmalı."
            ),
            "PDR_Kursusu": (
                "Üstün yetenekli öğrencilerde mükemmeliyetçilik, "
                "sosyal uyumsuzluk ve 'fazla zeki' etiketiyle akran "
                "baskısı riskleri gözetilmeli (Dabrowski'nin "
                "aşırı uyarılabilirlik teorisi)."
            ),
        },
        "kategori": "ParıltıVeÜstünlük",
        "akademik_uyari": (
            "BİLSEM yönlendirmesi değerlendirin. Sınıf içinde "
            "derinleştirici ek görevler hazırlayın. Akran öğretici "
            "rolü (peer tutor) verin — hem onu hem sınıfı besler."
        ),
        "aciliyet": "ORTA",
    },

    # ══════════════════════════════════════════════════════════════
    #  BÖLÜM 3 — DUYUŞSAL DURUM VE TUTUM GÖZLEMLERİ
    # ══════════════════════════════════════════════════════════════

    "sinav_oncesi_karnagir_ve_tuvalette_uzun_sure": {
        "ogretmen_metni": (
            "Sınav günleri okula gelmiyor ya da sabah tuvalet bahanesiyle "
            "sınıfta bulunmuyor. Geldiğinde elleri titriyor, rengi solmuş."
        ),
        "fakulte_analizi": {
            "PDR_Kursusu": (
                "Klinik düzeyde Sınav Kaygısı (Test Anxiety): Somatik "
                "belirtilerle (mide bulantısı, titreme, renk solması) "
                "birlikte görünüyor. Spielberger Sınav Kaygısı Ölçeği "
                "uygulanabilir. Psikoeğitim ve gevşeme teknikleri birinci "
                "basamak müdahale."
            ),
            "Bilisel_Psikoloji_Kursusu": (
                "Kaygı → Yüksek kortizol → Hipokampüs ve prefrontal korteks "
                "işlev baskılanması → Çalışma belleği kapasitesi düşüşü: "
                "Bilen öğrenci sınavda 'boşalıyor'. "
                "Kaygı bilgiyi silmiyor, erişimi engelliyor."
            ),
            "Olcme_Degerlendirme_Kursusu": (
                "Sınav formatı öğrencinin gerçek bilgisini ölçemiyor; "
                "ölçülen şey kaygıyla bilgi kesişimi. "
                "Düşük baskılı ortam, uzayan süre, tanıdık format "
                "ölçme güvenilirliğini artırır."
            ),
            "Sinif_Yonetimi_Kursusu": (
                "Sınav öncesi kısa nefes egzersizi, 'hata yapmak öğrenmenin "
                "parçası' normunu tüm sınıfa öğret. "
                "Puan odaklı değil öğrenme odaklı sınıf iklimi oluştur."
            ),
        },
        "kategori": "DuyuşsalDurum",
        "akademik_uyari": (
            "PDR ile derhal görüşün. Kısa vadede: sınav öncesi "
            "2 dakika diyafram nefesi egzersizi. Uzun vadede: "
            "kademeli maruziyet ve bilişsel yeniden yapılandırma."
        ),
        "aciliyet": "YÜKSEK",
    },

    "hatali_cevap_sonrasi_aglamak_ve_kapanmak": {
        "ogretmen_metni": (
            "Sorduğunuzda yanlış cevap verince ya da deftere kırmızı "
            "işaret görünce ağlıyor, başını masaya gizliyor, "
            "geri kalan dersi katılımı sıfıra iniyor."
        ),
        "fakulte_analizi": {
            "PDR_Kursusu": (
                "Bandura (Düşük Öz-Yeterlilik): Tek bir hata tüm "
                "yetkinlik inancını çökertecek kadar kırılgan bir "
                "öz-değerlendirme yapısı. Koşulsuz yetkinlik inancı "
                "henüz gelişmemiş; başarı = değer, başarısızlık = "
                "değersizlik olarak kodlanmış."
            ),
            "Bilisel_Psikoloji_Kursusu": (
                "Goleman: Amigdala aktivasyonu prefrontal korteksi "
                "devre dışı bırakıyor ('amygdala hijack'). "
                "Ağlama ve kapanma = duygusal aşırı yük; "
                "bu anda yeni öğrenme imkânsız."
            ),
            "Program_ve_Ogretim_Kursusu": (
                "Dweck (Büyüme Zihniyeti): 'Hata = başarısızlık' "
                "sabit zihniyet çerçevesi var. "
                "'Henüz bilmiyorum ama öğrenebilirim' normunu "
                "sistematik olarak öğret."
            ),
            "Aile_Perspektifi": (
                "Mükemmeliyetçi ebeveyn baskısı veya evde hataya "
                "verilen olumsuz tepkiler bu örüntüyü pekiştiriyor "
                "olabilir. Aile görüşmesi öncelikli."
            ),
        },
        "kategori": "DuyuşsalDurum",
        "akademik_uyari": (
            "Hata anında sınıf önünde yorum yapmayın — özel, "
            "gizli geri bildirim verin. Sınıf normunu değiştirin: "
            "'En güzel hata ödülü' gibi sembolik pratikler. "
            "Aile ile görüşün."
        ),
        "aciliyet": "YÜKSEK",
    },

    "gorev_verildiginde_surekli_izin_isteme": {
        "ogretmen_metni": (
            "Her görev verildiğinde 'Ben yapamam mıyım?', "
            "'Böyle mi yapayım?', 'Yanlış mı oluyor?' diye "
            "sürekli onay arıyor. Bağımsız başlamakta zorlanıyor."
        ),
        "fakulte_analizi": {
            "PDR_Kursusu": (
                "Bağımlı Öğrenme Örüntüsü + Düşük Öz-Yeterlilik: "
                "Öğrenci özerk karar verme kapasitesine güvenmiyor. "
                "Maslow (Güvenlik İhtiyacı): onay = güvenlik hissi. "
                "Uzun vadede öğrenilmiş çaresizliğe evrilebilir."
            ),
            "Aile_Perspektifi": (
                "Aşırı koruyucu ebeveyn (helicopter parenting) "
                "örüntüsü: Evde her karar ebeveyn tarafından "
                "alınıyor; bağımsız problem çözme fırsatı "
                "sistematik olarak elinden alınmış."
            ),
            "Program_ve_Ogretim_Kursusu": (
                "Montessori (Hazırlanmış Çevre): Görev yapısını "
                "öğrenci başlayabilecek kadar açık tasarla; "
                "kademeli olarak belirsizlik toleransını artır. "
                "İlk 'başlama cesareti' kazanımı hedefle."
            ),
            "Sinif_Yonetimi_Kursusu": (
                "Her onay isteğine anında karşılık verme alışkanlığı "
                "bağımlılığı pekiştiriyor. Kademeli olarak yanıtı "
                "ertele: 'Sen ne düşünüyorsun önce?' "
                "sorusu ile özerk düşünceyi ödüllendir."
            ),
        },
        "kategori": "DuyuşsalDurum",
        "akademik_uyari": (
            "Onay döngüsünü kır: 'Sen ne düşünüyorsun?' ile başla. "
            "Küçük bağımsız kararları öv. Aile ile "
            "bağımsızlık geliştirme konuşması yapın."
        ),
        "aciliyet": "ORTA",
    },

    "derste_ne_yaptigini_bilmiyor_ama_mutlu": {
        "ogretmen_metni": (
            "Derste ne yapıldığından habersiz görünüyor; "
            "ama keyifli, gülüyor, arkadaşlarıyla iletişimi güzel. "
            "Not defterinde hiçbir şey yok."
        ),
        "fakulte_analizi": {
            "Bilisel_Psikoloji_Kursusu": (
                "Düşük akademik bağlılık (low academic engagement) "
                "ama yüksek sosyal bağlılık. Vygotsky: Öğrenci "
                "sosyal aktivite modunda; bilişsel aktivasyon yok. "
                "Dikkat yönetimi ve hedef belirleme becerisi eksik."
            ),
            "Olcme_Degerlendirme_Kursusu": (
                "İşitsel işleme güçlüğü veya yönerge takip "
                "güçlüğü düşünülmeli. Sözel yönerge kavranmıyor "
                "olabilir — görsel yönerge ile test edin."
            ),
            "PDR_Kursusu": (
                "Öğrenme hedefinden kopukluk ama sosyal doyum tam: "
                "Okul öğrenciye sosyal ihtiyacı karşılayan bir "
                "mekan olarak işliyor. Akademik anlam eksikliği."
            ),
            "Sinif_Yonetimi_Kursusu": (
                "Görev yönergesini kişiselleştir: Öğrencinin "
                "adını kullan, göz teması kur, "
                "fiziksel yakınlık ile dikkat çek. "
                "Koltuk düzenlemesini gözden geçir."
            ),
        },
        "kategori": "SınıfYönetimi",
        "akademik_uyari": (
            "İşitsel işleme güçlüğü değerlendirmesi için RAM sevki. "
            "Beklerken görsel yönergeler (yazılı + semboller) ekleyin. "
            "Oturma düzenini tahtaya yakın revize edin."
        ),
        "aciliyet": "ORTA",
    },

    "okulu_sever_ama_ogrenmekten_zevk_almaz": {
        "ogretmen_metni": (
            "Her sabah neşeyle geliyor, teneffüsleri seviyor, "
            "öğretmeniyle ilişkisi güçlü. Ama ders saatlerinde "
            "tamamen kopuyor, 'ne zaman biter' diyor."
        ),
        "fakulte_analizi": {
            "PDR_Kursusu": (
                "Okul bağlılığı (school belonging) var ama "
                "öğrenme bağlılığı (academic engagement) yok. "
                "İki kavram ayrı: sosyal okul deneyimi anlamlı, "
                "bilişsel okul deneyimi anlamsız algılanıyor."
            ),
            "Program_ve_Ogretim_Kursusu": (
                "Dewey (Anlam ve İlgi): Müfredat öğrencinin "
                "ilgi ve merak yapısına dokunmuyor. "
                "İçerik öğrencinin gerçek yaşamından kopuk. "
                "Proje tabanlı öğrenme ve ilgi temelli seçmeli "
                "görevler bağlılığı artırır."
            ),
            "Bilisel_Psikoloji_Kursusu": (
                "İçsel motivasyon (Deci & Ryan, SDT) zedelenmiş: "
                "Özerklik, yeterlik ve ilişkili olma ihtiyaçlarından "
                "en az biri karşılanmıyor. Hangi ders/konu ilgisini "
                "çekiyor bulmak ve oradan köprü kurmak kritik."
            ),
            "Sinif_Yonetimi_Kursusu": (
                "Öğrencinin güçlü sosyal bağını öğrenme aktivasyonu "
                "için araçsallaştır: İşbirlikli öğrenme formatları, "
                "akran öğrenimi, sosyal bağlamda anlamlı görevler."
            ),
        },
        "kategori": "DuyuşsalDurum",
        "akademik_uyari": (
            "Öğrencinin ilgi alanlarını keşfedin ve dersi "
            "oradan bağlayın. İşbirlikli görevleri artırın. "
            "Motivasyon değerlendirmesi için PDR ile görüşün."
        ),
        "aciliyet": "ORTA",
    },

    # ══════════════════════════════════════════════════════════════
    #  BÖLÜM 4 — SOSYAL DİNAMİKLER VE AKRAN İLİŞKİLERİ
    # ══════════════════════════════════════════════════════════════

    "sinifin_nedense_sevmedigi_cocuk": {
        "ogretmen_metni": (
            "Açıkça kötü davranış göstermediği halde sınıfın "
            "büyük çoğunluğu onunla oynamak istemiyor, "
            "grup çalışmalarında kimse yanına gelmek istemiyor."
        ),
        "fakulte_analizi": {
            "PDR_Kursusu": (
                "Sosyal dışlanma (peer rejection): Sociometri testi "
                "(kim kimi tercih eder?) ile sınıf sosyal haritası "
                "çıkarılmalı. Dışlanma nedeni: sosyal ipuçlarını "
                "yanlış okuma (pragmatik dil güçlüğü?) veya "
                "kişisel hijyen sorunu veya farklılık? "
                "Kök neden araştırılmadan müdahale başarısız olur."
            ),
            "Ozel_Egitim_Kursusu": (
                "Otizm Spektrum Bozukluğu (hafif uç) veya "
                "Sosyal İletişim Bozukluğu: Sosyal pragmatik "
                "ipuçlarını (yüz ifadesi, ton, sıra bekleme) "
                "işleme güçlüğü. Değerlendirme gerekiyor."
            ),
            "Sinif_Yonetimi_Kursusu": (
                "Kapsayıcı sınıf iklimi rutinleri: Öğretmen grup "
                "atamalarını kendisi yapmalı, öğrenci seçimine bırakmamalı. "
                "Dışlanan öğrencinin güçlü olduğu bir alanda "
                "sınıf içinde statü kazanmasını sağla."
            ),
            "Program_ve_Ogretim_Kursusu": (
                "Sosyal beceri öğretimi müfredatı: "
                "Sıra alma, aktif dinleme, ortak oyun kuralları "
                "açıkça ve sistematik öğretilmeli (SEL programları)."
            ),
        },
        "kategori": "SosyalDinamik",
        "akademik_uyari": (
            "Sociometri uygulayın. Kök neden araştırın. "
            "OSB/SOIB şüphesinde RAM sevki. Beklerken: "
            "öğretmen belirlemeli grup atamaları, "
            "öğrencinin güçlü olduğu alanda görünürlük."
        ),
        "aciliyet": "YÜKSEK",
    },

    "sinifin_palyacosu_ama_ici_bos": {
        "ogretmen_metni": (
            "Sürekli gülüyor, espri yapıyor, sınıfı güldürüyor. "
            "Ama bireysel görüşmede derinden yorgun ve mutsuz "
            "görünüyor; 'kimse beni ciddiye almıyor' diyor."
        ),
        "fakulte_analizi": {
            "PDR_Kursusu": (
                "Sosyal maske (social masking / clowning): "
                "Mizah, kabul görme ve dışlanma korkusunu "
                "yönetme mekanizması. Gerçek benliği gizleme "
                "stratejisi. Altta yatan düşük benlik saygısı "
                "ve ait olma ihtiyacı (Maslow L3) kritik."
            ),
            "Bilisel_Psikoloji_Kursusu": (
                "Savunma mekanizması (Freud — psikodinamik): "
                "Duygusal acıyı hissetmemek için mizah "
                "bilişsel yeniden çerçeveleme işlevi görüyor. "
                "Kognitif kapasite başa çıkma stratejisine harcanıyor."
            ),
            "Sinif_Yonetimi_Kursusu": (
                "Mizah enerjisini yapıcıya dönüştür: "
                "Sınıf sunumlarında, drama etkinliklerinde, "
                "söyleşi liderliğinde kullan. "
                "Öğrenci değerini akademik bağlamda hissederse "
                "maske ihtiyacı azalır."
            ),
            "Aile_Perspektifi": (
                "Evde görünmez hissetme veya ciddi alınmama "
                "örüntüsü bu davranışı besliyor olabilir. "
                "Aile görüşmesinde gözlemin paylaşılması önemli."
            ),
        },
        "kategori": "DuyuşsalDurum",
        "akademik_uyari": (
            "Bireysel görüşme yapın — sakin ve yargısız. "
            "Mizah enerjisini yapıcı kanallara yönlendirin. "
            "Altta yatan mutsuzluk derinse PDR sevki."
        ),
        "aciliyet": "ORTA",
    },

    "cift_dilli_ogrenci_ve_dil_karisikligi": {
        "ogretmen_metni": (
            "Evde farklı bir dil konuşuluyor. Türkçede "
            "dilbilgisi hataları yapıyor, kelime bulmakta "
            "zorlanıyor ama kendi anadilinde akıcı."
        ),
        "fakulte_analizi": {
            "Program_ve_Ogretim_Kursusu": (
                "İkinci Dil Edinimi (Cummins — BICS/CALP): "
                "Sosyal dil (BICS) genellikle 2 yılda; "
                "akademik dil (CALP) 5-7 yılda ediniliyor. "
                "Akademik Türkçe henüz gelişim sürecinde; "
                "bu gelişimsel, patolojik değil."
            ),
            "Ozel_Egitim_Kursusu": (
                "Dil gecikme tanısı koymadan önce çift dillilik "
                "etkisi dışlanmalı. Öğrencinin anadilindeki "
                "yeterliliği değerlendirilmeli — her iki dilde "
                "güçlük varsa dil bozukluğu şüphesi; "
                "yalnızca Türkçede zorlanıyorsa dil edinimi süreci."
            ),
            "Bilisel_Psikoloji_Kursusu": (
                "Kod değiştirme (code-switching): İki dil sistemi "
                "çalışma belleğinde rekabet ediyor. "
                "Bu çift dillilik nörobilişsel avantaj da sağlar "
                "(bilişsel esneklik, yürütücü kontrol) — "
                "Bialystok (2011)."
            ),
            "PDR_Kursusu": (
                "Kimlik gelişimi: Anadili ve kültürünün "
                "sınıfta değersizleştirilmesi kimlik kargaşasına "
                "yol açar (Erikson — Kimlik vs. Rol Karmaşası). "
                "İki kültürlü kimliği onura kavuştur."
            ),
        },
        "kategori": "ÖğrenmeTarzı",
        "akademik_uyari": (
            "Anadilini değersizleştirmeyin. "
            "Akademik Türkçeyi gelişimsel süreç olarak destekleyin. "
            "Her iki dilde güçlük varsa dil terapisti değerlendirmesi."
        ),
        "aciliyet": "DÜŞÜK",
    },

    "akran_zorbaligi_yapan_cocuk": {
        "ogretmen_metni": (
            "Daha küçük veya zayıf arkadaşlarını sürekli "
            "rahatsız ediyor, aşağılıyor, sosyal dışlama "
            "organizasyonu yapıyor."
        ),
        "fakulte_analizi": {
            "PDR_Kursusu": (
                "Zorbalık davranışı genellikle güç ihtiyacı, "
                "empati eksikliği veya evde maruz kalınan "
                "şiddetin yeniden sahnelenmesidir (Olweus, 1993). "
                "Hem zorba hem mağdur için müdahale şart; "
                "yalnızca zorba disiplinlenirse sistem değişmez."
            ),
            "Ozel_Egitim_Kursusu": (
                "Dışsallaştırıcı davranış bozukluğu (ODD/CD) "
                "eşik kontrolü yapılmalı. "
                "Travma kaynaklı bağlanma güçlüğü (RAD) "
                "tabloya katkıda bulunuyor olabilir."
            ),
            "Bilisel_Psikoloji_Kursusu": (
                "Sosyal bilgi işleme (Crick & Dodge, 1994): "
                "Zorba öğrenci nötr sosyal ipuçlarını düşmanca "
                "yorumluyor (hostile attribution bias). "
                "Bu bilişsel çarpıklık değiştirilebilir."
            ),
            "Sinif_Yonetimi_Kursusu": (
                "Restoratif uygulamalar (restorative practices): "
                "Ceza odaklı değil onarım odaklı müdahale. "
                "Mağdur-zorba diyaloğu, sınıf normlarının yeniden inşası."
            ),
        },
        "kategori": "SosyalDinamik",
        "akademik_uyari": (
            "Hem zorba hem mağdur için PDR sevki. "
            "Aile görüşmesi zorunlu. Restoratif pratikler uygulayın. "
            "Sınıf normunu açık ve tutarlı biçimde yeniden kurun."
        ),
        "aciliyet": "ACİL",
    },

    "zorbaliga_ugrayan_ve_sessiz_kalan_cocuk": {
        "ogretmen_metni": (
            "Teneffüste yalnız, birlikte fotoğrafa bile "
            "alınmak istemiyor. Hiç şikâyet etmiyor ama "
            "sınıf içinde sürekli gergin ve ürkek görünüyor."
        ),
        "fakulte_analizi": {
            "PDR_Kursusu": (
                "Sessiz zorbalık mağduru: Suskunluk korku veya "
                "'söylersem daha kötü olur' inancından kaynaklanıyor. "
                "Mağdur çocuklar genellikle pasif, çekilgen, "
                "düşük öz-yeterlilikli profil gösteriyor (Olweus)."
            ),
            "Bilisel_Psikoloji_Kursusu": (
                "Kronik stres tepkisi: Süregelen tehdit algısı "
                "HPA eksenini aktif tutuyor, kortizol yüksek. "
                "Öğrenme için gerekli güvenli bağlanma ortamı yok. "
                "Akademik performans düşüşü beklenen sonuç."
            ),
            "Sinif_Yonetimi_Kursusu": (
                "Güvenli şikâyet kanalı oluştur: Anonim kutu, "
                "öğretmenle bireysel check-in rutini. "
                "Sınıf iklimi değerlendirmesi (sociometri)."
            ),
            "Aile_Perspektifi": (
                "Aile bilgilendirilmeli — ancak dikkatli: "
                "Ailenin tepkisi bazen durumu kötüleştirebilir. "
                "PDR koordinasyonuyla sistematik plan yapılmalı."
            ),
        },
        "kategori": "SosyalDinamik",
        "akademik_uyari": (
            "PDR ile derhal paylaşın. "
            "Anonim şikâyet kanalı açın. "
            "Aile ile koordineli bilgilendirme yapın. "
            "Oturma düzenini revize edin."
        ),
        "aciliyet": "ACİL",
    },

    # ══════════════════════════════════════════════════════════════
    #  BÖLÜM 5 — PARILTILI, GÜÇLÜ VE SIRA DIŞI PROFILLER
    # ══════════════════════════════════════════════════════════════

    "hikaye_anlatan_ama_yazan_degil": {
        "ogretmen_metni": (
            "Sözel olarak harikulade hikâyeler anlatıyor; "
            "kişi, mekân, olay örgüsü mükemmel kurgulanmış. "
            "Yazmaya geçince metin iki cümleye iniyor."
        ),
        "fakulte_analizi": {
            "Bilisel_Psikoloji_Kursusu": (
                "Gardner (Sözel-Dilsel Zeka): Sözel kanal güçlü; "
                "yazılı çıktı kanalında güçlük var. Bilgi var, "
                "aktarım aracı sorunlu. Çift kodlama teorisi "
                "(Paivio): Sözel bellekten yazılı üretime "
                "geçiş mekanizması yeterince otomasyona ulaşmamış."
            ),
            "Ozel_Egitim_Kursusu": (
                "Disgrafya veya çalışma belleği + grafomotor "
                "koordinasyon güçlüğü şüphesi. "
                "Ayrıca yazma kaygısı hikâyeyi kısa tutturuyor olabilir."
            ),
            "Program_ve_Ogretim_Kursusu": (
                "Ses kaydı ile ödev teslimi, sesli dikte, "
                "zihin haritasından yazıya köprü stratejisi. "
                "Önce sözlü anlat, sonra yaz — zinciri kır."
            ),
            "Olcme_Degerlendirme_Kursusu": (
                "Sözlü performans değerlendirmesi bu öğrencinin "
                "gerçek yazma potansiyelini ortaya çıkarır. "
                "Yazılı ürün tek geçerli ölçüt değil."
            ),
        },
        "kategori": "ParıltıVeÜstünlük",
        "akademik_uyari": (
            "Ses kaydı ve dikte uygulamaları başlatın. "
            "Yaratıcı yazma yarışmalarına sözlü kategoriyle katılın. "
            "Disgrafya şüphesinde RAM sevki."
        ),
        "aciliyet": "ORTA",
    },

    "sanat_dersinde_dunyayi_unutan_cocuk": {
        "ogretmen_metni": (
            "Diğer derslerde arka sırada uyuşuk ve kopuk. "
            "Görsel Sanatlar dersinde gözleri parlıyor, "
            "zil çalsa bile fırçasını bırakmıyor. "
            "Ürettiği işler yaşına göre olağanüstü."
        ),
        "fakulte_analizi": {
            "Bilisel_Psikoloji_Kursusu": (
                "Csikszentmihalyi (Akış / Flow): Yalnızca "
                "görsel sanatlar alanında 'akış' deneyimi yaşıyor. "
                "Bu alanda meydan okuma-beceri dengesi optimal; "
                "diğer derslerde bu denge yok."
            ),
            "Gardner_Perspektifi": (
                "Baskın Uzamsal-Görsel Zeka: Diğer derslerin "
                "öğretim modalitesi (sözel/sembolik) bu "
                "öğrencinin birincil işleme kanalıyla örtüşmüyor. "
                "Görsel materyal entegrasyonu diğer derslerde "
                "bağlılığı artırabilir."
            ),
            "Program_ve_Ogretim_Kursusu": (
                "Sanat entegrasyonlu öğretim (arts integration): "
                "Matematik geometri, Türkçe illüstrasyon, Fen "
                "diyagramları bu öğrenci için "
                "giriş kapısı olabilir."
            ),
            "PDR_Kursusu": (
                "Bu güçlü ilgiyi kariyer farkındalığı ile "
                "ilişkilendir (ilköğretimde kariyer eğitimi "
                "erken tutum oluşturur). "
                "Sanat yeteneğini BİLSEM veya sanat liseleri "
                "bağlamında aile ile paylaş."
            ),
        },
        "kategori": "ParıltıVeÜstünlük",
        "akademik_uyari": (
            "Sanat entegrasyonlu ders tasarımı deneyin. "
            "BİLSEM Görsel Sanatlar alanı için yönlendirme. "
            "Diğer derslerde görsel materyal ağırlığını artırın."
        ),
        "aciliyet": "DÜŞÜK",
    },

    "dogayi_ve_canliları_gozlemleyen_natüralist": {
        "ogretmen_metni": (
            "Her teneffüste bahçede böcek, bitki, kuş "
            "inceliyor. Sınıfa getirdiği doğa nesneleri "
            "hakkında ileri düzey bilgisi var. "
            "Fen dışı derslerde tamamen kopuk."
        ),
        "fakulte_analizi": {
            "Gardner_Perspektifi": (
                "Natüralist Zeka baskın: Canlı sistemleri "
                "sınıflandırma, örüntü tanıma, "
                "çevre ilişkisi kurma kapasitesi yüksek. "
                "Bu zekanın diğer derslere köprü kurma "
                "potansiyeli yüksek (doğadan matematik örüntüleri, "
                "biyoloji temelli Türkçe metinler)."
            ),
            "Program_ve_Ogretim_Kursusu": (
                "Dewey (Deneyim ve Doğa): Sınıf dışı öğrenme "
                "ortamları bu öğrenci için dönüştürücü. "
                "Proje tabanlı öğrenme, doğa gözlem defteri, "
                "küçük tarla/sera projesi."
            ),
            "PDR_Kursusu": (
                "Doğa sevgisi kariyer yönelimi için erken sinyal: "
                "Biyoloji, çevre mühendisliği, veterinerlik, "
                "ekoloji alanlarına yönlendirme. "
                "İlgi = motivasyon köprüsü."
            ),
            "Bilisel_Psikoloji_Kursusu": (
                "İçsel merak odaklı öğrenme (Curiosity-Driven "
                "Learning): Motivasyon tamamen içsel; "
                "dışsal ödül iç motivasyonu baskılayabilir "
                "(Deci & Ryan — SDT over-justification etkisi). "
                "Ödül sistemi dikkatle kurgulanmalı."
            ),
        },
        "kategori": "ParıltıVeÜstünlük",
        "akademik_uyari": (
            "Doğa günlüğü projesi başlatın. "
            "Fen dersi liderliği verin. "
            "BİLSEM Fen alanı için yönlendirme değerlendirin."
        ),
        "aciliyet": "DÜŞÜK",
    },

    "matematikte_kendi_yontemini_icat_eden_cocuk": {
        "ogretmen_metni": (
            "Öğretilen algoritmayı kullanmıyor; kendi "
            "bulduğu farklı bir yöntemle doğru sonuca "
            "ulaşıyor. Yöntemi açıklatınca tutarlı "
            "ve mantıklı bir sistem ortaya çıkıyor."
        ),
        "fakulte_analizi": {
            "Bilisel_Psikoloji_Kursusu": (
                "Yaratıcı / Sezgisel Matematiksel Düşünce: "
                "Öğrenci kavramsal anlayışa ulaşmış ve "
                "bunu kendi kodlama sistemiyle temsil ediyor. "
                "Bu, öğretilen prosedürün ötesinde "
                "derin anlama kanıtı (Sfard, 1991)."
            ),
            "Ozel_Egitim_Kursusu": (
                "Üstün Matematiksel Yetenek sinyali. "
                "Dyscalculia ile kafa karıştırılmamalı — "
                "dyscalculia'da kendi yöntem üretme görülmez."
            ),
            "Program_ve_Ogretim_Kursusu": (
                "Yapılandırmacı öğrenme (Constructivism): "
                "Öğrenci bilgiyi kendisi inşa ediyor. "
                "Bu süreci kırmak yerine destekle: "
                "'Yöntemin neden işe yarıyor?' "
                "sorusuyla matematiksel ispat zeminine taşı."
            ),
            "Olcme_Degerlendirme_Kursusu": (
                "Süreç odaklı değerlendirme şart: "
                "Yalnızca sonuca değil yönteme puan ver. "
                "Standart algoritma ısrarı bu profili köreltiyor."
            ),
        },
        "kategori": "ParıltıVeÜstünlük",
        "akademik_uyari": (
            "Yöntemi sınıfa açıklattırın — hem öğrenci "
            "hem sınıf kazanır. BİLSEM matematik alanı "
            "için değerlendirin. Yöntemi bastırmayın."
        ),
        "aciliyet": "DÜŞÜK",
    },

    # ══════════════════════════════════════════════════════════════
    #  BÖLÜM 6 — SINIF YÖNETİMİ VE ÖĞRENME ORTAMI GÖZLEM MATRİSİ
    # ══════════════════════════════════════════════════════════════

    "gruptaki_tek_konusanin_grubu_domine_etmesi": {
        "ogretmen_metni": (
            "Grup çalışmalarında bir öğrenci her şeyi yapıyor, "
            "karar veriyor, diğerleri sessizce izliyor. "
            "Grup notu yüksek ama öğrenme dağılımı yok."
        ),
        "fakulte_analizi": {
            "Program_ve_Ogretim_Kursusu": (
                "Grup çalışması tasarım hatası: Bireysel hesap "
                "verebilirlik (individual accountability) yok. "
                "Johnson & Johnson (1994) — İşbirlikli Öğrenmenin "
                "5 temel unsuru: olumlu karşılıklı bağımlılık, "
                "bireysel hesap verebilirlik, yüz yüze etkileşim, "
                "sosyal beceriler, grup sürecinin değerlendirilmesi."
            ),
            "Olcme_Degerlendirme_Kursusu": (
                "Grup notu bireysel öğrenmeyi gizliyor. "
                "Hem grup hem bireysel değerlendirme şart. "
                "Akran değerlendirme formu katkı görünürlüğünü artırır."
            ),
            "Bilisel_Psikoloji_Kursusu": (
                "Sosyal kaytarma (social loafing — Latané): "
                "Çaba bireysel tanımlanmadığında azalıyor. "
                "Her üyenin belirli parçadan sorumlu olduğu "
                "yapı kurulmalı (jigsaw yöntemi)."
            ),
            "PDR_Kursusu": (
                "Domine eden öğrenci için: Liderlik enerjisini "
                "yönetmeyi öğrenmeli. Sessiz kalan öğrenciler için: "
                "Katılmama alışkanlığı öz-yeterliliği erozyon. "
                "Her iki profil ayrı müdahale gerektiriyor."
            ),
        },
        "kategori": "SınıfYönetimi",
        "akademik_uyari": (
            "Jigsaw yöntemi veya rol belirleme (raportör, "
            "sorgulayıcı, yazıcı) kullanın. "
            "Hem grup hem bireysel değerlendirme ekleyin."
        ),
        "aciliyet": "DÜŞÜK",
    },

    "ders_basinda_donme_rituel": {
        "ogretmen_metni": (
            "Her ders başında kalemini bulmak, defterini "
            "açmak, oturmak gibi basit rutinleri yapamamış "
            "gibi 5-10 dakika harcıyor. Ders sonuna kadar "
            "ısınamıyor."
        ),
        "fakulte_analizi": {
            "Ozel_Egitim_Kursusu": (
                "DEHB başlangıç güçlüğü (initiation deficit): "
                "Görev başlatma yürütücü işlev bileşeninin zayıflığı. "
                "Doğrudan DEHB'i işaret etmez ama "
                "değerlendirme listesine alınmalı."
            ),
            "Bilisel_Psikoloji_Kursusu": (
                "Geçiş maliyeti (task-switching cost — Monsell): "
                "Önceki aktivite (teneffüs, önceki ders) "
                "bilişsel olarak kapatılamamış; yeni göreve "
                "kaynak tahsisi gecikiyor."
            ),
            "Sinif_Yonetimi_Kursusu": (
                "Ders girişi ritüeli tasarımı: "
                "İlk 3 dakika sabit aktivite (journal, warm-up sorusu, "
                "sessiz okuma) geçiş maliyetini azaltır "
                "ve tüm sınıf için faydalı."
            ),
            "Program_ve_Ogretim_Kursusu": (
                "Montessori (Hazırlık Ortamı): Malzemelerin "
                "sıralı ve erişilebilir hazır olması "
                "başlama güçlüğünü azaltır. "
                "Görsel ders başlangıç kontrol listesi."
            ),
        },
        "kategori": "SınıfYönetimi",
        "akademik_uyari": (
            "Ders başı 3 dakika sabit ritüel ekleyin. "
            "Bireysel görsel kontrol listesi (araçlar hazır mı?) "
            "önerin. Kronikse DEHB değerlendirmesi."
        ),
        "aciliyet": "DÜŞÜK",
    },

    "teneffuste_arkadas_edinemeyen_cocuk": {
        "ogretmen_metni": (
            "Teneffüslerde kapı kenarında tek başına duruyor, "
            "oyun gruplarına girmeye çalışıyor ama dahil olamıyor. "
            "Üzgün ama ne yapacağını bilmiyor."
        ),
        "fakulte_analizi": {
            "PDR_Kursusu": (
                "Sosyal beceri eksikliği (social skills deficit): "
                "Gruba katılma, konuşma başlatma ve sürdürme "
                "becerileri gelişmemiş. "
                "Elliot & Gresham Sosyal Beceri Değerlendirme "
                "Sistemi ile profil çıkarılabilir."
            ),
            "Bilisel_Psikoloji_Kursusu": (
                "Sosyal bilgi işleme zayıflığı: "
                "Gruba katılma fırsatlarını tanıyamıyor, "
                "uygun giriş cümleleri repertuarı yok. "
                "Bilgi var ama uygulama bağlamsal."
            ),
            "Ozel_Egitim_Kursusu": (
                "Sosyal-pragmatik iletişim güçlüğü veya "
                "hafif OSB spektrum değerlendirmesi yapılabilir; "
                "ancak çekingen/içe dönük kişilik özelliğiyle "
                "kafa karıştırılmamalı."
            ),
            "Sinif_Yonetimi_Kursusu": (
                "Yapılandırılmış teneffüs: Öğretmen gözetiminde "
                "kural odaklı oyun grupları, "
                "yönlendirilmiş sosyal aktiviteler "
                "bu öğrenci için güvenli pratik alanı. "
                "'Teneffüs koçluğu' kavramı."
            ),
        },
        "kategori": "SosyalDinamik",
        "akademik_uyari": (
            "PDR sosyal beceri grubu önerin. "
            "Yapılandırılmış teneffüs aktiviteleri tasarlayın. "
            "Güçlü yönüyle sınıf içinde sosyal statü kazandırın."
        ),
        "aciliyet": "ORTA",
    },

    "derste_konuşmayan_evde_çok_konuşan": {
        "ogretmen_metni": (
            "Sınıfta hiç konuşmuyor, soru sorulduğunda "
            "başını eğiyor. Ailesi 'evde çok konuşuyor, "
            "duramıyoruz' diyor."
        ),
        "fakulte_analizi": {
            "PDR_Kursusu": (
                "Seçici Dilsizlik (Selective Mutism): "
                "Bağlamsal konuşma inhibisyonu — yabancı/sosyal "
                "baskı ortamında konuşma tamamen bloke oluyor. "
                "DSM-5 Kaygı Bozuklukları kategorisinde yer alır. "
                "Psikolog/psikiyatrist değerlendirmesi gerekli."
            ),
            "Bilisel_Psikoloji_Kursusu": (
                "Amigdala aktivasyonu sosyal tehdit algısıyla "
                "tetikleniyor; dil üretimi cortex'ten gelen "
                "inhibitör sinyallerle bloke ediliyor. "
                "Zorlaştırmak semptomları şiddetlendirir."
            ),
            "Sinif_Yonetimi_Kursusu": (
                "Sözlü katılımı zorunlu tutmayın. "
                "Yazılı cevap, işaret, kağıda yazma "
                "gibi alternatif katılım kanalları açın. "
                "Güvenli ortam inşası zaman alır — sabır."
            ),
            "Program_ve_Ogretim_Kursusu": (
                "Kademeli maruz bırakma (fading): "
                "Fısıldama, iki kişilik grup, daha büyük grup "
                "sıralamasıyla konuşma alanını kademeli genişlet. "
                "Başarılı her adımı sessizce pekiştir."
            ),
        },
        "kategori": "ÖzelEğitimŞüphesi",
        "akademik_uyari": (
            "Sözlü katılım zorlaması yapmayın. "
            "Seçici Dilsizlik için psikiyatri/psikoloji sevki. "
            "Alternatif katılım kanalları açın."
        ),
        "aciliyet": "YÜKSEK",
    },

    # ══════════════════════════════════════════════════════════════
    #  BÖLÜM 7 — ÖZEL EĞİTİM VE GELİŞİMSEL DEĞERLENDİRME
    # ══════════════════════════════════════════════════════════════

    "goz_temas_eksikligi_ve_rutin_bagimlilik": {
        "ogretmen_metni": (
            "Göz teması kurmaktan kaçınıyor, "
            "günlük rutin değiştiğinde yoğun kaygı "
            "ve öfke tepkisi veriyor. Belirli nesnelere "
            "aşırı bağlılık gösteriyor."
        ),
        "fakulte_analizi": {
            "Ozel_Egitim_Kursusu": (
                "Otizm Spektrum Bozukluğu (OSB) değerlendirmesi: "
                "Göz teması güçlüğü, rutin/öngörülebilirlik ihtiyacı "
                "ve kısıtlı/tekrarlayıcı davranışlar üç temel kriter. "
                "M-CHAT veya CARS ile ön değerlendirme, "
                "ardından RAM/klinik psikoloji sevki."
            ),
            "Bilisel_Psikoloji_Kursusu": (
                "Merkezi tutarlılık teorisi (Frith): "
                "Detay odaklı işleme güçlü, "
                "bütünleştirici bağlam işleme zayıf. "
                "Bu bağlantısallık biçimi belirli alanlarda "
                "(örüntü, detay) olağanüstü performans üretebilir."
            ),
            "Sinif_Yonetimi_Kursusu": (
                "Rutin ve öngörülebilirlik bu öğrenci için "
                "işlevsel koşul: Günlük program görünür "
                "ve tutarlı olmalı. Değişiklikler önceden "
                "sözlü ve görsel olarak hazırlanmalı."
            ),
            "PDR_Kursusu": (
                "Aile eğitimi kritik: OSB farkındalığı, "
                "evde yapı ve destek sistemleri. "
                "Erken müdahale = en güçlü etki."
            ),
        },
        "kategori": "ÖzelEğitimŞüphesi",
        "akademik_uyari": (
            "RAM sevki öncelikli. Beklerken: Günlük "
            "görsel program, değişiklik öncesi uyarı, "
            "rutin tutarlılığı. Zorlamak kaygıyı artırır."
        ),
        "aciliyet": "ACİL",
    },

    "konusma_gecikmesi_ve_basit_komutlarda_zorluk": {
        "ogretmen_metni": (
            "İki kelimelik basit yönergeleri bile "
            "anlamıyor gibi görünüyor, çok az kelime "
            "kullanıyor, ifadesi yetersiz."
        ),
        "fakulte_analizi": {
            "Ozel_Egitim_Kursusu": (
                "Dil gelişim gecikmesi veya Dil Bozukluğu: "
                "Alıcı dil (anlama) ve/veya ifade edici dil "
                "(konuşma üretimi) etkilenmiş. "
                "Dil-Konuşma Terapisti değerlendirmesi şart. "
                "İşitme kaybı dışlanmalı (odyoloji testi)."
            ),
            "Bilisel_Psikoloji_Kursusu": (
                "İşitsel işleme bozukluğu (APD) ayırıcı tanısı: "
                "İşitme testi normal çıksa da merkezi işitsel "
                "korteks bilgiyi doğru çözümlemiyor olabilir. "
                "Gürültülü ortamda yönerge anlamak zorlaşıyor."
            ),
            "Program_ve_Ogretim_Kursusu": (
                "Görsel destekler (resimli yönergeler, "
                "semboller) sözlü yetersizliği telafi eder. "
                "Total Communication yaklaşımı: "
                "söz + jest + görsel eş zamanlı kullan."
            ),
            "PDR_Kursusu": (
                "Dil güçlüğü sosyal katılımı, öz-saygıyı "
                "ve akran ilişkilerini olumsuz etkiliyor. "
                "Erken müdahale kritik — gecikme kümülatiF."
            ),
        },
        "kategori": "ÖzelEğitimŞüphesi",
        "akademik_uyari": (
            "İşitme testi ve DKT (Dil-Konuşma Terapisti) "
            "değerlendirmesi için RAM sevki. "
            "Görsel yönergeler hemen başlatın."
        ),
        "aciliyet": "ACİL",
    },

    "keskin_isitsel_bellek_ama_gorsel_hafiza_sifir": {
        "ogretmen_metni": (
            "Bir kez duyduğu şarkıyı veya şiiri "
            "hafızasına kazıyor; panoya bir kez yazılan "
            "bilgiyi ise hiç hatırlamıyor."
        ),
        "fakulte_analizi": {
            "Bilisel_Psikoloji_Kursusu": (
                "Bellek modalitesi asimetrisi: "
                "İşitsel-sözel bellek olağanüstü güçlü, "
                "görsel-uzamsal bellek zayıf. "
                "Bu öğrenci için optimal öğrenme kanalı "
                "işitsel sunumdur (podcast, sesli kitap, "
                "sözel tartışma)."
            ),
            "Program_ve_Ogretim_Kursusu": (
                "Modalite eşleştirme (modality matching): "
                "Ders materyallerini sesli format, "
                "ritimli tekrar, söylenerek öğrenme "
                "biçimiyle sun. Görsel bilgileri "
                "sesle eşleştirerek çift kodla."
            ),
            "Olcme_Degerlendirme_Kursusu": (
                "Tahtaya yazılı soruların yanı sıra "
                "sözlü yönerge de ver. "
                "Yazılı sınavda dezavantajlı; sözlü ölçme "
                "gerçek bilgiyi daha güvenilir ölçer."
            ),
            "Ozel_Egitim_Kursusu": (
                "Görsel işleme güçlüğü (Visual Processing "
                "Disorder) şüphesi: Görsel hafıza, görsel "
                "sıralama ve görsel-uzamsal işleme "
                "nöropsikologla değerlendirilmeli."
            ),
        },
        "kategori": "ÖğrenmeTarzı",
        "akademik_uyari": (
            "İşitsel kanalı ön plana alın: Sesli ders, "
            "ritimli tekrar, podcast formatı. "
            "Görsel işleme değerlendirmesi planlayın."
        ),
        "aciliyet": "ORTA",
    },

    # ══════════════════════════════════════════════════════════════
    #  BÖLÜM 8 — ÖLÇME-DEĞERLENDİRME PARADOKSLARI
    # ══════════════════════════════════════════════════════════════

    "homeworku_mukemmel_sinav_cok_dusuk": {
        "ogretmen_metni": (
            "Ev ödevleri her zaman eksiksiz ve çok iyi. "
            "Sınav kağıdı çok düşük not. İkisi arasındaki "
            "makas büyüdükçe şüpheleniyor."
        ),
        "fakulte_analizi": {
            "Olcme_Degerlendirme_Kursusu": (
                "Ödev geçerliliği sorusu: Ev ödevi kim yapıyor? "
                "Kaynakla (aile/internet) desteklenmiş performans "
                "sınıf performansından ayrışıyor. "
                "Ödev ve sınav korelasyonu sistematik biçimde "
                "izlenmeli; düşük korelasyon alarm sinyali."
            ),
            "PDR_Kursusu": (
                "Sınav kaygısı veya test alma stratejisi eksikliği: "
                "Bilgi var ama sınav koşullarında erişim bloke. "
                "Ayrıca kopya/yardım alma davranışı "
                "dürüstlük ve etik konuşması gerektiriyor."
            ),
            "Program_ve_Ogretim_Kursusu": (
                "Ödev formatını çeşitlendir: "
                "Sınıfta anlık kısa yazma görevleri, "
                "exit ticket, mini quiz ile "
                "gerçek edinim düzeyi görünür kılınmalı."
            ),
            "Sinif_Yonetimi_Kursusu": (
                "Yargılamadan önce nedenini araştır: "
                "Öğrenci belki aileyle birlikte yapıyor. "
                "Bu patoloji olmayabilir — "
                "eğitim-aile işbirliği de olabilir. "
                "Bağlamı anla, sonra değerlendir."
            ),
        },
        "kategori": "ÖlçmeDeğerlendirme",
        "akademik_uyari": (
            "Sınıf içi kısa anlık değerlendirmeler ekleyin. "
            "Sınav kaygısı için PDR görüşmesi önerin. "
            "Ödev formatını çeşitlendirin."
        ),
        "aciliyet": "ORTA",
    },

    "bilen_ama_yanlis_yazdigini_fark_etmeyen": {
        "ogretmen_metni": (
            "Doğru cevabı biliyor, sesli söylüyor. "
            "Ama kağıda yazarken farklı bir şey yazıyor "
            "ve fark etmiyor. Kendi kağıdını okuduğunda "
            "da yanlışı görmüyor."
        ),
        "fakulte_analizi": {
            "Bilisel_Psikoloji_Kursusu": (
                "Grafomotor ve bilişsel çıktı ayrışması: "
                "Zihinsel temsil (doğru) ile motor çıktı "
                "(hatalı) arasında izleme mekanizması çalışmıyor. "
                "Öz-izleme (self-monitoring) ve revizyona "
                "odaklanmış metakognitif eğitim gerekiyor."
            ),
            "Ozel_Egitim_Kursusu": (
                "Disgrafya veya Görsel-Motor Entegrasyon "
                "Güçlüğü: Beery VMI testi ile "
                "görsel-motor koordinasyon değerlendirilebilir. "
                "Ayrıca yazım sonrası okuma güçlüğü "
                "ayrı bir profil işaret ediyor olabilir."
            ),
            "Program_ve_Ogretim_Kursusu": (
                "Yazı denetleme stratejisi öğret: "
                "Yaz → oku → karşılaştır → düzelt. "
                "Renkli kalemle hata işaretleme rutini. "
                "Sesli okuma ile yazıyı denetleme."
            ),
            "Olcme_Degerlendirme_Kursusu": (
                "Bu öğrenciyi yalnızca yazılı ürünle "
                "değerlendirmek adil değil. "
                "Sözlü cevapla yazılı cevabın karşılaştırılması "
                "gerçek bilgi düzeyini ortaya çıkarır."
            ),
        },
        "kategori": "BilişselGüçlük",
        "akademik_uyari": (
            "Yazı denetleme protokolü öğretin. "
            "Sözlü ek değerlendirme yapın. "
            "VMI testi için RAM referansı verin."
        ),
        "aciliyet": "ORTA",
    },

    # ══════════════════════════════════════════════════════════════
    #  BÖLÜM 9 — AİLE VE ÇEVRE KAYNAKLI GÖZLEMLER
    # ══════════════════════════════════════════════════════════════

    "pazartesi_sabahi_singin_ve_dusgun": {
        "ogretmen_metni": (
            "Her Pazartesi belirgin biçimde sinkin, "
            "yorgun ve bazen ağlamaklı geliyor. "
            "Hafta ortasına doğru normale dönüyor."
        ),
        "fakulte_analizi": {
            "PDR_Kursusu": (
                "Hafta sonu aile ortamından "
                "'dekompresyon' ihtiyacı: Ev ortamı "
                "stresli veya öngörülemez. "
                "Çocuk okulu güvenli alan olarak kullanıyor, "
                "hafta sonu bu güven ortamından uzak. "
                "Bronfenbrenner (Mikrosistem): Ev ortamı "
                "baskın olumsuz etkisi."
            ),
            "Aile_Perspektifi": (
                "Hafta sonu rutininin istikrarı ve "
                "güvenlik hissi sorgulanmalı. "
                "Boşanma süreci, alkol/bağımlılık, "
                "kronik çatışma, ihmal profilleri "
                "dikkatli ve sistematik araştırılmalı. "
                "Okul sosyal hizmeti veya PDR aracılık yapmalı."
            ),
            "Sinif_Yonetimi_Kursusu": (
                "Pazartesi sabahı öğrenciye özel, "
                "sessiz ve düşük baskılı karşılama rutini. "
                "Sıcak, yargısız bir ilk temas "
                "dönüşümü hızlandırır."
            ),
            "Bilisel_Psikoloji_Kursusu": (
                "Kronik stres + yetersiz uyku "
                "bilişsel kapasite profilini etkiliyor: "
                "Pazartesi günü bu öğrencide "
                "yüksek bilişsel yük gerektiren "
                "görevler başarısızlıkla sonuçlanır."
            ),
        },
        "kategori": "AileVeÇevre",
        "akademik_uyari": (
            "PDR ile paylaşın. "
            "Pazartesi sabahı düşük stresli rutin uygulayın. "
            "Ev ortamını araştırmak için dikkatli aile görüşmesi."
        ),
        "aciliyet": "YÜKSEK",
    },

    "cok_kirli_yorgun_ve_bakimsiz_gelen_cocuk": {
        "ogretmen_metni": (
            "Giysiler kirli, saçlar bakımsız, "
            "zaman zaman aç geldiğini söylüyor. "
            "Kıyafetler mevsime uygun değil."
        ),
        "fakulte_analizi": {
            "PDR_Kursusu": (
                "İhmal (Neglect) şüphesi: Fiziksel "
                "ihmalin temel göstergeleri. "
                "Zorunlu ihbar yükümlülüğü: "
                "Öğretmen olarak çocuğu koruma "
                "göreviniz var — ŞÖNİM/İl Müdürlüğü "
                "bilgilendirilmeli. PDR koordinasyonu."
            ),
            "Aile_Perspektifi": (
                "İhmal ekonomik kaynaklı da olabilir "
                "(farkında ihmal): Aile maddi sıkıntı, "
                "bilgisizlik veya tükenmişlik nedeniyle "
                "gereksinimleri karşılayamıyor. "
                "Sosyal hizmet desteği harekete geçirilmeli."
            ),
            "Bilisel_Psikoloji_Kursusu": (
                "Maslow (İhtiyaçlar Hiyerarşisi): "
                "Fizyolojik ihtiyaçlar (beslenme, ısınma, temizlik) "
                "karşılanmadan bilişsel öğrenme gerçekleşemez. "
                "Akademik müdahale ikincil; önce güvenli yaşam."
            ),
            "Sinif_Yonetimi_Kursusu": (
                "Öğrencinin onurunu koruyarak destek: "
                "Sınıf önünde dikkat çekmeden "
                "öğle yemeği, yedek malzeme, "
                "giysi desteği organize et."
            ),
        },
        "kategori": "AileVeÇevre",
        "akademik_uyari": (
            "ZORUNLU İHBAR: PDR ve okul yöneticisiyle "
            "derhal görüşün. ŞÖNİM/Sosyal Hizmetler "
            "bilgilendirilmeli. Öğrencinin onurunu koruyun."
        ),
        "aciliyet": "ACİL",
    },

    "ebeveyn_dersi_yaptiran_cocuk": {
        "ogretmen_metni": (
            "Ebeveyn her akşam dersi anlattığını "
            "söylüyor. Öğrenci sınıfta her şeyi biliyor "
            "gibi görünüyor ama kendi başına yapamıyor."
        ),
        "fakulte_analizi": {
            "Program_ve_Ogretim_Kursusu": (
                "Bağımlı uygulama tuzağı: "
                "Öğrenci bağımsız uygulama yapmıyor. "
                "Vygotsky ZPD: Sürekli destekle yapma, "
                "bağımsız yapma evresine geçişi engelliyor. "
                "'İskele' kalıcılaşıyor, 'fading' yok."
            ),
            "PDR_Kursusu": (
                "Ebeveyn kaygısı veya mükemmeliyetçilik: "
                "Aile çocuğun başarısızlığını tolere "
                "edemiyor; çocuğun özerkliğini "
                "farkında olmadan baltalıyor."
            ),
            "Olcme_Degerlendirme_Kursusu": (
                "Ev performansı ile sınıf performansı "
                "arasındaki makas büyüdükçe ödev "
                "geçerliliği sorgulanabilir. "
                "Sınıf içi bağımsız ölçme araçları "
                "gerçek düzeyi ortaya çıkarır."
            ),
            "Aile_Perspektifi": (
                "Aile görüşmesinde mesaj: "
                "'Hata yapmasına izin verin — "
                "hata öğrenmenin motoru.' "
                "Ebeveyne Vygotsky'nin 'fading' ilkesini "
                "pratik dilde açıkla."
            ),
        },
        "kategori": "AileVeÇevre",
        "akademik_uyari": (
            "Aile görüşmesinde 'hata toleransı' konuşun. "
            "Sınıf içi bağımsız ölçme artırın. "
            "Ev ödevini 'deneme-yanılma' bağlamına çekin."
        ),
        "aciliyet": "ORTA",
    },

    # ══════════════════════════════════════════════════════════════
    #  BÖLÜM 10 — SIKÇA GÖRÜLEN SAĞLIK VE GELİŞİMSEL GÖZLEMLER
    # ══════════════════════════════════════════════════════════════

    "gozlerini_kisiyor_ve_tahtaya_yaklasıyor": {
        "ogretmen_metni": (
            "Tahtayı okumak için gözlerini kısıyor, "
            "öne doğru eğiliyor veya kalkıp yaklaşıyor. "
            "Sınıf arkasından tahtayı okuyamıyor."
        ),
        "fakulte_analizi": {
            "PDR_Kursusu": (
                "Görme bozukluğu (miyopi) şüphesi: "
                "Temel sağlık ihtiyacı. "
                "Ailenin gözlükçü veya göz doktoru "
                "ziyareti için bilgilendirilmesi şart."
            ),
            "Bilisel_Psikoloji_Kursusu": (
                "Görme güçlüğü tüm görsel işleme "
                "görevlerinde bilişsel yükü artırıyor: "
                "Okuma, yazma takibi, şekil görme "
                "hepsi zorlaşıyor. Akademik performans "
                "dolaylı biçimde etkileniyor."
            ),
            "Sinif_Yonetimi_Kursusu": (
                "Öğrenciyi tahtaya yakın oturtur. "
                "Büyük fontlu materyal kullanır. "
                "Yazılı materyalin fotokopisi verilebilir."
            ),
            "Olcme_Degerlendirme_Kursusu": (
                "Görme güçlüğü giderilmeden yapılan "
                "değerlendirme geçersiz: Hata görme "
                "güçlüğünden mi yoksa bilgisizlikten mi? "
                "Ayrıştırılmalı."
            ),
        },
        "kategori": "SağlıkVeGelişim",
        "akademik_uyari": (
            "Aileyi göz muayenesi için yönlendirin. "
            "Beklerken öne oturtur, büyük font kullanın. "
            "Müdahale edilmezse akademik kayıp büyür."
        ),
        "aciliyet": "YÜKSEK",
    },

    "sik_kulak_enfeksiyonu_ve_anlamama": {
        "ogretmen_metni": (
            "Ailesinden sık kulak enfeksiyonu geçirdiğini "
            "öğrendik. Yüksek sesle konuşunca anlıyor, "
            "normal seste yanıt vermiyor."
        ),
        "fakulte_analizi": {
            "Ozel_Egitim_Kursusu": (
                "İletim tipi işitme kaybı şüphesi: "
                "Tekrarlayan orta kulak enfeksiyonları "
                "iletimsel işitme kaybına yol açabilir. "
                "Odyoloji testi şart. "
                "İşitme cihazı veya cerrahi tedavi gerekebilir."
            ),
            "Bilisel_Psikoloji_Kursusu": (
                "İşitsel işleme güçlüğü: "
                "Fonolojik farkındalık ve harf-ses "
                "eşleştirmesi olumsuz etkileniyor; "
                "okuma-yazma edinimi yavaşlıyor."
            ),
            "Program_ve_Ogretim_Kursusu": (
                "Görsel destekler, yazılı yönergeler, "
                "öğrenciye yakın konuşma, "
                "mikrofonlu ses sistemi (okul imkânına göre). "
                "FM sistemi desteği değerlendirilebilir."
            ),
            "PDR_Kursusu": (
                "Tanılanmamış işitme kaybı "
                "öz-yeterlilik ve sosyal ilişkileri "
                "ciddi biçimde etkiliyor. "
                "Arkadaşları 'anlamıyor' diye dışlıyor olabilir."
            ),
        },
        "kategori": "SağlıkVeGelişim",
        "akademik_uyari": (
            "Odyoloji testi için aileyi yönlendirin — ACİL. "
            "Beklerken: Öne oturtur, yüz yüze konuşun, "
            "görsel yönergeler kullanın."
        ),
        "aciliyet": "ACİL",
    },

    "cok_yorulup_uyuyan_ve_enerji_dalgalanmasi": {
        "ogretmen_metni": (
            "Bir gün enerjik, ertesi gün letarjik. "
            "Özellikle öğleden sonra masaya yatıyor, "
            "konsantre olamıyor. Zaman zaman başı dönüyor."
        ),
        "fakulte_analizi": {
            "PDR_Kursusu": (
                "Tıbbi değerlendirme öncelikli: "
                "Tiroid fonksiyon bozukluğu, anemi, "
                "kan şekeri düzensizliği (diyabet şüphesi), "
                "uyku apnesi gibi tıbbi durumlar "
                "bu tabloyu açıklayabilir. "
                "Aile pediyatri yönlendirmesi şart."
            ),
            "Bilisel_Psikoloji_Kursusu": (
                "Enerji dalgalanması → dikkat ve "
                "çalışma belleği dalgalanması → "
                "performans tutarsızlığı. "
                "Öğrencinin en verimli saatine "
                "kritik öğrenme görevlerini yerleştir."
            ),
            "Aile_Perspektifi": (
                "Uyku düzeni, beslenme alışkanlıkları "
                "ve günlük rutin hakkında aile ile "
                "görüşme. Ev faktörü tıbbi faktörden "
                "ayrıştırılmalı."
            ),
            "Sinif_Yonetimi_Kursusu": (
                "Hareketsiz oturma sürelerini kır: "
                "5-7 dakikada bir kısa hareket moltası. "
                "Öğleden sonra açık hava, ışık veya "
                "fiziksel aktivite dikkat sistemini yeniler."
            ),
        },
        "kategori": "SağlıkVeGelişim",
        "akademik_uyari": (
            "Pediyatri değerlendirmesi için aileyi yönlendirin. "
            "Beklerken: kritik görevleri sabah saatlerine alın, "
            "hareket molası ekleyin."
        ),
        "aciliyet": "YÜKSEK",
    },

    # ══════════════════════════════════════════════════════════════
    #  BÖLÜM 11 — ÖĞRETMEN-ÖĞRENCİ İLİŞKİ DİNAMİKLERİ
    # ══════════════════════════════════════════════════════════════

    "sadece_bu_ogretmenle_cok_iyi_calisan_cocuk": {
        "ogretmen_metni": (
            "Geçen yıl çok sorunluydu. Bu yıl yanımda "
            "çiçek gibi açıldı. Diğer öğretmenlerde "
            "hâlâ sorun yaşıyor."
        ),
        "fakulte_analizi": {
            "PDR_Kursusu": (
                "Güvenli bağlanma ilişkisi (Bowlby): "
                "Bu öğretmen bu öğrenci için "
                "'güvenli üs' işlevi görüyor. "
                "Bağlanma figürü değişince öğrenme "
                "kapasitesi değişiyor — akademik performans "
                "bağlanma güvenliğine koşullu."
            ),
            "Sinif_Yonetimi_Kursusu": (
                "İlişki temelli sınıf yönetimi (Pianta): "
                "Öğretmen-öğrenci ilişkisi kalitesi "
                "akademik çıktının en güçlü yordayıcılarından. "
                "Bu öğretmenin ne yaptığını belgele "
                "ve aktarılabilir pratikler olarak adlandır."
            ),
            "Program_ve_Ogretim_Kursusu": (
                "Diğer öğretmenlere köprü kur: "
                "Neyin işe yaradığını (hangi dil, "
                "hangi ödül, hangi yaklaşım) yazılı "
                "olarak geçiş dosyasına ekle."
            ),
            "Bilisel_Psikoloji_Kursusu": (
                "Güvenli ortamda amigdala aktivasyonu düşük, "
                "prefrontal korteks kapasitesi yüksek. "
                "Öğrenme nörobiyolojik olarak güvenlik "
                "hissine bağlı (Siegel — mindsight)."
            ),
        },
        "kategori": "ÖğretmenÖğrenciDinamiği",
        "akademik_uyari": (
            "İşe yarayanları belgeleyin ve "
            "sonraki öğretmene yazılı geçiş raporu hazırlayın. "
            "PDR ile güvenli bağlanma stratejilerini paylaşın."
        ),
        "aciliyet": "DÜŞÜK",
    },

    "ogretmenden_belirgin_bicimde_korkan_cocuk": {
        "ogretmen_metni": (
            "Öğretmen yaklaştığında kasılıyor, "
            "ses yükselince ağlamaklı oluyor, "
            "sürekli 'yapamıyorum' deyip özür diliyor."
        ),
        "fakulte_analizi": {
            "PDR_Kursusu": (
                "Otorite figürü kaygısı veya geçmiş travma: "
                "Evde veya önceki eğitim deneyiminde "
                "disiplin biçimi korkuya dayalı olmuş olabilir. "
                "Güvenli bağlanma örüntüsü zedelenmiş."
            ),
            "Sinif_Yonetimi_Kursusu": (
                "Ses tonu, fiziksel mesafe ve yaklaşım "
                "biçimi derhal revize edilmeli. "
                "Korku temelli öğrenme ortamı "
                "bilişsel kapasite ve öğrenme çıktısını "
                "sistemik olarak baskılıyor."
            ),
            "Bilisel_Psikoloji_Kursusu": (
                "Tehdit algısı → Amigdala aktivasyonu → "
                "Prefrontal korteks inhibisyonu → "
                "Öğrenme bloke. Korkutucu ortamda "
                "hiçbir pedagojik teknik işe yaramaz."
            ),
            "Aile_Perspektifi": (
                "Okul öncesi veya ev ortamında "
                "otoriter/cezalandırıcı yaklaşım örüntüsü var mı? "
                "PDR ile değerlendirilmeli. "
                "Gerekirse çocuk psikiyatrisi yönlendirmesi."
            ),
        },
        "kategori": "ÖğretmenÖğrenciDinamiği",
        "akademik_uyari": (
            "Yaklaşım biçimini, ses tonunu ve "
            "fiziksel mesafeyi derhal gözden geçirin. "
            "Travma şüphesinde PDR ve ailenin koordinasyonu."
        ),
        "aciliyet": "YÜKSEK",
    },

    # ══════════════════════════════════════════════════════════════
    #  BÖLÜM 12 — SINIF İKLİMİ VE GRUP DİNAMİKLERİ
    # ══════════════════════════════════════════════════════════════

    "sinifin_genel_motivasyon_dusukluğu": {
        "ogretmen_metni": (
            "Bütün sınıf isteksiz, ilgisiz. "
            "'Ne zaman biter?' sorusu her derste. "
            "Bireysel değil, kolektif motivasyon sorunu."
        ),
        "fakulte_analizi": {
            "Program_ve_Ogretim_Kursusu": (
                "Öğretim tasarımı gözden geçirilmeli: "
                "Dewey — anlam ve ilgi odaklı müfredat. "
                "Pasif alıcı rolü, tek tip sunum biçimi, "
                "öğrenci seçimi olmayan görevler "
                "kolektif motivasyon çöküşünün en yaygın nedeni."
            ),
            "Bilisel_Psikoloji_Kursusu": (
                "Deci & Ryan (SDT): Özerklik, yeterlik "
                "ve ilişkili olma ihtiyaçlarından "
                "en az biri karşılanmıyor. "
                "Öğrencilerin seçim yapabildiği, "
                "anlamlı gördüğü görevler motivasyonu artırır."
            ),
            "Sinif_Yonetimi_Kursusu": (
                "Sınıf iklimi değerlendirmesi: "
                "Öğrencilere anket uygula — "
                "'Sınıfta en sıkıldığın şey nedir?' "
                "Elde edilen veri reform için zemin sağlar."
            ),
            "PDR_Kursusu": (
                "Kolektif umutsuzluk (collective "
                "learned helplessness): "
                "Grupta 'çaba fark etmez' inancı yaygınlaşmış. "
                "Sınıf düzeyinde büyüme zihniyeti "
                "müdahalesi gerekebilir (Dweck)."
            ),
        },
        "kategori": "SınıfYönetimi",
        "akademik_uyari": (
            "Sınıfa kısa anket uygulayın. "
            "Bir sonraki ders birimini proje tabanlı "
            "ve seçim içerecek şekilde tasarlayın. "
            "Öğrenci sesini duyun."
        ),
        "aciliyet": "ORTA",
    },

    "rekabet_yuksek_isbirligi_sifir_sinif": {
        "ogretmen_metni": (
            "Çocuklar birbirinin notunu sorguluyor, "
            "birbirinin başarısına sevinemiyor, "
            "grupta çalışmak istemiyor."
        ),
        "fakulte_analizi": {
            "Program_ve_Ogretim_Kursusu": (
                "Değerlendirme sisteminin norm referanslı "
                "(sıralamaya dayalı) yapısı rekabeti "
                "doğrudan besliyor. "
                "Kriter referanslı değerlendirmeye "
                "geçiş kültürel dönüşüm başlatır."
            ),
            "PDR_Kursusu": (
                "Sosyal Karşılaştırma Teorisi (Festinger): "
                "Öğrenciler sürekli yukarı yönlü "
                "karşılaştırma yapıyor — hem özgüven hem "
                "empati zedeleniyor. "
                "SEL (Sosyal-Duygusal Öğrenme) programı gerekli."
            ),
            "Sinif_Yonetimi_Kursusu": (
                "Sınıf normunu yeniden inşa et: "
                "Bireysel değil sınıf hedefleri belirle. "
                "'Bu hafta sınıf olarak ne öğrendik?' "
                "sorusu kolektif kimliği pekiştirir."
            ),
            "Bilisel_Psikoloji_Kursusu": (
                "Dışsal ödül (not, sıralama) içsel "
                "motivasyonu baskılıyor (over-justification). "
                "Öğrenme sürecini ödüllendiren sistemler "
                "işbirliğini teşvik eder."
            ),
        },
        "kategori": "SınıfYönetimi",
        "akademik_uyari": (
            "Sınıf hedefleri oluşturun. "
            "Norm referanslı değerlendirmeyi azaltın. "
            "İşbirlikli öğrenme aktivitesi ekleyin."
        ),
        "aciliyet": "ORTA",
    },

    # ══════════════════════════════════════════════════════════════
    #  BÖLÜM 13 — DAHA FAZLA TEK NOKTA GÖZLEMİ
    # ══════════════════════════════════════════════════════════════

    "her_gun_baskasinin_kalemini_alan_cocuk": {
        "ogretmen_metni": (
            "Her gün kalemini, silgisini, defterini "
            "evde bırakıyor ve arkadaşlarından alıyor. "
            "Arkadaşlar şikâyetçi."
        ),
        "fakulte_analizi": {
            "PDR_Kursusu": (
                "Birincil ihtimaller: DEHB unutkanlığı, "
                "ekonomik yetersizlik veya ev ilgisizliği. "
                "Bunların ayrıştırılması doğru müdahaleyi belirler. "
                "Yargılamadan önce araştır."
            ),
            "Ozel_Egitim_Kursusu": (
                "Yürütücü işlev güçlüğü (planlama, "
                "hazırlık organize etme): "
                "DEHB değerlendirmesi listeye alınmalı."
            ),
            "Sinif_Yonetimi_Kursusu": (
                "Görsel çeklist (çantaya her gece bakılacak "
                "kontrol listesi) yürütücü işlev desteği. "
                "Sınıfta yedek malzeme bankası oluşturmak "
                "akran çatışmasını azaltır."
            ),
            "Aile_Perspektifi": (
                "Ekonomik ihtiyaç şüphesinde: "
                "Okul fırsatları (yardım sandığı vb.) "
                "onurunu koruyarak sunulabilir. "
                "Ailede farkındalık oluşturma."
            ),
        },
        "kategori": "SınıfYönetimi",
        "akademik_uyari": (
            "Neden araştırın. Görsel çeklist önerin. "
            "Ekonomik ihtiyaç varsa kaynak aktivasyonu. "
            "DEHB şüphesi varsa RAM yönlendirmesi."
        ),
        "aciliyet": "DÜŞÜK",
    },

    "yaratici_yazida_inanilmaz_ama_dogrusal_problemde_kaybolan": {
        "ogretmen_metni": (
            "Yaratıcı yazma görevlerinde hayranlık "
            "uyandıran eserler üretiyor. "
            "Matematik veya mantık sorularında tamamen "
            "nereye tutunacağını bilemiyor."
        ),
        "fakulte_analizi": {
            "Gardner_Perspektifi": (
                "Sözel-dilsel ve belki içsel-öze dönük "
                "zeka güçlü; mantıksal-matematiksel zeka "
                "bağıl olarak zayıf. Bilişsel profil asimetrisi."
            ),
            "Bilisel_Psikoloji_Kursusu": (
                "Anlatısal (narrative) düşünce sistemi "
                "(Bruner) baskın; paradigmatik "
                "(mantıksal-analitik) düşünce zayıf. "
                "Matematik öğretimini hikâye bağlamına "
                "koyarak anlatısal düşünce köprüsü kur."
            ),
            "Program_ve_Ogretim_Kursusu": (
                "Matematik problemlerini anlatı formatında "
                "sun: 'Ali'nin 3 elmasi vardı...' "
                "Hikâye bağlamı mantıksal yapıya köprü kurar."
            ),
            "Olcme_Degerlendirme_Kursusu": (
                "Bu öğrencinin güçlü alanı not sisteminde "
                "görünür değil. Portfolyo değerlendirme "
                "çok boyutlu resim sunar."
            ),
        },
        "kategori": "ÖğrenmeTarzı",
        "akademik_uyari": (
            "Matematik için anlatı/hikâye bağlamı kullanın. "
            "Portfolyoya yaratıcı çalışmaları ekleyin. "
            "Güçlü alanı köprü olarak değerlendirin."
        ),
        "aciliyet": "DÜŞÜK",
    },

    "koridorda_aglarken_bulunan_cocuk": {
        "ogretmen_metni": (
            "Teneffüste koridorda yalnız ve sessizce "
            "ağlarken bulundu. Sorulunca 'bir şey yok' "
            "diyor ama gözleri kırmızı."
        ),
        "fakulte_analizi": {
            "PDR_Kursusu": (
                "Acil PDR değerlendirmesi: "
                "Akran zorbalığı, aile sorunu, "
                "depresif duygu durumu veya travma işareti. "
                "'Bir şey yok' ifadesi sıkça savunma "
                "mekanizması — zorlamadan, güvenli "
                "ortamda tekrar konuş."
            ),
            "Bilisel_Psikoloji_Kursusu": (
                "Duygusal baskı bilişsel kapasite "
                "için en güçlü engel. "
                "Bu çocuğun o gün öğrenme kapasitesi "
                "ciddi biçimde baskılanmış durumdadır."
            ),
            "Sinif_Yonetimi_Kursusu": (
                "O ders için akademik baskıyı kaldır. "
                "Güvenli bağlanma sunmak "
                "akademik içerikten önce gelir."
            ),
            "Aile_Perspektifi": (
                "Gün sonu aile ile temasa geç: "
                "Hafif ve merak edici bir dil kullan, "
                "yargılamadan paylaş. "
                "Aile bilgisi var mı araştır."
            ),
        },
        "kategori": "DuyuşsalDurum",
        "akademik_uyari": (
            "PDR ile aynı gün görüşün. "
            "O ders için akademik baskıyı kaldırın. "
            "Akşam aile ile temasa geçin."
        ),
        "aciliyet": "ACİL",
    },

    "beden_egitiminde_parlayan_ama_sinifta_kaybolan": {
        "ogretmen_metni": (
            "Beden Eğitimi dersinde sınıfın tartışmasız "
            "en iyisi — koordinasyon, hız, liderlik. "
            "Sınıfta masa başında ise tamamen kaybolmuş."
        ),
        "fakulte_analizi": {
            "Gardner_Perspektifi": (
                "Bedensel-Kinestetik Zeka baskın. "
                "Sınıf ortamı bu zekanın işleyişini "
                "aktive edemiyor. Harekete dayalı "
                "öğrenme aktiviteleri entegre edilmeli."
            ),
            "Program_ve_Ogretim_Kursusu": (
                "Montessori (Hareketle Öğrenme): "
                "Sınıfta fiziksel aktivasyonlu öğrenme "
                "görevleri tasarla — dramatizasyon, "
                "manipülatif materyal, rol yapma, "
                "sınıf dışı gözlem."
            ),
            "PDR_Kursusu": (
                "Spor alanındaki yetkinlik ve liderliği "
                "kariyer farkındalığıyla ilişkilendir. "
                "Özgüveni bu alandan besleyerek "
                "akademik alana transfer denemesi yap."
            ),
            "Bilisel_Psikoloji_Kursusu": (
                "Çoklu temsil sistemi: "
                "Soyut akademik içeriği bedensel "
                "simülasyonla temsil etme "
                "(sayıları beden hareketleriyle temsil etme, "
                "tarihsel olayları dramatize etme)."
            ),
        },
        "kategori": "ÖğrenmeTarzı",
        "akademik_uyari": (
            "Hareket temelli öğrenme aktiviteleri ekleyin. "
            "Spor liderliğini sınıfa taşıyın. "
            "Güçlü öz-güveni akademik alana köprüleyin."
        ),
        "aciliyet": "DÜŞÜK",
    },

    "kardesinin_golgesi_altinda_kalan_cocuk": {
        "ogretmen_metni": (
            "Abisi/ablası aynı okulda çok başarılıydı. "
            "Öğretmenler 'kardeşin gibi olacaksın' diyor. "
            "Çocuk giderek içe çekiliyor."
        ),
        "fakulte_analizi": {
            "PDR_Kursusu": (
                "Kardeş gölgesi (sibling shadow effect): "
                "Sürekli karşılaştırma kimlik gelişimini "
                "zedeliyor (Erikson — Kimlik vs. Rol Karmaşası). "
                "'Kardeşin gibi ol' mesajı "
                "'sen yeterli değilsin' olarak işleniyor."
            ),
            "Bilisel_Psikoloji_Kursusu": (
                "Sosyal karşılaştırma (Festinger): "
                "Yukarı yönlü karşılaştırma "
                "bir kardeşle sınırlı kalmıyor, "
                "tüm sınıfla yapılır hale geliyor. "
                "Benlik saygısı sistematik aşınıyor."
            ),
            "Sinif_Yonetimi_Kursusu": (
                "Hiçbir öğrenci başkasıyla "
                "karşılaştırılmamalı — bu etik ilke. "
                "Bireysel ilerleme kıyaslaması: "
                "'Geçen aya göre sen neredesin?'"
            ),
            "Program_ve_Ogretim_Kursusu": (
                "Bu öğrenciye özgü güçlü alanlar "
                "görünür kılınmalı: "
                "Farklı bir projede ön plana çıkar. "
                "Kendine ait bir başarı anlatısı oluştur."
            ),
        },
        "kategori": "DuyuşsalDurum",
        "akademik_uyari": (
            "Kardeş karşılaştırmasını tüm öğretmenlerle "
            "konuşun — sistemik müdahale şart. "
            "Bu öğrenciye özgü güçlü alanlar inşa edin."
        ),
        "aciliyet": "ORTA",
    },

    "yabanci_uyruklu_yeni_gelen_cocuk": {
        "ogretmen_metni": (
            "Türkçe bilmiyor veya çok az biliyor. "
            "Sınıfta ne söylendiğini anlamıyor, "
            "arkadaşlarından uzak duruyor."
        ),
        "fakulte_analizi": {
            "Program_ve_Ogretim_Kursusu": (
                "İkinci Dil Edinimi (Krashen — Input Hypothesis): "
                "Anlaşılabilir girdi (i+1) prensibi: "
                "Mevcut düzeyinin biraz üstünde, "
                "bağlamdan tahmin edilebilir dil sunulmalı. "
                "Görsel destekler, işaret dili, "
                "ikili çalışmalar (aynı anadilli akran)."
            ),
            "PDR_Kursusu": (
                "Kültür şoku ve uyum süreci: "
                "Yeni ülke, yeni dil, yeni okul — "
                "üç büyük stresörün aynı anda etkisi. "
                "Temel güvenlik ve ait olma hissi "
                "akademik başarıdan önce gelir."
            ),
            "Sinif_Yonetimi_Kursusu": (
                "Buddy sistem: Destekleyici bir akran "
                "eşleştirmesi. "
                "Kültürel kökenini sınıfta değerli kıl: "
                "Ülkesini tanıtma etkinliği "
                "statü kazandırır."
            ),
            "Ozel_Egitim_Kursusu": (
                "Dil engelini öğrenme güçlüğüyle "
                "karıştırmayın: Türkçe edinimi tamamlanmadan "
                "bilişsel değerlendirme güvenilmez. "
                "En az 1-2 yıl dil edinimi için zaman tanı."
            ),
        },
        "kategori": "AileVeÇevre",
        "akademik_uyari": (
            "Buddy sistemi kurun. Görsel yönergeler. "
            "Kültürel kimliği sınıfta değerli kılın. "
            "Dil gecikmesini öğrenme güçlüğüyle karıştırmayın."
        ),
        "aciliyet": "ORTA",
    },

    "asillik_ve_kural_tanımazlık": {
        "ogretmen_metni": (
            "Kurallara uymayı reddediyor, "
            "sürekli itiraz ediyor, sınır konduğunda "
            "tırmandırıyor. Kaos çıkarmayı seviyor "
            "gibi görünüyor."
        ),
        "fakulte_analizi": {
            "PDR_Kursusu": (
                "Karşı Gelme Karşı Koyma Bozukluğu (ODD) "
                "veya otorite figürüne yönelik travma tepkisi. "
                "Çocuğun 'ne zaman' kuralı çiğnediğini "
                "gözlemle: sadece belirli kişilerle mi, "
                "tüm otoritelerle mi? "
                "Bu ayrım tanıyı belirler."
            ),
            "Bilisel_Psikoloji_Kursusu": (
                "Reaktif bağlanma veya güven kırılması: "
                "Otorite figürleri geçmişte öngörülemez "
                "davranmışsa itaatsizlik uyarlanabilir "
                "savunma mekanizmasıdır."
            ),
            "Sinif_Yonetimi_Kursusu": (
                "Güç mücadelesinden kaçın: "
                "Sınıf önünde karşı çıkmak tırmandırır. "
                "Seçim ver: 'Şimdi mi yaparsın, 5 dakika "
                "sonra mı?' Bağlantı kur, sonra düzelt "
                "(Connection before correction — Dan Siegel)."
            ),
            "Ozel_Egitim_Kursusu": (
                "ODD veya CD şüphesinde RAM/çocuk psikiyatrisi. "
                "Disiplin cezaları bu profilde "
                "davranışı pekiştiriyor, değiştirmiyor."
            ),
        },
        "kategori": "DuyuşsalDurum",
        "akademik_uyari": (
            "Güç mücadelesinden kaçının. "
            "'Connection before correction.' "
            "ODD şüphesinde RAM/çocuk psikiyatrisi sevki."
        ),
        "aciliyet": "YÜKSEK",
    },

    "hedefe_yonelik_ve_odakli_cogu_zaman_mutlu_cocuk": {
        "ogretmen_metni": (
            "Verilen ödevi titizlikle yapıyor, "
            "sorulara merakla katılıyor, "
            "hatalardan utanmıyor, "
            "yardım istemekten çekinmiyor."
        ),
        "fakulte_analizi": {
            "PDR_Kursusu": (
                "Sağlıklı psikososyal gelişim (Erikson — "
                "Çalışkanlık vs. Aşağılık Duygusu): "
                "Bu çocuk 'çalışkanlık' evresinde "
                "sağlıklı bir yerde. "
                "Güvenli bağlanma ve büyüme zihniyeti "
                "güçlü görünüyor."
            ),
            "Bilisel_Psikoloji_Kursusu": (
                "İçsel motivasyon (SDT): Özerklik, "
                "yeterlik ve bağlılık ihtiyaçları "
                "dengeli biçimde karşılanıyor. "
                "Bu profili korumak, geliştirmek kadar önemli."
            ),
            "Program_ve_Ogretim_Kursusu": (
                "Zenginleştirme görevi ver: "
                "Mevcut zorluk seviyesi "
                "'akış' deneyimini sürdüremeyecek kadar "
                "düşerse motivasyon kırılabilir."
            ),
            "Sinif_Yonetimi_Kursusu": (
                "Bu öğrenci sınıf normunu şekillendiriyor. "
                "Pozitif davranışlarını görünür kıl; "
                "sınıfın büyüme zihniyeti kültürüne "
                "katkısını fark ettir."
            ),
        },
        "kategori": "ParıltıVeÜstünlük",
        "akademik_uyari": (
            "Bu profili koru: Zorluk düzeyini artır. "
            "Sınıf modeli olarak konumlanmasına izin ver. "
            "Zenginleştirme görevi ekle."
        ),
        "aciliyet": "DÜŞÜK",
    },

    "not_icin_calisan_ama_neden_bilmeyen_cocuk": {
        "ogretmen_metni": (
            "Her sınavda en yüksek notu alıyor. "
            "'Neden öğreniyorsun?' sorusuna "
            "'not almak için' diyor. "
            "Sınav bitti mi, konuyu unutuyor."
        ),
        "fakulte_analizi": {
            "Bilisel_Psikoloji_Kursusu": (
                "Yüzeysel (surface) öğrenme stratejisi: "
                "Bilgi sınava kadar tutulmuş ama "
                "uzun süreli belleğe geçmemiş. "
                "Germane load (verimli yük) düşük — "
                "ezber baskın, anlama yok."
            ),
            "PDR_Kursusu": (
                "Deci & Ryan (SDT): Dışsal motivasyon "
                "(not) tamamen baskın; içsel motivasyon "
                "(merak, anlam) yok. "
                "Uzun vadede tükenmişlik ve "
                "'boş başarı sendromu' riski."
            ),
            "Program_ve_Ogretim_Kursusu": (
                "Değerlendirme reformu gerekiyor: "
                "Bilgiyi transfer eden, "
                "bağlantı kuran, anlam oluşturan "
                "görevler dışsal motivasyonu aşındırır, "
                "içsel motivasyona zemin hazırlar."
            ),
            "Aile_Perspektifi": (
                "Aile muhtemelen not odaklı pekiştirme "
                "uyguluyor. 'Ne öğrendin?' yerine "
                "'kaç aldın?' sorusu kültürel norm. "
                "Aile görüşmesi: not=başarı mitini sorgula."
            ),
        },
        "kategori": "DuyuşsalDurum",
        "akademik_uyari": (
            "Anlam ve transfer gerektiren görevler ekleyin. "
            "Not yerine öğrenmeyi ödüllendiren "
            "dil ve pratikler geliştirin. "
            "Aile ile motivasyon konuşması yapın."
        ),
        "aciliyet": "DÜŞÜK",
    },

    "gunluk_performans_cok_degisken_olan_cocuk": {
        "ogretmen_metni": (
            "Bugün her şeyi biliyor, yarın hiç bilmiyor. "
            "Tutarsızlık o kadar büyük ki "
            "'neyi ne zaman öğreneceğini bilmiyorum' diyorum."
        ),
        "fakulte_analizi": {
            "Ozel_Egitim_Kursusu": (
                "DEHB performans değişkenliği (performance "
                "variability): DEHB'in en karakteristik "
                "özelliklerinden biri tutarsız performans. "
                "'Yapabiliyorsa neden yapmıyor?' sorusu "
                "yanlış — yapabilirlik her gün aynı değil."
            ),
            "Bilisel_Psikoloji_Kursusu": (
                "Durum-bağımlı bellek (state-dependent memory): "
                "Öğrenme gerçekleştiği koşullarla "
                "hatırlama koşulları örtüşmüyorsa "
                "erişim güçleşiyor. "
                "Ayrıca uyku kalitesi, açlık ve "
                "stres günlük değişkenlik açıklıyor."
            ),
            "PDR_Kursusu": (
                "Ev ortamı veya dışsal stresörler "
                "günden güne değişiyor mu? "
                "Performans dalgalanması "
                "ev ortamı haritasıyla örtüşüyor mu "
                "gözlemle (Pazartesi vs. Cuma)."
            ),
            "Sinif_Yonetimi_Kursusu": (
                "Performansın yüksek olduğu günleri "
                "ve koşulları kaydet: "
                "Hangi saat, hangi aktivite, ne yemiş, "
                "kim yanında? Örüntü çıkarılınca "
                "tahmin edilebilirlik artar."
            ),
        },
        "kategori": "ÖzelEğitimŞüphesi",
        "akademik_uyari": (
            "Performans günlüğü tutun — koşulları not edin. "
            "DEHB değerlendirmesi için RAM yönlendirmesi. "
            "Tutarsızlıkla değil örüntüyle çalışın."
        ),
        "aciliyet": "ORTA",
    },

    "parmak_kaldiran_ama_cevap_veremeyen_cocuk": {
        "ogretmen_metni": (
            "Sorulan soruya istekle parmak kaldırıyor. "
            "İsmi okunduğunda ise donuyor, "
            "'bilmiyorum' diyor veya hiç cevap veremiyor."
        ),
        "fakulte_analizi": {
            "Bilisel_Psikoloji_Kursusu": (
                "Sosyal değerlendirilme kaygısı + "
                "çalışma belleği baskılanması: "
                "Parmak kaldırma anında (sosyal baskı yok) "
                "bilgi erişilebilir; "
                "isim okunduğunda (sosyal baskı yüksek) "
                "kaygı erişimi bloke ediyor."
            ),
            "PDR_Kursusu": (
                "Performans kaygısı (performance anxiety): "
                "Yalnış anlama korkusu, "
                "arkadaşların gülmesi veya öğretmen "
                "tepkisine ilişkin olumsuz beklenti. "
                "Güvenli ortam inşası kritik."
            ),
            "Sinif_Yonetimi_Kursusu": (
                "Baskısız katılım teknikleri: "
                "Düşün-Çiftleş-Paylaş, yazarak cevap, "
                "mini beyaz tahta, 'pas geçme hakkı'. "
                "Anında cevap beklentisini azalt."
            ),
            "Program_ve_Ogretim_Kursusu": (
                "Wait time (bekleme süresi — Rowe, 1986): "
                "Sorudan sonra en az 5 saniye beklemek "
                "cevap kalitesini ve katılımı artırıyor. "
                "Türk sınıflarında ortalama bekleme "
                "süresi çok kısa."
            ),
        },
        "kategori": "DuyuşsalDurum",
        "akademik_uyari": (
            "Bekleme süresini artırın. "
            "Düşün-Çiftleş-Paylaş kullanın. "
            "Pas geçme hakkı tanıyın. "
            "Performans kaygısı için PDR'a yönlendirin."
        ),
        "aciliyet": "DÜŞÜK",
    },

    "okuma_cok_hizli_ama_anlama_sifir": {
        "ogretmen_metni": (
            "Metni en hızlı okuyan o. "
            "Anlama sorularında ise hiçbir şeyi yok. "
            "Hız ve anlama arasındaki makas çarpıcı."
        ),
        "fakulte_analizi": {
            "Bilisel_Psikoloji_Kursusu": (
                "Çözümleme otomasyonu anlama kaynaklarını "
                "serbest bırakmıyor: Çözümleme (decoding) "
                "çok hızlı ama işleme derinliği sığ. "
                "Hız = anlama değil. "
                "Anlama için yavaşlama stratejileri gerekli "
                "(Rasinski — okuma akıcılığı modeli)."
            ),
            "Program_ve_Ogretim_Kursusu": (
                "Anlama stratejileri öğretimi: "
                "Öngörme, soru üretme, özetleme, "
                "görselleştirme, bağ kurma. "
                "Reciprocal Teaching (Palincsar & Brown)."
            ),
            "Olcme_Degerlendirme_Kursusu": (
                "Okuma puanı = hız değil anlama. "
                "Bu öğrenci okuma testinde başarılı "
                "görünüyor ama gerçek okuryazarlık "
                "ölçülmüyor."
            ),
            "PDR_Kursusu": (
                "Hız yarışı motivasyonu: "
                "Belki hızı bir statü kaynağı olarak kullanıyor. "
                "Anlama hedefini ödüllendiren norm değişikliği."
            ),
        },
        "kategori": "BilişselGüçlük",
        "akademik_uyari": (
            "Anlama stratejileri öğretimi başlatın. "
            "Okuma hızını değil derinliğini ödüllendirin. "
            "Yavaş okuma pratiği ekleyin."
        ),
        "aciliyet": "ORTA",
    },

    "empati_gucu_cok_yuksek_duyarli_cocuk": {
        "ogretmen_metni": (
            "Bir arkadaşı üzüldüğünde o da ağlıyor. "
            "Haberleri izleyince günlerce etkileniyor. "
            "Sınıftaki her olumsuz dinamiği fark ediyor "
            "ve içselleştiriyor."
        ),
        "fakulte_analizi": {
            "PDR_Kursusu": (
                "Yüksek Duyarlı Çocuk Profili (Aron, 1997): "
                "Nörobilişsel olarak çevresel uyaranları "
                "çok derin işliyor. "
                "Patoloji değil, nörolojik varyasyon. "
                "Duygusal sınır oluşturma becerileri "
                "öğretilmeli."
            ),
            "Bilisel_Psikoloji_Kursusu": (
                "Ayna nöron sistemi olağanüstü aktif: "
                "Başkasının acısı neredeyse kişisel acı "
                "olarak işleniyor. "
                "Duygusal düzenleme değil duygusal "
                "mesafe becerisi öğretilmeli."
            ),
            "Program_ve_Ogretim_Kursusu": (
                "Bu özellik kişilerarası ve bakım "
                "mesleklerine (psikoloji, tıp, sosyal hizmet, "
                "sanat) güçlü yönelim sinyali. "
                "Empatik rolü güçlü mesleklerle "
                "erken ilişkilendir."
            ),
            "Sinif_Yonetimi_Kursusu": (
                "Duygusal uyarıcı yoğunluğunu düşük tut: "
                "Sınıfta dramatik içerik miktarını dengele, "
                "bu öğrenci için çıkış stratejileri "
                "(köşeye çekilme, derin nefes) öğret."
            ),
        },
        "kategori": "ParıltıVeÜstünlük",
        "akademik_uyari": (
            "Duygusal sınır becerilerini öğretin. "
            "Empatiyi güce dönüştürün — sosyal liderlik. "
            "Tükenmişlik önleme için PDR ile görüşün."
        ),
        "aciliyet": "DÜŞÜK",
    },

    "dijital_oyunda_uzman_ama_derse_ilgisiz": {
        "ogretmen_metni": (
            "Karmaşık strateji oyunlarında lider, "
            "online arkadaşları var, kendi oyun taktiklerini "
            "yazan biri. Sınıfta ise her şey sıkıcı."
        ),
        "fakulte_analizi": {
            "Bilisel_Psikoloji_Kursusu": (
                "Oyun ortamı optimal bilişsel uyarımı sağlıyor: "
                "Anında geri bildirim, artan zorluk, "
                "anlık ödül — tüm öğrenme motivatörleri aktif. "
                "Okul bunu sunamıyor (Csikszentmihalyi — akış)."
            ),
            "Program_ve_Ogretim_Kursusu": (
                "Oyunlaştırma (gamification): "
                "Oyunun unsurlarını derse entegre et. "
                "Anında geri bildirim, seviye atlama, "
                "seçim özgürlüğü. "
                "Minecraft Eğitim, Kahoot gibi araçlar "
                "köprü olabilir."
            ),
            "PDR_Kursusu": (
                "Dijital yetkinlik gerçek bir beceri seti — "
                "değersizleştirme motivasyonu kırar. "
                "Oyun liderliğini tanı ve sınıfa taşı. "
                "Dijital kariyer (yazılım, oyun tasarımı) "
                "bağlantısı kur."
            ),
            "Ozel_Egitim_Kursusu": (
                "Yoğun oyun bağımlılığı şüphesi ayrıştırılmalı: "
                "Sosyal ilişkileri, uyku düzeni, "
                "beslenme etkileniyorsa "
                "oyun bağımlılığı değerlendirmesi gerekebilir."
            ),
        },
        "kategori": "ÖğrenmeTarzı",
        "akademik_uyari": (
            "Oyunlaştırma unsurları ekleyin. "
            "Dijital yetkinliği tanıyın ve sınıfa taşıyın. "
            "Oyun bağımlılığı şüphesinde PDR sevki."
        ),
        "aciliyet": "DÜŞÜK",
    },

    "yas_icin_cok_olgun_konusan_cocuk": {
        "ogretmen_metni": (
            "Yaşına göre olağanüstü olgun konuşuyor: "
            "Soyut etik kavramlar, politik tartışmalar, "
            "derin varoluşsal sorular soruyor. "
            "Akranlarıyla bağ kurmakta zorlanıyor."
        ),
        "fakulte_analizi": {
            "Ozel_Egitim_Kursusu": (
                "Üstün Yetenek Profili: Zihinsek ileri evre, "
                "sosyal-duygusal eş zamansız gelişim "
                "(asynchronous development — Silverman). "
                "Zihni yaşından büyük, duygusal ve "
                "sosyal olgunluğu yaşına uygun — "
                "bu uyumsuzluk sıkça yaşanır."
            ),
            "PDR_Kursusu": (
                "Dabrowski'nin Aşırı Uyarılabilirlik Kuramı: "
                "Entelektüel ve psişik aşırı duyarlılık. "
                "Varoluşsal sorular normal değil — "
                "derin anlam arayışı bu profilde erken başlar. "
                "Yalnızlık hissi ve akran uyumsuzluğu "
                "sürekli PDR takibini gerektiriyor."
            ),
            "Program_ve_Ogretim_Kursusu": (
                "Felsefi tartışma ortamı (Mathew Lipman — "
                "Çocuklar için Felsefe): "
                "Bu öğrencinin ihtiyaç duyduğu entelektüel "
                "etkileşim ortamını yarat."
            ),
            "Sinif_Yonetimi_Kursusu": (
                "Akran uyumsuzluğunu azaltmak için "
                "karma yaş grupları veya üst sınıf "
                "seçmeli derslere yönlendir. "
                "BİLSEM yönlendirmesi öncelikli."
            ),
        },
        "kategori": "ParıltıVeÜstünlük",
        "akademik_uyari": (
            "BİLSEM ve üstün yetenek programı için "
            "değerlendirin. Entelektüel etkileşim ortamı "
            "yaratın. Akran uyumsuzluğu için PDR desteği."
        ),
        "aciliyet": "ORTA",
    },

}

# ══════════════════════════════════════════════════════════════════════════════
#  YARDIMCI FONKSİYONLAR
# ══════════════════════════════════════════════════════════════════════════════

def get_by_category(kategori: str) -> dict:
    """Belirli bir kategorideki tüm maddeleri döndürür."""
    return {
        k: v for k, v in SYMPTOM_TAXONOMY.items()
        if v.get("kategori") == kategori
    }


def get_by_aciliyet(aciliyet: str) -> dict:
    """Belirli aciliyet seviyesindeki tüm maddeleri döndürür."""
    return {
        k: v for k, v in SYMPTOM_TAXONOMY.items()
        if v.get("aciliyet") == aciliyet
    }


def search_by_keyword(keyword: str) -> dict:
    """Öğretmen gözlem metninde anahtar kelime araması."""
    keyword = keyword.lower()
    return {
        k: v for k, v in SYMPTOM_TAXONOMY.items()
        if keyword in v.get("ogretmen_metni", "").lower()
    }


def get_all_categories() -> list:
    """Tüm kategori isimlerini döndürür."""
    return list({v.get("kategori") for v in SYMPTOM_TAXONOMY.values()})


def get_summary_table() -> list[dict]:
    """Tüm maddelerin özet tablosunu döndürür."""
    return [
        {
            "id": k,
            "kategori": v.get("kategori", ""),
            "aciliyet": v.get("aciliyet", ""),
            "kursular": list(v.get("fakulte_analizi", {}).keys()),
            "kisa_metin": v.get("ogretmen_metni", "")[:60] + "...",
        }
        for k, v in SYMPTOM_TAXONOMY.items()
    ]


# ══════════════════════════════════════════════════════════════════════════════
#  DEMO
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print(f"Toplam madde sayısı: {len(SYMPTOM_TAXONOMY)}")
    print(f"Kategoriler: {get_all_categories()}\n")

    acil = get_by_aciliyet("ACİL")
    print(f"ACİL müdahale gerektiren maddeler ({len(acil)} adet):")
    for k in acil:
        print(f"  - {k}")

    print("\n--- Örnek madde ---")
    ornek = SYMPTOM_TAXONOMY["sirada_sallanma_ve_zihinden_hizli_cozme"]
    print(f"Gözlem: {ornek['ogretmen_metni'][:80]}...")
    for kursus, analiz in ornek["fakulte_analizi"].items():
        print(f"\n[{kursus}]\n  {analiz[:100]}...")
