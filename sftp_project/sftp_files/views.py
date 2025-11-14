from django.http import JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from .sftp_utils import get_sftp_credentials
from .models import FileMetadata
import pysftp
import datetime
import os
import io

@csrf_exempt
def upload_file(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        sftp_credentials = get_sftp_credentials()

        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        filename, extension = os.path.splitext(uploaded_file.name)
        unique_filename = f'{filename}_{timestamp}{extension}'

        remote_dir = 'desktop/uploaded'
        remote_path = f'{remote_dir}/{unique_filename}'

        try:
            cnopts = pysftp.CnOpts()
            cnopts.hostkeys = None
            with pysftp.Connection(**sftp_credentials, cnopts=cnopts) as sftp:
                if not sftp.exists(remote_dir):
                    sftp.makedirs(remote_dir)
                sftp.putfo(uploaded_file, remote_path)

            metadata = FileMetadata.objects.create(
                filename=unique_filename,
                filepath=remote_path
            )
            return JsonResponse({'message': 'File uploaded successfully', 'file_id': metadata.id})
        except pysftp.ConnectionException as e:
            return JsonResponse({'error': f'SFTP Connection Error: {e}'}, status=500)
        except Exception as e:
            return JsonResponse({'error': f'An unexpected error occurred: {e}'}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def download_file(request, file_id):
    if request.method == 'GET':
        try:
            metadata = FileMetadata.objects.get(id=file_id)
        except FileMetadata.DoesNotExist:
            return JsonResponse({'error': 'File not found'}, status=404)

        sftp_credentials = get_sftp_credentials()

        try:
            cnopts = pysftp.CnOpts()
            cnopts.hostkeys = None
            with pysftp.Connection(**sftp_credentials, cnopts=cnopts) as sftp:
                file_buffer = io.BytesIO()
                sftp.getfo(metadata.filepath, file_buffer)
                file_buffer.seek(0)

                response = FileResponse(file_buffer, as_attachment=True, filename=metadata.filename)
                return response
        except pysftp.ConnectionException as e:
            return JsonResponse({'error': f'SFTP Connection Error: {e}'}, status=500)
        except IOError as e:
            return JsonResponse({'error': f'File not found on SFTP server: {e}'}, status=404)
        except Exception as e:
            return JsonResponse({'error': f'An unexpected error occurred: {e}'}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)
