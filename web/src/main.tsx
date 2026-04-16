import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import App from './App.tsx';
import { ApiProvider } from './providers/api.provider.tsx';
import { ConfigProvider } from './providers/config.provider.tsx';
import { OAuthProvider } from './providers/oauth.provider.tsx';
import { UserProvider } from './providers/user.provider.tsx';

import './index.css';

const root = document.getElementById('root')!;

createRoot(root).render(
  <StrictMode>
    <ConfigProvider>
      <OAuthProvider>
        <ApiProvider>
          <UserProvider>
            <App />
          </UserProvider>
        </ApiProvider>
      </OAuthProvider>
    </ConfigProvider>
  </StrictMode>,
)
