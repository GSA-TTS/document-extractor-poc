import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router';
import { AlertType, callCreateDocumentApi } from './uploadPageController';

export interface UseUploadPageHook {
  alertMessage: string;
  alertType: AlertType;
  fileInputRef: React.RefObject<HTMLInputElement | null>;
  handleSubmit: (event: React.FormEvent<HTMLFormElement>) => Promise<void>;
  showAlert: (message: string, type: AlertType) => void;
}

export function useUploadPage(signOut: () => Promise<void>): UseUploadPageHook {
  const [alertMessage, setAlertMessage] = useState<string>('');
  const [alertType, setAlertType] = useState<AlertType>('success');
  const fileInputRef = useRef<HTMLInputElement>(null);
  const navigate = useNavigate();

  function showAlert(message: string, type: AlertType) {
    setAlertMessage(message);
    setAlertType(type);
  }

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const file = fileInputRef.current?.files?.[0];

    if (!file) {
      showAlert('Please select a file to upload!', 'error');
      return;
    }

    const { responseData, failure } = await callCreateDocumentApi(file);

    if (failure === 'unauthenticated') {
      showAlert(
        'You are no longer signed in! Please sign in again. You will be navigated to the sign in page in a few seconds.',
        'error'
      );
      setTimeout(() => {
        signOut();
      }, 5000);
      return;
    } else if (!failure) {
      showAlert('An error occurred while uploading!', 'error');
      return;
    }

    if (responseData) {
      sessionStorage.setItem('documentId', responseData.documentId);
      showAlert('File uploaded successfully!', 'success');
      navigate('/verify-document');
    }
  }

  return {
    alertMessage,
    alertType,
    fileInputRef,
    handleSubmit,
    showAlert,
  };
}
