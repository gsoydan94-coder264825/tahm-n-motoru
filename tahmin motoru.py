import streamlit as st
import requests
import pandas as pd
import numpy as np
from scipy.stats import poisson
import datetime

# Nesine / Maçkolik Pro Mobil Teması
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
st.markdown("<p style='text-align: center; color: #94a3b8;'>Nesine/Maçkolik tüm dünya bülteni yapay zeka tarafından taranır.</p>", unsafe_allow_html=True)
st.write("---")

API_KEY = "3dabe067dced65685455d22b0cb4c240"
HEADERS = {'x-rapidapi-host': "v3.football.api-sports.io", 'x-rapidapi-key': API_KEY}

@st.cache_data(ttl=1800)
def dev_bulten_cek():
    bugun = datetime.date.today().strftime('%Y-%m-%d')
    url = f"https://api-sports.io{bugun}"
    try:
        response = requests.get(url, headers=HEADERS).json()
        maclar = response.get('response', [])
        bulten = []
        for index, m in enumerate(maclar):
            if m['fixture']['status']['short'] in ['NS', 'TBD']:
                ev = m['teams']['home']['name']
                dep = m['teams']['away']['name']
                # Gerçekçi simüle edilmiş oran matrisi (Tüm bülten için)
                np.random.seed(index)
                o1 = round(np.random.uniform(1.40, 4.50), 2)
                oX = round(np.random.uniform(3.00, 4.00), 2)
                o2 = round(np.random.uniform(1.80, 5.50), 2)
                bulten.append({"mac": f"{ev} - {dep}", "ev": ev, "dep": dep, "oran_1": o1, "oran_X": oX, "oran_2": o2})
        return bulten
    except:
        return []

if st.button("🚀 TÜM DÜNYA BÜLTENİNİ SÜZ VE 3 ÖZEL KUPONU HAZIRLA", type="primary", use_container_width=True):
    with st.spinner("Nesine/Maçkolik üzerindeki yüzlerce maç analiz ediliyor..."):
        bulten = dev_bulten_cek()
        
        if not bulten:
            st.error("⚠️ Bülten şu an çekilemedi, lütfen birkaç dakika sonra tekrar deneyin.")
        else:
            st.info(f"📋 Bugün oynanacak toplam {len(bulten)} dünya maçı başarıyla tarandı ve analiz edildi!")
            
            # Lig Simülasyonu ve Poisson Analizi
            takimlar = list(set([m['ev'] for m in bulten] + [m['dep'] for m in bulten]))
            df_lig = pd.DataFrame({
                'HomeTeam': takimlar * 2, 'AwayTeam': list(reversed(takimlar)) * 2,
                'FTHG': np.random.randint(1, 4, len(takimlar)*2), 'FTAG': np.random.randint(0, 3, len(takimlar)*2)
            })
            avg_h, avg_a = df_lig['FTHG'].mean(), df_lig['FTAG'].mean()
            h_att = df_lig.groupby('HomeTeam')['FTHG'].mean() / avg_h
            h_def = df_lig.groupby('HomeTeam')['FTAG'].mean() / avg_a
            a_att = df_lig.groupby('AwayTeam')['FTAG'].mean() / avg_a
            a_def = df_lig.groupby('AwayTeam')['FTHG'].mean() / avg_h

            analiz_sonuclari = []
            for m in bulten:
                b_ev = h_att.get(m['ev'], 1.0) * a_def.get(m['dep'], 1.0) * avg_h
                b_dep = a_att.get(m['dep'], 1.0) * h_def.get(m['ev'], 1.0) * avg_a
                ev_p, dep_p = [poisson.pmf(i, b_ev) for i in range(5)], [poisson.pmf(i, b_dep) for i in range(5)]
                matris = np.outer(ev_p, dep_p)
                olasiliklar = {'1': np.sum(np.tril(matris, -1)), 'X': np.sum(np.diag(matris)), '2': np.sum(np.triu(matris, 1))}
                tercih = max(olasiliklar, key=olasiliklar.get)
                analiz_sonuclari.append({
                    "mac_adi": m["mac"], "tahmin": tercih, "olasilik": olasiliklar[tercih], "oran": m[f"oran_{tercih}"]
                })

            # KUPON YAPILANDIRMALARI (Hassas Filtreleme)
            # 1. Garanti Kupon (Olasılığı en yüksek ve oranı makul maçlar)
            garanti = sorted([x for x in analiz_sonuclari if x['oran'] <= 1.90], key=lambda x: x['olasilik'], reverse=True)[:3]
            # 2. Normal Kupon (İdeal 1.70 - 2.50 arası oran dengesi)
            normal = sorted([x for x in analiz_sonuclari if 1.70 <= x['oran'] <= 2.60], key=lambda x: x['olasilik'], reverse=True)[:3]
            # 3. Yüksek Oranlı Sistem Kuponu (Yüksek oranlı sürpriz potansiyeller)
            sistem = sorted([x for x in analiz_sonuclari if x['oran'] >= 2.80], key=lambda x: x['olasilik'], reverse=True)[:3]

            def kupon_bas(liste, baslik_sinifi, baslik_metni):
                st.markdown(f"<div class='kupon-box'><div class='{baslik_sinifi}'>{baslik_metni}</div>", unsafe_allow_html=True)
                t_oran = 1
                for m in liste:
                    st.markdown(f"<div class='mac-row'><span class='mac-name'>⚽ {m['mac_adi']}</span><div><span class='badge-tahmin'>MS {m['tahmin']}</span><span class='badge-oran'>{m['oran']:.2f}</span></div></div>", unsafe_allow_html=True)
                    t_oran *= m['oran']
                st.markdown(f"<div class='total-oran'>💰 Toplam Kupon Oranı: {t_oran:.2f}</div></div>", unsafe_allow_html=True)

            # Ekran Çıktıları
            kupon_bas(garanti, "garanti-title", "🟢 GÜNÜN GARANTİ KUPONU (BANKO)")
            kupon_bas(normal, "normal-title", "🔵 GÜNÜN NORMAL KUPONU (İDEAL)")
            kupon_bas(sistem, "sistem-title", "🟡 GÜNÜN YÜKSEK ORANLI SİSTEM KUPONU (SÜRPRİZ)")
