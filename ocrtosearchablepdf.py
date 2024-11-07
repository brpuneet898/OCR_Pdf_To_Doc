pip install pdfservices-sdk

# OCR to Searchable

import os
import logging
from datetime import datetime

from adobe.pdfservices.operation.auth.service_principal_credentials import ServicePrincipalCredentials
from adobe.pdfservices.operation.exception.exceptions import ServiceApiException, ServiceUsageException, SdkException
from adobe.pdfservices.operation.io.cloud_asset import CloudAsset
from adobe.pdfservices.operation.io.stream_asset import StreamAsset
from adobe.pdfservices.operation.pdf_services import PDFServices
from adobe.pdfservices.operation.pdf_services_media_type import PDFServicesMediaType
from adobe.pdfservices.operation.pdfjobs.jobs.ocr_pdf_job import OCRPDFJob
from adobe.pdfservices.operation.pdfjobs.result.ocr_pdf_result import OCRPDFResult

logging.basicConfig(level=logging.INFO)

def ocr_to_searchable_pdf(pdf_file_path, output_dir):
    try:
        with open(pdf_file_path, 'rb') as file:
            input_stream = file.read()
        credentials = ServicePrincipalCredentials(
            client_id="c889b3608c3b4afc8d2b27009f4b7367",
            client_secret="p8e-pGrkHYHVs3jCao9Bj0eJ4Fny4THKyJfQ"
        )
        pdf_services = PDFServices(credentials=credentials)
        input_asset = pdf_services.upload(input_stream=input_stream,
                                          mime_type=PDFServicesMediaType.PDF)
        ocr_pdf_job = OCRPDFJob(input_asset=input_asset)
        location = pdf_services.submit(ocr_pdf_job)
        pdf_services_response = pdf_services.get_job_result(location, OCRPDFResult)
        result_asset: CloudAsset = pdf_services_response.get_result().get_asset()
        stream_asset: StreamAsset = pdf_services.get_content(result_asset)
        output_file_path = os.path.join(output_dir, 'searchable.pdf')
        with open(output_file_path, "wb") as file:
            file.write(stream_asset.get_input_stream())

        logging.info(f'OCR and conversion to searchable PDF successful. '
                     f'Searchable PDF file saved at: {output_file_path}')

    except (ServiceApiException, ServiceUsageException, SdkException) as e:
        logging.exception(f'Exception encountered while executing OCR operation: {e}')

pdf_file_path = '/content/L&T Purchase Order.pdf'
output_dir = '/content/'

if __name__ == "__main__":
    ocr_to_searchable_pdf(pdf_file_path, output_dir)