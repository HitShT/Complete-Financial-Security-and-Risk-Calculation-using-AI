class Grading:
    """
    docstring for Grading.
    Class to grade several different arrays of data based on VIT's formula
    This allows me to grade a random set of number fairly and research is done by VIT
    """
    def __init__(self,data):
        self.data = data
        self.relativeGrading()
        self.grade()
        # print(self.data)
        # print(self.grading)
        # print(self.marks)
    def std_dev(self):
        #returns std_dev
        # pip install numpy
        from numpy import std
        if not self.data:
            return 0
        return std(self.data)
    def mean(self):
        #returns mean
        try:
            return sum(self.data)/len(self.data)
        except:
            return 0
    def relativeGrading(self):
        '''
            Grading is done based on the following
            mean + 1.5 sigma = S
            mean + 1 sigma = A
            mean + 0.5 sigma = B
            mean  = C
            mean - 0.5 sigma = D
            mean - 1 sigma = E
            mean - 1.5 sigma = F
        '''
        self.mn,self.std = self.mean(),self.std_dev()
        self.grading = [self.mn]*7
        for i in range(7):
            self.grading[i] = round(self.grading[i] + (1.5-i*0.5)*self.std,2)
    def give_grade(self,i):
        #Returns marks based on the grade defined in relativeGrading
        return [10,9,8,7,6,5,4,3][i]
    def grade(self):
        '''
            Grading the marks
            Length of array = 7, so linear search is good enough
        '''
        self.marks = [3]*len(self.data)

        for i in range(len(self.data)):
            for j in range(7):
                if(self.data[i] > self.grading[j]):
                    self.marks[i] = self.give_grade(j)
                    break


class GradeColumns:
    '''
    docstring for GradeColumns
    There are functions for each column of the dataset to grade and return a numeric value
    The methodology behind the grading of a column depends upon the type of the data in column
    If there are range of numeric values, we are using the VIT Grading Policy
    This kind of columns have a special set... method which takes in the entire array of input
    This input is processed according to the grading methodology
    and the result from grade.... is returned in the form of a list containing marks between 3 and 10, 3 being the lowest 10 being the highest
    Rest columns are graded based on the type of input, these columns usually have a fixed number of classes and can easily be graded
    '''
    def setPremiumData(self,data):
        self.premiumData = Grading(data)
    def gradePremiumData(self):
        '''
        13-i because for premium its the opposite, lower the premium better the choice
        and grading is between 3 and 10, so as to maintain parity with other
        grading functions, grade is subtracted from 13, so updated range remains 3 to 10
        '''
        return [13-i for i in self.premiumData.marks]
    def setExclusion(self,data):
        self.exclusionData = Grading(data)
    def gradeExclusion(self):
        return self.exclusionData.marks
    def gradeSublimits(self,data):
        data = data.lower()
        if(data == "no" or "single" in data or data == "na"):
            return 10
        elif("si" in data):
            return 3
    def setNoClaim(self,data):
        self.noClaimData = Grading(data)
    def gradeNoClaim(self):
        return self.noClaimData.marks
    def gradeRestoration(self,data):
        if(data == "YES"):
            return 10
        if(data == "YNO"):
            return 5
        return 3
    def gradeCopay(self,data):
        data = data.lower()
        if("n" in data):
            return 10
        return 0
    def setClaimsSettle(self,data):
        self.ClaimsSettle = Grading(data)
    def gradeClaimsSettle(self):
        return self.ClaimsSettle.marks

class Testing:
    def __init__(self):
        '''
            To test the Grading class.
            Didn't use unittest class as the range of possible input is very limited
            and using selected datasets are enough
        '''
        grade = GradeColumns()
        self.premium = [6325,10535,13595,8370]
        grade.setPremiumData(self.premium)
        print(grade.gradePremiumData())
        self.exclusion = [4,4,2,3]
        grade.setExclusion(self.exclusion)
        print(grade.gradeExclusion())
        self.sublimits = ["no","SINGLE PRIVATE ROOM","na","no"]
        for i in self.sublimits:
            print(grade.gradeSublimits(i),end = " ")
        print()
        self.noClaimBonus = [100,100,50,100]
        grade.setNoClaim(self.noClaimBonus)
        print(grade.gradeNoClaim())
        self.restoration = ["YES"]*4
        for i in self.restoration:
            print(grade.gradeRestoration(i),end = " ")
        print()
        self.copay = ["NA","NA","NO","NA"]
        for i in self.copay:
            print(grade.gradeCopay(i),end = " ")
        print()
        self.claimsSettled = [89,87,88,92]
        grade.setClaimsSettle(self.claimsSettled)
        print(grade.gradeClaimsSettle())
# test = Testing()
