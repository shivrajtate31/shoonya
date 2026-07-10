import streamlit as st
from conscience import evaluate_beliefs  # import your core function

st.set_page_config(page_title="Shoonya Belief Evaluator", layout="wide")

st.title(" Shoonya: Belief Evaluation System")
st.subheader("Evaluate beliefs against your core values")

with st.expander(" Instructions"):
    st.markdown("""
    - Paste multiple beliefs (one per line).
    - Hit **Evaluate** to see how each belief aligns with Shoonya's values.
    """)

input_text = st.text_area(" Enter beliefs (one per line)", height=300)

if st.button(" Evaluate"):
    with st.spinner("Evaluating..."):
        beliefs = input_text.strip().split("\n")
        beliefs = [b for b in beliefs if b.strip()]

        results = evaluate_beliefs(beliefs)

        st.success("Done!")

        for idx, result in enumerate(results, 1):
            st.markdown(f"### 🔹 Belief #{idx}")
            st.markdown(f"> {result['belief']}")
            st.markdown(f" **Match Score:** {result['match_score']}")
            if result["matched_values"]:
                st.markdown(f" **Matches:** {', '.join(result['matched_values'])}")
            else:
                st.markdown(f" **Matches:** None")
            st.divider()

        # Summary
        from collections import Counter
        flat_matches = [val for r in results for val in r["matched_values"]]
        summary = dict(Counter(flat_matches))
        if summary:
            st.subheader(" Summary")
            for k, v in summary.items():
                st.markdown(f" **{k}**: {v} matches")
