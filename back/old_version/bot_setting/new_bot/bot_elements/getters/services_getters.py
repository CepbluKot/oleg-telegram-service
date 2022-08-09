def get_all_services_names():
    
    services = [
        " Услуга 1",
        " Услуга 2",
        " Услуга 3",
    ]
    
    return services


def get_service_weeks(service_name: str):
    weeks = []
    if service_name == "Услуга 1":
        weeks = [
            "01.01.2022 - 08.01.2022",
            "08.01.2022 - 15.01.2022"
        ]
    elif service_name == "Услуга 2":
        weeks = [
            "15.01.2022 - 22.01.2022"
        ]
    elif service_name == "Услуга 3":
        weeks = [
            "02.02.2022 - 09.02.2022",
            "10.02.2022 - 17.02.2022",
            "18.02.2022 - 25.02.2022"
        ]
    
    return weeks


def get_service_days(service_name: str, service_week: str):
    days = []
    if service_name == "Услуга 1" and service_week == "01.01.2022 - 08.01.2022":
        days = [
            "1",
            "2",
            "4",
        ]

    elif service_name == "Услуга 1" and service_week == "08.01.2022 - 15.01.2022":
        days = [
            "8",
            "10",
            "12",
        ]

    elif service_name == "Услуга 2" and service_week == "15.01.2022 - 22.01.2022":
        days = [
            "16",
            "18",
            "20",
        ]

    elif service_name == "Услуга 3" and service_week == "02.02.2022 - 09.02.2022":
        days = [
            "3",
            "4",
            "7",
        ]
    
    elif service_name == "Услуга 3" and service_week == "10.02.2022 - 17.02.2022":
        days = [
            "10",
            "14",
            "17",
        ]

    elif service_name == "Услуга 3" and service_week == "18.02.2022 - 25.02.2022":
        days = [
            "20",
            "24",
            "15",
        ]

    return days

