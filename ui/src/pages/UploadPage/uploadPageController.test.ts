import { describe, expect, it, vi } from 'vitest';
import { callCreateDocumentApi } from './uploadPageController';
import * as api from '../../utils/api';

// Mock the authorizedFetch function
vi.mock('../../utils/api', () => ({
  authorizedFetch: vi.fn(),
}));

class MockFileReader {
  onload: (() => void) | null = null;
  onerror: (() => void) | null = null;
  result: string | null = null;
  error: Error | null = null;

  readSuccess: boolean = true;

  readAsDataURL(file: File): void {
    setTimeout(() => {
      if (this.readSuccess) {
        this.result = `data:${file.type};base64,mockBase64Data`;
        if (this.onload) this.onload();
      } else {
        this.error = new Error('File read error');
        if (this.onerror) this.onerror();
      }
    }, 0);
  }
}

// allow `new FileReader()` to work even in a node (test) environment
vi.stubGlobal('FileReader', MockFileReader);

describe('callCreateDocumentApi', () => {
  const mockAuthorizedFetch = api.authorizedFetch as ReturnType<typeof vi.fn>;

  // Create a mock File object
  const createMockFile = (name = 'test.pdf', type = 'application/pdf') => {
    return new File(['mock file content'], name, { type });
  };

  it('should upload a file successfully', async () => {
    // Mock a successful response
    const mockDocumentId = 'test-document-id';
    const mockResponse = {
      ok: true,
      status: 200,
      json: vi.fn().mockResolvedValue({
        message: 'File uploaded successfully',
        documentId: mockDocumentId,
      }),
    };
    mockAuthorizedFetch.mockResolvedValue(mockResponse);

    const mockFile = createMockFile();
    const result = await callCreateDocumentApi(mockFile);

    expect(mockAuthorizedFetch).toHaveBeenCalledWith('/api/document', {
      method: 'POST',
      body: expect.stringContaining('"file_name":"test.pdf"'),
    });

    expect(result).toEqual({
      responseData: {
        message: 'File uploaded successfully',
        documentId: mockDocumentId,
      },
      failure: undefined,
    });
  });

  it('should return unauthenticated failure when API returns 401', async () => {
    // Mock a 401 unauthorized response
    const mockResponse = {
      ok: false,
      status: 401,
      statusText: 'Unauthorized',
    };
    mockAuthorizedFetch.mockResolvedValue(mockResponse);

    const mockFile = createMockFile();
    const result = await callCreateDocumentApi(mockFile);

    expect(result).toEqual({
      failure: 'unauthenticated',
      responseData: undefined,
    });
  });

  it('should return unauthenticated failure when API returns 403', async () => {
    // Mock a 403 forbidden response
    const mockResponse = {
      ok: false,
      status: 403,
      statusText: 'Forbidden',
    };
    mockAuthorizedFetch.mockResolvedValue(mockResponse);

    const mockFile = createMockFile();
    const result = await callCreateDocumentApi(mockFile);

    expect(result).toEqual({
      failure: 'unauthenticated',
      responseData: undefined,
    });
  });

  it('should return other failure when API returns other error status', async () => {
    // Mock a 500 server error response
    const mockResponse = {
      ok: false,
      status: 500,
      statusText: 'Internal Server Error',
    };
    mockAuthorizedFetch.mockResolvedValue(mockResponse);

    const mockFile = createMockFile();
    const result = await callCreateDocumentApi(mockFile);

    expect(result).toEqual({
      failure: 'other',
      responseData: undefined,
    });
  });

  it('should return other failure when fetch throws an exception', async () => {
    // Mock a network error
    mockAuthorizedFetch.mockRejectedValue(new Error('Network error'));

    const mockFile = createMockFile();
    const result = await callCreateDocumentApi(mockFile);

    expect(result).toEqual({
      failure: 'other',
      responseData: undefined,
    });
  });

  it('should handle files with different names and types', async () => {
    // Mock a successful response
    const mockResponse = {
      ok: true,
      status: 200,
      json: vi.fn().mockResolvedValue({
        message: 'File uploaded successfully',
        documentId: 'test-document-id',
      }),
    };
    mockAuthorizedFetch.mockResolvedValue(mockResponse);

    const mockFileName = 'DogCow.jpeg';
    const mockFile = createMockFile(mockFileName, 'image/jpeg');
    const result = await callCreateDocumentApi(mockFile);

    expect(mockAuthorizedFetch).toHaveBeenCalledWith('/api/document', {
      method: 'POST',
      body: expect.stringContaining(`"file_name":"${mockFileName}"`),
    });

    expect(result).toEqual({
      responseData: expect.anything(),
      failure: undefined,
    });
  });

  it('should handle file reading errors', async () => {
    // Set the MockFileReader to fail
    const originalFileReader = globalThis.FileReader;
    const mockFileReaderInstance = new MockFileReader();
    mockFileReaderInstance.readSuccess = false;

    // Override the FileReader constructor to return our configured instance
    vi.stubGlobal('FileReader', function () {
      return mockFileReaderInstance;
    });

    const mockFile = createMockFile();
    const result = await callCreateDocumentApi(mockFile);

    expect(result).toEqual({
      failure: 'other',
      responseData: undefined,
    });

    // Restore the original FileReader
    vi.stubGlobal('FileReader', originalFileReader);
  });

  it('should handle empty files', async () => {
    const mockResponse = {
      ok: true,
      status: 200,
      json: vi.fn().mockResolvedValue({
        message: 'File uploaded successfully',
        documentId: 'test-document-id',
      }),
    };
    mockAuthorizedFetch.mockResolvedValue(mockResponse);

    const emptyFile = new File([], 'empty.pdf', { type: 'application/pdf' });
    const result = await callCreateDocumentApi(emptyFile);

    expect(result).toEqual({
      responseData: expect.anything(),
      failure: undefined,
    });
  });
});
