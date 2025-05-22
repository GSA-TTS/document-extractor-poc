import { Routes, Route, useNavigate } from 'react-router';
import UploadPage from './pages/UploadPage/UploadPage';
import VerifyPage from './pages/VerifyPage/VerifyPage';
import DownloadPage from './pages/DownloadPage/DownloadPage';
import NotSignedInPage from './pages/NotSignedInPage';
import SignInPage from './pages/SignInPage/SignInPage';
import { useEffect, useState } from 'react';

export default function App() {
  const [authToken, setAuthToken] = useState<string>(() => {
    return sessionStorage.getItem('auth_token') || '';
  });

  const [justSignedOut, setJustSignedOut] = useState<boolean>(false);

  const navigate = useNavigate();

  async function signOut(): Promise<void> {
    setAuthToken('');
    setJustSignedOut(true);
    navigate('/');
  }

  useEffect(() => {
    if (authToken) {
      sessionStorage.setItem('auth_token', authToken);
      setJustSignedOut(false);
    } else {
      sessionStorage.removeItem('auth_token');
    }
  }, [authToken]);

  return (
    <Routes>
      <Route
        path="/verify-document"
        element={
          authToken ? <VerifyPage signOut={signOut} /> : <NotSignedInPage />
        }
      />
      <Route
        path="/download-document"
        element={
          authToken ? <DownloadPage signOut={signOut} /> : <NotSignedInPage />
        }
      />
      <Route
        path="/upload-document"
        element={
          authToken ? <UploadPage signOut={signOut} /> : <NotSignedInPage />
        }
      />
      <Route
        path="/"
        element={
          <SignInPage
            setAuthToken={setAuthToken}
            justSignedOut={justSignedOut}
          />
        }
      />
    </Routes>
  );
}
