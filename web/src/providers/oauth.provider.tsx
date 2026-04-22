import Keycloak from "keycloak-js";
import { createContext, useContext, useEffect, useRef, useState } from "react";
import { useConfig } from "./config.provider";

type Profile = {
  fullName: string,
  username: string,
}

export type OAuthContextType = {
  profile: Profile,
  token: string,
  logout: () => void,
  hasRole: (role: string | Array<string>) => boolean,
}

const OAuthContext = createContext<OAuthContextType>(null!);

export const OAuthProvider: React.FunctionComponent<React.PropsWithChildren> = ({ children }) => {

  const { apiUrl, ...config } = useConfig();

  const [profile, setProfile] = useState<Profile>(null!);
  const [loading, setLoading] = useState(true);
  const [authenticated, setAuthenticated] = useState(false);
  const isInitialized = useRef(false);
  const keycloakRef = useRef<Keycloak>(null!);

  useEffect(() => {
    if (isInitialized.current) return;
    isInitialized.current = true;

    keycloakRef.current = new Keycloak(config);

    const init = async () => {

      try {

        const auth = await keycloakRef.current.init({
          onLoad: 'check-sso',
        });

        if (!auth) {
          keycloakRef.current.login();
          return;
        }

        setAuthenticated(auth);
        setProfile({
          username: keycloakRef.current.tokenParsed?.preferred_username,
          fullName: keycloakRef.current.tokenParsed?.name,
        });
      } catch (error) {
        setAuthenticated(false);
        setProfile(null!);
      } finally {
        setLoading(false);
      }


    }

    const interval = setInterval(() => {
      keycloakRef.current.updateToken(30).catch(() => keycloakRef.current.logout());
    }, 10000);

    init();

    return () => clearInterval(interval);

  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (!authenticated || !profile) {
    return <div>Not authenticated</div>;
  }

  return (
    <OAuthContext.Provider value={{
      profile,
      token: keycloakRef.current.token!,
      logout: () => {
        setLoading(true);
        keycloakRef.current.logout({ redirectUri: window.location.origin });
      },
      hasRole: (role: string | Array<string>) => {
        if (Array.isArray(role)) {
          return role.some(r => keycloakRef.current.hasRealmRole(r));
        }
        return keycloakRef.current.hasRealmRole(role);
      },
    }}>
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
