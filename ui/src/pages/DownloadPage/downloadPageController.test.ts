import { describe, expect, it, vi, beforeEach, afterEach } from 'vitest';
import {
  generateCsvData,
  downloadCSV,
  downloadJSON,
} from './downloadPageController';
import { ExtractedData } from '../../utils/api';

const extractedData: ExtractedData = {
  bKey: { value: 'DogCow' },
  aKey: { value: 'Moof' },
  cKey: { value: undefined },
  dKey: { value: 'something with, commas' },
};

describe('generateCsvData', () => {
  it('sorts the entries', () => {
    const csvData = generateCsvData(extractedData);
    expect(csvData.indexOf('aKey')).toBeLessThan(csvData.indexOf('bKey'));
  });

  it('puts empty quotes for undefined values', () => {
    const csvData = generateCsvData(extractedData);
    expect(csvData).toContain('"cKey",""');
  });

  it('puts all the data from the extracted data in the CSV', () => {
    const csvData = generateCsvData(extractedData);
    expect(csvData).toContain('"aKey","Moof"');
    expect(csvData).toContain('"bKey","DogCow"');
    expect(csvData).toContain('"cKey",""');
    expect(csvData).toContain('"dKey","something with, commas"');
  });
});

describe('downloadCSV & downloadJSON', () => {
  const mockRevokeObjectURL = vi.fn();
  const mockClick = vi.fn();

  const mockLink = {
    href: '',
    download: '',
    click: mockClick,
  };

  beforeEach(() => {
    const mockCreateElement = vi.fn();
    vi.stubGlobal('document', {
      createElement: mockCreateElement,
    });
    vi.stubGlobal('URL', {
      createObjectURL: vi.fn(),
      revokeObjectURL: mockRevokeObjectURL,
    });
    mockCreateElement.mockReturnValue(mockLink);
  });

  afterEach(() => {
    // Restore original globals
    vi.unstubAllGlobals();
  });

  it('download link is clicked for JSON', async () => {
    await downloadJSON({});

    expect(mockLink.download).toBe('document.json');
    expect(mockClick).toHaveBeenCalledTimes(1);
  });

  it('should revoke the object URL after download', async () => {
    vi.useFakeTimers();

    await downloadJSON({});

    expect(mockRevokeObjectURL).not.toHaveBeenCalled();

    // Fast-forward time to trigger the setTimeout callback
    vi.advanceTimersByTime(1000);

    expect(mockRevokeObjectURL).toHaveBeenCalled();

    vi.useRealTimers();
  });

  it('download link is clicked for a CSV', async () => {
    await downloadCSV({
      extracted_data: {
        aKey: { value: 'Moof', confidence: '0.9' },
      },
    });

    expect(mockLink.download).toBe('document.csv');
    expect(mockClick).toHaveBeenCalledTimes(1);
  });
});
