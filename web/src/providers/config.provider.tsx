import { createContext, useContext, useEffect, useState } from "react";

type ConfigContextType = {
  url: string,
  realm: string,
  clientId: string,
  apiUrl: string,
}

const ConfigContext = createContext<ConfigContextType>(null!);

export const ConfigProvider: React.FunctionComponent<React.PropsWithChildren> = ({ children }) => {
  const [config, setConfig] = useState<ConfigContextType>(null!);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchConfig = async () => {
      try {
        setLoading(true);
        const response = await fetch('/config.json');
        const config = await response.json();
        setConfig(config);
      } catch (error) {
        setConfig(null!);
      } finally {
        setLoading(false);
      }
    }

    fetchConfig();
  }, [])

  if (loading) {
    return <div>Loading...</div>;
  }

  if (!config) {
    return <div>Config not found</div>;
  }

  return (
    <ConfigContext.Provider value={config}>
      {children}
    </ConfigContext.Provider>
  )
}

export const useConfig = () => {
  const context = useContext(ConfigContext);

  if (!context) {
    throw new Error('useConfig must be used within a ConfigProvider');
  }

  return context;
}
