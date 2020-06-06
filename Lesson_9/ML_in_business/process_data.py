def weekly_lic_age(years):
    weeks_a_year = 52
    return int(years * weeks_a_year)


def map_for_dict_gender(gender):
    dict_gender = {"Male": 0, "Female": 1}
    res = dict_gender.get(gender)
    return res


def map_for_dict_maristat(maristat):
    dict_maristat = {"Other": 0, "Alone": 1}
    res = dict_maristat.get(maristat)
    return res


def f_soc_category(category):
    if len(category) >= 4:
        return category[:4]
    else:
        return "CSP5"


def f_veh_usage(usage):
    prob_usage = ["Private+trip to office", "Private", "Professional", "Professional run"]
    if usage in prob_usage:
        return usage
    else:
        return "Private+trip to office"


def f_risk_area(risk):
    const_risk_area = 7     # most probable risk area
    if risk:
        return int(risk)
    else:
        return const_risk_area


def f_out_usage(out_us):
    ou_for_new_client = 0.0
    if out_us:
        return float(out_us)
    else:
        return ou_for_new_client


def process_input(json_input):

    lic_age = weekly_lic_age(json_input["LicAge"])
    gender = map_for_dict_gender(json_input["Gender"])
    mari_stat = map_for_dict_maristat(json_input["MariStat"])
    socio_categ = f_soc_category(json_input["SocioCateg"])
    veh_usage = f_veh_usage(json_input["VehUsage"])
    drive_age = int(json_input["DrivAge"])
    has_km_limit = int(json_input["HasKmLimit"])
    bonus_malus = int(json_input["BonusMalus"])
    out_use_nb = f_out_usage(json_input["OutUseNb"])
    risk_area = f_risk_area(json_input["RiskArea"])
    drive_age_sq = drive_age ** 2

    data_list = [lic_age,
                 gender,
                 mari_stat,
                 socio_categ,
                 veh_usage,
                 drive_age,
                 has_km_limit,
                 bonus_malus,
                 out_use_nb,
                 risk_area,
                 drive_age_sq
                 ]

    return data_list
