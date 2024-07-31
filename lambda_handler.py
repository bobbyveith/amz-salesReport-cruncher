import json
from requests_toolbelt.multipart import decoder
import base64
from main import main


def lambda_handler(event, context):
    # Decode the multipart/form-data
    content_type = event['headers']['content-type']
    body = base64.b64decode(event["body"])
    multipart_data = decoder.MultipartDecoder(body, content_type)

    csv_file = None
    txt_file = None

    for part in multipart_data.parts:
        if part.headers[b'Content-Disposition'].decode().find('csvFile') != -1:
            csv_file = part.content
        elif part.headers[b'Content-Disposition'].decode().find('txtFile') != -1:
            txt_file = part.content

    if not csv_file or not txt_file:
        return {
            'statusCode': 400,
            'body': json.dumps('Both csvFile and txtFile must be provided')
        }

    # Process the CSV and TXT data
    # Here is where you would pass the data to your processing module
    xlsx_data = main(csv_file, txt_file)

    # Return the XLSX file as a response
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'Content-Disposition': 'attachment; filename="result.xlsx"'
        },
        'body': base64.b64encode(xlsx_data).decode('utf-8'),
        'isBase64Encoded': True
    }
