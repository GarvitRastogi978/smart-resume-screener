import streamlit as st
from pathlib import Path
import pandas as pd
from io import BytesIO

# Import project modules (assumes project structure with src/)
from src.parse_resume import extract_text, extract_years_of_experience
from src.nlp_utils import build_skill_phrase_matcher
from src.matcher import extract_skills_with_matcher
from src.scoring import combined_match_score

ROOT = Path(__file__).parent
SKILLS_FILE = ROOT / 'skills_list.txt'

# Load skills
with open(SKILLS_FILE, 'r', encoding='utf-8') as f:
    SKILLS = [line.strip() for line in f if line.strip()]

# Build matcher once
matcher = build_skill_phrase_matcher(SKILLS)

st.set_page_config(page_title="Smart Resume Screener | Garvit Rastogi", layout="wide")
st.title("📑 Smart Resume Screener — AI-powered HR tool 🚀🎯")

col_left, col_right = st.columns([1, 2])

with col_left:
    st.header("Upload 📥")
    st.subheader("Single resume 1️⃣")
    uploaded_file = st.file_uploader("Drop a resume (PDF or DOCX)", type=["pdf","docx"], key='single')

    st.markdown("---")
    st.subheader("Bulk upload 🔢")
    st.write("Upload multiple resumes (PDF/DOCX). Files will be processed and ranked.")
    bulk_files = st.file_uploader("Bulk upload (multiple)", type=["pdf","docx"], accept_multiple_files=True, key='bulk')

    st.markdown("---")
    jd_text = st.text_area("Paste Job Description (JD) here👇", height=220)
    weight = st.slider("Combine weights (JD similarity vs Skill coverage)", 0.0, 1.0, 0.6)
    min_score = st.slider("Minimum pass score (0..100)", 0, 100, 50)
    run_button = st.button("Score Resume(s)")

with col_right:
    st.header("Results 🏆")

    if run_button:
        if not jd_text.strip():
            st.warning("Please paste a Job Description (JD) to score against.")
        elif (not uploaded_file) and (not bulk_files):
            st.warning("Upload at least one resume (single or bulk).")
        else:
            results = []

            # Helper to process a single file object
            def process_file(file_obj):
                # Save to temp bytes and call extract_text which accepts path; we will write to a temp file
                tmp_path = ROOT / "tmp_uploads"
                tmp_path.mkdir(exist_ok=True)
                saved = tmp_path / file_obj.name
                with open(saved, "wb") as f:
                    f.write(file_obj.getbuffer())
                text = extract_text(str(saved))
                years = extract_years_of_experience(text)
                resume_skills = extract_skills_with_matcher(text, matcher, SKILLS)
                jd_required = extract_skills_with_matcher(jd_text, matcher, SKILLS)
                # combined_match_score currently returns values 0..1 for score, sim, scov
                score, jd_sim, scov = combined_match_score(jd_text, text, jd_required, resume_skills, weights=(weight, 1-weight))
                # convert to percent
                score_pct = score * 100.0
                jd_sim_pct = jd_sim * 100.0
                scov_pct = scov * 100.0
                missing = sorted([s for s in jd_required if s.lower() not in {x.lower() for x in resume_skills}])
                result = {
                    'filename': file_obj.name,
                    'match_score_pct': round(score_pct, 2),
                    'jd_similarity_pct': round(jd_sim_pct, 2),
                    'skill_coverage_pct': round(scov_pct, 2),
                    'years_experience': years,
                    'matched_skills': ';'.join(sorted(list(resume_skills))),
                    'required_skills': ';'.join(sorted(list(jd_required))),
                    'missing_skills': ';'.join(missing)
                }
                return result, resume_skills, jd_required, text

            # Process single file first (if provided)
            if uploaded_file:
                res, resume_skills, jd_required, text = process_file(uploaded_file)
                results.append(res)

                st.subheader(f"Results — {uploaded_file.name}")
                st.metric("Match score", f"{res['match_score_pct']:.1f} / 100")
                st.write(f"JD vs Resume similarity: {res['jd_similarity_pct']:.1f}% | Skill coverage: {res['skill_coverage_pct']:.1f}%")
                if res['years_experience']:
                    st.write(f"Estimated years of experience (heuristic): {res['years_experience']}")

                st.markdown("**Matched skills (from resume)**")
                st.write(resume_skills)
                st.markdown("**Required skills (from JD)**")
                st.write(jd_required)
                st.markdown("**Missing skills**")
                if res['missing_skills']:
                    st.warning(res['missing_skills'])
                else:
                    st.success("No missing skills detected!")

            # Process bulk files
            if bulk_files:
                st.subheader('Bulk results')
                with st.spinner('Processing bulk files...'):
                    for bf in bulk_files:
                        try:
                            r, _, _, _ = process_file(bf)
                            results.append(r)
                        except Exception as e:
                            st.error(f"Failed to process {bf.name}: {e}")

                if results:
                    df = pd.DataFrame(results)
                    df.sort_values('match_score_pct', ascending=False, inplace=True)
                    st.dataframe(df[['filename','match_score_pct','jd_similarity_pct','skill_coverage_pct','years_experience']])

                    # show pass/fail based on min_score
                    df['status'] = df['match_score_pct'].apply(lambda x: 'PASS' if x >= min_score else 'REJECT')
                    st.markdown('### Ranked results (top 50)')
                    st.dataframe(df.head(50))

                    # Provide download
                    csv_bytes = df.to_csv(index=False).encode('utf-8')
                    st.download_button('Download bulk results CSV', data=csv_bytes, file_name='bulk_screen_results.csv', mime='text/csv')

                    # allow clicking a row to inspect details? simple approach: let user pick file name
                    pick = st.selectbox('Inspect a file from results', options=df['filename'].tolist())
                    pick_row = df[df['filename']==pick].iloc[0]
                    st.markdown(f"**Selected:** {pick_row['filename']} — Score: {pick_row['match_score_pct']} / 100 — {pick_row['status']}")
                    st.markdown('**Matched skills**')
                    st.write(pick_row['matched_skills'].split(';'))
                    st.markdown('**Missing skills**')
                    if pick_row['missing_skills']:
                        st.warning(pick_row['missing_skills'])
                    else:
                        st.success('No missing skills!')

            # If only single was processed and no bulk, provide a CSV for single
            if uploaded_file and (not bulk_files):
                df_single = pd.DataFrame([res])
                csv = df_single.to_csv(index=False).encode('utf-8')
                st.download_button('Download single result CSV', data=csv, file_name=f"{uploaded_file.name}_screen.csv", mime='text/csv')

    else:
        st.info('Upload a resume and paste a Job Description (JD), then click "Score Resume(s)".')

# Footer / tips
st.markdown('---')
st.write('Tips: Improve the skills list in skills_list.txt and add synonyms to increase match quality.')