import pandas as pd
import numpy as np


def load_reports():
    return pd.read_excel("Выписки/Выписка122.xls"), pd.read_excel("Выписки/Выписка123.xls")

def load_uni_file():
    return pd.read_csv("uni.csv", sep=';', encoding='ISO-8859-1')

def join_data(report_dataframes, uni_dataframe):
    report_df = pd.concat(report_dataframes)
    report_df.reset_index(inplace=True, drop=True)

    return pd.merge(report_df, uni_dataframe, left_on='Код авторизации', right_on='AuthCode')

def generate_report(total_info):
    total_info['Время обработки'] = pd.Timestamp("now")
    total_info['Время обработки'] = total_info['Время обработки'].map(lambda x: x.strftime('%d.%m.%Y %H:%M'))

    total_info['Комиссия'] = np.round(total_info['Сумма операции'] * 0.0125, 2)

    total_info['Сумма к переводу'] = np.round(total_info['Сумма операции'] - total_info['Комиссия'], 2)

    return total_info

def save_report(total_info):
    final_report = total_info[
        ['Номер устройства',
        'Дата операции',
        'Дата обработки',
        'Сумма операции',
        'Торговая уступка',
        'К перечислению',
        'РРН',
        'Тип операции',
        'Код авторизации',
        'Время обработки',
        'OrderID',
        'Комиссия',
        'Сумма к переводу',
        'Номер платежного поручения',
        'Дата платежного поручения'
        ]
    ]

    final_report.to_excel('Отчет.xlsx', index=False)

def main():
    report = generate_report(join_data(load_reports(), load_uni_file()))
    save_report(report)

if __name__ == "__main__":
    main()