from fastapi import FastAPI, HTTPException

from zipcode_db import ZipCodeDB
from zipcode_dto import ZipCodeDTO


class ZipCodeApp(FastAPI):

    def index(self):
        return {"app_name": "Zip Code App"}

    def hc(self):
        return {"status": "OK"}

    def get_zip_code(self, zipcode=None):
        if(zipcode is None or len(zipcode) != 8):
            message = 'Zip Code must contain 8 characters'
            raise HTTPException(status_code=404, detail=message)

        zip_code = self.zip_code_fromdb(zipcode)

        if zip_code:
            return zip_code
        else:
            message = f'Zip code {zipcode} does not exist.'
            raise HTTPException(status_code=404, detail=message)

    def zip_code_fromdb(self, param=''):

        db = ZipCodeDB('base/cep.db')
        zip_codes = db.select_where(f"cep = '{param}'")
        db.close()

        result = []
        for zipcode in zip_codes:
            result.append(f"{ZipCodeDTO(zipcode).to_dict()}")
        return result
