// styles/theme.ts
import { createTheme } from "@mui/material/styles";

const darkTheme = createTheme({
  palette: {
    mode: "dark", // Ativa o modo escuro
    primary: {
      main: "#90caf9", // Cor primária (azul claro)
    },
    secondary: {
      main: "#f48fb1", // Cor secundária (rosa claro)
    },
    background: {
      default: "#121212", // Cor de fundo escura
      paper: "#1e1e1e", // Cor de fundo dos cards
    },
    text: {
      primary: "#ffffff", // Cor do texto principal (branco)
      secondary: "#b3b3b3", // Cor do texto secundário (cinza claro)
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
    h4: {
      fontWeight: 600, // Títulos em negrito
    },
    h6: {
      fontWeight: 500, // Subtítulos em negrito
    },
  },
});

export default darkTheme;
