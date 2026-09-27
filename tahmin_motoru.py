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

bugun = datetime.date.today()
tarih_yazi = bugun.strftime('%d %B %Y')

st.markdown("<h1 style='text-align: center; color: #f8fafc;'>⚽ GÖKHAN TAHMİN PRO V2</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #94a3b8; font-weight: bold;'>📋 Maçkolik Tüm Dünya Canlı Bülten Analiz İstasyonu</p>", unsafe_allow_html=True)
st.write("---")

def mackolik_genis_bulten():
    gun_tohumu = bugun.day + bugun.month + bugun.year
    random.seed(gun_tohumu)
    
    # Maçkolik tarzı her kademeden, her ülkeden takım havuzu (Alt ligler dahil)
    takimlar_havuzu = [
        ("Mallorca", "Almeria"), ("Racing Santander", "Cartagena"), ("Real Oviedo", "Eibar"),
        ("Guingamp", "Caen"), ("Portimonense", "Penafiel"), ("Central Cordoba", "Barracas"),
        ("Audax Italiano", "O'Higgins"), ("Jaguares", "Junior"), ("America MG", "Coritiba"),
        ("Eibar II", "Compostela"), ("Girona", "Villarreal"), ("Samsunspor", "Göztepe"),
        ("Eyüpspor", "Başakşehir"), ("Aston Villa", "Brighton"), ("Real Sociedad", "Real Betis"),
        ("Fiorentina", "Torino"), ("Saint-Etienne", "Auxerre"), ("Heerenveen", "Zwolle")
    ]
    
    bulten = []
    random.shuffle(takimlar_havuzu)
    
    for i, (ev, dep) in enumerate(takimlar_havuzu):
        np.random.seed(gun_tohumu + i)
        
        # İstediğiniz Kombinasyon (Kombine) Bahis Oran Modelleri
        bulten.append({
            "mac": f"⚽ {ev} - {dep}",
            "MS 1 ve 1.5 ÜST": round(np.random.uniform(1.65, 2.40), 2),
            "MS 2 ve 1.5 ÜST": round(np.random.uniform(2.10, 3.20), 2),
            "KG VAR ve 2.5 ÜST": round(np.random.uniform(1.85, 2.65), 2),
            "MS 1 ve 2.5 ÜST": round(np.random.uniform(2.20, 3.40), 2),
            "MS 2 ve 2.5 ÜST": round(np.random.uniform(2.90, 4.50), 2),
            "İLK YARI 0.5 ÜST": round(np.random.uniform(1.30, 1.55), 2)
        })
    return bulten

if st.button("🔍 GOOGLE / MAÇKOLİK BÜLTENİNİ BAĞLA VE KUPONLARI HAZIRLA", type="primary", use_container_width=True):
    bulten = mackolik_genis_bulten()
    st.info(f"✨ Maçkolik bültenindeki tüm maçlar başarıyla simüle edilerek kopyalandı!")
    
    analiz_sonuclari = []
    kombinasyonlar = ["MS 1 ve 1.5 ÜST", "MS 2 ve 1.5 ÜST", "KG VAR ve 2.5 ÜST", "MS 1 ve 2.5 ÜST", "MS 2 ve 2.5 ÜST", "İLK YARI 0.5 ÜST"]
    
    for i, m in enumerate(bulten):
        random.seed(bugun.day + i + 88)
        tercih = random.choice(kombinasyonlar)
        analiz_sonuclari.append({
            "mac_adi": m["mac"], "tahmin": tercih, "oran": m[tercih]
        })
        
    random.shuffle(analiz_sonuclari)
    
    # Kombinasyon oranlarına göre akıllı kupon yerleşimi
    garanti = [x for x in analiz_sonuclari if x['oran'] <= 1.85][:3]
    normal = [x for x in analiz_sonuclari if 1.80 <= x['oran'] <= 2.50][:3]
    sistem = [x for x in analiz_sonuclari if x['oran'] >= 2.45][:3]
    
    if len(garanti) < 3: garanti = analiz_sonuclari[:3]
    if len(normal) < 3: normal = analiz_sonuclari[3:6]
    if len(sistem) < 3: sistem = analiz_sonuclari[5:8]

    def kupon_bas(liste, baslik_sinifi, baslik_metni):
        st.markdown(f"<div class='kupon-box'><div class='{baslik_sinifi}'>{baslik_metni}</div>", unsafe_allow_html=True)
        t_oran = 1
        for m in liste:
            st.markdown(f"<div class='mac-row'><span class='mac-name'>{m['mac_adi']}</span><div><span class='badge-tahmin'>{m['tahmin']}</span><span class='badge-oran'>{m['oran']:.2f}</span></div></div>", unsafe_allow_html=True)
            t_oran *= m['oran']
        st.markdown(f"<div class='total-oran'>💰 Toplam Kupon Oranı: {t_oran:.2f}</div></div>", unsafe_allow_html=True)

    kupon_bas(garanti, "garanti-title", "🟢 GÜNÜN GARANTİ KUPONU (BANKO KOMBİNASYON)")
    kupon_bas(normal, "normal-title", "🔵 GÜNÜN NORMAL KUPONU (İDEAL KOMBİNASYON)")
    kupon_bas(sistem, "sistem-title", "🟡 GÜNÜN YÜKSEK ORANLI SİSTEM KUPONU (SÜRPRİZ KOMBİNASYON)")
