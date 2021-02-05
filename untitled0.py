# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 08:58:51 2021

@author: tmusetessier
"""

"""
Collect BLS data from DOMO, include forecasting for employment growth by sector by MSA and re-upload
"""
import domo_api as domo



import pandas as pd
import numpy as np
import psycopg2
from io import StringIO
import os


class _Connection(object):
    """Connect to the database and upload data"""

    def __init__(self):
        username = "postgres@fcp-postgres-prod"
        pw = "2Dnq1DaV1yIT"
        server = "fcp-postgres-prod.postgres.database.azure.com"
        db = "fcp_dw"
        self.connectionString = username + ":" + pw + "@" + server + "/" + db
        self.connection = psycopg2.connect(
            user=username, password=pw, host=server, dbname=db
        )
        self.cursor = self.connection.cursor()



    def copy_from_stringio(self, df, table):
        conn=self.connection
        buffer = StringIO()
        df.to_csv(buffer,index=False, header=False)
        buffer.seek(0)
        
        cursor = conn.cursor()
        try:
            cursor.copy_from(buffer, table, sep=",",null='')
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            os.remove(tmp_df)
            print("Error: %s" % error)
            conn.rollback()
            cursor.close()
            return 1
        print("copy_from_stringio() done")
        cursor.close()


    def upload(self,data):
        data.to_csv('testing.csv')
        self.copy_from_stringio(data,'"ExternalData".office_forecasting')


    def costar_export(self):
        cur = self.connection.cursor()
        cur.execute(
            """
            select period,slice,geography_name,cbsa_code,geography_code,office_employment,population,total_employment_
            from "ExternalData".costar_office
            """)
        data=cur.fetchall()        
        costar=pd.DataFrame(data,columns=['Period','Slice','Geography Name','CBSA Code','Geography Code','Office Employment','Population','Total Employment'])
        return costar


def dw_upload(data):
    connect=_Connection()
    connect.upload(data)



# Assigning quarters to date
def find_period(date):
    period = " Q" + str(int((date.month + 2) / 3))
    return str(date.year) + period


# Connect to DOMO
# Download existing BLS data table into Dataframe
def domo_download():
    return domo.export_dataset("EMPLMNT_BY_SECTOR_BY_MSA")


def prepare_domo_data(employment_by_sector):
    employment_by_sector["area_code"] = pd.to_numeric(employment_by_sector["area_code"])
    cbsa_codes = employment_by_sector[["area_code", "area_def"]].drop_duplicates()
    cbsa_codes = cbsa_codes.dropna(how="any")
    cbsa_codes.append([np.nan, "US Total"])
    employment_by_sector = employment_by_sector.merge(
        how="left", right=cbsa_codes, on="area_def"
    )
    print(employment_by_sector.columns)
    employment_by_sector.drop(axis=1, columns="area_code_x")
    employment_by_sector.rename(columns={"area_code_y": "CBSA Code"}, inplace=True)
    employment_by_sector["date"] = pd.to_datetime(employment_by_sector["date"])
    employment_by_sector["Period"] = employment_by_sector["date"].apply(find_period)
    return employment_by_sector
    


# Download Forecasting data / Ingest saved/scrubbed copy of Forecasting Data into Dataframe
def prepare_bls_forecasting():
    conn=_Connection()
    costar=conn.costar_export()
    costar['CBSA Code']=pd.to_numeric(costar['CBSA Code'])
    costar["Office % by Pop"] = costar["Office Employment"] / costar["Population"]
    costar["Office % by Employed"] = (
        costar["Office Employment"] / costar["Total Employment"]
    )
    costar.to_csv("check.csv")
    return costar


# Clean and merge the datasets
def combine_datasets(by_sector, costar):
    combined = by_sector.merge(how="right", right=costar, on=["CBSA Code", "Period"])
    return combined


# Upload resulting table into existing DOMO dataset
def domo_upload(final):
    domo.update_dataset("BLS Statistics and Forecasts", dataset_df=final)
    return None


def main():
    employment_by_sector = domo_download()
    employment_by_sector_cleaned = prepare_domo_data(employment_by_sector)
    costar = prepare_bls_forecasting()
    combined = combine_datasets(employment_by_sector_cleaned, costar)
    domo_upload(combined)
    dw_upload(combined)


if __name__ == "__main__":
    main()
