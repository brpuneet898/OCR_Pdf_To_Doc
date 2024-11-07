pip install pdfservices-sdk

import logging
import os
from datetime import datetime
from google.colab import files

from adobe.pdfservices.operation.auth.service_principal_credentials import ServicePrincipalCredentials
from adobe.pdfservices.operation.exception.exceptions import ServiceApiException, ServiceUsageException, SdkException
from adobe.pdfservices.operation.io.cloud_asset import CloudAsset
from adobe.pdfservices.operation.io.stream_asset import StreamAsset
from adobe.pdfservices.operation.pdf_services import PDFServices
from adobe.pdfservices.operation.pdf_services_media_type import PDFServicesMediaType
from adobe.pdfservices.operation.pdfjobs.jobs.export_pdf_job import ExportPDFJob
from adobe.pdfservices.operation.pdfjobs.params.export_pdf.export_pdf_params import ExportPDFParams
from adobe.pdfservices.operation.pdfjobs.params.export_pdf.export_pdf_target_format import ExportPDFTargetFormat
from adobe.pdfservices.operation.pdfjobs.result.export_pdf_result import ExportPDFResult

logging.basicConfig(level=logging.INFO)

class ExportPDFToDOCX:
    def __init__(self, pdf_file_path):
        try:
            with open(pdf_file_path, 'rb') as file:
                input_stream = file.read()
            credentials = ServicePrincipalCredentials(
                client_id="c889b3608c3b4afc8d2b27009f4b7367",
                client_secret="p8e-pGrkHYHVs3jCao9Bj0eJ4Fny4THKyJfQ"
            )
            pdf_services = PDFServices(credentials=credentials)
            input_asset = pdf_services.upload(input_stream=input_stream, mime_type=PDFServicesMediaType.PDF)
            export_pdf_params = ExportPDFParams(target_format=ExportPDFTargetFormat.DOCX)
            export_pdf_job = ExportPDFJob(input_asset=input_asset, export_pdf_params=export_pdf_params)
            location = pdf_services.submit(export_pdf_job)
            pdf_services_response = pdf_services.get_job_result(location, ExportPDFResult)
            result_asset: CloudAsset = pdf_services_response.get_result().get_asset()
            stream_asset: StreamAsset = pdf_services.get_content(result_asset)
            output_file_path = self.create_output_file_path()
            with open(output_file_path, "wb") as file:
                file.write(stream_asset.get_input_stream())

            logging.info(f'Conversion successful. DOCX file saved to {output_file_path}')

        except (ServiceApiException, ServiceUsageException, SdkException) as e:
            logging.exception(f'Exception encountered while executing operation: {e}')
    @staticmethod
    def create_output_file_path() -> str:
        now = datetime.now()
        time_stamp = now.strftime("%Y-%m-%dT")
        os.makedirs("/content/", exist_ok=True)
        return f"/content/export_{time_stamp}.docx"

if __name__ == "__main__":
    pdf_file_path = '/content/searchable.pdf'
    ExportPDFToDOCX(pdf_file_path)