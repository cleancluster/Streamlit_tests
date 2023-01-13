#!/usr/bin/env python
# coding: utf-8

# #### App egenskaber:
# - Man skal kunne vælge om det er aktiviteter, deltagere eller forskere man gerne vil eksportere som CSV fil til indberetning.
# - Den valgte entitet skal måske først lægges ind i streamlit af brugeren som en excel fil. 
# - Denne excel fil skal så undergå data-cleaning for at komme på det format som indberetningen skal have.
# - Entiteten skal også visualiseres i et sådan omfang at man har overblik over hvordan fordelingen er. (se Visualiseringsmuligheder for brugeren)
# - En download knap hvor man kan downloade CSV filen med det navn som det skal have til indberetningen for den valgte entitet.
# - Gør det dynamisk i forhold til hvilken entitet man vælger, så det ikke er hardcodede blokke, men dynamiske funktioner.
# - Hvis vi vælger at gå videre med at man selv skal kunne uploade data, så beskriv tydeligt hvordan den uploadede excel fil skal se ud.
# - Husk at opdatere requirements file hvis der er brug for nye packages (det er ikke sikkert man ved præcis hvilke dependencies den mangler før man prøver i cloud service).
# - Mulighed for at søge baseret på titel.
# 
# #### Visualiserings muligheder for brugeren
# - Vælge et tidsrum for start eller slut som tager de dataværdier med kun.
# - reset knap for options
# - Få det til at spille mht. at resette (multiselect skal være ingen valgte hvorved de andre widgets også resetter).
# 
# 
# #### Download muligheder for brugeren
# - Måske vælge encoding muligheder / andre options for hvordan den endelige fil skal se ud.
# 

# In[14]:


import numpy as np
import altair as alt
import pandas as pd
import streamlit as st

# Overskrift for applikationen
st.header('Indberetning til Uddannelses- og Forskningsstyrelsen og Danmarks Erhvervsfremmebestyrelses sekretariat')

# Beskrivelse af applikationen og en klar instruks om hvad man skal gøre.
st.markdown('Dette er en applikation der forbereder data om CLEANs aktiviteter til indberetning til Uddannelses- og Forskningsstyrelsen og Danmarks Erhvervsfremmebestyrelses sekretariat. Ud fra sidebaren til venstre kan man vælge hvilken entitet man gerne vil kigge på. ')

# Markdown til potentiel titel for sidebar:
st.sidebar.markdown('## ')

# Using "with" notation 
# converting dataframe to csv with utf-8 encoding.
def convert_df(df):
    return df.to_csv().encode('utf-8')


def clear_multi():
    st.session_state.multiselect = []
    return

def choose_subsets(df, column_str_list, subset_str_list):
    temp_df = pd.DataFrame()
    for i in range(len(column_str_list)):
        temp_df = pd.concat([temp_df, df[df[column_str_list[i]] == subset_str_list[i]]])
    return temp_df



# Sidebar: pt. er alt som skal i sidebar skrevet direkte i denne 'with' block.
# Man kan godt tilføje senere uden for denne block, så skal man bare skrive st.sidebar før sin commando.
with st.sidebar:
    st.markdown("## Skal du selv uploade et dokument?")
    # label_visibility ="collapsed" betyder at den 'radio' widget ikke har sin egen overskrift.
    upload_option = st.radio("collapsed",
        ("Nej", "Ja"),
        label_visibility="collapsed"
    )
    st.markdown("## Vælg en entitet")
    chosen_entity = st.radio("collapsed",
        ("Aktivitet", "Deltager", "Forsker"),
        label_visibility="collapsed"
    )
    
# Potentiel upload knap hvis dette skal være en mulighed gennem applikationen.
# Så skal den uploadede fil gennemgå data cleaning.
if upload_option == "Ja" and chosen_entity != None:
    uploaded_file = st.file_uploader("Upload den excel fil som repræsenterer dit valg af entitet", "Nuværende entitet = "+chosen_entity)

# Main script: Hvor de forskellige visualiseringer også kommer til at foregå, efter man har valgt sin entitet.
# Disse visualiseringer kan skrives som funktioner og kaldes.
if upload_option == "Nej" and chosen_entity != None:
    # Afhængigt af hvilken entitet man vælger skal der vælges tilsvarende data.
    df = pd.read_excel("Aktiviteter - Alle.xlsx")
    
    if chosen_entity == "Aktivitet":
        # Hardcoded til at fjerne timestamp fra datomærkningerne (afhænger af data struktur).
        df["Startdato"] = df["Startdato"].dt.date
        df["Slutdato"] = df["Slutdato"].dt.date
        df_altered = df
        selected_features = st.sidebar.multiselect("Hvilke features vil du gerne kigge på?", list(df.columns), key="multiselect")
        
        if "Startdato" in selected_features:
            st.sidebar.markdown("### Vælg et interval for Startdato")
            min_start = df["Startdato"].sort_values().iloc[0]
            max_start = df["Startdato"].sort_values().iloc[-1]
            start_date1 = st.sidebar.date_input('Start på interval', min_start, min_start, max_start)
            end_date1 = st.sidebar.date_input('Slut på interval', max_start, min_start, max_start)
            df_altered = df_altered[(df_altered['Startdato'] >= start_date1) & (df_altered['Startdato'] <= end_date1)]
                
        if "Slutdato" in selected_features:
            st.sidebar.markdown("### Vælg et interval for Slutdato")
            min_slut = df["Slutdato"].sort_values().iloc[0]
            max_slut = df["Slutdato"].sort_values().iloc[-1]
            start_date2 = st.sidebar.date_input('Start på interval', min_slut, min_slut, max_slut)
            end_date2 = st.sidebar.date_input('Slut på interval', max_slut, min_slut, max_slut)
            df_altered = df_altered[(df_altered['Slutdato'] >= start_date2) & (df_altered['Slutdato'] <= end_date2)]
        
        if "Titel" in selected_features:
            st.sidebar.markdown("### Søg efter en bestemt Aktivitet ud fra titel")
            search_str = st.sidebar.text_input("Collapsed", key="Search_input", label_visibility="collapsed")
            df_altered = df_altered.loc[df_altered['Titel'].str.contains(search_str, case=False)]
        
        if "Aktivitetstype" in selected_features:
            st.sidebar.markdown("### Vælg aktivitetstyper")
            selected_types = st.sidebar.multiselect("Collapsed", list(df_altered["Aktivitetstype"].unique()), key="multiselect_types", label_visibility="collapsed")
            df_altered = choose_subsets(df_altered, ["Aktivitetstype" for k in range(len(selected_types))], selected_types)
                
            
        st.sidebar.button("Nulstil valg", on_click=clear_multi)
        
        st.markdown("## Nu vises df_altered med "+str(len(df_altered.index))+" dataværdier")
        st.write(df_altered)
    
    
    # VISUALISERINGER
    st.markdown("## Nu vises data for "+chosen_entity)
    
    csv = convert_df(df_altered)
    # Download knap til at downloade en csv fil som har den korrekte struktur, følgende instrukserne fra Klyngeindeberetningsstruktur-2022-final.pdf.
    st.download_button(
        "Tryk for at downloade",
        csv,
        "CLEAN_"+chosen_entity+".csv",
        "text/csv",
        key='browser-data'
    )


# In[13]:


["Aktivitetstype" for k in range(6)]

