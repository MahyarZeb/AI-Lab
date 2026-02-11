import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# ----------------------------
# 1. Page Configuration
# ----------------------------
st.set_page_config(
    page_title="EDA Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Exploratory Data Analysis Interface 23i-2031 Mahyar Zeb")

# ----------------------------
# 2. Sidebar: Dataset Ingestion
# ----------------------------
st.sidebar.header("Dataset Controls")

uploaded_file = st.sidebar.file_uploader(
    "Upload a csv File",
    type=["csv"]
)

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.sidebar.success("File uploaded")

        # ----------------------------
        # 3.Dataset preview
        # ----------------------------
        st.subheader("Dataset preview and Meta data")
        st.dataframe(df.head())

        st.subheader("Dataset data")

        col1, col2 = st.columns(2)

        with col1:
            st.write("### Dimensional Properties")
            st.write(f"**Rows:** {df.shape[0]}")
            st.write(f"**Columns:** {df.shape[1]}")

            st.write("### Data types")
            st.write(df.dtypes)

        with col2:
            st.write("### Missing values from coloumn")
            st.write(df.isnull().sum())

            st.write("### Statistical summary (Numerical coloumn)")
            st.write(df.describe())


        st.sidebar.header("Feature Selection")
        selected_column = st.sidebar.selectbox("Select a column for analysis",df.columns)

        st.subheader(f"Visualization for: {selected_column}")

      
        # ----------------------------
        # Attribute type
        # ----------------------------
        if pd.api.types.is_numeric_dtype(df[selected_column]):
            attribute_type = "Numerical"
        else:
            attribute_type = "Categorical"

        st.write(f"**Detected attribute Type:** {attribute_type}")

        # -------------------------------
        # Visualization Section
        # -------------------------------
        fig, ax = plt.subplots(figsize=(5, 5))

        if attribute_type == "Numerical":
            sns.histplot(df[selected_column].dropna(), bins=25, kde=True, ax=ax)
            ax.set_title(f"Histogram from {selected_column}")
            ax.set_xlabel(selected_column)
            ax.set_ylabel("Frequency")

        else:
            value_counts = df[selected_column].value_counts()
            sns.barplot(
                x=value_counts.index,
                y=value_counts.values,
                ax=ax
            )
            ax.set_title(f"Bar chart from {selected_column}")
            ax.set_xlabel(selected_column)
            ax.set_ylabel("Count")
            plt.xticks(rotation=45)

        st.pyplot(fig)

    except Exception as e:
        st.error("upload a valid csv file")
        st.error(str(e))

else:
    st.info("upload a csv file to begin.")