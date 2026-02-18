import streamlit as st
import math
import itertools
import pandas as pd

# Konfiguracja strony
st.set_page_config(page_title="Math Coincidence Finder", layout="centered")

def find_coincidences(selected_constants, threshold):
    results = []
    names = list(selected_constants.keys())
    
    # Przeszukujemy kombinacje: a^b - c
    for c1, c2, c3 in itertools.permutations(names, 3):
        v1, v2, v3 = selected_constants[c1], selected_constants[c2], selected_constants[c3]
        try:
            val = (v1 ** v2) - v3
            diff = abs(val - round(val))
            
            if diff <= threshold:
                results.append({
                    "Formuła": f"{c1}^{c2} - {c3}",
                    "Wynik": round(val, 8),
                    "Błąd": f"{diff:.10f}"
                })
        except OverflowError:
            continue
            
    return pd.DataFrame(results).sort_values(by="Błąd")

# --- UI ---
st.title("🎯 Poszukiwacz Zbiegów Okoliczności")
st.markdown("Znajdź wyrażenia matematyczne bliskie liczbom całkowitym (jak $e^\\pi - \\pi$).")

with st.sidebar:
    st.header("Ustawienia")
    # Wybór progu czułości
    threshold = st.slider("Czułość (maks. błąd)", 0.0001, 0.05, 0.01, format="%.4f")
    
    # Wybór stałych do testowania
    st.subheader("Dostępne stałe")
    const_pool = {
        "π (pi)": math.pi,
        "e (Euler)": math.e,
        "φ (Złota)": (1 + 5**0.5) / 2,
        "√2": 2**0.5,
        "γ (Mascheroni)": 0.57721,
        "163": 163  # Do stałej Ramanujana
    }
    
    selected_names = st.multiselect(
        "Wybierz stałe do analizy:", 
        options=list(const_pool.keys()),
        default=["π (pi)", "e (Euler)", "φ (Złota)"]
    )

# Mapowanie nazw na wartości
active_constants = {name.split()[0]: const_pool[name] for name in selected_names}

if len(active_constants) < 3:
    st.warning("Wybierz co najmniej 3 stałe, aby uruchomić algorytm.")
else:
    st.subheader("Znalezione dopasowania")
    df_results = find_coincidences(active_constants, threshold)
    
    if not df_results.empty:
        st.dataframe(df_results, use_container_width=True, hide_index=True)
        st.success(f"Znaleziono {len(df_results)} interesujących wyników!")
    else:
        st.info("Brak wyników w tym zakresie. Spróbuj zwiększyć czułość lub dodać więcej stałych.")

# Ciekawostka na dole
st.info("**Wskazówka:** Spróbuj dodać '163' i sprawdź kombinację $e^{\pi \sqrt{163}}$. To tzw. stała Ramanujana, która jest niemal idealnie całkowita!")