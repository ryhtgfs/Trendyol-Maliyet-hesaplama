import streamlit as st

st.set_page_config(page_title="Trendyol Maliyet Hesaplama", layout="centered")
st.title("📦 Trendyol Maliyet Hesaplama Aracı")
st.markdown("Mobil uyumlu, KDV dahil kargo hesaplı kar hesaplama uygulaması.")

st.divider()

# === Ürün Bilgisi ===
st.header("1️⃣ Ürün Bilgileri")
satis = st.number_input("Satış Fiyatı (TL)", min_value=0.0, format="%.2f")
maliyet = st.number_input("Ürün Maliyeti (TL)", min_value=0.0, format="%.2f")
kdv_dahil = st.checkbox("KDV Dahil Maliyet", value=True)
komisyon = st.number_input("Trendyol Komisyonu (%)", min_value=0.0, format="%.2f")

# === Kargo Bilgisi ===
st.header("2️⃣ Kargo Bilgileri")
kargo_tipi = st.selectbox("Kargo Firması", ["PTT", "Sürat", "Desi"])

col1, col2, col3, col4 = st.columns(4)
with col1:
    en = st.number_input("En (cm)", min_value=0.0, format="%.1f")
with col2:
    boy = st.number_input("Boy (cm)", min_value=0.0, format="%.1f")
with col3:
    yukseklik = st.number_input("Yükseklik (cm)", min_value=0.0, format="%.1f")
with col4:
    kg = st.number_input("Ağırlık (kg)", min_value=0.0, format="%.1f")

def hesapla_desi(en, boy, yukseklik, kg):
    hacimsel_desi = (en * boy * yukseklik) / 3000
    kullanilan = max(hacimsel_desi, kg)
    return round(hacimsel_desi, 2), round(kullanilan, 2)

def get_desi_price(desi: float, kargo_firmasi: str) -> float:
    desi_int = int(round(min(desi, 20)))
    desi_fiyatlari = {
        "PTT": [
            62.03, 62.03, 62.03, 76.80, 76.80, 80.44, 85.47, 90.53, 100.59, 110.68,
            125.81, 132.01, 138.64, 145.31, 151.95, 158.58, 165.22, 171.86, 178.50, 185.17, 191.81
        ],
        "Sürat": [
            67.96, 67.96, 67.96, 75.86, 82.77, 87.39, 101.01, 107.84, 114.66, 121.49,
            128.31, 137.46, 145.24, 151.07, 154.71, 160.41, 165.81, 174.57, 183.37, 192.15, 200.91
        ]
    }
    try:
        fiyat_kdv_haric = desi_fiyatlari[kargo_firmasi][desi_int]
        return round(fiyat_kdv_haric * 1.20, 2)
    except (KeyError, IndexError):
        return 0.0

hacimsel_desi, kullanilan_desi = hesapla_desi(en, boy, yukseklik, kg)
ptt_fiyat = get_desi_price(kullanilan_desi, "PTT")
surat_fiyat = get_desi_price(kullanilan_desi, "Sürat")

desi_info = f"📏 Desi (Hacimsel): {hacimsel_desi} | Kullanılan Desi: {kullanilan_desi}"
kargo_info = f"🚚 PTT: {ptt_fiyat} TL | Sürat: {surat_fiyat} TL"
st.info(desi_info + "\n" + kargo_info)

# === HESAPLAMA ===
if st.button("💰 Hesapla"):
    if not kdv_dahil:
        maliyet *= 1.20

    if kargo_tipi in ["PTT", "Sürat"]:
        if satis < 150:
            kargo = (27.08 if kargo_tipi == "PTT" else 35.83) * 1.20
        elif satis < 300:
            kargo = (51.66 if kargo_tipi == "PTT" else 62.49) * 1.20
        else:
            kargo = get_desi_price(kullanilan_desi, kargo_tipi)
    else:
        kargo = get_desi_price(kullanilan_desi, "PTT")

    hizmet = 10.19
    stopaj = round(0.0083 * satis, 2)
    komisyon_tutar = round((komisyon / 100) * satis, 2)
    toplam_maliyet = maliyet + kargo + hizmet + stopaj + komisyon_tutar
    kar_tl = satis - toplam_maliyet
    kar_yuzde = (kar_tl / satis) * 100 if satis != 0 else 0

    st.subheader("📊 Sonuçlar")
    st.write(f"**Satış Fiyatı:** {satis:.2f} TL")
    st.write(f"**Ürün Maliyeti (KDV Dahil):** {maliyet:.2f} TL")
    st.write(f"**Kargo Ücreti:** {kargo:.2f} TL")
    st.write(f"**Komisyon:** {komisyon_tutar:.2f} TL")
    st.write(f"**Hizmet Bedeli:** {hizmet:.2f} TL")
    st.write(f"**Stopaj:** {stopaj:.2f} TL")
    st.markdown(f"**Toplam Maliyet:** `{toplam_maliyet:.2f}` TL")

    if kar_tl >= 0:
        st.success(f"✅ **Kar (TL): {kar_tl:.2f} TL** | **Kar (%): {kar_yuzde:.2f}%**")
    else:
        st.error(f"❌ **Zarar (TL): {kar_tl:.2f} TL** | **Zarar (%): {kar_yuzde:.2f}%**")
