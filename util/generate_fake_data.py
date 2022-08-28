from faker import Faker
from faker.providers import BaseProvider
import random
import csv
import pandas as pd
from pathlib import Path

def name_to_email(name):
    name = str(name)
    email_part = name.replace(" ", ".")
    email = f'{email_part}@test.com'
    return email

def generate_fakes():

    file_dir = Path(__file__).parent.resolve()
    file_name = 'testing_responses.csv'
    input_file = str(file_dir / Path('testing_responses.csv'))
    df = pd.read_csv(input_file)

    df['Email'] = df['Name'].apply(name_to_email)


    # fake = Faker()

    # fake_phones = []
    # for n in range(1, 12688):
    #     fake_phones.append(fake.phone_number())

    # df = pd.DataFrame({'Phone': fake_phones})

    output_file = str(file_dir / Path('testing_responses_output.csv'))
    df.to_csv(output_file, index=False)

if __name__ == '__main__':
    # fake_email = name_to_email('Andy Baumgartner')
    # print(fake_email)

    generate_fakes()