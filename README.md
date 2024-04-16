# Funder Extraction App

Extract funder names and their corresponding ROR IDs from a given funding statement. Utilizes the `ner-english-large` model from the [Flair library](https://github.com/flairNLP/flair?tab=readme-ov-file) for named entity recognition (NER) to identify organization names and the ROR API to retrieve the associated ROR IDs.

## Installation

   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the Streamlit app:

   ```
   streamlit run app.py
   ```

2. Access the app in your browser at `http://localhost:8501`

3. Enter a funding statement in the text box.

4. Click the "Extract" button to extract funder names and ROR IDs.

5. The extracted funders and their ROR IDs will be displayed in a table.
