import pandas as pd

def load_data(anonymized_path, auxiliary_path):
    """
    Load anonymized and auxiliary datasets.
    """
    anon = pd.read_csv(anonymized_path)
    aux = pd.read_csv(auxiliary_path)
    return anon, aux


def link_records(anon_df, aux_df):
    """
    Attempt to link anonymized records to auxiliary records
    using exact matching on quasi-identifiers.

    Returns a DataFrame with columns:
      anon_id, matched_name
    containing ONLY uniquely matched records.
    """

    anon_ids = []
    matched_names = []

    for i in range(len(anon_df)):
        match = False
        for j in range(len(aux_df)):
            anon = anon_df[i]
            aux = aux_df[j]

            if anon['age'] == aux['age'] and anon['zip3'] == aux['zip3'] and anon['gender'] == aux['gender']:
                if match:
                    i = anon_ids.index(anon['anon_id'])
                    anon_ids.pop(i)
                    matched_names.pop(i)
                else:
                    anon_ids.append(anon['anon_id'])
                    matched_names.append(aux['name'])

    d = {"anon_id": anon_ids, "matched_name": matched_names}
    return pd.DataFrame(data=d)

        


def deanonymization_rate(matches_df, anon_df):
    """
    Compute the fraction of anonymized records
    that were uniquely re-identified.
    """
    return len(matches_df) / len(anon_df)
