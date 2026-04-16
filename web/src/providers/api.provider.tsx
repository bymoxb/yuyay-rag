import { createContext, useEffect, useState } from "react";
import client from "../services/client";
import { useConfig } from "./config.provider";
import { useOAuth } from "./oauth.provider";

const ApiContext = createContext({});

export const ApiProvider: React.FunctionComponent<React.PropsWithChildren> = ({ children }) => {

  const { apiUrl } = useConfig();
  const { updateToken, token } = useOAuth();
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);

    client.defaults.baseURL = apiUrl;

    const interceptor = client.interceptors.request.use(async (config) => {
      await updateToken(30);
      config.headers.Authorization = `Bearer ${token}`;

      return config;
    });


    setLoading(false);
    return () => {
      client.interceptors.request.eject(interceptor);
    };
  }, [])

  if (loading) {
    return <div>Loading...</div>
  }

  return (
    <ApiContext.Provider value={{}}>
      {children}
    </ApiContext.Provider>
  )
}
