import { ExtractedData, UpdateDocumentResponse } from '../../utils/api';

export function generateCsvData(extractedData: ExtractedData): string {
  let csvData = 'Field,Value\n';

  const sortedEntries = Object.entries(extractedData).sort(([keyA], [keyB]) =>
    keyA.localeCompare(keyB, undefined, { numeric: true })
  );

  // Construct CSV content
  sortedEntries.forEach(([key, field]) => {
    let value = field.value !== undefined ? `"${field.value}"` : '""';
    csvData += `"${key}",${value}\n`;
  });

  return csvData;
}

export async function downloadCSV(verifiedData: UpdateDocumentResponse) {
  const csvContent = generateCsvData(verifiedData.extracted_data ?? {});

  await downloadData(csvContent, 'text/csv', 'document.csv');
}

export async function downloadJSON(verifiedData: UpdateDocumentResponse) {
  const jsonContent = JSON.stringify(verifiedData, null, 2);

  await downloadData(jsonContent, 'application/json', 'document.json');
}

async function downloadData(
  content: string,
  contentType: string,
  filename: string
) {
  const blob = new Blob([content], { type: contentType });
  const url = URL.createObjectURL(blob);

  try {
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    link.click();
  } finally {
    setTimeout(() => {
      URL.revokeObjectURL(url);
    }, 1000); // Small delay to ensure download starts
  }
}
