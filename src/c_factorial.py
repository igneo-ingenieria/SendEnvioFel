import datetime
import logging
import check_connection
import requests
import os

from typing import Dict, List, Any, Union
from operator import contains
from clases import  Employee
from dotenv import load_dotenv

from send_email import send_email, comprobar_formato_gmail

load_dotenv(override=True)

class Factorial:

    BASE_URL = "https://api.factorialhr.com/api/2026-01-01/resources"

    def __init__(self):

        self.body_html = """<html> <body> <img src="cid:imagen1"> </body> </html>"""
        self.image_rute =  "/app/image/imagen_felicitar_cumpleanios.png"
        self.actual_date = datetime.datetime.today().strftime("%m-%d")
        self.smtp_server = os.getenv("SMTP_SERVER")
        self.sender_password = os.getenv("SENDER_PASSWORD")
        self.sender_email = os.getenv("SENDER_EMAIL")
        self.smtp_port= os.getenv("SMTP_PORT")
        self.subject_gmail = 'FELIZ ANIVERSÁRIO'
        self.token = os.getenv("FACTORIAL_API_TOKEN")
        self.page_limit = int(os.getenv("FACTORIAL_PAGE_LIMIT", "100"))
        self.logger = logging.getLogger(__name__)
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

    def get_employees(self) -> list[Employee]:
        logging.info("Procesando clase Factorial")
        all_employees = []
        cursor = None
        total_processed = 0
        page = 1
        while True:
            params = {"limit": 100, "page": page}
            page += 1
            if cursor:
                params["cursor"] = cursor
            payload = self._make_request("GET", "/employees/employees", params=params)#make_request retorna false si hay error en ejecucion
            if payload is not False:
                employees = payload.get("data", [])
                all_employees.extend([Employee.from_dict(employee) for employee in employees])
                meta = payload.get("meta", {})

                total_processed += len(employees)
                has_next_page = bool(meta.get("has_next_page", False))
                cursor = meta.get("end_cursor")

                logging.info(
                    "Pagina procesada: registros=%s, total_procesado=%s, has_next_page=%s pagina=%s",
                    len(employees),
                    total_processed,
                    has_next_page,
                    page
                )

                if not has_next_page:
                    break

        logging.info("Carga finalizada. Total de empleados procesados: %s", total_processed)

        if len(employees) > 0:
            return all_employees
        else:
            logging.error("No existen empleados o ha fallado la conexion con la API")
            return []


    def proceso_cumpleaños(self):
        # Comprobacion de conexion a internet
        load_dotenv(override=True)

        if check_connection.conexion() is True:
            logging.info("Conexion establecida")
            logging.info("Procesando clase Factorial")
            employees = self.get_employees() # Lista con todos los empleados de la API
        else:
            logging.error("Conexion fallida")
            return False

        if len(employees) > 0: # Si la lista no esta vacia
            logging.info("Numero de empleados obtenidos: %s", len(employees))
            for employee in employees:
                if employee.birthday_on is not None and employee.is_terminating == False:
                    mes_dia = "-".join([employee.birthday_on.split('-')[1], employee.birthday_on.split('-')[2]])
                    if (self.actual_date == mes_dia) and contains(employee.login_email, 'nipdobrasil.com.br') and not employee.is_terminating:
                        recipient_email = employee.login_email
                        subject = self.subject_gmail
                        smtp_port = self.smtp_port  # TLS port
                        if comprobar_formato_gmail(recipient_email):
                            if send_email(self.sender_email,self.sender_password,recipient_email,subject,
                            self.smtp_server,self.body_html,self.image_rute,smtp_port):
                                logging.info(f"Email enviado correctamente a {employee.full_name} al correo {employee.login_email}")
                            else:
                                return False
                        else:
                            logging.error(f'El Email del usuario {employee.full_name} tiene un formato incrorrecto {employee.login_email}')
                            continue
        return True
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Union[Dict, List, Any]:
        """
        Realiza uma requisição para a API com retentativas.

        Args:
            method (str): Método HTTP (GET, POST, PUT, DELETE)
            endpoint (str): Endpoint da API (sem a URL base)
            **kwargs: Argumentos adicionais para a requisição

        Returns:
            Union[Dict, List, Any]: Resposta da API em formato JSON

        Raises:
            FactorialException: Se a requisição falhar.
        """
        url = f"{self.BASE_URL}/{endpoint.lstrip('/')}"
        self.logger.debug(f"Fazendo requisição {method} para {url}", extra=kwargs)

        try:
            response = self.session.request(method, url, **kwargs)
            # Lança HTTPError para respostas 4xx/5xx
            #response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error("Erro na requisição para a API FactorialHR", exc_info=True)
            self.logger.error(f"Erro ao comunicar com a API FactorialHR: {e}")
            return False



