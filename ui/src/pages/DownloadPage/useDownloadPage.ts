import React, { useState } from 'react';
import { UpdateDocumentResponse } from '../../utils/api.ts';
import { downloadCSV, downloadJSON } from './downloadPageController.ts';

export function useDownloadPage() {
  const [verifiedData] = useState<UpdateDocumentResponse>(() => {
    const storedData = sessionStorage.getItem('verifiedData');
    return storedData ? JSON.parse(storedData)?.updated_document : {};
  });

  async function handleDownloadSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!verifiedData.extracted_data) {
      console.error('No data available to download');
      return;
    }

    // get the selected file type (CSV or JSON) from the radio buttons
    const selectedElement = document.querySelector(
      "input[name='download-file-type']:checked"
    ) as HTMLInputElement | null;

    if (!selectedElement) {
      console.error('No file type selected');
      return;
    }

    const fileType = selectedElement.value;

    if (!fileType) {
      console.error('No file type selected');
      return;
    }

    // download function based on the selected file type
    if (fileType === 'csv') {
      await downloadCSV(verifiedData);
    } else {
      await downloadJSON(verifiedData);
    }
  }

  return {
    handleDownloadSubmit,
    verifiedData,
  };
}
