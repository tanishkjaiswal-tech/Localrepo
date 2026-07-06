from pydantic import BaseModel, EmailStr , Field
from typing import List, Dict, Optional , Annotated

class Patient(BaseModel):
    name: Annotated[str, Field(max_lenght=50 , title = 'Name of the patient' , description= 'Give the name of the patient in less than 50 chars',examples=['Nitish','Amit'])]
    email: EmailStr
    age: int = Field(gt = 0, lt = 120)
    weight: Annotated[float,Field(gt=0,strict= True)]
    married: bool = False
    allergies:Optional[List[str]]  = Field(max_lenght=5)
    contact_details: Dict[str, str]


@field_validator('email')
@classmethod
def validate_email(cls, value):
    valid_domains = ['gmail.com', 'yahoo.com', 'outlook.com']
    domain = value.split('@')[-1]
    if domain not in valid_domains:
        raise ValueError(f'Invalid email domain: {domain}. Allowed domains are: {valid_domains}')

        return value
    

@field_validator('name')
@classmethod
def validate_name(cls, value):
    if not value.isalpha():
        raise ValueError('Name must contain only alphabetic characters')
    return value

@field_validator('age', mode = 'After')
@classmethod
def validate_age(cls, value):
    if value < 0 or value > 120:
        raise ValueError('Age must be between 0 and 120')
    return value


@field_validator(mode = 'After')
def validate_emergency_contact(cls, model):
    if model.age > 60 and 'emergency' not in model.contact_details:
        raise ValueError('Emergency contact is required')
    return model


@computed_field
@property
def bmi(self) -> float:
    return self.weight / ((self.height / 100) ** 2)  # Assuming height is in centimeters


def insert_patient(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.email)
    print(patient.bmi)
    print('Inserted')


patient_info = {'name' : 'nitish' ,'email': 'absd@gmail.com', 'age' : '30' ,'weight':75.2,'married':True,'allergies':['pollen','dust'],'contact_details':{ 'phone' : '34567788'}}

patient1 = Patient(**patient_info)
insert_patient(patient1)

 
