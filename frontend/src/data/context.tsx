import React, { createContext, useState } from 'react';

interface InputContextType {
    tickerSymbol: string;
    setTickerSymbol: (value: string) => void;
    strikePrice: string;
    setStrikePrice: (value: string) => void;
    expirationDate: string;
    setExpirationDate: (value: string) => void;
  }
  
  // Provide a default value for the context
  const defaultValue: InputContextType = {
    tickerSymbol: '',
    setTickerSymbol: () => {},
    strikePrice: '',
    setStrikePrice: () => {},
    expirationDate: '',
    setExpirationDate: () => {},
  };

export const InputContext = createContext<InputContextType>(defaultValue);
// Create a provider component
export const InputProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const [tickerSymbol, setTickerSymbol] = useState('XYZ');
    const [strikePrice, setStrikePrice] = useState('100.00');
    const [expirationDate, setExpirationDate] = useState('09/20/24');
  
    return (
      <InputContext.Provider value={{ tickerSymbol, setTickerSymbol, strikePrice, setStrikePrice, expirationDate, setExpirationDate }}>
        {children}
      </InputContext.Provider>
    );
  };