ccc= 0
while ccc < len(array_time):
    for zapis in connections.coll_connector.find(
            {
                "date": {"$gt": start, "$lt": end},
                "doctor_id": array_doc_id[id_],
                "time": array_time[ccc],
            }
    ):
        array_zapis_fio.append(zapis["patient_name"])  # ФИО
        array_zapis_worry.append(
            zapis["patient_info"]
        )  # Беспокойства
    ccc += 1