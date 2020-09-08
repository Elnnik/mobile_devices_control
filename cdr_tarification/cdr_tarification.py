import csv
from typing import Dict 

def get_tariffication_values(csv_file_name:str, mobile_number:str, msisdn_origin_index:int, msisdn_dest_index:int, call_duration_index:int, sms_number_index:int) -> Dict:
    """
    Возвращает словарь значений для тарификации абонента: Исходящие минуты, Входящие минуты, Исходящие СМС, Входящие СМС
    """

    with open(csv_file_name) as csv_file:
        
        csv_reader = csv.reader(csv_file, delimiter=',')

        tariffication_values_dict = {}

        for row in csv_reader:

            if row[msisdn_origin_index] == mobile_number:
                
                tariffication_values_dict['outgoing_calls_duration'] = float( row[call_duration_index] )
                tariffication_values_dict['outgoing_sms_count'] = int( row[sms_number_index] ) 

            if row[msisdn_dest_index] == mobile_number:

                incoming_calls_duration = float ( row[call_duration_index] )
                tariffication_values_dict['incoming_calls_duration'] = float ( row[call_duration_index] )
                tariffication_values_dict['incoming_sms_count'] = int ( row[sms_number_index] )


    return tariffication_values_dict


def sms_and_calls_tariffication(tariffication_values_dict: Dict) -> Dict:
    """
    Возвращает словарь с тарификацией Телефонии, СМС и общей тарификацией
    """

    outgoing_calls_coeff = 4
    incoming_calls_coeff = 1
    all_sms_coeff = 1

    incoming_calls_free_minutes = 5
    free_sms_count = 5
    
    tariffication_dict = {}

    tariffication_dict['Outgoing_calls_tariffication'] = outgoing_calls_tariffication = tariffication_values_dict.get('outgoing_calls_duration', 0) * outgoing_calls_coeff
    
    if (tariffication_values_dict.get('incoming_calls_duration', 0) > 5):
        tariffication_dict['Incoming_calls_tariffication'] = incoming_calls_tariffication = (tariffication_values_dict['incoming_calls_duration'] - 5) * incoming_calls_coeff
    else:
        tariffication_dict['Incoming_calls_tariffication'] = incoming_calls_tariffication = 0
    
    sms_count_total = tariffication_values_dict.get('incoming_sms_count', 0) + tariffication_values_dict.get('outgoing_sms_count', 0)
    
    if (sms_count_total > free_sms_count):
        tariffication_dict['Incoming_and_Outcoming_sms_tariffication'] = incoming_and_outcoming_sms_tariffication = (sms_count_total - free_sms_count) * all_sms_coeff
    else:
        tariffication_dict['Incoming_and_Outcoming_sms_tariffication'] = incoming_and_outcoming_sms_tariffication = 0
    
    tariffication_dict['Total_tariffication_value'] = outgoing_calls_tariffication + incoming_calls_tariffication + incoming_and_outcoming_sms_tariffication
    
    return tariffication_dict

FILE_NAME = 'data.csv'
PHONE_NUMBER = '968247916'

tariffication_values_dict = get_tariffication_values(FILE_NAME, PHONE_NUMBER, 1, 2, 3, 4)

print(f'Phone number: {PHONE_NUMBER}')

for k, v in sms_and_calls_tariffication(tariffication_values_dict).items():
    print(f'{k}: {v}')
