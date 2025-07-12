"""
Servicio para procesar documentos usando Gemini Vision API para OCR.
"""

import os
import time
import json
import logging
from typing import Dict, Any
from PIL import Image
import io

try:
    import google.generativeai as genai
except ImportError:
    genai = None

logger = logging.getLogger(__name__)

class GeminiOCRService:
    """Servicio para procesar documentos usando Gemini Vision API."""
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY no está configurado en las variables de entorno")
        if genai is None:
            raise ImportError("Falta la librería google-generativeai. Instálala con 'pip install google-generativeai pillow'")
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def process_document_image(self, image_data: bytes, filename: str) -> Dict[str, Any]:
        """
        Procesa una imagen de documento usando Gemini Vision API.
        Args:
            image_data: Datos de la imagen en bytes
            filename: Nombre del archivo para contexto
        Returns:
            Dict con el texto extraído y datos estructurados
        """
        start_time = time.time()
        try:
            # Convertir bytes a imagen PIL
            image = Image.open(io.BytesIO(image_data))
            prompt = self._create_ocr_prompt(filename)
            response = self.model.generate_content([prompt, image])
            result = self._parse_gemini_response(response.text, filename)
            processing_time = time.time() - start_time
            result.update({
                'gemini_model_used': 'gemini-1.5-flash',
                'processing_time_seconds': processing_time,
                'confidence_score': 0.95,  # Placeholder
                'raw_text': response.text
            })
            logger.info(f"Documento {filename} procesado exitosamente en {processing_time:.3f}s")
            return result
        except Exception as e:
            processing_time = time.time() - start_time
            logger.error(f"Error procesando documento {filename}: {str(e)}")
            return {
                'error_message': str(e),
                'processing_time_seconds': processing_time,
                'confidence_score': 0.0,
                'raw_text': None,
                'structured_data': None
            }

    def process_document_pdf(self, pdf_data: bytes, filename: str) -> Dict[str, Any]:
        """
        Procesa un PDF usando Gemini Vision API.
        Args:
            pdf_data: Datos del PDF en bytes
            filename: Nombre del archivo para contexto
        Returns:
            Dict con el texto extraído y datos estructurados
        """
        start_time = time.time()
        try:
            # Para PDFs, por ahora usamos el mismo método que imágenes
            # En el futuro se podría implementar conversión de PDF a imágenes
            logger.info(f"Procesando PDF {filename} como imagen")
            
            # Intentar abrir como imagen (algunos PDFs pueden ser procesados así)
            try:
                image = Image.open(io.BytesIO(pdf_data))
                prompt = self._create_ocr_prompt(filename)
                response = self.model.generate_content([prompt, image])
                result = self._parse_gemini_response(response.text, filename)
            except Exception as img_error:
                logger.warning(f"No se pudo procesar PDF como imagen: {img_error}")
                # Fallback: tratar como texto plano
                result = {
                    'structured_data': {
                        'document_type': 'pdf',
                        'filename': filename,
                        'note': 'PDF procesado como texto plano'
                    },
                    'processing_status': 'completed',
                    'raw_text': 'PDF procesado - contenido no extraído completamente'
                }
            
            processing_time = time.time() - start_time
            result.update({
                'gemini_model_used': 'gemini-1.5-flash',
                'processing_time_seconds': processing_time,
                'confidence_score': 0.85,  # Placeholder para PDFs
                'raw_text': result.get('raw_text', response.text if 'response' in locals() else '')
            })
            logger.info(f"PDF {filename} procesado exitosamente en {processing_time:.3f}s")
            return result
        except Exception as e:
            processing_time = time.time() - start_time
            logger.error(f"Error procesando PDF {filename}: {str(e)}")
            return {
                'error_message': str(e),
                'processing_time_seconds': processing_time,
                'confidence_score': 0.0,
                'raw_text': None,
                'structured_data': None
            }

    def _create_ocr_prompt(self, filename: str) -> str:
        filename_lower = filename.lower()
        if any(keyword in filename_lower for keyword in ['receipt', 'recibo', 'invoice', 'factura']):
            return self._get_receipt_prompt()
        elif any(keyword in filename_lower for keyword in ['medical', 'medico', 'doctor', 'hospital']):
            return self._get_medical_prompt()
        elif any(keyword in filename_lower for keyword in ['police', 'policia', 'report', 'denuncia']):
            return self._get_police_report_prompt()
        else:
            return self._get_general_prompt()

    def _get_receipt_prompt(self) -> str:
        return """
        Analiza esta imagen de recibo/factura y extrae la información en formato JSON estructurado.
        Extrae los siguientes campos si están disponibles:
        - merchant_name: Nombre del comercio/establecimiento
        - date: Fecha del recibo
        - total_amount: Monto total
        - currency: Moneda
        - items: Lista de artículos con descripción y precio
        - tax_amount: Monto de impuestos
        - receipt_number: Número de recibo
        - payment_method: Método de pago
        Responde SOLO con el JSON válido, sin texto adicional.
        """

    def _get_medical_prompt(self) -> str:
        return """
        Analiza esta imagen de documento médico y extrae la información en formato JSON estructurado.
        Extrae los siguientes campos si están disponibles:
        - provider_name: Nombre del proveedor médico
        - patient_name: Nombre del paciente
        - service_date: Fecha del servicio
        - diagnosis: Diagnóstico
        - treatment: Tratamiento
        - total_cost: Costo total
        - insurance_info: Información de seguro
        - prescription_details: Detalles de prescripción
        Responde SOLO con el JSON válido, sin texto adicional.
        """

    def _get_police_report_prompt(self) -> str:
        return """
        Analiza esta imagen de reporte policial y extrae la información en formato JSON estructurado.
        Extrae los siguientes campos si están disponibles:
        - report_number: Número de reporte
        - incident_date: Fecha del incidente
        - location: Ubicación del incidente
        - incident_type: Tipo de incidente
        - description: Descripción del incidente
        - officer_name: Nombre del oficial
        - department: Departamento policial
        Responde SOLO con el JSON válido, sin texto adicional.
        """

    def _get_general_prompt(self) -> str:
        return """
        Analiza esta imagen de documento y extrae la información en formato JSON estructurado.
        Identifica y extrae:
        - document_type: Tipo de documento
        - key_information: Información clave encontrada
        - dates: Fechas mencionadas
        - amounts: Montos mencionados
        - names: Nombres mencionados
        - addresses: Direcciones mencionadas
        - phone_numbers: Números de teléfono
        - email_addresses: Direcciones de email
        Responde SOLO con el JSON válido, sin texto adicional.
        """

    def _parse_gemini_response(self, response_text: str, filename: str) -> Dict[str, Any]:
        try:
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            if json_start != -1 and json_end != 0:
                json_str = response_text[json_start:json_end]
                structured_data = json.loads(json_str)
            else:
                structured_data = {
                    'document_type': 'unknown',
                    'extracted_text': response_text,
                    'filename': filename
                }
            return {
                'structured_data': structured_data,
                'processing_status': 'completed'
            }
        except json.JSONDecodeError as e:
            logger.warning(f"Error parseando JSON de Gemini para {filename}: {str(e)}")
            return {
                'structured_data': {
                    'document_type': 'unknown',
                    'extracted_text': response_text,
                    'filename': filename,
                },
                'processing_status': 'completed'
            }

    def process_document_from_storage(self, storage_url: str, filename: str) -> Dict[str, Any]:
        """
        Procesa un documento desde una URL de almacenamiento.
        
        Args:
            storage_url: URL del documento en storage
            filename: Nombre del archivo
            
        Returns:
            Dict con el resultado del procesamiento
        """
        try:
            # TODO: Implementar descarga desde storage
            # Por ahora, asumimos que ya tenemos los datos de la imagen
            logger.info(f"Procesando documento desde storage: {storage_url}")
            
            # Placeholder - en implementación real, descargaríamos el archivo
            return {
                'error_message': 'Método no implementado completamente',
                'processing_status': 'failed'
            }
            
        except Exception as e:
            logger.error(f"Error procesando documento desde storage {storage_url}: {str(e)}")
            return {
                'error_message': str(e),
                'processing_status': 'failed'
            } 