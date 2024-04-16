import streamlit as st
import pandas as pd
from extract_funders_flair import extract_funders_and_ror_ids


def main():
    st.title("Extract Funders from Funding Statement")
    st.markdown("Enter a funding statement to extract funder names and ROR IDs.")
    funding_statement = st.text_area("Funding Statement", height=200)
    if st.button("Extract"):
        if funding_statement.strip():
            with st.spinner("Extracting funders and ROR IDs..."):
                try:
                    results = extract_funders_and_ror_ids(funding_statement)
                    if results:
                        table_data = []
                        for org_name, ror_id, country in results:
                            search_link = f'<a href="https://ror.org/search?query={org_name}" target="_blank">Search</a>'
                            if ror_id:
                                table_data.append({
                                    "Organisation": org_name,
                                    "ROR ID": f'<a href="{ror_id}" target="_blank">{ror_id}</a>',
                                    "Country": country if country else "",
                                    "Request": "",
                                    "Search": search_link
                                })
                            else:
                                table_data.append({
                                    "Organisation": org_name,
                                    "ROR ID": "",
                                    "Country": "",
                                    "Request": '<a href="https://curation-request.ror.org" target="_blank">Add record</a>',
                                    "Search": search_link
                                })
                        df = pd.DataFrame(table_data)
                        df = df.fillna("")  # Replace NaN values with empty strings
                        markdown_table = df.to_markdown(index=False)
                        st.markdown(markdown_table, unsafe_allow_html=True)
                    else:
                        st.markdown("**No funders found in the provided funding statement.**")
                except Exception as e:
                    st.error(f"An error occurred during extraction: {str(e)}")
        else:
            st.warning("Please enter a funding statement.")


if __name__ == "__main__":
    main()
