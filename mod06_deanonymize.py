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

    qi_cols = ["age", "zip3", "gender"]

    candidates = anon_df[["anon_id", *qi_cols]].merge(
        aux_df[[*qi_cols, "name"]],
        on=qi_cols,
        how="inner",
    ).rename(columns={"name": "matched_name"})

    candidates = candidates[["anon_id", "matched_name"]].drop_duplicates()
    name_counts = candidates.groupby("anon_id")["matched_name"].nunique()
    unique_ids = name_counts[name_counts == 1].index

    return candidates[candidates["anon_id"].isin(unique_ids)].reset_index(drop=True)

        


def deanonymization_rate(matches_df, anon_df):
    """
    Compute the fraction of anonymized records
    that were uniquely re-identified.
    """
    return len(matches_df) / len(anon_df)
