import tkinter as tk
from tkinter import ttk, messagebox

root = tk.Tk()
root.title("Trendyol Maliyet Hesaplama")
root.configure(padx=10, pady=10)

dark_mode = tk.BooleanVar(value=False)

def apply_theme():
    bg = "#2E2E2E" if dark_mode.get() else "SystemButtonFace"
    fg = "white" if dark_mode.get() else "black"
    root.configure(bg=bg)
    for child in root.winfo_children():
        try:
            child.configure(bg=bg, fg=fg)
        except:
            pass

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

def hesapla_desi(en, boy, yukseklik, kg):
    hacimsel_desi = (en * boy * yukseklik) / 3000
    kullanilan = max(hacimsel_desi, kg)
    return round(hacimsel_desi, 2), round(kullanilan, 2)

def guncelle_desi_label(*args):
    try:
        en = float(entry_en.get())
        boy = float(entry_boy.get())
        yukseklik = float(entry_yukseklik.get())
        kg = float(entry_kg.get())
        hacimsel_desi, kullanilan = hesapla_desi(en, boy, yukseklik, kg)
        ptt_fiyat = get_desi_price(kullanilan, "PTT")
        surat_fiyat = get_desi_price(kullanilan, "Sürat")
        desi_var.set(f"Desi (Hacimsel): {hacimsel_desi}, Kullanılan: {kullanilan} | PTT: {ptt_fiyat} TL, Sürat: {surat_fiyat} TL")
    except:
        desi_var.set("Desi: -")

def hesapla():
    try:
        satis = float(entry_satis.get())
        maliyet = float(entry_maliyet.get())
        komisyon = float(entry_komisyon.get())
        kdv_dahil = kdv_var.get()
        kargo_tipi = kargo_combo.get()

        if not kdv_dahil:
            maliyet *= 1.20

        if kargo_tipi in ["PTT", "Sürat"]:
            if satis < 150:
                kargo = (27.08 if kargo_tipi == "PTT" else 35.83) * 1.20
            elif satis < 300:
                kargo = (51.66 if kargo_tipi == "PTT" else 62.49) * 1.20
            else:
                en = float(entry_en.get())
                boy = float(entry_boy.get())
                yukseklik = float(entry_yukseklik.get())
                kg = float(entry_kg.get())
                _, kullanilan = hesapla_desi(en, boy, yukseklik, kg)
                kargo = get_desi_price(kullanilan, kargo_tipi)
        elif kargo_tipi == "Desi":
            en = float(entry_en.get())
            boy = float(entry_boy.get())
            yukseklik = float(entry_yukseklik.get())
            kg = float(entry_kg.get())
            _, kullanilan = hesapla_desi(en, boy, yukseklik, kg)
            kargo = get_desi_price(kullanilan, "PTT")
        else:
            messagebox.showerror("Hata", "Geçersiz kargo tipi")
            return

        hizmet = 10.19
        stopaj = round(0.0083 * satis, 2)
        komisyon_tutar = round((komisyon / 100) * satis, 2)
        kargo_tutar = round(kargo, 2)
        maliyet_tl = round(maliyet, 2)

        toplam_maliyet = maliyet_tl + kargo_tutar + hizmet + stopaj + komisyon_tutar
        kar_tl = satis - toplam_maliyet
        kar_yuzde = (kar_tl / satis) * 100

        renk = "green" if kar_tl >= 0 else "red"

        result_window = tk.Toplevel(root)
        result_window.title("Sonuç Detayları")
        result_text = tk.Text(result_window, wrap="word", font=("Segoe UI", 10))
        result_text.insert("1.0", f"Satış Fiyatı: {satis:.2f} TL\n")
        result_text.insert("end", f"Ürün Maliyeti (KDV Dahil): {maliyet_tl:.2f} TL\n")
        result_text.insert("end", f"Kargo Ücreti (KDV Dahil): {kargo_tutar:.2f} TL\n")
        result_text.insert("end", f"Komisyon: {komisyon_tutar:.2f} TL\n")
        result_text.insert("end", f"Hizmet Bedeli: {hizmet:.2f} TL\n")
        result_text.insert("end", f"Stopaj: {stopaj:.2f} TL\n")
        result_text.insert("end", f"Toplam Maliyet: {toplam_maliyet:.2f} TL\n")
        result_text.insert("end", f"Kar (TL): {kar_tl:.2f} TL\n", ("kar",))
        result_text.insert("end", f"Kar (%): {kar_yuzde:.2f}%\n", ("kar",))
        result_text.tag_config("kar", foreground=renk, font=("Segoe UI", 10, "bold"))
        result_text.configure(state="disabled")
        result_text.pack(expand=True, fill="both")

    except Exception as e:
        messagebox.showerror("Hata", str(e))

# Tema seçici
tk.Checkbutton(root, text="Koyu Tema", variable=dark_mode, command=apply_theme).grid(row=0, column=2, padx=5)

# === Ürün Bilgisi ===
frame_urun = tk.LabelFrame(root, text="Ürün Bilgisi", font=("Segoe UI", 10, "bold"))
frame_urun.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

entry_satis = tk.Entry(frame_urun)
tk.Label(frame_urun, text="Satış Fiyatı (TL)", font=("Segoe UI", 9, "bold")).grid(row=0, column=0, sticky="w")
entry_satis.grid(row=0, column=1, pady=2)

entry_maliyet = tk.Entry(frame_urun)
tk.Label(frame_urun, text="Ürün Maliyeti (TL)", font=("Segoe UI", 9, "bold")).grid(row=1, column=0, sticky="w")
entry_maliyet.grid(row=1, column=1, pady=2)

kdv_var = tk.BooleanVar(value=True)
tk.Checkbutton(frame_urun, text="KDV Dahil", variable=kdv_var).grid(row=1, column=2, padx=5)

entry_komisyon = tk.Entry(frame_urun)
tk.Label(frame_urun, text="Komisyon (%)", font=("Segoe UI", 9, "bold")).grid(row=2, column=0, sticky="w")
entry_komisyon.grid(row=2, column=1, pady=2)

# === Kargo Bilgisi ===
frame_kargo = tk.LabelFrame(root, text="Kargo Bilgisi", font=("Segoe UI", 10, "bold"))
frame_kargo.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

kargo_combo = ttk.Combobox(frame_kargo, values=["PTT", "Sürat", "Desi"], state="readonly")
kargo_combo.set("PTT")
tk.Label(frame_kargo, text="Kargo Tipi", font=("Segoe UI", 9, "bold")).grid(row=0, column=0, sticky="w")
kargo_combo.grid(row=0, column=1, pady=2)

entry_en = tk.Entry(frame_kargo)
tk.Label(frame_kargo, text="En (cm)", font=("Segoe UI", 9)).grid(row=1, column=0, sticky="w")
entry_en.grid(row=1, column=1, pady=2)
entry_en.bind("<KeyRelease>", guncelle_desi_label)

entry_boy = tk.Entry(frame_kargo)
tk.Label(frame_kargo, text="Boy (cm)", font=("Segoe UI", 9)).grid(row=2, column=0, sticky="w")
entry_boy.grid(row=2, column=1, pady=2)
entry_boy.bind("<KeyRelease>", guncelle_desi_label)

entry_yukseklik = tk.Entry(frame_kargo)
tk.Label(frame_kargo, text="Yükseklik (cm)", font=("Segoe UI", 9)).grid(row=3, column=0, sticky="w")
entry_yukseklik.grid(row=3, column=1, pady=2)
entry_yukseklik.bind("<KeyRelease>", guncelle_desi_label)

entry_kg = tk.Entry(frame_kargo)
tk.Label(frame_kargo, text="Ağırlık (kg)", font=("Segoe UI", 9)).grid(row=4, column=0, sticky="w")
entry_kg.grid(row=4, column=1, pady=2)
entry_kg.bind("<KeyRelease>", guncelle_desi_label)

# Desi göstergesi
desi_var = tk.StringVar()
desi_var.set("Desi: -")
tk.Label(root, textvariable=desi_var, fg="blue", font=("Segoe UI", 9, "italic")).grid(row=2, column=0, columnspan=3, pady=(5, 10))

# Hesapla butonu
hesapla_btn = tk.Button(root, text="💰 Hesapla", command=hesapla, bg="#4CAF50", fg="white", padx=10, pady=5, activebackground="#45a049")
hesapla_btn.grid(row=3, column=0, columnspan=3, pady=10)

apply_theme()
root.mainloop()
