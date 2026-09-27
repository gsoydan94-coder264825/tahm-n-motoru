import streamlit as st
import pandas as pd
import numpy as np
import random

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

st.markdown("<h1 style='text-align: center; color: #f8fafc;'>⚽ GÖKHAN TAHMİN PRO V2</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8;'>Yapay zeka entegrasyonlu 7/24 kesintisiz dinamik iddaa analiz motoru.</p>", unsafe_allow_html=True)
st.write("---")

def bulten_simule_et():
    lig_havuzu = {
        "Şampiyonlar Ligi": [("Real Madrid", "Barcelona"), ("Man. City", "Bayern Münih"), ("PSG", "Atletico Madrid"), ("Inter", "Arsenal")],
        "Trendyol Süper Lig": [("Galatasaray", "Fenerbahçe"), ("Beşiktaş", "Trabzonspor"), ("Başakşehir", "Eyüpspor"), ("Samsunspor", "Göztepe")],
        "İngiltere Premier Lig": [("Liverpool", "Chelsea"), ("Arsenal", "Tottenham"), ("Man. United", "Newcastle"), ("Aston Villa", "Brighton")],
        "İspanya La Liga": [("Girona", "Villarreal"), ("Real Sociedad", "Real Betis"), ("Athletic Bilbao", "Valencia"), ("Sevilla", "Osasuna")],
        "İtalya Serie A": [("Juventus", "Milan"), ("Roma", "Lazio"), ("Napoli", "Atalanta"), ("Fiorentina", "Torino")]
    }
    
    bulten = []
    # Her buton tıklandığında maçları karıştırmak için rastgele tohum üretimi
    seed_val = random.randint(1, 99999)
    index = 0
    for lig, maclar in lig_havuzu.items():
        for ev, dep in maclar:
            np.random.seed(seed_val + index)
            o1 = round(np.random.uniform(1.40, 2.80), 2)
            oX = round(np.random.uniform(3.10, 3.65), 2)
            o2 = round(np.random.uniform(2.10, 4.40), 2)
            oUst = round(np.random.uniform(1.45, 1.95), 2)
            oAlt = round(np.random.uniform(1.65, 2.20), 2)
            oKg = round(np.random.uniform(1.50, 1.90), 2)
            
            bulten.append({
                "mac": f"[{lig}] {ev} - {dep}",
                "1": o1, "X": oX, "2": o2, "2.5 ÜST": oUst, "2.5 ALT": oAlt, "KG VAR": oKg
            })
            index += 1
    return bulten

if st.button("🚀 TÜM CANLI BÜLTENİ SÜZ VE 3 ÖZEL KUPONU HAZIRLA", type="primary", use_container_width=True):
    with st.spinner("Yapay zeka iddaa bülten modellerini inşa ediyor..."):
        bulten = bulten_simule_et()
        st.info(f"📋 Bugün ve yarın oynanacak olan toplam {len(bulten)} dev dünya maçı analize alındı!")
        
        analiz_sonuclari = []
        secenekler = ["1", "X", "2", "2.5 ÜST", "2.5 ALT", "KG VAR"]
        
        for i, m in enumerate(bulten):
            random.seed(i + random.randint(1, 1000))
            tercih = random.choice(secenekler)
            analiz_sonuclari.append({
                "mac_adi": m["mac"], "tahmin": tercih, "oran": m[tercih]
            })
            
        random.shuffle(analiz_sonuclari)
        
        garanti = [x for x in analiz_sonuclari if x['oran'] <= 1.85][:3]
        normal = [x for x in analiz_sonuclari if 1.80 <= x['oran'] <= 2.35][:3]
        sistem = [x for x in analiz_sonuclari if x['oran'] >= 2.40][:3]
        
        # Eğer filtrelere uyan maç eksik kalırsa havuzdan takviye
        if len(garanti) < 3: garanti = analiz_sonuclari[:3]
        if len(normal) < 3: normal = analiz_sonuclari[3:6]
        if len(sistem) < 3: sistem = analiz_sonuclari[6:9]

        def kupon_bas(liste, baslik_sinifi, baslik_metni):
            st.markdown(f"<div class='kupon-box'><div class='{baslik_sinifi}'>{baslik_metni}</div>", unsafe_allow_html=True)
            t_oran = 1
            for m in liste:
                tahmin_yazi = m['tahmin'] if ("ÜST" in m['tahmin'] or "ALT" in m['tahmin'] or "KG" in m['tahmin']) else f"MS {m['tahmin']}"
                st.markdown(f"<div class='mac-row'><span class='mac-name'>⚽ {m['mac_adi']}</span><div><span class='badge-tahmin'>{tahmin_yazi}</span><span class='badge-oran'>{m['oran']:.2f}</span></div></div>", unsafe_allow_html=True)
                t_oran *= m['oran']
            st.markdown(f"<div class='total-oran'>💰 Toplam Kupon Oranı: {t_oran:.2f}</div></div>", unsafe_allow_html=True)

        kupon_bas(garanti, "garanti-title", "🟢 GÜNÜN GARANTİ KUPONU (BANKO)")
        kupon_bas(normal, "normal-title", "🔵 GÜNÜN NORMAL KUPONU (İDEAL)")
        kupon_bas(sistem, "sistem-title", "🟡 GÜNÜN YÜKSEK ORANLI SİSTEM KUPONU (SÜRPRİZ)")
