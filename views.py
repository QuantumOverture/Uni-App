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
    # ApiKey = 'PLEASE GO TO API.DATA.GOV for a key or search for it on Google or your favorite search engine'
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
        "Student_enrollment": WebsiteJSON["results"][0]["latest.student.enrollment.all"],
        "10_years_avg_earnings":WebsiteJSON["results"][0]["latest.earnings.10_yrs_after_entry.working_not_enrolled.mean_earnings"],
        "Number_of_grad_students": WebsiteJSON["results"][0]["latest.student.grad_students"],
        "Number_of_in_debt_students":WebsiteJSON["results"][0]["latest.aid.cumulative_debt.number"],
        "School_type": WebsiteJSON["results"][0]["school.ownership"],
        "Principle_Loan": WebsiteJSON["results"][0]["latest.aid.loan_principal"],
        "6_years_avg_earnings": WebsiteJSON["results"][0]["latest.earnings.6_yrs_after_entry.working_not_enrolled.mean_earnings"],
        "admission_rate":WebsiteJSON["results"][0]["latest.admissions.admission_rate.overall"],
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
        "percent_men": WebsiteJSON["results"][0]["latest.student.demographics.men"],
        "percent_women": WebsiteJSON["results"][0]["latest.student.demographics.women"],
        "first_gen": WebsiteJSON["results"][0]["latest.student.demographics.first_generation"],
        "four_year_completion":WebsiteJSON["results"][0]["latest.completion.completion_rate_4yr_100nt"],
        "religious_affiliation":WebsiteJSON["results"][0]["school.religious_affiliation"],
        "race_white":WebsiteJSON["results"][0]["latest.student.demographics.race_ethnicity.white"],
        "race_black": WebsiteJSON["results"][0]["latest.student.demographics.race_ethnicity.black"],
        "race_asian": WebsiteJSON["results"][0]["latest.student.demographics.race_ethnicity.asian"],
        "race_aian": WebsiteJSON["results"][0]["latest.student.demographics.race_ethnicity.aian"],
        "race_nhpi": WebsiteJSON["results"][0]["latest.student.demographics.race_ethnicity.nhpi"],
        "race_hispanic": WebsiteJSON["results"][0]["latest.student.demographics.race_ethnicity.hispanic"],
    }

    # add percentage of majors to content
    for z in Majors:
        content[RemoveExtraInfo(z)] = WebsiteJSON["results"][0]["latest.academics.program_percentage."+RemoveExtraInfo(z)] * 100

    return render(request,'MainApp/SpecificUni.html',content)

@sensitive_variables()
def UniReport(request,UniName):
    # ApiKey = 'PLEASE GO TO API.DATA.GOV for a key or search for it on Google or your favorite search engine'
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
