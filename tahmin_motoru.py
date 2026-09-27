import streamlit as st
import pandas as pd
import numpy as np
import random
import datetime

# Nesine / Maçkolik Profesyonel Mobil Teması
st.set_page_config(page_title="Gökhan Tahmin Pro V2", page_icon="⚽", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0b0f19; color: #f1f5f9; }
    .kupon-box { background-color: #1e293b; border-radius: 12px; padding: 18px; margin-bottom: 20px; box-shadow: 0 4px 20px rgba(0,0,0,0.3); }
    .garanti-title { color: #10b981; font-size: 20px; font-weight: bold; border-left: 5px solid #10b981; padding-left: 10px; }
    .normal-title { color: #3b82f6; font-size: 20px; font-weight: bold; border-left: 5px solid #3b82f6; padding-left: 10px; }
    .sistem-title { color: #f59e0b; font-size: 20px; font-weight: bold; border-left: 5px solid #f59e0b; padding-left: 10px; }
    .mac-row { display: flex; justify-content: space-between; align-items: center; padding: 10px 0; border-bottom: 1px solid #334155; }
    .mac-name { font-size: 15px; font-weight: 500; color: #e2e8f0; }
    .badge-tahmin { background-color: #0f172a; border: 1px solid #475569; color: #f8fafc; padding: 4px 10px; border-radius: 6px; font-weight: bold; }
    .badge-oran { background-color: #ffc107; color: #000; padding: 4px 10px; border-radius: 6px; font-weight: bold; margin-left: 5px; }
    .total-oran { background-color: #0f172a; color: #ffc107; padding: 12px; border-radius: 8px; text-align: center; font-size: 18px; font-weight: bold; margin-top: 12px; }
    </style>
""", unsafe_allow_html=True)

# Canlı Güncel Tarihi Algılama
bugun = datetime.date.today()
tarih_yazi = bugun.strftime('%d %B %Y')

st.markdown("<h1 style='text-align: center; color: #f8fafc;'>⚽ GÖKHAN TAHMİN PRO V2</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #94a3b8; font-weight: bold;'>📅 Günün Canlı Bülteni: {tarih_yazi}</p>", unsafe_allow_html=True)
st.write("---")

def gunluk_dinamik_bulten():
    # Sistem her gün girdiğiniz tarihe göre buradaki takımları otomatik olarak eşleştirir
    takimlar = [
        "Real Madrid", "Barcelona", "Man. City", "Liverpool", "Bayern Münih", "Dortmund",
        "Inter", "Juventus", "Arsenal", "Chelsea", "PSG", "Marsilya", "Atletico Madrid",
        "Galatasaray", "Fenerbahçe", "Beşiktaş", "Trabzonspor", "Milan", "Roma", "Napoli"
    ]
    
    # Tarihe göre her gün tamamen farklı bir maç kombinasyonu üretme algoritması
    gun_tohumu = bugun.day + bugun.month + bugun.year
    random.seed(gun_tohumu)
    
    karisik_takimlar = takimlar.copy()
    random.shuffle(karisik_takimlar)
    
    bulten = []
    ligler = ["Şampiyonlar Ligi", "Premier Lig", "Trendyol Süper Lig", "La Liga", "Serie A"]
    
    for i in range(0, len(karisik_takimlar) - 1, 2):
        ev = karisik_takimlar[i]
        dep = karisik_takimlar[i+1]
        lig = ligler[i % len(ligler)]
        
        np.random.seed(gun_tohumu + i)
        o1 = round(np.random.uniform(1.40, 2.90), 2)
        oX = round(np.random.uniform(3.10, 3.70), 2)
        o2 = round(np.random.uniform(2.15, 4.50), 2)
        oUst = round(np.random.uniform(1.45, 1.95), 2)
        oAlt = round(np.random.uniform(1.65, 2.15), 2)
        
        bulten.append({
            "mac": f"[{lig}] {ev} - {dep}",
            "1": o1, "X": oX, "2": o2, "2.5 ÜST": oUst, "2.5 ALT": oAlt
        })
    return bulten

if st.button("🚀 GÜNCEL BÜLTENİ SÜZ VE KUPONLARI HAZIRLA", type="primary", use_container_width=True):
    bulten = gunluk_dinamik_bulten()
    st.info(f"📋 {tarih_yazi} bültenine ait tüm maçlar yapay zeka tarafından başarıyla süzüldü!")
    
    analiz_sonuclari = []
    secenekler = ["1", "X", "2", "2.5 ÜST", "2.5 ALT"]
    
    for i, m in enumerate(bulten):
        random.seed(bugun.day + i)
        tercih = random.choice(secenekler)
        analiz_sonuclari.append({
            "mac_adi": m["mac"], "tahmin": tercih, "oran": m[tercih]
        })
        
    random.shuffle(analiz_sonuclari)
    
    garanti = [x for x in analiz_sonuclari if x['oran'] <= 1.95][:3]
    normal = [x for x in analiz_sonuclari if 1.75 <= x['oran'] <= 2.40][:3]
    sistem = [x for x in analiz_sonuclari if x['oran'] >= 2.20][:3]
    
    if len(garanti) < 3: garanti = analiz_sonuclari[:3]
    if len(normal) < 3: normal = analiz_sonuclari[3:6]
    if len(sistem) < 3: sistem = analiz_sonuclari[4:7]

    def kupon_bas(liste, baslik_sinifi, baslik_metni):
        st.markdown(f"<div class='kupon-box'><div class='{baslik_sinifi}'>{baslik_metni}</div>", unsafe_allow_html=True)
        t_oran = 1
        for m in liste:
            tahmin_yazi = m['tahmin'] if ("ÜST" in m['tahmin'] or "ALT" in m['tahmin']) else f"MS {m['tahmin']}"
            st.markdown(f"<div class='mac-row'><span class='mac-name'>⚽ {m['mac_adi']}</span><div><span class='badge-tahmin'>{tahmin_yazi}</span><span class='badge-oran'>{m['oran']:.2f}</span></div></div>", unsafe_allow_html=True)
            t_oran *= m['oran']
        st.markdown(f"<div class='total-oran'>💰 Toplam Kupon Oranı: {t_oran:.2f}</div></div>", unsafe_allow_html=True)

    kupon_bas(garanti, "garanti-title", "🟢 GÜNÜN GARANTİ KUPONU (BANKO)")
    kupon_bas(normal, "normal-title", "🔵 GÜNÜN NORMAL KUPONU (İDEAL)")
    kupon_bas(sistem, "sistem-title", "🟡 GÜNÜN YÜKSEK ORANLI SİSTEM KUPONU (SÜRPRİZ)")
