import streamlit as st
import numpy as np
import pandas as pd
import pickle


df_part_path = "postcode analysis/data/postcode_parts.pickle"

with open(df_part_path, 'rb') as handle:
    df_part = pickle.load(handle)

postcode_parts = list(df_part.keys().sort())
population_components = df_part["Area"].columns.sort()

st.title("Postcode Component Threshold Selection")

part = st.selectbox(
    'Select a postcode componenet:',
     postcode_parts)

population = st.selectbox(
    'Select a population group:',
     population_components)

threshold = st.text_input("Select a threshold", 1000)

try:
    threshold = int(threshold)

except:
    st.warning("Please enter an integer number for threshold.")

else:
    s_count = df_part[part][population][df_part[part][population].sort_values() < threshold]
    small_groups = s_count.count()
    total_groups = df_part[part][population].count()

    df_info = pd.DataFrame({
        "Total Groups":[total_groups],
        "# Groups Smaller Than Threshold": [small_groups],
        "% Groups Smaller Than Threshold": "{:.1f}".format(round((small_groups/total_groups)*100,1))
    })

    st.table(df_info.assign(hack='').set_index('hack')) #hack to hide index

    st.write("Problem {}s:".format(part.lower()))
    st.write(s_count.sort_values().to_frame())