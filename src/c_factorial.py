import logging
import requests

class Factorial:
    def hello(self):
        logging.info("Procesando clase Factorial")
        url = "https://api.factorialhr.com/api/2026-01-01/resources/employees/employees"

        headers = {
        "accept": "application/json",
        "authorization": "Bearer ckQA56t7MKm_JBJBAPel29U9QdFV94syEr_5MicfZkE"
        }

        response = requests.get(url, headers=headers)

        logging.info(response.text)
        employees = response.json().get("data", [])
        for employee in employees:
            logging.info(employee.get("full_name"))
            logging.info(employee.get("email"))


        ##employees_data = response.get("data", [])


