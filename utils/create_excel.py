import pandas as pd


def Turma_xlsx(file_path, df):

    # use to_excel function and specify the sheet_name and index
    # to store the dataframe in specified sheet
    with pd.ExcelWriter(file_path) as writer:

        for idx, turma in enumerate(df['id_turma'].unique()):
            aux = df[df['id_turma'] == turma].copy()

            aux.to_excel(
                writer,
                sheet_name=f"{idx + 1}-{turma}",
                index=False,

            )