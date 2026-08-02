import streamlit as st
import pandas as pd
import gspread

def učitaj_podatke():
        podaci_računa=dict(st.secrets["gsp_service_account"])
        klijent=gspread.service_account_from_dict(podaci_računa)

        tablica=klijent.open("Knjige")
        radni_list=tablica.worksheet("Knjige")

        podaci=radni_list.get_all_records()
        Knjig=pd.DataFrame(podaci)

        return Knjige, radni_list
Knjige, radni_list=učitaj_podatke()

if not Knjige.empty:
    Knjige["Pisac"]=pd.to_numeric(Knjige["Pisac"]), errors="coerce")
    Knjige["Godina izdavanja"]=pd.to_numeric(Knjige["Godina izdavanja"]), errors="coerce")
    Knjige["Žanr"]=pd.to_numeric(Knjige["Žanr"]), errors="coerce")
    Knjige["Ocjena"]=pd.to_numeric(Knjige["Ocjena"]), errors="coerce")

st.title("Knjige")
st.subheader(" Knjige")

if  Knjige.empty:
    st.info("U tablici još nema književnih djela.")

else:
     st.dataframe(Knjige, hide_index=True,)

st.subheader("Dodaj novo književno djelo")

with st.form("forma_za_dodavanje_književnog_djela", clear_on_submit=True):
     naslov=st.text_input("Književno djelo")
     pisac=st.text_input("Pisac")
     godina_izdavanja=st.number_input("Godina izdavanja", min_value=1900, max_value=2100, value=None, placeholder="Unesite godinu izdavanja")
     žanr=st.text_input("Žanr")
     ocjena=st.slider("Ocjena", min_value=1, max_value=10, value=5)
     gumb_dodaj=st.form_submit_button("DODAJ KNJIGU")

if gumb_dodaj:
    if naslov.strip() and pisac.strip() and godina_izdavanja.strip() and žanr.strip() and ocjena.strip() is not None:
        novi_red=[naslov.strip(), pisac.strip(), int(godina_izdavanja), žanr.strip(), int(ocjena)]
        radni_list.append_row(novi_red)

        st.success("Knjiga je uspješno dodana!")
        st.rerun()

    else:
         st.warning("Unesite naslov,pisca, godinu izdavanja i žanr književnog djela.")

st.subheader("Pretraži knjižvena djela")

if djela.empty:
     st.info("Nema književnih djela za pretraživanje!")

else:
    traženi_pisac=st.text_input("Pretraži po piscu"),
    placeholder=("Primjerice, Miroslav Krleža")
    tražena_godina_izdavanja=st.number_input("Upišite godinu:",min_value=1900, max_value=2100, value=None,
    placeholder=("Unesite godinu")
    traženi_žanr=st.text_input("Pretraži po žanru"),
    placeholder=("Primjerice, psihološki triler")

filtrirana_djela=djela

    if traženi_pisac.strip():
        filtrirana_djela=filtrirana_djela[filtrirana_djela["Traženi pisac"]
                                          .str contains(traženi_pisac.strip(), case=False)]

    if tražena_godina_izdavanja is not None:
        filtrirana_djela=filtrirana_djela[filtrirana_djela["Godina izdavanja"]==int(tražena_godina_izdavanja)]

     iftraženi_žanr.strip():
            filtrirana_djela=filtrirana_djela[filtrirana_djela["Traženi žanr"]
                                              .str contains(traženi_žanr.strip(), case=False)]

    if filtrirana_djela.empty:
        st.info("Nije pronađeno nijedno književno djelo.")

    else:
        st.dataframe(filtrirana_djela, hide_index=True,)

st.subheader("Brisanje književnih djela")

if djela.empty:
    st.info("Nema književnih djela za prikazivanje")
else:
    def opis_djela(indeks):
        djelo=djela.iloc[indeks]
        return(f"{djelo["Naslov"]} {djelo["Pisac"]}{int(djelo["Godina izdavanja"])}{djelo["Žanr"]}{djelo["Ocjena"]}")

    odabrani_indeks=st.selectbox"Odaberite tekst za brisanje"
                                        options=range(len(djela)),
                                        index=None,
                                        placeholder="Odaberite jedno književno djelo",
                                        format_func=opis_djela
                                        )

    if st.button("IZBRIŠI KNJIŽEVNO DJELO"):
         if odabrani_indeks is not None:
              redak_u_tablici=odabrani_indeks +2
              radni_list.delete_rows(redak_u_tablici)

              st.rerun()

    else:
         st.warning("Najprije odaberite književno djelo za brisanje!")

st.subeader("Najbolje tri knjige")

if Knjige.empty:
     st.info("Nema književnih djela za prikaz!")

else:
     najbolje_tri=Knjige.sort_values(by="Ocjena", ascending=False).head(3)

     st.dataframe(najbolje_tri, hide_index=True,)




