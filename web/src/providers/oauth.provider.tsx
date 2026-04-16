import Keycloak from "keycloak-js";
import { createContext, useContext, useEffect, useRef, useState } from "react";
import { useConfig } from "./config.provider";

type OAuthContextType = {
  username: string,
  token: string,
  updateToken: (seconds: number) => Promise<boolean>,
  logout: () => void,
}

const OAuthContext = createContext<OAuthContextType>(null!);

export const OAuthProvider: React.FunctionComponent<React.PropsWithChildren> = ({ children }) => {

  const { apiUrl, ...config } = useConfig();

  const [data, setData] = useState<OAuthContextType>(null!);
  const [loading, setLoading] = useState(true);
  const [authenticated, setAuthenticated] = useState(false);
  const isInitialized = useRef(false);

  useEffect(() => {
    if (isInitialized.current) return;
    isInitialized.current = true;

    const init = async () => {

      try {
        const keycloak = new Keycloak(config);

        const auth = await keycloak.init({
          onLoad: 'check-sso',
        });

        if (!auth) {
          keycloak.login();
        }

        setAuthenticated(auth);
        setData({
          username: keycloak.tokenParsed?.preferred_username || '',
          token: keycloak.token || '',
          updateToken: keycloak.updateToken,
          logout: () => keycloak.logout({ redirectUri: window.location.origin }),
        });
      } catch (error) {
        setAuthenticated(false);
        setData(null!);
      } finally {

        setLoading(false);
      }


    }

    init();
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (!authenticated || !data) {
    return <div>Not authenticated</div>;
  }

  return (
    <OAuthContext.Provider value={data}>
      {children}
    </OAuthContext.Provider>
  )
}

export const useOAuth = () => {
  const context = useContext(OAuthContext);

  if (!context) {
    throw new Error('useOAuth must be used within an OAuthProvider');
  }

  return context;
}
