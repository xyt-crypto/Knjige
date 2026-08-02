import streamlit as st
import pandas as pd
import gspread

# -----------------------------
# UČITAVANJE PODATAKA
# -----------------------------

def učitaj_podatke():
    podaci_računa = dict(st.secrets["gcp_service_account"])
    klijent = gspread.service_account_from_dict(podaci_računa)

    tablica = klijent.open("Knjige")
    radni_list = tablica.worksheet("Knjige")

    podaci = radni_list.get_all_records()
    Knjige = pd.DataFrame(podaci)

    return Knjige, radni_list

Knjige, radni_list = učitaj_podatke()


# -----------------------------
# KONVERZIJE
# -----------------------------

if not Knjige.empty:
    Knjige["Godina izdavanja"] = pd.to_numeric(Knjige["Godina izdavanja"], errors="coerce")
    Knjige["Ocjena"] = pd.to_numeric(Knjige["Ocjena"], errors="coerce")


# -----------------------------
# PRIKAZ TABLICE
# -----------------------------

st.title("Knjige")
st.subheader("Popis književnih djela")

if Knjige.empty:
    st.info("U tablici još nema književnih djela.")
else:
    st.dataframe(Knjige, hide_index=True)


# -----------------------------
# DODAVANJE KNJIGE
# -----------------------------

st.subheader("Dodaj novo književno djelo")

with st.form("forma_za_dodavanje_književnog_djela", clear_on_submit=True):
    naslov = st.text_input("Naslov")
    pisac = st.text_input("Pisac")
    godina_izdavanja = st.number_input(
        "Godina izdavanja",
        min_value=1900,
        max_value=2100,
        value=2000,
        placeholder="Unesite godinu"
    )
    žanr = st.text_input("Žanr")
    ocjena = st.slider("Ocjena", min_value=1, max_value=10, value=5)

    gumb_dodaj = st.form_submit_button("DODAJ KNJIGU")

if gumb_dodaj:
    if naslov.strip() and pisac.strip() and žanr.strip():
        novi_red = [naslov.strip(), pisac.strip(), int(godina_izdavanja), žanr.strip(), int(ocjena)]
        radni_list.append_row(novi_red)
        st.success("Knjiga je uspješno dodana!")
        st.rerun()
    else:
        st.warning("Unesite naslov, pisca, godinu izdavanja i žanr.")


# -----------------------------
# PRETRAŽIVANJE
# -----------------------------

st.subheader("Pretraži književna djela")

djela = Knjige.copy()

if djela.empty:
    st.info("Nema književnih djela za pretraživanje.")
else:
    traženi_pisac = st.text_input("Pretraži po piscu", placeholder="Primjerice, Miroslav Krleža")
    tražena_godina = st.number_input("Pretraži po godini", min_value=1900, max_value=2100, value=None, placeholder="Unesite godinu")
    traženi_žanr = st.text_input("Pretraži po žanru", placeholder="Primjerice, psihološki triler")

    filtrirana = djela

    if traženi_pisac.strip():
        filtrirana = filtrirana[filtrirana["Pisac"].str.contains(traženi_pisac.strip(), case=False)]

    if tražena_godina is not None:
        filtrirana = filtrirana[filtrirana["Godina izdavanja"] == int(tražena_godina)]

    if traženi_žanr.strip():
        filtrirana = filtrirana[filtrirana["Žanr"].str.contains(traženi_žanr.strip(), case=False)]

    if filtrirana.empty:
        st.info("Nije pronađeno nijedno književno djelo.")
    else:
        st.dataframe(filtrirana, hide_index=True)


# -----------------------------
# BRISANJE
# -----------------------------

st.subheader("Brisanje književnih djela")

if djela.empty:
    st.info("Nema književnih djela za prikazivanje.")
else:

    def opis_djela(indeks):
        djelo = djela.iloc[indeks]
        return f"{djelo['Naslov']} – {djelo['Pisac']} ({int(djelo['Godina izdavanja'])})"

    odabrani_indeks = st.selectbox(
        "Odaberite djelo za brisanje",
        options=range(len(djela)),
        index=None,
        placeholder="Odaberite jedno književno djelo",
        format_func=opis_djela
    )

    if st.button("IZBRIŠI KNJIŽEVNO DJELO"):
        if odabrani_indeks is not None:
            redak_u_tablici = odabrani_indeks + 2
            radni_list.delete_rows(redak_u_tablici)
            st.success("Djelo je izbrisano.")
            st.rerun()
        else:
            st.warning("Najprije odaberite djelo za brisanje!")


# -----------------------------
# NAJBOLJE TRI KNJIGE
# -----------------------------

st.subheader("Najbolje tri knjige")

if Knjige.empty:
    st.info("Nema književnih djela za prikaz.")
else:
    najbolje_tri = Knjige.sort_values(by="Ocjena", ascending=False).head(3)
    st.dataframe(najbolje_tri, hide_index=True)
