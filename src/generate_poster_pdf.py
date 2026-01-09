
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.patches import Rectangle
from textwrap import wrap
import os

# A3 Landscape Dimensions (inches)
# 420mm = 16.53 inches
# 297mm = 11.69 inches
WIDTH = 16.53
HEIGHT = 11.69
DPI = 300

FIGURES_DIR = r"g:\Drive'ım\Dersler - Projeler\Bitirme Projesi-A Güz Dönemi\reports\figures"
OUTPUT_PATH = r"g:\Drive'ım\Dersler - Projeler\Bitirme Projesi-A Güz Dönemi\reports\Proje_Posteri.pdf"

# Colors
HEADER_COLOR = '#1f77b4' # Tech Blue
TEXT_COLOR = '#000000'
BG_COLOR = '#ffffff'

def draw_text_box(ax, title, text, x, y, width, height, fontsize=10):
    # Title background
    ax.add_patch(Rectangle((x, y - 0.5), width, 0.5, facecolor='#eeeeee', edgecolor='none'))
    # Title
    ax.text(x + 0.1, y - 0.35, title, fontsize=fontsize+4, fontweight='bold', color='darkblue')
    
    # Body text
    # Heuristic: approx 6-7 chars per inch for fontsize 10-12
    char_width = int(width * 8) 
    
    wrapped_lines = []
    for paragraph in text.split('\n'):
        if paragraph.strip() == "":
            wrapped_lines.append("")
        else:
            wrapped_lines.extend(wrap(paragraph, width=char_width))
            
    wrapped_text = "\n".join(wrapped_lines)
    
    ax.text(x + 0.1, y - 0.7, wrapped_text, fontsize=fontsize, va='top', ha='left', wrap=True)

def create_poster():
    fig = plt.figure(figsize=(WIDTH, HEIGHT))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, WIDTH)
    ax.set_ylim(0, HEIGHT)
    ax.axis('off')
    
    # --- HEADER ---
    header_height = 1.5
    ax.add_patch(Rectangle((0, HEIGHT - header_height), WIDTH, header_height, facecolor=HEADER_COLOR, edgecolor='none'))
    
    title = "TÜRKİYE İLLERİNİN SOSYO-EKONOMİK GELİŞMİŞLİK DÜZEYLERİNE GÖRE\nMAKİNE ÖĞRENMESİ YÖNTEMLERİYLE KÜMELENMESİ"
    ax.text(WIDTH/2, HEIGHT - 0.75, title, fontsize=20, fontweight='bold', color='white', ha='center', va='center')
    
    student_info = "Emir Can Demir (241307109) | Bilişim Sistemleri Mühendisliği"
    ax.text(WIDTH/2, HEIGHT - 1.3, student_info, fontsize=14, color='white', ha='center')

    # --- COLUMNS ---
    # 3 Columns
    margin = 0.5
    col_width = (WIDTH - (4 * margin)) / 3
    col1_x = margin
    col2_x = margin * 2 + col_width
    col3_x = margin * 3 + col_width * 2
    
    content_top = HEIGHT - header_height - 0.5
    
    # --- COLUMN 1: ÖZET, GİRİŞ, METOT ---
    
    # ÖZET
    ozet_text = (
        "Bu çalışmada, Türkiye'deki 81 ilin sosyo-ekonomik gelişmişlik düzeyleri makine öğrenmesi yöntemleriyle analiz edilmiştir.\n"
        "TÜİK ve TCMB gibi kurumlardan elde edilen 24 farklı değişken (nüfus, eğitim, sağlık, ekonomi vb.) kullanılmıştır.\n"
        "K-Means ve Hiyerarşik Kümeleme algoritmaları uygulanmış, iller benzerliklerine göre 5 farklı kümeye ayrılmıştır.\n"
        "Sonuçlar, Sanayi ve Teknoloji Bakanlığı'nın SEGE raporlarıyla karşılaştırılmış ve yüksek tutarlılık gözlemlenmiştir."
    )
    draw_text_box(ax, "ÖZET", ozet_text, col1_x, content_top, col_width, 2, fontsize=11)
    
    # GİRİŞ
    giris_y = content_top - 2.8
    giris_text = (
        "Bölgesel gelişmişlik farklarının doğru tespiti, kalkınma politikalarının etkinliği için kritiktir.\n"
        "Geleneksel yöntemler genellikle manuel indekslemeye dayanırken, bu proje veri madenciliği ve ML algoritmaları ile nesnel bir sınıflandırma sunmayı amaçlar.\n"
        "Amaç: İllerin sosyo-ekonomik karakteristiklerine göre homojen gruplara ayrılması."
    )
    draw_text_box(ax, "GİRİŞ", giris_text, col1_x, giris_y, col_width, 2, fontsize=11)
    
    # METOT
    metot_y = giris_y - 2.5
    metot_text = (
        "Veri Seti: 81 İl, 24 Değişken (Ölçeklenmiş/Normalize).\n"
        "Algoritmalar:\n"
        "- K-Means Kümeleme\n"
        "- Hiyerarşik Kümeleme (Ward Yöntemi)\n"
        "Optimal K Belirleme:\n"
        "- Elbow Yöntemi (Dirsek Noktası)\n"
        "- Silhouette Skoru (0.348)\n"
        "- Calinski-Harabasz İndeksi"
    )
    draw_text_box(ax, "METOT", metot_text, col1_x, metot_y, col_width, 3, fontsize=11)

    # --- COLUMN 2: DENEYSEL ÇALIŞMA (GÖRSELLER) ---
    
    ax.text(col2_x + col_width/2, content_top + 0.2, "DENEYSEL ÇALIŞMA VE BULGULAR", fontsize=14, fontweight='bold', color='darkblue', ha='center')
    
    # Image 1: Map
    img1_path = os.path.join(FIGURES_DIR, "kmeans_dagilim.png")
    if os.path.exists(img1_path):
        img1 = mpimg.imread(img1_path)
        img_h = 3.5
        ax.imshow(img1, extent=[col2_x, col2_x + col_width, content_top - img_h, content_top], aspect='auto')
        ax.text(col2_x + col_width/2, content_top - img_h - 0.2, "Şekil 1: K-Means İllerin Küme Dağılımı", fontsize=9, ha='center', style='italic')
    
    # Image 2: Profiles
    img2_y = content_top - 4.2
    img2_path = os.path.join(FIGURES_DIR, "kume_profilleri.png")
    if os.path.exists(img2_path):
        img2 = mpimg.imread(img2_path)
        img_h = 3.5
        ax.imshow(img2, extent=[col2_x, col2_x + col_width, img2_y - img_h, img2_y], aspect='auto')
        ax.text(col2_x + col_width/2, img2_y - img_h - 0.2, "Şekil 2: Küme Profilleri (Normalize Değerler)", fontsize=9, ha='center', style='italic')

    # --- COLUMN 3: SONUÇLAR, KAYNAKÇA ---
    
    # SONUÇLAR
    sonuc_text = (
        "Analiz sonucunda 5 temel küme tespit edilmiştir:\n"
        "Küme 0: En gelişmiş iller (Mavi) - İstanbul, Ankara, İzmir.\n"
        "Küme 1: Sanayileşmiş geçiş illeri (Kocaeli, Bursa, Antalya).\n"
        "Küme 2: Orta gelişmişlik düzeyindeki Anadolu illeri.\n"
        "Küme 3: Tarım ağırlıklı gelişmekte olan iller.\n"
        "Küme 4: Sosyo-ekonomik açıdan desteğe ihtiyaç duyan doğu illeri.\n\n"
        "Elde edilen küme yapısı, SEGE-2022 sonuçları ile %65 (NMI Skoru) oranında örtüşmektedir."
    )
    draw_text_box(ax, "SONUÇLAR", sonuc_text, col3_x, content_top, col_width, 4, fontsize=11)
    
    # KAYNAKÇA
    kaynak_y = content_top - 4.5
    kaynak_text = (
        "[1] T.C. Sanayi ve Teknoloji Bakanlığı (2022). SEGE-2022 Raporu.\n"
        "[2] TÜİK (2024). İl Göstergeleri Veri Tabanı.\n"
        "[3] MacQueen, J. (1967). Some Methods for Classification.\n"
        "[4] Özkan, B., Uzun, S. (2017). Türkiye'de İllerin Gelişmişlik Düzeylerinin Belirlenmesi.\n"
        "[5] Scikit-learn Documentation. Clustering Algorithms."
    )
    draw_text_box(ax, "KAYNAKÇA", kaynak_text, col3_x, kaynak_y, col_width, 2.5, fontsize=10)
    
    # Footer
    ax.text(WIDTH/2, 0.2, "Emir Can Demir | 241307109 | Kocaeli Üniversitesi Teknoloji Fakültesi", fontsize=9, ha='center', color='gray')

    plt.savefig(OUTPUT_PATH, format='pdf', bbox_inches='tight')
    print(f"Poster saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    create_poster()
