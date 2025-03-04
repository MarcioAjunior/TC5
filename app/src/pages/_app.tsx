// pages/_app.tsx
import { ThemeProvider } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";
import darkTheme from "../styles/theme";
import type { AppProps } from "next/app";

function MyApp({ Component, pageProps }: AppProps) {
  return (
    <ThemeProvider theme={darkTheme}>
      <CssBaseline /> {/* Reseta o CSS e aplica o tema escuro */}
      <Component {...pageProps} />
    </ThemeProvider>
  );
}

export default MyApp;
