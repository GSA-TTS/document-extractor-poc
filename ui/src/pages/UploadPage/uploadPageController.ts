import { authorizedFetch, NewDocumentResponse } from '../../utils/api.ts';

export type AlertType = 'error' | 'success';

interface CallCreateDocumentApiResponse {
  responseData?: NewDocumentResponse;
  failure?: 'unauthenticated' | 'other';
}

export async function callCreateDocumentApi(
  file: File
): Promise<CallCreateDocumentApiResponse> {
  try {
    const base64File = await readFileAsBase64(file);
    const requestBody = {
      file_content: base64File,
      file_name: file.name,
    };

    const response = await authorizedFetch('/api/document', {
      method: 'POST',
      body: JSON.stringify(requestBody),
    });

    if (response.ok) {
      const data = (await response.json()) as NewDocumentResponse;
      return {
        responseData: data,
      };
    } else if (response.status === 401 || response.status === 403) {
      return {
        failure: 'unauthenticated',
      };
    } else {
      console.error('File failed to upload!');
      return {
        failure: 'other',
      };
    }
  } catch (error) {
    console.error('Upload failed:', error);
    return {
      failure: 'other',
    };
  }
}

function readFileAsBase64(file: File): Promise<string> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);

    reader.onload = function () {
      const base64Result = reader.result as string;
      const base64File = base64Result.split(',')[1];
      resolve(base64File);
    };

    reader.onerror = function () {
      reject(reader.error);
    };
  });
}
