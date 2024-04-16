import re
import requests
from flair.data import Sentence
from flair.models import SequenceTagger

ROR_URL = "https://api.ror.org/organizations"
MODEL_PATH = 'flair/ner-english-large'
model = SequenceTagger.load(MODEL_PATH)


def extract_organisation_names(text):
    org_tags = []
    sentence = Sentence(text)
    model.predict(sentence)
    print(sentence.get_spans('ner'))
    names = {entity.text for entity in sentence.get_spans(
        'ner') if entity.tag == 'ORG'}
    return list(names)


def get_ror_id(org_name):
    if org_name is None or not re.search(r"[a-zA-Z]", org_name):
        return None, None
    org_name = re.sub(r'[{."\\]', "", org_name)
    matched = requests.get(ROR_URL, {"affiliation": org_name})
    if matched.status_code != 200:
        return None, None
    matched = matched.json()
    for matched_org in matched["items"]:
        if matched_org["chosen"]:
            ror_id = matched_org["organization"]["id"]
            country = matched_org["organization"].get(
                "country", {}).get("country_name")
            return ror_id, country
    return None, None


def extract_funders_and_ror_ids(text):
    org_names = extract_organisation_names(text)
    ror_ids_countries = [get_ror_id(org_name) for org_name in org_names]
    names_awards_ids = []
    for org_name, (ror_id, country) in zip(org_names, ror_ids_countries):
        names_awards_ids.append((org_name, ror_id, country))
    return names_awards_ids
