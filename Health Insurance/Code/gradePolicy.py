import os
from grading import GradeColumns
import pandas as pd #pip install pandas

# print(help(os.listdir))
# print(help(os.path))
# files = os.listdir("./Data") #Not all OS friendly
path_data = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Data'))
new_path_data = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Graded Data'))
files = os.listdir(path_data)
# print(files)


def gradeAndCreate(file_name):
    #Gets the file name, reads the file, drops the link to doc and the link to policy
    data = pd.read_csv(os.path.join(path_data,file_name))
    data = data.drop(["Link to doc","Link to policy"],axis = 1)

    #getting data
    company = list(data["Company"])
    plan = list(data["Plan"])
    premium = list(map(float,data["Premium"]))
    exclusionYears = list(map(float,data["Exclusion Years"]))
    sublimits = list(data["Sublimits"])
    noClaimBonus = list(map(float,data["No Claim Bonus"]))
    restoration = list(data["restoration"])
    copay = list(data["Co Pay"])
    claimsSettled = list(map(float,data["Claims Settled"]))
    #grading data
    grader = GradeColumns() #initialzing grader
    number_rows = len(premium)
    totalMarks = [0]*number_rows #summation of all cols

    grader.setPremiumData(premium)
    premium = grader.gradePremiumData()
    grader.setExclusion(exclusionYears)
    exclusionYears = grader.gradeExclusion()
    grader.setNoClaim(noClaimBonus)
    noClaimBonus = grader.gradeNoClaim()
    grader.setClaimsSettle(claimsSettled)
    claimsSettled = grader.gradeClaimsSettle()
    for i in range(number_rows):
        sublimits[i] = grader.gradeSublimits(sublimits[i])
        restoration[i] = grader.gradeRestoration(restoration[i])
        copay[i] = grader.gradeCopay(copay[i])
        totalMarks[i] = premium[i]+exclusionYears[i]+noClaimBonus[i]+claimsSettled[i]
        totalMarks[i] += sublimits[i] + restoration[i] + copay[i]
        #add functions to generate relative importance

    #Create a new csv in Graded Data/file name
    newName = os.path.join(new_path_data,file_name)
    resp = {
        "Company":company,
        "Plan":plan,
        "Premium":premium,
        "Exclusion Years":exclusionYears,
        "Sublimits":sublimits,
        "No Claim Bonus":noClaimBonus,
        "restoration":restoration,
        "Co Pay":copay,
        "Claims Settled":claimsSettled,
        "Total Marks":totalMarks
    }
    df = pd.DataFrame(data = resp)
    df.to_csv(newName,sep=',',index=False)

for i in files:
    gradeAndCreate(i)
