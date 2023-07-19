# project: p2
# submitter: kenigsztein
# partner: none
# hours: 15 


import zipfile 
import csv
import io
class ZippedCSVReader:
    
    def __init__(self, zipfile_path):
        self.z = zipfile.ZipFile(zipfile_path)
        self.paths = []
        for file in self.z.filelist:
            self.paths.append(file.filename)
            
    def rows(self, csv_path = None):
        if csv_path != None:
            with self.z.open(csv_path) as csv_file:
                for row in csv.DictReader(io.TextIOWrapper(csv_file)):
                    yield row
        else: 
            for p in self.paths: 
                with self.z.open(p) as csv_file:
                    for row in csv.DictReader(io.TextIOWrapper(csv_file)):
                        yield row
            
tree_reader = ZippedCSVReader("trees.zip")
data_reader = ZippedCSVReader("mini.zip")

class Loan:
    def __init__(self, amount, purpose, race, sex, income, decision):
        self.amount = amount
        self.purpose = purpose
        self.race = race
        self.sex = sex
        self.income = income
        self.decision = decision 
        self.attributes = ['amount', 'purpose', 'race', 'sex', 'income', 'decision']
        self.attr_values = [self.amount, self.purpose, self.race, self.sex, self.income, self.decision]
        
    def __repr__(self):
        return f'Loan({repr(self.amount)}, {repr(self.purpose)}, {repr(self.race)}, {repr(self.sex)}, {repr(self.income)}, {repr(self.decision)})'

    def __getitem__(self, lookup):
        
        if hasattr(self,lookup):
            return getattr(self,lookup)
        else: 
            return int(lookup in self.attr_values)

class Bank:
    
    def __init__(self, name, reader):
        self.name = name
        self.reader = reader
        self.dicts = []
        dict_generator = data_reader.rows()
        
    
        
        for dic in dict_generator:
            action_taken = ""
            if int(dic["action_taken"]) == 1:
                action_taken = "approve"
            else: 
                action_taken = "deny"
                    
            amount = ""
            if dic["loan_amount_000s"] == None:
                amount = 0
                
            if dic['loan_amount_000s'] == "":
                dic['loan_amount_000s'] = 0
            
            elif dic["applicant_income_000s"] == "":
                dic["applicant_income_000s"] = 0
            loan = Loan(int(dic["loan_amount_000s"]), dic["loan_purpose_name"], dic["applicant_race_name_1"], dic["applicant_sex_name"], int(dic["applicant_income_000s"]), action_taken)
            
           
            if name == dic["agency_abbr"] or name == None:
    
                self.dicts.append(loan)
            
        
    def loans(self):
        return self.dicts
       
def get_bank_names(reader):
    bank_names = reader.rows()
    bank_list = []
    for dic in bank_names:
        if dic["agency_abbr"] in bank_list:
            continue
        else:
            bank_list.append(dic["agency_abbr"])
    return sorted(bank_list)
            




class SimplePredictor:
    def __init__(self):
        self.approve = 0
        self.denied = 0

    def predict(self, loan):
        if loan["purpose"] == 'Refinancing':
            self.approve += 1 
            return True 
        else:
            self.denied += 1
            return False 
   

    def get_approved(self):
        return self.approve

    def get_denied(self):
        return self.denied

    
# class Node(self, field, threshold, left, right):
#     def __init__(self, field, threshold, left, right):
#         self.field = field
#         self.threshold = threshold
#         self.left = left
#         self.right = right
#         # TODO: call parent constructor
#         # TODO: create attributes with same names/values as the parameters

#     def dump(self, indent=0):
#         if self.field == "class":
#             line = "class=" + str(self.threshold)
#         else:
#             line = self.field + " <= " + str(self.threshold)
#         print("  "*indent+line)
#         if ????:
#             self.left.dump(indent+1)
# 	if self.right != None:
#             ????

    