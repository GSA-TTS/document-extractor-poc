import Layout from '../../components/Layout';
import { useUploadPage } from './useUploadPage';

interface UploadPageProps {
  signOut: () => Promise<void>;
}

export default function UploadPage({ signOut }: UploadPageProps) {
  const { alertMessage, alertType, fileInputRef, handleSubmit } =
    useUploadPage(signOut);

  return (
    <Layout signOut={signOut}>
      <div className="site-wrapper grid-container padding-bottom-15">
        {/* Start of the alert section */}
        {alertMessage && (
          <div
            className={`usa-alert usa-alert--${alertType} usa-alert--no-icon`}
          >
            <div className="usa-alert__body">
              <p className="usa-alert__text">{alertMessage}</p>
            </div>
          </div>
        )}
        {/* End alert section */}
        {/* Start of the step indicator section */}
        <div
          className="usa-step-indicator usa-step-indicator--counters margin-bottom-6"
          aria-label="Document processing steps"
        >
          <ol className="usa-step-indicator__segments">
            <li
              className="usa-step-indicator__segment usa-step-indicator__segment--current"
              aria-current="step"
            >
              <span className="usa-step-indicator__segment-label">
                Upload documents{' '}
                <span className="usa-sr-only">— current step</span>
              </span>
            </li>
            <li className="usa-step-indicator__segment">
              <span className="usa-step-indicator__segment-label">
                Verify documents and data{' '}
                <span className="usa-sr-only">— not completed</span>
              </span>
            </li>
            <li className="usa-step-indicator__segment">
              <span className="usa-step-indicator__segment-label">
                Save and download CSV file{' '}
                <span className="usa-sr-only">— not completed</span>
              </span>
            </li>
          </ol>
        </div>

        {/* End step indicator section */}
        <h1 className="font-ui-xl margin-bottom-2">Upload documents</h1>
        <form id="upload-form" onSubmit={handleSubmit}>
          {/* Start of the card section */}
          <ul className="usa-card-group">
            <li className="usa-card tablet:grid-col-6 widescreen:grid-col-4">
              <div className="usa-card__container">
                <div className="usa-card__header">
                  <h2 className="usa-card__heading font-body-md">
                    File upload
                  </h2>
                </div>
                <div className="usa-card__body">
                  {/* Start of the file input section */}
                  <div className="usa-form-group">
                    <span className="usa-hint" id="file-input-specific-hint">
                      Files must be under 4 MB
                    </span>
                    <label
                      className="usa-label margin-top-1"
                      htmlFor="file-input-single"
                    >
                      Attach a JPG, PDF, TIFF, HEIC, or PNG file
                    </label>
                    <input
                      id="file-input-single"
                      className="usa-file-input"
                      type="file"
                      name="file-input-single"
                      accept=".jpg,.pdf,.tiff,.heic,.png"
                      ref={fileInputRef}
                    />
                  </div>
                  {/* End file input section */}
                </div>
              </div>
            </li>
          </ul>
          {/* End card section */}
          {/* Start button section */}
          <div className="display-flex flex-column flex-align-end tablet:grid-col-6">
            <button id="upload-button" className="usa-button" type="submit">
              Process data
            </button>
          </div>
          {/* End button section */}
        </form>
      </div>
    </Layout>
  );
}
