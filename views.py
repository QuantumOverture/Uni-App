from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.debug import sensitive_variables
from .forms import RedirectToUni
import json
import requests


def RemoveExtraInfo(Major_String):
    OpenBracketIndex = -1
    Index = 0
    while Index <= len(Major_String)-1:
        if Major_String[Index] == "(":
            OpenBracketIndex = Index
            Index += 1
        elif Major_String[Index] ==")":
            Major_String = Major_String[:OpenBracketIndex] + Major_String[Index+1:]
            OpenBracketIndex = -1
            Index = 0
        else:
            Index += 1


    return Major_String


def MajorNamesList(Majors):
    # Convert into proper format here for api call
    # (ANTHING BETWEEN THESE TWO IS EXTRA INFO AND NOT PART OF API CALL)
    # Replace _ with spaces when providing extra info
    ResultString = ""
    for i in Majors:
        ResultString += "latest.academics.program_percentage."+RemoveExtraInfo(i)+","

    return ResultString

def AddExtraInfo(Major_String):
    return Major_String.replace("(","").replace(")","").replace("_"," ")

@sensitive_variables()
def SpecificUni(request,NAME,ID):
    Majors = ["agriculture","(natural_)resources(_and_conservation)","architecture","ethnic_cultural_gender(_studies)",
              "communication","communications_technology","computer(_science_and_information studies)","personal(_and)_culinary(_studies)",
              "education","engineering","engineering_technology(_and_engineering_related field)","(foreign_)language(_,literature,and_linguistics)",
              "family(_and)_consumer_science","legal(_profession_and_studies)","english","humanities","library(_science)","biological(_and_biomedical_science)",
              "mathematics","military(_technology_and_applied_sciences)","multidiscipline","parks_recreation_fitness(_studies)",
              "philosophy_religious","theology_religious_vocation","physical_science","science_technology","psychology","security_law_enforcement",
              "public_administration(_and)_social_service","social_science","construction","mechanic_(and_)repair_technology",
              "precision_production","transportation","visual_performing(_arts)","health","business_marketing","history"
             ]
    # Here forward to ID - Star rating - Text Review in Database fields
    # error check here if ID of school exists or not and NAME  exists in the the university's title
    # ApiKey = 'NOPE'
    URL = 'https://api.data.gov/ed/collegescorecard/v1/schools?'
    Fields = "&_fields=school.name,school.state," \
             "school.ownership,latest.admissions.admission_rate.overall," \
             "latest.student.enrollment.all,latest.cost.attendance.academic_year,latest.admissions.sat_scores.average.overall,"\
             "latest.aid.loan_principal,latest.aid.median_debt.completers.overall," \
             "latest.aid.cumulative_debt.number,latest.student.demographics.avg_family_income," \
             "latest.earnings.10_yrs_after_entry.working_not_enrolled.mean_earnings,latest.earnings.6_yrs_after_entry.working_not_enrolled.mean_earnings," \
             "latest.student.grad_students,latest.cost.program_reporter.program_1.cip_6_digit.full_program," \
             "school.region_id,school.degree_urbanization,school.school_url," \
             "school.carnegie_basic,school.carnegie_size_setting,school.city," \
             "latest.student.demographics.first_generation,latest.completion.completion_rate_4yr_100nt," \
             "school.religious_affiliation,latest.student.demographics.race_ethnicity.white," \
             "latest.student.demographics.race_ethnicity.black,latest.student.demographics.race_ethnicity.asian," \
             "latest.student.demographics.race_ethnicity.hispanic,latest.student.demographics.race_ethnicity.aian," \
             "latest.student.demographics.race_ethnicity.nhpi,latest.student.demographics.men,latest.student.demographics.women,"+MajorNamesList(Majors)

    WebSiteResponse = requests.get(URL+'id='+str(ID)+Fields+"&api_key="+ApiKey)
    WebsiteJSON = json.loads(WebSiteResponse.text)

    content = {
        "ID": ID,
        "NAME":NAME,
        "Proper_NAME":WebsiteJSON["results"][0]["school.name"],
        "Cost_Of_Attendance": WebsiteJSON["results"][0]["latest.cost.attendance.academic_year"],
        "Average_SAT" :WebsiteJSON["results"][0]["latest.admissions.sat_scores.average.overall"],
        "Student_enrollment": WebsiteJSON["results"][0]["latest.student.enrollment.all"],
        "10_years_avg_earnings":WebsiteJSON["results"][0]["latest.earnings.10_yrs_after_entry.working_not_enrolled.mean_earnings"],
        "Number_of_grad_students": WebsiteJSON["results"][0]["latest.student.grad_students"],
        "Number_of_in_debt_students":WebsiteJSON["results"][0]["latest.aid.cumulative_debt.number"],
        "School_type": WebsiteJSON["results"][0]["school.ownership"],
        "Principle_Loan": WebsiteJSON["results"][0]["latest.aid.loan_principal"],
        "6_years_avg_earnings": WebsiteJSON["results"][0]["latest.earnings.6_yrs_after_entry.working_not_enrolled.mean_earnings"],
        "admission_rate":round(WebsiteJSON["results"][0]["latest.admissions.admission_rate.overall"] * 100,2),
        "state":WebsiteJSON["results"][0]["school.state"],
        "average_family_income":WebsiteJSON["results"][0]["latest.student.demographics.avg_family_income"],
        "median_debt":WebsiteJSON["results"][0]["latest.aid.median_debt.completers.overall"],
        "top_program_cost":WebsiteJSON["results"][0]["latest.cost.program_reporter.program_1.cip_6_digit.full_program"],
        "region": WebsiteJSON["results"][0]["school.region_id"],
        "town_type":WebsiteJSON["results"][0]["school.degree_urbanization"],
        "url":WebsiteJSON["results"][0]["school.school_url"],
        "school_type":WebsiteJSON["results"][0]["school.carnegie_basic"],
        "setting_size":WebsiteJSON["results"][0]["school.carnegie_size_setting"],
        "city":WebsiteJSON["results"][0]["school.city"],
        "percent_men": round(WebsiteJSON["results"][0]["latest.student.demographics.men"] * 100,2),
        "percent_women": round(WebsiteJSON["results"][0]["latest.student.demographics.women"] * 100,2),
        "first_gen": round(WebsiteJSON["results"][0]["latest.student.demographics.first_generation"] * 100,2),
        "four_year_completion":round(WebsiteJSON["results"][0]["latest.completion.completion_rate_4yr_100nt"] * 100,2),
        "religious_affiliation":WebsiteJSON["results"][0]["school.religious_affiliation"],
        "race_white": round(WebsiteJSON["results"][0]["latest.student.demographics.race_ethnicity.white"] * 100,2),
        "race_black": round(WebsiteJSON["results"][0]["latest.student.demographics.race_ethnicity.black"] * 100,2),
        "race_asian": round(WebsiteJSON["results"][0]["latest.student.demographics.race_ethnicity.asian"] * 100,2),
        "race_aian": round(WebsiteJSON["results"][0]["latest.student.demographics.race_ethnicity.aian"] * 100,2),
        "race_nhpi": round(WebsiteJSON["results"][0]["latest.student.demographics.race_ethnicity.nhpi"] * 100,2),
        "race_hispanic": round(WebsiteJSON["results"][0]["latest.student.demographics.race_ethnicity.hispanic"] * 100,2),
    }

    # get integer data into proper format

    School_type_dict = {1:"Public",2:"Private(Non-Profit)",3:"Private(For-Profit)"}
    School_type_cg_dict = { None:"None",
                            0:"NOT CLASSIFIED",
                            -2:"NOT APPLICABLE",
                            1:"Associate's Colleges: High Transfer-High Traditional",
                            2:"Associate's Colleges: High Transfer-Mixed Traditional/Nontraditional",
                            3:"Associate's Colleges: High Transfer-High Nontraditional",
                            4:"Associate's Colleges: Mixed Transfer/Career & Technical-High Traditional",
                            5:"Associate's Colleges: Mixed Transfer/Career & Technical-Mixed Traditional/Nontraditional",
                            6:"Associate's Colleges: Mixed Transfer/Career & Technical-High Nontraditional",
                            7:"Associate's Colleges: High Career & Technical-High Traditional",
                            8:"Associate's Colleges: High Career & Technical-Mixed Traditional/Nontraditional",
                            9:"Associate's Colleges: High Career & Technical-High Nontraditional",
                            10:"Special Focus Two-Year: Health Professions",
                            11:"Special Focus Two-Year: Technical Professions",
                            12:"Special Focus Two-Year: Arts & Design",
                            13:"Special Focus Two-Year: Other Fields",
                            14:"Baccalaureate/Associate's Colleges: Associate's Dominant",
                            15:"Doctoral Universities: Very High Research Activity",
                            16:"Doctoral Universities: High Research Activity",
                            17:"Doctoral/Professional Universities",
                            18:"Master's Colleges & Universities: Larger Programs",
                            19:"Master's Colleges & Universities: Medium Programs",
                            20:"Master's Colleges & Universities: Small Programs",
                            21:"Baccalaureate Colleges: Arts & Sciences Focus",
                            22:"Baccalaureate Colleges: Diverse Fields",
                            23:"Baccalaureate/Associate's Colleges: Mixed Baccalaureate/Associate's",
                            24:"Special Focus Four-Year: Faith-Related Institutions",
                            25:"Special Focus Four-Year: Medical Schools & Centers",
                            26:"Special Focus Four-Year: Other Health Professions Schools",
                            27:"Special Focus Four-Year: Engineering Schools",
                            28:"Special Focus Four-Year: Other Technology-Related Schools",
                            29:"Special Focus Four-Year: Business & Management Schools",
                            30:"Special Focus Four-Year: Arts, Music & Design Schools",
                            31:"Special Focus Four-Year: Law Schools",
                            32:"Special Focus Four-Year: Other Special Focus Institutions",
                            33:"Tribal Colleges"
                        }
    setting_size_dict = {None:"None",
                         0:"NOT CLASSIFIED",
                        -2:"NOT APPLICABLE",
                        1:"Two-year, very small",
                        2:"Two-year, small",
                        3:"Two-year, medium",
                        4:"Two-year, large",
                        5:"Two-year, very large",
                        6:"Four-year, very small, primarily nonresidential",
                        7:"Four-year, very small, primarily residential",
                        8:"Four-year, very small, highly residential",
                        9:"Four-year, small, primarily nonresidential",
                        10:"Four-year, small, primarily residential",
                        11:"Four-year, small, highly residential",
                        12:"Four-year, medium, primarily nonresidential",
                        13:"Four-year, medium, primarily residential",
                        14:"Four-year, medium, highly residential",
                        15:"Four-year, large, primarily nonresidential",
                        16:"Four-year, large, primarily residential",
                        17:"Four-year, large, highly residential",
                        18:"Exclusively graduate/professional"
                        }
    region_weather_dict = {0:"US Service School( Please Research on own )",1:"warm to hot summers and super cold winters",
                           2:"cool to cold winters and hot,humid summers",
                           3:"warm to hot summers and super cold winters",
                           4:"warm to hot summers and super cold winters",
                           5:"mild winters and humid,hot summers",
                           6:"mild winters and EXTREME dry summers",
                           7:"cool and wet in every season expect summer(where it is dry)",
                           8:"Dry and hot summers with mild to cold winters",
                           9:"Outlying Areas ( Please Research on own )"
                           }

    religious_afflil_dict={  None:"None",
                            -1:"Not reported",
                            -2:"Not applicable",
                            22:"American Evangelical Lutheran Church",
                            24:"African Methodist Episcopal Zion Church",
                            27:"Assemblies of God Church",
                            28:"Brethren Church",
                            30:"Roman Catholic",
                            33:"Wisconsin Evangelical Lutheran Synod",
                            34:"Christ and Missionary Alliance Church",
                            35:"Christian Reformed Church",
                            36:"Evangelical Congregational Church",
                            37:"Evangelical Covenant Church of America",
                            38:"Evangelical Free Church of America",
                            39:"Evangelical Lutheran Church",
                            40:"International United Pentecostal Church",
                            41:"Free Will Baptist Church",
                            42:"Interdenominational",
                            43:"Mennonite Brethren Church",
                            44:"Moravian Church",
                            45:"North American Baptist",
                            47:"Pentecostal Holiness Church",
                            48:"Christian Churches and Churches of Christ",
                            49:"Reformed Church in America",
                            50:"Episcopal Church, Reformed",
                            51:"African Methodist Episcopal",
                            52:"American Baptist",
                            53:"American Lutheran",
                            54:"Baptist",
                            55:"Christian Methodist Episcopal",
                            57:"Church of God",
                            58:"Church of Brethren",
                            59:"Church of the Nazarene",
                            60:"Cumberland Presbyterian",
                            61:"Christian Church (Disciples of Christ)",
                            64:"Free Methodist",
                            65:"Friends",
                            66:"Presbyterian Church (USA)",
                            67:"Lutheran Church in America",
                            68:"Lutheran Church - Missouri Synod",
                            69:"Mennonite Church",
                            71:"United Methodist",
                            73:"Protestant Episcopal",
                            74:"Churches of Christ",
                            75:"Southern Baptist",
                            76:"United Church of Christ",
                            77:"Protestant, not specified",
                            78:"Multiple Protestant Denomination",
                            79:"Other Protestant",
                            80:"Jewish",
                            81:"Reformed Presbyterian Church",
                            84:"United Brethren Church",
                            87:"Missionary Church Inc",
                            88:"Undenominational",
                            89:"Wesleyan",
                            91:"Greek Orthodox",
                            92:"Russian Orthodox",
                            93:"Unitarian Universalist",
                            94:"Latter Day Saints (Mormon Church)",
                            95:"Seventh Day Adventists",
                            97:"The Presbyterian Church in America",
                            99:"Other (none of the above)",
                            100:"Original Free Will Baptist",
                            101:"Ecumenical Christian",
                            102:"Evangelical Christian",
                            103:"Presbyterian",
                            105:"General Baptist",
                            106:"Muslim",
                            107:"Plymouth Brethren"

    }


    content["School_type"] = School_type_dict[content["School_type"]]
    content["school_type"] = School_type_cg_dict[content["school_type"]]
    content["setting_size"] = setting_size_dict[content["setting_size"]]
    content["region"] = region_weather_dict[content["region"]]
    content["religious_affiliation"] = religious_afflil_dict[content["religious_affiliation"]]
    # add percentage of majors to content
    MajorList = []
    for z in Majors:
        MajorList.append(AddExtraInfo(z)+": "+str(round(WebsiteJSON["results"][0]["latest.academics.program_percentage."+RemoveExtraInfo(z)] * 100,2))
                         +"%  [ Around :"+str(round(content["Student_enrollment"] * WebsiteJSON["results"][0]["latest.academics.program_percentage."+RemoveExtraInfo(z)]))
                         +" Students ] "
                         )
    content["major_list"] = MajorList

    return render(request,'MainApp/SpecificUni.html',content)

@sensitive_variables()
def UniReport(request,UniName):
    # ApiKey = 'NOPE'
    URL = 'https://api.data.gov/ed/collegescorecard/v1/schools?'
    UniName = UniName.replace(" ","%20")
    Fields = "&_fields=school.name,id,school.state,school.ownership"

    WebSiteResponse = requests.get(URL+'school.name='+UniName+Fields+"&api_key="+ApiKey)
    WebsiteJSON = json.loads(WebSiteResponse.text)


    content = { "UniName":UniName,"UniList" :[] }

    for i in WebsiteJSON["results"]:
        content["UniList"].append({"schoolname":i["school.name"],"ID":i["id"],"state":i["school.state"],"ownership":i["school.ownership"]})

    if len(content["UniList"]) == 0:
        # Error --> No result page need to be built
        return HttpResponse("<h1>NO RESULTS</h1>")
    else:
        return render(request,'MainApp/UniReport.html',content)

def HomePage(request):
    if request.method == 'POST':
        RedirectBar = RedirectToUni(request.POST)
        if RedirectBar.is_valid():
            UniName = RedirectBar.cleaned_data['UniName']
            # Show User result(zero or more) before redirect and let them choose ==> Or redirect to result page then take to uni
            return redirect("result/"+UniName)
    else:
        RedirectBar = RedirectToUni()
    content = {
        "RedirectBar": RedirectBar,
    }
    return render(request,'MainApp/Homepage.html',content)
