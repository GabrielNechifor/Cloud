from google.cloud import bigquery
from datetime import datetime


def insert_row(user, name, description, input_type, output_type, input_language, output_language):
    client = bigquery.Client()

    table_id = "cloud-test-shell.dataset_project_cloud.ResourcesInformation"

    table = client.get_table(table_id)  # Make an API request.
    rows_to_insert = [(user, name, description, input_type, output_type, input_language, output_language, datetime.today().strftime('%Y-%m-%d'))]

    errors = client.insert_rows(table, rows_to_insert)  # Make an API request.
    if errors == []:
        print("New rows have been added.")


def getListOfResources(user):    
    # Construct a BigQuery client object.
    client = bigquery.Client()

    # TODO(developer): Set table_id to the ID of the table to browse data rows.
    table_id = "cloud-test-shell.dataset_project_cloud.ResourcesInformation"
    table_with_deleted_objects_id = "cloud-test-shell.dataset_project_cloud.DeletedResources"

    # Download all rows from a table.
    rows_iter = client.list_rows(table_id)  # Make an API request.
    deleted_rows_iter = client.list_rows(table_with_deleted_objects_id)

    # Iterate over rows to make the API requests to fetch row data.
    rows = list(rows_iter)
    deleted_rows = list(deleted_rows_iter)

    resultData = []
    for row in rows:
        ok = 1
        for deleted_row in deleted_rows:
            if row[0] == deleted_row[0] and row[1] == deleted_row[1]:
                ok = 0
        if ok == 1 and row[0] == user:
            d = {}
            d['Name'] = row[1]
            d['Description'] = row[2]
            d['Type'] = row[3] + '_to_' + row[4]
            d['CreationDate'] = str(row[7]).split(" ")[0]
            resultData.append(d)

    return resultData

def deleteResource(user, name):
    # Construct a BigQuery client object.
    client = bigquery.Client()

    # TODO(developer): Set table_id to the ID of the table to browse data rows.
    table_id = "cloud-test-shell.dataset_project_cloud.DeletedResources"

    table = client.get_table(table_id)  # Make an API request.
    rows_to_insert = [(user, name)]
    
    errors = client.insert_rows(table, rows_to_insert)  # Make an API request.
    if errors == []:
        print("New rows have been added.")
        return True
    else:
        return False


def getAResource(user, name):    
    # Construct a BigQuery client object.
    client = bigquery.Client()

    # TODO(developer): Set table_id to the ID of the table to browse data rows.
    table_id = "cloud-test-shell.dataset_project_cloud.ResourcesInformation"

    # Download all rows from a table.
    rows_iter = client.list_rows(table_id)  # Make an API request.

    # Iterate over rows to make the API requests to fetch row data.
    rows = list(rows_iter)

    resultData = []
    for row in rows:
        if row[0] == user and row[1] == name:
            d = []
            d.append(row[2])
            d.append(row[3])
            d.append(row[4])
            d.append(row[5])
            d.append(row[6])
            resultData = d

    return resultData

