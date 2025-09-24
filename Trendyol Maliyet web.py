import streamlit as st

st.set_page_config(page_title="Trendyol Maliyet Hesaplama", layout="centered")
st.title("📦 Trendyol Maliyet Hesaplama")

# === Ürün Bilgisi ===
st.header("1️⃣ Ürün Bilgisi")
satis = st.number_input("Satış Fiyatı (TL)", min_value=0.0, step=0.01)
maliyet = st.number_input("Ürün Maliyeti (TL)", min_value=0.0, step=0.01)
kdv_dahil = st.checkbox("KDV Dahil", value=True)
komisyon = st.number_input("Komisyon (%)", min_value=0.0, step=0.1)

# === Kargo Bilgisi ===
st.header("2️⃣ Kargo Bilgisi")
kargo_tipi = st.selectbox("Kargo Tipi", ["PTT", "Sürat", "Desi"])

col1, col2 = st.columns(2)
with col1:
    en = st.number_input("En (cm)", min_value=0.0, step=0.1)
    boy = st.number_input("Boy (cm)", min_value=0.0, step=0.1)
with col2:
    yukseklik = st.number_input("Yükseklik (cm)", min_value=0.0, step=0.1)
    kg = st.number_input("Ağırlık (kg)", min_value=0.0, step=0.1)

# === Desi Hesaplama ===
def hesapla_desi(en, boy, yukseklik, kg):
    hacimsel_desi = (en * boy * yukseklik) / 3000
    kullanilan = max(hacimsel_desi, kg)
    return round(hacimsel_desi, 2), round(kullanilan, 2)

hacimsel_desi, kullanilan_desi = hesapla_desi(en, boy, yukseklik, kg)

# === Kargo Fiyatları ===
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

ptt_fiyat = get_desi_price(kullanilan_desi, "PTT")
surat_fiyat = get_desi_price(kullanilan_desi, "Sürat")

desi_text = f"📏 Desi (Hacimsel): {hacimsel_desi}, Kullanılan: {kullanilan_desi} | 🚚 PTT: {ptt_fiyat} TL, Sürat: {surat_fiyat} TL"
st.info(desi_text)

# === Hesaplama ===
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
    elif kargo_tipi == "Desi":
        kargo = get_desi_price(kullanilan_desi, "PTT")
    else:
        st.error("Geçersiz kargo tipi")
        st.stop()

    hizmet = 10.19
    stopaj = round(0.0083 * satis, 2)
    komisyon_tutar = round((komisyon / 100) * satis, 2)
    kargo_tutar = round(kargo, 2)
    maliyet_tl = round(maliyet, 2)

    toplam_maliyet = maliyet_tl + kargo_tutar + hizmet + stopaj + komisyon_tutar
    kar_tl = satis - toplam_maliyet
    kar_yuzde = (kar_tl / satis) * 100 if satis > 0 else 0

    renk = "✅" if kar_tl >= 0 else "❌"
    st.subheader("📊 Sonuçlar")
    st.write(f"**Satış Fiyatı:** {satis:.2f} TL")
    st.write(f"**Ürün Maliyeti (KDV Dahil):** {maliyet_tl:.2f} TL")
    st.write(f"**Kargo Ücreti (KDV Dahil):** {kargo_tutar:.2f} TL")
    st.write(f"**Komisyon:** {komisyon_tutar:.2f} TL")
    st.write(f"**Hizmet Bedeli:** {hizmet:.2f} TL")
    st.write(f"**Stopaj:** {stopaj:.2f} TL")
    st.write(f"**Toplam Maliyet:** `{toplam_maliyet:.2f}` TL")

    if kar_tl >= 0:
        st.success(f"{renk} Kar (TL): {kar_tl:.2f} TL | Kar (%): {kar_yuzde:.2f}%")
    else:
        st.error(f"{renk} Zarar (TL): {kar_tl:.2f} TL | Zarar (%): {kar_yuzde:.2f}%")
