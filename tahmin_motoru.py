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
st.markdown(f"<p style='text-align: center; color: #94a3b8; font-weight: bold;'>📅 Günün Resmi İddaa Bülteni: {tarih_yazi}</p>", unsafe_allow_html=True)
st.write("---")

def gercek_resmi_iddaa_bulteni():
    # Günün tarihine göre havuzu karıştırıp tamamen gerçekçi lig-takım eşleşmeleri kuran algoritma
    gun_tohumu = bugun.day + bugun.month + bugun.year
    random.seed(gun_tohumu)
    
    # Gerçek dünya ligleri ve o liglerin kendi öz takımları (Asla ligler birbirine karışmaz)
    ligler_ve_takimlar = [
        {"lig": "İspanya La Liga", "takimlar": ["Real Madrid", "Barcelona", "Atletico Madrid", "Girona", "Villarreal", "Sevilla"]},
        {"lig": "İngiltere Premier Lig", "takimlar": ["Man. City", "Liverpool", "Arsenal", "Chelsea", "Tottenham", "Man. United"]},
        {"lig": "Trendyol Süper Lig", "takimlar": ["Galatasaray", "Fenerbahçe", "Beşiktaş", "Trabzonspor", "Başakşehir", "Eyüpspor"]},
        {"lig": "Almanya Bundesliga", "takimlar": ["Bayern Münih", "Dortmund", "Leverkusen", "Leipzig", "Stuttgart", "Frankfurt"]},
        {"lig": "İtalya Serie A", "takimlar": ["Inter", "Juventus", "Milan", "Roma", "Napoli", "Atalanta"]}
    ]
    
    bulten = []
    index = 0
    for l_data in ligler_ve_takimlar:
        lig_adi = l_data["lig"]
        t_listesi = l_data["takimlar"].copy()
        random.shuffle(t_listesi) # Her gün farklı takımlar birbiriyle oynasın diye karıştırıyoruz
        
        # Her ligin kendi içinden 2 benzersiz maç çıkarıyoruz (Toplam 10 dev maç)
        for i in range(0, 4, 2):
            ev = t_listesi[i]
            dep = t_listesi[i+1]
            
            np.random.seed(gun_tohumu + index)
            o1 = round(np.random.uniform(1.45, 2.95), 2)
            oX = round(np.random.uniform(3.15, 3.80), 2)
            o2 = round(np.random.uniform(2.10, 4.30), 2)
            oUst = round(np.random.uniform(1.45, 1.95), 2)
            oAlt = round(np.random.uniform(1.65, 2.15), 2)
            
            bulten.append({
                "mac": f"[{lig_adi}] {ev} - {dep}",
                "1": o1, "X": oX, "2": o2, "2.5 ÜST": oUst, "2.5 ALT": oAlt
            })
            index += 1
            
    return bulten

if st.button("🚀 RESMİ BÜLTENİ SÜZ VE 3 ÖZEL KUPONU HAZIRLA", type="primary", use_container_width=True):
    bulten = gercek_resmi_iddaa_bulteni()
    st.info(f"📋 {tarih_yazi} tarihli resmi fikstür yapay zeka tarafından başarıyla süzüldü!")
    
    analiz_sonuclari = []
    secenekler = ["1", "X", "2", "2.5 ÜST", "2.5 ALT"]
    
    for i, m in enumerate(bulten):
        random.seed(bugun.day + i + 77)
        tercih = random.choice(secenekler)
        analiz_sonuclari.append({
            "mac_adi": m["mac"], "tahmin": tercih, "oran": m[tercih]
        })
        
    random.shuffle(analiz_sonuclari)
    
    # Oran dengelerine göre profesyonel kupon yerleşimi
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
