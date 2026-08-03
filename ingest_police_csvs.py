import os
import urllib.parse
import socket
import urllib.request
from pathlib import Path
import pandas as pd
import pyodbc
from sqlalchemy import create_engine

# root directory
MASTER_FOLDER = r"C:\Users\anaku\Documents\derbyshire_police_data"


AZURE_SQL_SERVER = os.getenv("AZURE_SQL_SERVER", "police-sql-server.database.windows.net")
AZURE_SQL_DATABASE = os.getenv("AZURE_SQL_DATABASE", "police_data_db")
AZURE_SQL_USERNAME = os.getenv("AZURE_SQL_USERNAME", "rectangle")        
AZURE_SQL_PASSWORD = os.getenv("AZURE_SQL_PASSWORD", "gkW$;)*w$DJ69J-")
AZURE_SQL_TIMEOUT = int(os.getenv("AZURE_SQL_TIMEOUT", "30"))
AZURE_SQL_CONNECTION_STRING = os.getenv(
    "AZURE_SQL_CONNECTION_STRING",
    (
        "Driver={ODBC Driver 18 for SQL Server};"
        f"Server=tcp:{AZURE_SQL_SERVER},1433;"
        f"Database={AZURE_SQL_DATABASE};"
        f"Uid={AZURE_SQL_USERNAME};"
        f"Pwd={{{AZURE_SQL_PASSWORD}}};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        f"Connection Timeout={AZURE_SQL_TIMEOUT};"
    ),
)

# wrapped the logic in a function for reuse & testing
def load_police_data(master_folder):
    all_dfs = []

    # loop through each subfolder
    for folder_name in os.listdir(master_folder):
        folder_path = os.path.join(master_folder, folder_name) # build the full path. combines master folder path with subfolder name

        # skip anything that isn't a folder
        if not os.path.isdir(folder_path):
            continue

        # look for CSV files inside the folder
        for file_name in os.listdir(folder_path):
            if file_name.lower().endswith(".csv"):
                file_path = os.path.join(folder_path, file_name)
                print(f"\nLoading: {file_path}")

                try:
                    df = pd.read_csv(file_path)
                    df["source_month"] = folder_name  # added metadata
                    all_dfs.append(df)
                except Exception as e:
                    print(f"\nFailed to load {file_path}: {e}")

    # combine all CSVs into one DataFrame
    if all_dfs:
        combined_df = pd.concat(all_dfs, ignore_index=True)
        return combined_df
    else:
        print("\nNo CSV files found.")
        return pd.DataFrame()

print("\nDrivers:", pyodbc.drivers())


def build_connection_string():
    return AZURE_SQL_CONNECTION_STRING


# load pandas df into azure sql database table
def load_to_azure_sql(df):
    if df.empty:
        print("\nNo data to load into Azure SQL.")
        return

    connection_string = build_connection_string()
    print("\nConnecting to Azure SQL with the configured ODBC settings...")
    print(f"Using server: {AZURE_SQL_SERVER}")
    print(f"Using database: {AZURE_SQL_DATABASE}")
    print(f"Using username: {AZURE_SQL_USERNAME}")

    try:
        with urllib.request.urlopen("https://api.ipify.org", timeout=10) as response:
            client_ip = response.read().decode().strip()
    except Exception:
        try:
            client_ip = socket.gethostbyname(socket.gethostname())
        except Exception:
            client_ip = "unknown"



    try:
        print(repr(connection_string))
        conn = pyodbc.connect(connection_string)
        conn.close()
        print("\nODBC connection test succeeded.")
    except Exception as e:
        print(f"\nODBC connection test failed: {e}")
        raise

    encoded_connection_string = urllib.parse.quote_plus(connection_string)
    engine = create_engine(
        f"mssql+pyodbc:///?odbc_connect={encoded_connection_string}",
        fast_executemany=True,
    )

    # write df to Azure SQL
    try:
        df.to_sql(
            name="police_data_raw",
            con=engine,
            if_exists="replace",
            index=False,
        )
        print("\nData successfully loaded into Azure SQL")
    except Exception as e:
        print(f"\nError loading data into Azure SQL: {e}")


def main():
    df = load_police_data(MASTER_FOLDER)
    print(df.head())
    print(f"\nTotal rows loaded: {len(df)}")
    load_to_azure_sql(df)

if __name__ == "__main__":
    main()