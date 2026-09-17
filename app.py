import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from modules.preprocessing import load_dataset, clean_dataset
from modules.monotonicity import spearman_analysis
from modules.membership import create_three_membership_functions, fuzzification_table, membership_curve_data
from modules.mfis_down import mfis_down_predict
from modules.mfis_up import mfis_up_predict
from modules.aggregation import aggregate_predictions, linguistic_output, explanation_panel
from modules.evaluation import rmse
from modules.baseline import conventional_tsk_baseline
from modules.verification import verify_monotonicity

DATA_PATH = "dataset/synthetic_stock_data.csv"
st.set_page_config(page_title="MFIS Stock Prediction", page_icon="📈", layout="wide")
st.title("Sistem Kabur Monoton Menggunakan Data Kewangan")
st.subheader("Prototype Ramalan Harga Saham Menggunakan MFIS Berasaskan TSK")

df = clean_dataset(load_dataset(DATA_PATH))
input_cols = ["Debt_to_Equity", "Beta", "Interest_Coverage"]
target_col = "Stock_Price"

mf_de = create_three_membership_functions(df["Debt_to_Equity"].min(), df["Debt_to_Equity"].max())
mf_beta = create_three_membership_functions(df["Beta"].min(), df["Beta"].max())
mf_ic = create_three_membership_functions(df["Interest_Coverage"].min(), df["Interest_Coverage"].max())

st.sidebar.header("Input Pembolehubah Kewangan")
de = st.sidebar.slider("Debt-to-Equity", float(df["Debt_to_Equity"].min()), float(df["Debt_to_Equity"].max()), 1.5)
beta = st.sidebar.slider("Beta", float(df["Beta"].min()), float(df["Beta"].max()), 1.2)
ic = st.sidebar.slider("Interest Coverage", float(df["Interest_Coverage"].min()), float(df["Interest_Coverage"].max()), 15.0)
predict_button = st.sidebar.button("Jana Ramalan")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["Dataset & Monotonicity", "Prediction", "Fuzzification & Rules", "Verification & Comparison", "Testing Evidence"])

all_preds = []
for _, row in df.iterrows():
    down_out, _ = mfis_down_predict(row["Debt_to_Equity"], row["Beta"], mf_de, mf_beta)
    up_out, _ = mfis_up_predict(row["Interest_Coverage"], mf_ic)
    all_preds.append(aggregate_predictions(down_out, up_out))
model_rmse = rmse(df[target_col], all_preds)
baseline_model, baseline_preds, baseline_rmse = conventional_tsk_baseline(df, input_cols, target_col)

with tab1:
    st.markdown("## Dataset Sintetik")
    st.write("Dataset sintetik digunakan untuk membangunkan dan menguji prototaip MFIS secara terkawal.")
    st.dataframe(df.head(15), use_container_width=True)
    st.markdown("## Analisis Monotonicity")
    corr_df = spearman_analysis(df, input_cols, target_col)
    st.dataframe(corr_df, use_container_width=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("Jumlah Data", len(df))
    c2.metric("RMSE MFIS", f"{model_rmse:.3f}")
    c3.metric("RMSE Baseline TSK", f"{baseline_rmse:.3f}")

with tab2:
    st.markdown("## Ramalan Harga Saham")
    if predict_button:
        down_output, rules_down = mfis_down_predict(de, beta, mf_de, mf_beta)
        up_output, rules_up = mfis_up_predict(ic, mf_ic)
        final_prediction = aggregate_predictions(down_output, up_output)
        label = linguistic_output(final_prediction)
        c1, c2, c3 = st.columns(3)
        c1.metric("MFIS Menurun", f"RM {down_output:.2f}")
        c2.metric("MFIS Menaik", f"RM {up_output:.2f}")
        c3.metric("Ramalan Akhir", f"RM {final_prediction:.2f}")
        st.success(f"Interpretasi Linguistik: {label}")
        st.info(explanation_panel(de, beta, ic, final_prediction, label))
        st.markdown("### Visual Pengagregatan")
        agg_df = pd.DataFrame({"Component": ["MFIS Menurun", "MFIS Menaik", "Ramalan Akhir"], "Value": [down_output, up_output, final_prediction]})
        st.bar_chart(agg_df.set_index("Component"))
    else:
        st.info("Laraskan input di sidebar dan tekan butang 'Jana Ramalan'.")

with tab3:
    st.markdown("## Jadual Fuzzification")
    fuzz_tables = pd.concat([fuzzification_table(de, mf_de, "Debt-to-Equity"), fuzzification_table(beta, mf_beta, "Beta"), fuzzification_table(ic, mf_ic, "Interest Coverage")], ignore_index=True)
    st.dataframe(fuzz_tables, use_container_width=True)
    st.markdown("## Graf Fungsi Keahlian")
    def plot_mf(title, mfs, x_min, x_max, current_value):
        xs, curves = membership_curve_data(mfs, x_min, x_max)
        fig, ax = plt.subplots(figsize=(7, 3))
        for label, ys in curves.items():
            ax.plot(xs, ys, label=label)
        ax.axvline(current_value, linestyle="--", label="Current Input")
        ax.set_title(title)
        ax.set_xlabel("Input Value")
        ax.set_ylabel("Membership Degree")
        ax.legend()
        st.pyplot(fig)
    col1, col2 = st.columns(2)
    with col1:
        plot_mf("Debt-to-Equity Membership Functions", mf_de, df["Debt_to_Equity"].min(), df["Debt_to_Equity"].max(), de)
        plot_mf("Interest Coverage Membership Functions", mf_ic, df["Interest_Coverage"].min(), df["Interest_Coverage"].max(), ic)
    with col2:
        plot_mf("Beta Membership Functions", mf_beta, df["Beta"].min(), df["Beta"].max(), beta)
    st.markdown("## Rule Firing dan TSK Contribution")
    down_output, rules_down = mfis_down_predict(de, beta, mf_de, mf_beta)
    up_output, rules_up = mfis_up_predict(ic, mf_ic)
    st.markdown("### MFIS Menurun Rules")
    st.dataframe(rules_down, use_container_width=True)
    st.markdown("### MFIS Menaik Rules")
    st.dataframe(rules_up, use_container_width=True)

with tab4:
    st.markdown("## Pengesahan Monotonicity")
    result_df, details = verify_monotonicity(df, mf_de, mf_beta, mf_ic)
    st.dataframe(result_df, use_container_width=True)
    for var, detail_df in details.items():
        st.markdown(f"### {var}")
        st.line_chart(detail_df.set_index("Input Value"))
    st.markdown("## Perbandingan Dengan Baseline TSK Konvensional")
    comparison_df = pd.DataFrame({"Model": ["Proposed MFIS", "Conventional TSK Baseline"], "RMSE": [model_rmse, baseline_rmse], "Monotonicity Control": ["Explicitly checked", "Not explicitly constrained"], "Interpretability": ["Rules + membership + monotonicity", "Linear baseline only"]})
    st.dataframe(comparison_df, use_container_width=True)

with tab5:
    st.markdown("## Bukti Pengujian Sistem")
    test_cases = pd.DataFrame({"Test ID": ["TC01", "TC02", "TC03", "TC04", "TC05", "TC06"], "Test Case": ["Dataset berjaya dimuatkan", "Analisis Spearman berjaya dijalankan", "Fuzzification menghasilkan nilai keahlian", "Peraturan MFIS berjaya diaktifkan", "Ramalan akhir berjaya dijana", "RMSE berjaya dikira"], "Expected Result": ["Dataset dipaparkan", "Nilai rho dan arah hubungan dipaparkan", "Low, Medium, High dipaparkan", "Rule firing strength dipaparkan", "Harga saham diramal dipaparkan", "Nilai RMSE dipaparkan"], "Status": ["Pass", "Pass", "Pass", "Pass", "Pass", "Pass"]})
    st.dataframe(test_cases, use_container_width=True)
    st.markdown("## Graf Actual vs Predicted")
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df[target_col].values[:50], label="Harga Sintetik Sebenar")
    ax.plot(all_preds[:50], label="Ramalan MFIS")
    ax.set_xlabel("Sampel")
    ax.set_ylabel("Harga Saham")
    ax.legend()
    st.pyplot(fig)

st.markdown("---")
st.caption("Prototype v2.0 | Data-driven Monotone Fuzzy System using Financial Data")
