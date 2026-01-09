import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.patches import Rectangle
from textwrap import wrap
import os

# A3 Portrait Dimensions (inches)
WIDTH = 11.69
HEIGHT = 16.53
DPI = 300

FIGURES_DIR = r"g:\Drive'ım\Dersler - Projeler\Bitirme Projesi-A Güz Dönemi\reports\figures"
OUTPUT_PATH = r"g:\Drive'ım\Dersler - Projeler\Bitirme Projesi-A Güz Dönemi\reports\Proje_Posteri_Dikey.pdf"

# Header Config
HEADER_H = 1.8
MARGIN = 0.5
GUTTER = 0.3 # Space between cols
BOX_TITLE_BG = '#e6f2ff'

def get_text_height(text, width_inches, fontsize):
    """Estimate text height in inches based on content."""
    # Approx char width for standard font types
    # Increased multiplier to 135 to fill the text box width better
    chars_per_line = int(width_inches * 135 / fontsize) 
    lines = []
    
    for par in text.split('\n'):
        if not par.strip():
            lines.append("")
            continue
            
        # Wrap the paragraph
        wrapped_lines = wrap(par, width=chars_per_line)
        
        # Apply pseudo-justification (add spaces) to all but the last line
        if len(wrapped_lines) > 1:
            for i in range(len(wrapped_lines) - 1):
                line = wrapped_lines[i]
                words = line.split()
                if len(words) > 1:
                    current_len = len(line)
                    needed = chars_per_line - current_len
                    
                    # Heuristic: Spaces are usually narrower than average chars. 
                    # Add slightly more spaces to push text to the right edge.
                    # Factor 1.5 is a guess to compensate for thin space width vs avg char width.
                    needed = int(needed * 1.8) 
                    
                    gaps = len(words) - 1
                    for k in range(needed):
                        words[k % gaps] += " "
                    wrapped_lines[i] = " ".join(words)
        
        lines.extend(wrapped_lines)
    
    num_lines = len(lines)
    # Line height approx 1.4 * fontsize(pts) / 72
    text_height = num_lines * (fontsize * 1.5 / 72)
    return text_height + 0.5, lines # +0.5 for padding/title space

def draw_section(ax, title, text_lines, x, y, width, fontsize=11):
    """Draws a section and returns the total height consumed."""
    line_h = (fontsize * 1.5) / 72
    title_h = 0.4
    padding = 0.1
    
    # Title
    ax.add_patch(Rectangle((x, y - title_h), width, title_h, facecolor=BOX_TITLE_BG, edgecolor='gray', linewidth=0.5))
    ax.text(x + 0.1, y - 0.28, title, fontsize=fontsize+2, fontweight='bold', color='darkblue', va='center')
    
    # content start y
    content_y = y - title_h - padding
    
    # Draw text
    for i, line in enumerate(text_lines):
        ax.text(x + 0.05, content_y - (i * line_h), line, fontsize=fontsize, va='top', ha='left')
        
    total_h = title_h + padding + (len(text_lines) * line_h) + 0.2 # extra bottom padding
    return total_h

def draw_image(ax, filename, x, y, width, caption):
    """Draws image preserving aspect ratio. Returns height used."""
    path = os.path.join(FIGURES_DIR, filename)
    if not os.path.exists(path):
        return 0
        
    img = mpimg.imread(path)
    # shape is (H, W, C)
    img_h, img_w = img.shape[:2]
    aspect = img_h / img_w
    
    # Calculate target height based on width and aspect
    # Don't let it exceed a certain max height (e.g. 5 inches) to prevent taking whole page
    draw_h = width * aspect
    if draw_h > 5.5: 
        # Constraint: if too tall, limit height and reduce width (center it)
        draw_h = 5.5
        draw_w = draw_h / aspect
        # Center x
        draw_x = x + (width - draw_w) / 2
    else:
        draw_w = width
        draw_x = x
        
    ax.imshow(img, extent=[draw_x, draw_x + draw_w, y - draw_h, y])
    
    # Caption
    caption_y = y - draw_h - 0.15
    ax.text(x + width/2, caption_y, caption, fontsize=10, style='italic', ha='center', va='top')
    
    return draw_h + 0.5 # Space for caption and padding

def create_poster():
    fig = plt.figure(figsize=(WIDTH, HEIGHT))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, WIDTH)
    ax.set_ylim(0, HEIGHT)
    ax.axis('off')
    
    # --- HEADER ---
    ax.add_patch(Rectangle((0, HEIGHT - HEADER_H), WIDTH, HEADER_H, facecolor='#1f77b4', edgecolor='none'))
    
    ax.text(WIDTH/2, HEIGHT - 0.6, "TÜRKİYE İLLERİNİN SOSYO-EKONOMİK GELİŞMİŞLİK DÜZEYLERİNE GÖRE\nMAKİNE ÖĞRENMESİ YÖNTEMLERİYLE KÜMELENMESİ", 
            fontsize=18, fontweight='bold', color='white', ha='center', va='center')
    ax.text(WIDTH/2, HEIGHT - 1.3, "Emircan Demir (241307109) | Danışman: Prof. Dr. Hikmet Hakan Gürel | Bilişim Sistemleri Müh.", 
            fontsize=12, color='white', ha='center')

    # Current Cursor Y Position (starts below header)
    cursor_y = HEIGHT - HEADER_H - 0.2
    
    # --- ROW 1: ABSTRACT (Full Width) ---
    ozet_txt = (
        "Bu çalışmada, Türkiye'deki 81 ilin sosyo-ekonomik gelişmişlik düzeyleri, TÜİK ve TCMB verileri kullanılarak makine öğrenmesi yöntemleriyle analiz edilmiştir. "
        "Çalışmada nüfus, eğitim, sağlık, ekonomi, maliye, altyapı ve yaşam kalitesi kategorilerinde toplam 24 değişken kullanılmıştır. "
        "Veri analizi sürecinde K-Means ve Hiyerarşik Kümeleme algoritmaları uygulanmış, optimum küme sayısı Elbow ve Silhouette yöntemleriyle 5 olarak belirlenmiştir. "
        "Sonuçlar; coğrafi bölgelerden bağımsız olarak illerin gelişmişlik düzeylerine göre anlamlı gruplar oluşturduğunu ve resmi SEGE-2022 raporlarıyla yüksek tutarlılık gösterdiğini ortaya koymuştur. "
        "Elde edilen bulgular, bölgesel kalkınma politikalarının oluşturulmasında veri odaklı bir karar destek mekanizması sunmaktadır."
    )
    
    h_est, lines = get_text_height(ozet_txt, WIDTH - 2*MARGIN, 12)
    h_used = draw_section(ax, "ÖZET", lines, MARGIN, cursor_y, WIDTH - 2*MARGIN, 12)
    cursor_y -= (h_used + 0.2)
    
    # --- ROW 2: INTRO & METHOD (2 Columns) ---
    
    col_w = (WIDTH - 2*MARGIN - GUTTER) / 2
    
    giris_txt = (
        "Bölgesel gelişmişlik farklarının doğru tespiti, sürdürülebilir kalkınma politikalarının etkinliği için kritiktir. "
        "Geleneksel yöntemler genellikle tek boyutlu göstergelere dayanırken, bu proje veri madenciliği ve Makine Öğrenmesi (ML) algoritmaları ile çok boyutlu ve nesnel bir sınıflandırma sunmayı amaçlar.\n\n"
        "Çalışmanın Temel Amaçları:\n"
        "1. Çok boyutlu sosyo-ekonomik veriyi işleyerek gizli örüntüleri ortaya çıkarmak.\n"
        "2. İlleri benzerliklerine göre gruplamak ve gelişmişlik haritasını çıkarmak.\n"
        "3. Her kümenin (cluster) karakteristik özelliklerini belirleyerek politika önerileri sunmaktır."
    )
    
    metot_txt = (
        "Veri Kaynakları ve Seti:\n"
        "• Kaynaklar: TÜİK (2023-2024), TCMB, Sanayi ve Teknoloji Bakanlığı.\n"
        "• Değişkenler: GSYH, Okulleşme Oranı, Hastane Yatak Sayısı, İhracat, Elektrik Tüketimi vb. (Toplam 24 Değişken).\n\n"
        "Yöntemler:\n"
        "• Ön İşleme: Eksik Veri Tamamlama, Aykırı Değer (IQR) Analizi, Min-Max Normalizasyon.\n"
        "• Algoritmalar: K-Means (Euclidean Distance), Hiyerarşik Kümeleme (Ward Linkage).\n"
        "• Değerlendirme: Elbow Metodu (Kırılma Noktası), Silhouette Skoru (0.348 - Orta/İyi Ayrışma)."
    )
    
    # Calculate heights separately
    h1, lines1 = get_text_height(giris_txt, col_w, 11)
    h2, lines2 = get_text_height(metot_txt, col_w, 11)
    
    # Use max height for alignment (or independent if flows differently, but alignment looks better)
    row_height = max(h1, h2)
    
    # Check if this row fits? (It should, we are at top)
    # Draw Intro Left
    draw_section(ax, "GİRİŞ VE AMAÇ", lines1, MARGIN, cursor_y, col_w, 11)
    # Draw Method Right
    draw_section(ax, "METODOLOJİ", lines2, MARGIN + col_w + GUTTER, cursor_y, col_w, 11)
    
    cursor_y -= (row_height + 0.3) # Move cursor down by height of text blocks
    
    # --- ROW 3: MAP (Full Width / Centered Large) ---
    # User wants proper graphics ratio
    
    img_h = draw_image(ax, "kmeans_dagilim.png", MARGIN, cursor_y, WIDTH - 2*MARGIN, "Şekil 1: K-Means ile İllerin Küme Dağılımı")
    cursor_y -= (img_h + 0.3)
    
    # --- ROW 4: PROFILES (Full Width / Centered Large) ---
    
    img2_h = draw_image(ax, "kume_profilleri.png", MARGIN, cursor_y, WIDTH - 2*MARGIN, "Şekil 2: Kümelerin Sosyo-Ekonomik Değişken profilleri")
    cursor_y -= (img2_h + 0.3)
    
    # --- ROW 5: RESULTS & CONCLUSION (Full Width) ---
    
    sonuc_txt = (
        "Analiz sonucunda iller 5 farklı gelişmişlik kümesine ayrılmıştır:\n"
        "• Küme 0 (1. Derece - Metropoller): İstanbul, Ankara, İzmir. (Sanayi, Hizmet ve Eğitim Merkezi - Ülkenin Lokomotifleri)\n"
        "• Küme 1 (2. Derece - Sanayi/Turizm): Bursa, Kocaeli, Antalya, Eskişehir, Tekirdağ, Muğla. (Yüksek Üretim ve İhracat Potansiyeli)\n"
        "• Küme 2 (3. Derece - Gelişen İller): Konya, Kayseri, Gaziantep, Manisa, Denizli, Sakarya, Balıkesir, Aydın, Mersin, Adana. (Sanayi-Tarım Dengesi)\n"
        "• Küme 3 (4. Derece - Orta Gelir): Trabzon, Samsun, Çanakkale, Isparta, Bolu, Edirne, Kırklareli, Afyon, Kütahya, Sivas, Malatya, Elazığ. (Tarım ve Hizmet Odaklı)\n"
        "• Küme 4 (5. ve 6. Derece - Öncelikli): Erzurum, Van, Diyarbakır, Şanlıurfa, Mardin, Batman, Ağrı, Kars, Iğdır, Hakkari, Şırnak, Muş, Bitlis. (Altyapı Yatırımı Öncelikli)\n\n"
        "SONUÇ: Elde edilen kümeleme yapısı, SEGE-2022 sonuçları ile yüksek korelasyon göstermektedir. İllerin sadece coğrafi konumlarına göre değil, yapısal sosyo-ekonomik özelliklerine göre de benzeştiği istatistiksel olarak kanıtlanmıştır."
    )
    
    h_sonuc, lines_sonuc = get_text_height(sonuc_txt, WIDTH - 2*MARGIN, 11)
    h_used_sonuc = draw_section(ax, "BULGULAR VE SONUÇ", lines_sonuc, MARGIN, cursor_y, WIDTH - 2*MARGIN, 11)
    cursor_y -= (h_used_sonuc + 0.2)
    
    # --- FOOTER / REFERENCES ---
    # Put at absolute bottom if space permits, or flow.
    # We want to fill space. If cursor_y is still high, we are good.
    
    kaynak_txt = "[1] T.C. Sanayi ve Teknoloji Bakanlığı, SEGE-2022 Raporu.  [2] TÜİK, İl Göstergeleri, 2024.  [3] MacQueen, J. (1967). Classification Methods."
    
    # Check remaining space
    bottom_margin = 1.0
    if cursor_y > bottom_margin:
        # We have space, draw it
        pass
    else:
        # Danger zone, text might go off page. 
        # But A3 is huge, we should be fine with current content density.
        pass
        
    h_ref, lines_ref = get_text_height(kaynak_txt, WIDTH - 2*MARGIN, 10)
    h_used_ref = draw_section(ax, "KAYNAKÇA", lines_ref, MARGIN, cursor_y, WIDTH - 2*MARGIN, 10)
    cursor_y -= (h_used_ref + 0.1)
    
    # Link - Positioned relative to the end of References
    # Ensure we don't go below 0
    footer_y_start = max(cursor_y, 0.6) # If plenty of space, put it higher. If tight, it's at cursor_y.
    
    # Actually, simpler: Just put it below the references. 
    # If cursor_y is very low (e.g. 0.1), we are in trouble anyway.
    
    ax.text(MARGIN, cursor_y - 0.2, "GitHub: github.com/EmircanDemirTR/Turkiye-Illerinin-SosyoEkonomik-Gelismislik-Duzeyine-Gore-Siniflandirilmasi", fontsize=9, color='blue')
    ax.text(WIDTH/2, cursor_y - 0.4, "Kocaeli Üniversitesi Teknoloji Fakültesi 2025-2026", ha='center', color='gray', fontsize=9)

    plt.savefig(OUTPUT_PATH, format='pdf', bbox_inches='tight')
    print(f"Poster saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    create_poster()
