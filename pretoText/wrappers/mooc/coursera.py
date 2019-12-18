from bs4 import BeautifulSoup
from random import randint
from redtoolkit.utils import parallelism
import json
import requests
import pandas as pd
import re
import time


__all__ = ["dump_from_search", "dump_all"]


def dump_all(save_csv=None):
    return dump_from_search("", save_csv=save_csv)


def dump_from_search(search_text, save_csv=None):

    courses = _courses_from_search_api(search_text)
    results = parallelism.perform_job(
        list(courses), _iteration_task, level=parallelism.HARD
    )
    df = pd.concat(results, sort=True).drop_duplicates().reset_index(drop=True)

    if save_csv:
        df.to_csv(save_csv)
    else:
        df.to_csv(search_text.replace(" ", "_") + ".csv")

    return df


def _iteration_task(course):
    courses = []

    course_slug = course["slug"]
    course.update(_course_from_slug_api(course_slug))

    if "language" not in course or course["language"] != "en":
        return

    course.update(_scrape_from_course_page(course_slug))
    courses.append(course)

    if "specialization" in course:
        spec_link = course["specialization_link"]
        spec = _spec_from_slug_api(spec_link.split("/")[-1])
        courses.append(spec)

    return pd.DataFrame.from_records(courses)


"""

Working APIs

https://api.coursera.org/api/courses.v1?q=search&query=&start=3000&limit=10&fields=domainTypes&includes=partnerIds

https://www.coursera.org/api/catalogResults.v2?q=search&query=machine+learning&limit=10&debug=true&fields=debug,courseId,domainId,onDemandSpecializationId,specializationId,subdomainId,suggestions,courses.v1(name,description,slug,photoUrl,courseStatus,partnerIds),onDemandSpecializations.v1(name,description,slug,logo,courseIds,launchedAt,partnerIds),specializations.v1(name,description,shortName,logo,primaryCourseIds,display,partnerIds),partners.v1(name)&includes=courseId,domainId,onDemandSpecializationId,specializationId,subdomainId,suggestions,courses.v1(partnerIds),onDemandSpecializations.v1(partnerIds),specializations.v1(partnerIds)

https://www.coursera.org/api/onDemandSpecializations.v1?fields=domainTypes,subtitleLanguages,capstone,courseIds,description,interchangeableCourseIds,metadata,tagline,partners.v1(description,name,squareLogo),courses.v1(courseProgress,courseType,description,instructorIds,membershipIds,name,startDate,subtitleLanguages,v1Details,vcMembershipIds,workload),v1Details.v1(courseSyllabus),memberships.v1(grade,vcMembershipId),vcMemberships.v1(certificateCodeWithGrade)&includes=courseIds,instructorIds,partnerIds,instructors.v1(partnerIds),courses.v1(courseSyllabus,courseProgress,instructorIds,membershipIds,subtitleLanguages,v1Details,vcMembershipIds)&q=slug&slug=foundational-finance

https://www.coursera.org/api/onDemandCourses.v1?q=slug&slug=data-analysis-with-python&fields=debug,brandingImage%2CcertificatePurchaseEnabledAt%2Cpartners.v1(squareLogo%2CrectangularLogo)%2Cinstructors.v1(fullName)%2CoverridePartnerLogos%2CsessionsEnabledAt%2CdomainTypes%2CpremiumExperienceVariant%2CisRestrictedMembership&includes=partnerIds,sessionIds

https://api.coursera.org/api/onDemandCourses.v1?q=slug&slug=data-analysis-with-python&fields=courseDetails,domainTypes

"""


def _courses_from_search_api(search_text):

    API_URL = "https://api.coursera.org/api/courses.v1"
    API_QUERY_PART = "?q=search&query="
    API_PAGE_START = "&start="
    API_PAGE_SIZE = "&limit="
    API_PAGE_DETAILS = "&fields=description"

    req_url = API_URL + API_QUERY_PART + search_text
    req = requests.get(req_url + API_PAGE_SIZE + "1")
    req.raise_for_status()

    total = req.json()["paging"]["total"]
    has_next = True
    next_start = 0

    while has_next:

        req = requests.get(
            req_url + API_PAGE_START + str(next_start) + API_PAGE_SIZE + "1000"
        )
        req_json = req.json()

        for item in req.json()["elements"]:
            yield {"slug": item["slug"], "title": item["name"]}

        paging = req.json()["paging"]
        has_next = "next" in paging
        if has_next:
            next_start = paging["next"]


def _course_from_slug_api(course_slug):
    API_URL = "https://www.coursera.org/api/onDemandCourses.v1"
    API_QUERY_PART = "?q=slug&slug="
    API_PAGE_DETAILS = "&fields=level,domainTypes"
    API_PAGE_INCLUDES = "&includes=partnerIds"

    req_url = (
        API_URL + API_QUERY_PART + course_slug + API_PAGE_DETAILS + API_PAGE_INCLUDES
    )
    req = requests.get(req_url)
    req.raise_for_status()

    req_json = req.json()
    elements = req_json["elements"]
    if not elements:
        return {}

    item = elements[0]
    partners = req_json["linked"]["partners.v1"]

    course = {
        "description": "none" if "description" not in item else item["description"],
        "level": "mixed" if "level" not in item else item["level"],
        "language": item["primaryLanguageCodes"][0],
        "partner": "none" if not partners else partners[0]["name"],
        "estimatedWorkload": "none"
        if "estimatedWorkload" not in item
        else item["estimatedWorkload"],
    }

    if "domainTypes" not in item:
        cats = []
        for domainType in item["domainTypes"]:
            cats.append(domainType["domainId"] + "/" + domainType["subdomainId"])
        course["categories"] = "\n".join(cats)

    return course


def _scrape_from_course_page(course_slug):

    BASE_URL = "https://www.coursera.org/"
    PAGE_BASE_URL = BASE_URL + "learn/"
    req = requests.get(PAGE_BASE_URL + course_slug)
    soup = BeautifulSoup(req.text, features="lxml")

    item = {"type": "course", "link": req.url}

    spec = soup.find("a", {"class": re.compile("s12nLink")})
    if spec:
        item["specialization"] = spec.span.get_text()
        item["specialization_link"] = BASE_URL + spec.get("href")

    rating = soup.find("div", {"class": re.compile("CourseRating")})
    if rating:
        item["rating"] = rating.span.get_text()

        ratings_count = rating.find("div", {"class": re.compile("P_gjs17i")})
        if ratings_count:
            item["ratings_count"] = re.sub("[^0-9]", "", ratings_count.span.get_text())

    enrollment = soup.find("span", {"class": re.compile("enrolledSmallFontViewCount")})
    if enrollment:
        item["enrollment"] = enrollment.span.get_text()

    return item


def _spec_from_slug_api(spec_slug):

    API_URL = "https://www.coursera.org/api/onDemandSpecializations.v1"
    API_QUERY_PART = "?q=slug&slug="
    API_PAGE_DETAILS = "&fields=domainTypes,capstone,courseIds,description,interchangeableCourseIds,metadata,tagline,partners.v1(description,name,squareLogo),courses.v1(courseProgress,courseType,description,instructorIds,membershipIds,name,startDate,subtitleLanguages,v1Details,vcMembershipIds,workload),v1Details.v1(courseSyllabus),memberships.v1(grade,vcMembershipId),vcMemberships.v1(certificateCodeWithGrade)&includes=courseIds,instructorIds,partnerIds,instructors.v1(partnerIds),courses.v1(courseProgress,instructorIds,membershipIds,subtitleLanguages,v1Details,vcMembershipIds)"

    req_url = API_URL + API_QUERY_PART + spec_slug + API_PAGE_DETAILS
    req = requests.get(req_url)
    req.raise_for_status()

    elements = req.json()["elements"]
    if not elements:
        return {}

    item = elements[0]
    metadata = item["metadata"]

    spec = {
        "description": item["description"],
        "level": "mixed" if "level" not in metadata else metadata["level"],
        "tagline": item["tagline"],
        "certificateDescription": metadata["certificateDescription"],
        "title": item["name"],
        "type": "specialization",
    }

    if "domainTypes" in item:
        cats = []
        for domainType in item["domainTypes"]:
            cats.append(domainType["domainId"] + "/" + domainType["subdomainId"])
        spec["categories"] = "\n".join(cats)

    tags_cleaner = re.compile(r"<co-content>|</co-content>|<text>|</text>|<text />")

    if "cmlLearningObjectives" in metadata:
        lobjs = []
        for learningObjective in metadata["cmlLearningObjectives"]:
            lobj = learningObjective["definition"]["value"]
            lobj = tags_cleaner.sub("\n", lobj)
            lobjs.append(lobj.strip())
        spec["learningObjectives"] = "\n".join(lobjs)

    if "cmlRecommendedBackground" in metadata:
        recommendedBackground = metadata["cmlRecommendedBackground"]
        rback = recommendedBackground["definition"]["value"]
        rback = tags_cleaner.sub("\n", rback)
        spec["recommendedBackground"] = rback.strip()

    return spec


def _scrape_from_spec_page(spec_link):

    req = requests.get(spec_link)
    soup = BeautifulSoup(req.text, features="lxml")

    item = {"title": spec_name, "type": "specialization"}

    description = soup.find("div", {"class": "content-inner"})
    if description:
        item["description"] = description.get_text()

    return item
